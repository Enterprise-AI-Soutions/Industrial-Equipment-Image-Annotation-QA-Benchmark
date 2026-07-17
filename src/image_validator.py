"""
Image validation and processing utilities.
Validates image files exist, loads images, checks dimensions,
and validates bounding boxes fit within actual image bounds.
"""

from pathlib import Path
from PIL import Image
import numpy as np
from src.config import IMAGE_DIR

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


def resolve_image_file(reference_name: str, image_dir: Path = IMAGE_DIR) -> Path | None:
    """
    Resolve an annotation image reference to an actual file in data/images/.

    Handles common mismatches between annotation filenames and actual files:
    - Extension differences  (pump.jpg -> pump_001.png)
    - Numeric suffix         (pump -> pump_001)
    - Underscore spacing     (air_compressor -> air_compressor_001)

    Parameters
    ----------
    reference_name : str
        The filename as written in the annotation JSON (e.g. "pump.jpg").
    image_dir : Path
        Directory to search.

    Returns
    -------
    Path or None
        Absolute path to the resolved file, or None if not found.
    """
    if not image_dir.exists():
        return None

    # 1. Exact match first
    exact = image_dir / reference_name
    if exact.exists():
        return exact

    # 2. Stem-based fuzzy match: strip suffix, search for stem anywhere in filename
    ref_stem = Path(reference_name).stem.lower()   # e.g. "pump"

    candidates = [
        f for f in image_dir.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    ]

    # Try: file stem starts with ref_stem (pump -> pump_001)
    for c in candidates:
        if c.stem.lower().startswith(ref_stem):
            return c

    # Try: ref_stem starts with file stem (longer ref shorter file)
    for c in candidates:
        if ref_stem.startswith(c.stem.lower()):
            return c

    return None


class ImageValidator:
    """Validates image files and their properties against annotation data."""

    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}

    def __init__(self, image_dir: Path = IMAGE_DIR):
        """Initialize with image directory."""
        self.image_dir = image_dir
        self.errors = []

    def validate_image_exists(self, filename: str) -> bool:
        """
        Check if image file exists in data/images directory.
        Also tries fuzzy resolution for mismatched filenames.
        """
        resolved = resolve_image_file(filename, self.image_dir)
        if resolved is None:
            self.errors.append(f"Image file not found: {filename} (searched in {self.image_dir})")
            return False
        return True

    def validate_image_format(self, filename: str) -> bool:
        """Validate that file has supported image format."""
        ext = Path(filename).suffix.lower()
        is_valid = ext in self.SUPPORTED_FORMATS
        if not is_valid:
            self.errors.append(
                f"Unsupported image format: {ext}. Supported: {self.SUPPORTED_FORMATS}"
            )
        return is_valid

    def load_image_pil(self, filename: str) -> Image.Image:
        """
        Load image using PIL/Pillow with fuzzy filename resolution.

        Returns
        -------
        PIL Image object

        Raises
        ------
        FileNotFoundError, ValueError
        """
        resolved = resolve_image_file(filename, self.image_dir)
        if resolved is None:
            raise FileNotFoundError(f"Image not found: {filename}")
        try:
            return Image.open(resolved)
        except Exception as e:
            raise ValueError(f"Cannot load image {filename}: {e}")

    def get_image_dimensions(self, filename: str) -> tuple | None:
        """
        Get actual image dimensions (width, height) by loading the file.

        Returns
        -------
        tuple (width, height) or None on error
        """
        try:
            img = self.load_image_pil(filename)
            return img.size   # PIL: (width, height)
        except Exception as e:
            self.errors.append(f"Cannot get dimensions for {filename}: {e}")
            return None

    def validate_bbox_within_image(self, filename: str, bbox: list) -> dict:
        """
        Validate that bounding box coordinates are within actual image dimensions.

        Parameters
        ----------
        filename : str
            Image filename from annotation.
        bbox : list
            [x, y, width, height]

        Returns
        -------
        dict
            {valid, image_width, image_height, resolved_filename, errors}
        """
        result = {
            "valid": False,
            "image_width": None,
            "image_height": None,
            "resolved_filename": None,
            "errors": [],
        }

        resolved = resolve_image_file(filename, self.image_dir)
        if resolved is None:
            result["errors"].append(f"Image file not found: {filename}")
            return result

        result["resolved_filename"] = resolved.name

        dims = self.get_image_dimensions(filename)
        if dims is None:
            result["errors"].append(f"Could not read dimensions from {filename}")
            return result

        img_w, img_h = dims
        result["image_width"] = img_w
        result["image_height"] = img_h

        x, y, w, h = bbox

        if x < 0 or y < 0:
            result["errors"].append(f"BBox has negative coordinates: x={x}, y={y}")
        if w <= 0 or h <= 0:
            result["errors"].append(f"BBox has non-positive size: w={w}, h={h}")
        if x + w > img_w:
            result["errors"].append(
                f"BBox exceeds image width: x({x})+w({w})={x+w} > img_width({img_w})"
            )
        if y + h > img_h:
            result["errors"].append(
                f"BBox exceeds image height: y({y})+h({h})={y+h} > img_height({img_h})"
            )

        result["valid"] = len(result["errors"]) == 0
        return result

    def get_errors(self) -> list:
        """Get list of validation errors."""
        return self.errors

    def clear_errors(self):
        """Clear error list."""
        self.errors = []


def validate_annotation_with_image(annotation: dict, image_validator: ImageValidator) -> tuple:
    """
    Validate a single annotation against its actual image file.

    Checks:
    - Image file exists (with fuzzy filename resolution)
    - BBox coordinates within actual image dimensions

    Parameters
    ----------
    annotation : dict
        Raw annotation dict with 'image' and 'bbox' keys.
    image_validator : ImageValidator

    Returns
    -------
    tuple: (is_valid, error_messages, image_info_dict)
    """
    errors = []
    image_filename = annotation.get('image', '')

    if not image_filename:
        errors.append("Annotation has no 'image' field")
        return False, errors, {}

    bbox = annotation.get('bbox', [])

    # Validate bbox within image bounds (also resolves filename and gets dims)
    result = image_validator.validate_bbox_within_image(image_filename, bbox)
    errors.extend(result["errors"])

    image_info = {
        "reference_filename": image_filename,
        "resolved_filename": result.get("resolved_filename"),
        "image_width": result.get("image_width"),
        "image_height": result.get("image_height"),
    }

    return result["valid"], errors, image_info
