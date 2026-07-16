"""
Enhanced annotation validation with image file verification.
"""

import json
from pathlib import Path
from src.schemas import Annotation, BoundingBox
from src.image_validator import ImageValidator, validate_annotation_with_image


def validate_annotations_with_images(file_path: str, check_images: bool = True):
    """
    Validate annotation file and optionally verify images exist.
    
    Args:
        file_path: Path to annotation JSON file
        check_images: Whether to verify image files exist
        
    Returns:
        dict: Validation report with results and errors
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Annotation file not found: {file_path}")
    
    # Load raw JSON
    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    # Handle both list and dict with 'annotations' key
    if isinstance(raw_data, dict) and 'annotations' in raw_data:
        annotations_list = raw_data['annotations']
    elif isinstance(raw_data, list):
        annotations_list = raw_data
    else:
        raise ValueError("Invalid annotation file format")
    
    # Validate each annotation
    validated = []
    errors = []
    image_errors = []
    image_validator = ImageValidator()
    
    for idx, item in enumerate(annotations_list):
        try:
            # Convert bbox array to BoundingBox object if needed
            if isinstance(item.get('bbox'), (list, tuple)):
                item['bbox'] = BoundingBox.from_array(item['bbox']).to_dict()
            
            # Validate against schema
            annotation = Annotation(**item)
            validated.append(annotation)
            
            # Check images if requested
            if check_images:
                is_valid, img_errors = validate_annotation_with_image(item, image_validator)
                if not is_valid:
                    image_errors.append({
                        'annotation_id': annotation.annotation_id,
                        'errors': img_errors
                    })
        
        except Exception as e:
            errors.append({
                'index': idx,
                'error': str(e),
                'data': item
            })
    
    return {
        'total_annotations': len(annotations_list),
        'valid_annotations': len(validated),
        'invalid_annotations': len(errors),
        'image_validation_errors': len(image_errors),
        'validation_errors': errors,
        'image_errors': image_errors,
        'status': 'PASSED' if len(errors) == 0 and len(image_errors) == 0 else 'FAILED',
        'validated_data': validated
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate annotation file with optional image verification'
    )
    parser.add_argument('file', help='Path to annotation JSON file')
    parser.add_argument(
        '--check-images',
        action='store_true',
        default=True,
        help='Verify image files exist and bboxes are within bounds'
    )
    parser.add_argument(
        '--no-check-images',
        action='store_false',
        dest='check_images',
        help='Skip image file verification'
    )
    
    args = parser.parse_args()
    
    report = validate_annotations_with_images(args.file, check_images=args.check_images)
    
    Path("reports").mkdir(exist_ok=True)
    
    output_file = "reports/validation_report_enhanced.json"
    
    # Save report
    report_to_save = {
        'total_annotations': report['total_annotations'],
        'valid_annotations': report['valid_annotations'],
        'invalid_annotations': report['invalid_annotations'],
        'image_validation_errors': report['image_validation_errors'],
        'status': report['status'],
        'validation_errors': report['validation_errors'],
        'image_errors': report['image_errors']
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report_to_save, f, indent=4)
    
    print(f"\nValidation Report:")
    print(f"==================")
    print(f"Total Annotations: {report['total_annotations']}")
    print(f"Valid Annotations: {report['valid_annotations']}")
    print(f"Invalid Annotations: {report['invalid_annotations']}")
    print(f"Image Validation Errors: {report['image_validation_errors']}")
    print(f"Status: {report['status']}")
    print(f"\nReport saved to: {Path(output_file).resolve()}")
    
    if report['validation_errors']:
        print(f"\n❌ Validation Errors:")
        for error in report['validation_errors']:
            print(f"  - Index {error['index']}: {error['error']}")
    
    if report['image_errors']:
        print(f"\n❌ Image Errors:")
        for error in report['image_errors']:
            print(f"  - Annotation {error['annotation_id']}: {', '.join(error['errors'])}")
    
    if report['status'] == 'PASSED':
        print("\n✅ All validations passed!")
