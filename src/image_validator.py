"""
Image validation and processing utilities.
Validates image files exist, loads images, and validates image properties.
"""

from pathlib import Path
from PIL import Image
import cv2
import numpy as np
from src.config import IMAGE_DIR


class ImageValidator:
    """Validates image files and their properties."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    def __init__(self, image_dir: Path = IMAGE_DIR):
        """Initialize with image directory."""
        self.image_dir = image_dir
        self.errors = []
    
    def validate_image_exists(self, filename: str) -> bool:
        """
        Check if image file exists in data/images directory.
        
        Args:
            filename: Name of image file
            
        Returns:
            bool: True if file exists, False otherwise
        """
        image_path = self.image_dir / filename
        exists = image_path.exists()
        if not exists:
            self.errors.append(f"Image file not found: {filename} at {image_path}")
        return exists
    
    def validate_image_format(self, filename: str) -> bool:
        """
        Validate that file has supported image format.
        
        Args:
            filename: Name of image file
            
        Returns:
            bool: True if format is supported
        """
        ext = Path(filename).suffix.lower()
        is_valid = ext in self.SUPPORTED_FORMATS
        if not is_valid:
            self.errors.append(f"Unsupported image format: {ext}. Supported: {self.SUPPORTED_FORMATS}")
        return is_valid
    
    def load_image_pil(self, filename: str) -> Image.Image:
        """
        Load image using PIL/Pillow.
        
        Args:
            filename: Name of image file
            
        Returns:
            PIL Image object
            
        Raises:
            FileNotFoundError: If image not found
            ValueError: If image cannot be loaded
        """
        image_path = self.image_dir / filename
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            raise ValueError(f"Cannot load image {filename}: {str(e)}")
    
    def load_image_cv2(self, filename: str) -> np.ndarray:
        """
        Load image using OpenCV.
        
        Args:
            filename: Name of image file
            
        Returns:
            OpenCV image array (BGR format)
            
        Raises:
            FileNotFoundError: If image not found
            ValueError: If image cannot be loaded
        """
        image_path = self.image_dir / filename
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Cannot load image {filename} with OpenCV")
        
        return image
    
    def get_image_dimensions(self, filename: str) -> tuple:
        """
        Get image dimensions (width, height).
        
        Args:
            filename: Name of image file
            
        Returns:
            tuple: (width, height) in pixels
        """
        try:
            image = self.load_image_pil(filename)
            return image.size  # PIL returns (width, height)
        except Exception as e:
            self.errors.append(f"Cannot get dimensions for {filename}: {str(e)}")
            return None
    
    def validate_bbox_within_image(self, filename: str, bbox: list) -> bool:
        """
        Validate that bounding box fits within image boundaries.
        
        Args:
            filename: Name of image file
            bbox: Bounding box as [x, y, width, height]
            
        Returns:
            bool: True if bbox is within image, False otherwise
        """
        try:
            width, height = self.get_image_dimensions(filename)
            if width is None or height is None:
                return False
            
            x, y, w, h = bbox
            
            # Check bounds
            if x < 0 or y < 0:
                self.errors.append(f"BBox has negative coordinates: x={x}, y={y}")
                return False
            
            if x + w > width or y + h > height:
                self.errors.append(f"BBox exceeds image bounds: ({x}+{w}={x+w} > {width}) or ({y}+{h}={y+h} > {height})")
                return False
            
            return True
        except Exception as e:
            self.errors.append(f"Cannot validate bbox: {str(e)}")
            return False
    
    def get_errors(self) -> list:
        """Get list of validation errors."""
        return self.errors
    
    def clear_errors(self):
        """Clear error list."""
        self.errors = []


def validate_annotation_with_image(annotation: dict, image_validator: ImageValidator) -> tuple:
    """
    Validate annotation against actual image.
    
    Args:
        annotation: Annotation dict with image, bbox, etc.
        image_validator: ImageValidator instance
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check image exists
    if not image_validator.validate_image_exists(annotation.get('image', '')):
        errors.append(f"Image not found: {annotation.get('image')}")
        return False, errors
    
    # Check bbox is within image
    bbox = annotation.get('bbox', [])
    if not image_validator.validate_bbox_within_image(annotation.get('image', ''), bbox):
        errors.extend(image_validator.get_errors())
        image_validator.clear_errors()
        return False, errors
    
    return True, errors
