# Path: apps/core/utils.py
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import slugify
import os
import uuid
from io import BytesIO

class ImageHandler:
    """Simplified utility class for image handling and optimization"""

    @staticmethod
    def generate_unique_filename(filename):
        """Generate a unique filename while preserving extension"""
        name, ext = os.path.splitext(filename)
        return f"{slugify(name)}-{uuid.uuid4().hex[:8]}{ext}"

    @staticmethod
    def optimize_image(image_file, max_size=(800, 800), quality=85):
        """
        Optimize image size and quality.
        Returns a BytesIO object containing the optimized image.
        """
        img = Image.open(image_file)

        # Convert to RGB if needed
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background

        # Resize if larger than max_size
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save optimized image
        output = BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return output

    @classmethod
    def save_and_optimize_image(cls, image_file, path):
        """Save and optimize an image file"""
        filename = cls.generate_unique_filename(image_file.name)
        full_path = os.path.join(path, filename)

        # Optimize the image
        optimized = cls.optimize_image(image_file)

        # Save the optimized image
        default_storage.save(full_path, ContentFile(optimized.getvalue()))

        return full_path
    