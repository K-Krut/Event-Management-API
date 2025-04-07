import base64
import imghdr
from django.core.files.base import ContentFile


def base64_to_image_file(base64_string, filename="avatar"):
    if "base64," in base64_string:
        base64_string = base64_string.split("base64,")[1]

    decoded = base64.b64decode(base64_string)
    extension = imghdr.what(None, decoded) or "png"
    return ContentFile(decoded, name=f"{filename}.{extension}")


def convert_file(file_str):
    if file_str:
        try:
            return base64_to_image_file(file_str)
        except Exception:
            return None
    return None
