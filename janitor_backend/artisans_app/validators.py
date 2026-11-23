"""
This file runs some extra validation checks on some of the data that is being
sent to the server. It is used in the serializers.py file to validate data before it is saved
to the database.
"""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

MAX_IMAGE_SIZE_BYTES = 3 * 1024 * 1024  # 3MB

def validate_image_size(image_file):
    """
    Validates that the uploaded image file does not exceed
    the maximum allowed size of 3MB.
    
    args:
        image_file: The uploaded image file to validate.
    """
    if image_file.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError("Image file is too large. Maximum size allowed is 3MB.")



image_extension_validator = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png"],
    message="Only JPG, JPEG and PNG images are allowed."
)
