"""
Image visualization utilities for drawing bounding boxes and annotations.
"""

from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from src.config import IMAGE_DIR, REPORT_DIR
from src.image_validator import ImageValidator


class AnnotationVisualizer:
    """Visualizes annotations by drawing bounding boxes on images."""
    
    def __init__(self, image_dir: Path = IMAGE_DIR, output_dir: Path = REPORT_DIR):
        """Initialize visualizer."""
        self.image_dir = image_dir
        self.output_dir = Path(output_dir) / "visualizations"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.validator = ImageValidator(image_dir)
    
    def draw_bbox_pil(self, image: Image.Image, bbox: list, label: str, 
                      confidence: float = None, color: tuple = (0, 255, 0)) -> Image.Image:
        """
        Draw bounding box on image using PIL.
        
        Args:
            image: PIL Image object
            bbox: [x, y, width, height]
            label: Equipment label
            confidence: Confidence score (optional)
            color: RGB color tuple
            
        Returns:
            PIL Image with drawn bbox
        """
        draw = ImageDraw.Draw(image)
        x, y, w, h = bbox
        
        # Draw rectangle
        draw.rectangle(
            [(x, y), (x + w, y + h)],
            outline=color,
            width=2
        )
        
        # Draw label with confidence
        text = label.upper()
        if confidence:
            text += f" ({confidence:.2f})"
        
        # Draw text background
        text_bbox = draw.textbbox((x, y - 20), text)
        draw.rectangle(text_bbox, fill=color)
        draw.text((x, y - 20), text, fill=(255, 255, 255))
        
        return image
    
    def draw_bbox_cv2(self, image: np.ndarray, bbox: list, label: str,
                      confidence: float = None, color: tuple = (0, 255, 0)) -> np.ndarray:
        """
        Draw bounding box on image using OpenCV.
        
        Args:
            image: OpenCV image array (BGR)
            bbox: [x, y, width, height]
            label: Equipment label
            confidence: Confidence score (optional)
            color: BGR color tuple
            
        Returns:
            OpenCV image with drawn bbox
        """
        x, y, w, h = bbox
        
        # Draw rectangle (BGR format for OpenCV)
        cv2.rectangle(image, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
        
        # Draw label with confidence
        text = label.upper()
        if confidence:
            text += f" ({confidence:.2f})"
        
        # Draw text background
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 1
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        
        cv2.rectangle(
            image,
            (int(x), int(y - text_size[1] - 5)),
            (int(x + text_size[0]), int(y)),
            color,
            -1
        )
        cv2.putText(image, text, (int(x), int(y - 5)), font, font_scale, (255, 255, 255), thickness)
        
        return image
    
    def visualize_annotation(self, image_filename: str, annotation: dict, 
                            output_name: str = None, use_cv2: bool = True) -> Path:
        """
        Create visualization with bounding box.
        
        Args:
            image_filename: Name of image file in data/images
            annotation: Annotation dict with bbox, label, confidence
            output_name: Output filename (optional)
            use_cv2: Use OpenCV (True) or PIL (False)
            
        Returns:
            Path to output image
        """
        image_path = self.image_dir / image_filename
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Prepare output name
        if output_name is None:
            output_name = f"viz_{Path(image_filename).stem}.jpg"
        
        output_path = self.output_dir / output_name
        
        # Load and visualize
        if use_cv2:
            image = cv2.imread(str(image_path))
            image = self.draw_bbox_cv2(
                image,
                annotation['bbox'],
                annotation['label'],
                annotation.get('confidence'),
                color=(0, 255, 0)  # Green in BGR
            )
            cv2.imwrite(str(output_path), image)
        else:
            image = Image.open(image_path)
            image = self.draw_bbox_pil(
                image,
                annotation['bbox'],
                annotation['label'],
                annotation.get('confidence'),
                color=(0, 255, 0)  # Green in RGB
            )
            image.save(output_path)
        
        return output_path
    
    def visualize_comparison(self, image_filename: str, annotations: list,
                            output_name: str = None) -> Path:
        """
        Create side-by-side comparison of multiple annotations on same image.
        
        Args:
            image_filename: Name of image file
            annotations: List of annotation dicts
            output_name: Output filename
            
        Returns:
            Path to output image
        """
        image_path = self.image_dir / image_filename
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Prepare output name
        if output_name is None:
            output_name = f"comp_{Path(image_filename).stem}.jpg"
        
        output_path = self.output_dir / output_name
        
        # Load image
        image = cv2.imread(str(image_path))
        
        # Draw all annotations with different colors
        colors = [
            (0, 255, 0),      # Green
            (255, 0, 0),      # Blue
            (0, 165, 255),    # Orange
            (255, 255, 0)     # Cyan
        ]
        
        for idx, annotation in enumerate(annotations):
            color = colors[idx % len(colors)]
            image = self.draw_bbox_cv2(
                image,
                annotation['bbox'],
                f"{annotation['label']}_{idx+1}",
                annotation.get('confidence'),
                color=color
            )
        
        cv2.imwrite(str(output_path), image)
        return output_path
    
    def batch_visualize(self, annotations_list: list, image_mapping: dict = None) -> list:
        """
        Create visualizations for multiple annotations.
        
        Args:
            annotations_list: List of annotation dicts
            image_mapping: Dict mapping image_id to filename
            
        Returns:
            List of output paths
        """
        output_paths = []
        
        for idx, annotation in enumerate(annotations_list):
            try:
                image_file = annotation.get('image', '')
                output_name = f"viz_{idx:03d}_{Path(image_file).stem}.jpg"
                
                path = self.visualize_annotation(image_file, annotation, output_name)
                output_paths.append(path)
            except Exception as e:
                print(f"Error visualizing annotation {idx}: {str(e)}")
        
        return output_paths


def create_annotation_summary_image(image_filename: str, annotations: list,
                                   metadata: dict = None) -> Path:
    """
    Create a summary image with all annotations and metadata.
    
    Args:
        image_filename: Name of image file
        annotations: List of annotations
        metadata: Image metadata dict
        
    Returns:
        Path to output image
    """
    visualizer = AnnotationVisualizer()
    
    # Load image
    image_path = visualizer.image_dir / image_filename
    image = cv2.imread(str(image_path))
    
    if image is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")
    
    # Draw all annotations
    colors = [(0, 255, 0), (255, 0, 0), (0, 165, 255), (255, 255, 0)]
    
    for idx, annotation in enumerate(annotations):
        color = colors[idx % len(colors)]
        image = visualizer.draw_bbox_cv2(image, annotation['bbox'], 
                                        annotation['label'], 
                                        annotation.get('confidence'), color)
    
    # Add metadata text if provided
    if metadata:
        y_offset = 30
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        color = (255, 255, 255)
        thickness = 1
        
        for key, value in metadata.items():
            text = f"{key}: {value}"
            cv2.putText(image, text, (10, y_offset), font, font_scale, color, thickness)
            y_offset += 25
    
    # Save
    output_name = f"summary_{Path(image_filename).stem}.jpg"
    output_path = visualizer.output_dir / output_name
    cv2.imwrite(str(output_path), image)
    
    return output_path
