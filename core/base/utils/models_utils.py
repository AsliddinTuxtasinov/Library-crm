from os.path import splitext

from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify


def slugify_upload(instance, filename):
    """
    Generate a slugified upload path for a file based on the model name and file name.

    Args:
        instance: The instance of the model the file is associated with.
        filename: The original file name including the extension.

    Returns:
        str: A string representing the upload path in the format 'model_name/slugified_file_name.extension'.
    """
    # Retrieve the model name associated with the instance (lowercased)
    folder = ContentType.objects.get_for_model(instance).model

    # Split the file name into the base name and extension
    name, ext = splitext(filename)

    # Slugify the base name (replace spaces and special characters with hyphens)
    # If slugify returns an empty string, fall back to the original name
    slugified_name = slugify(name) or name

    # Construct and return the final upload path
    return f"{folder}/{slugified_name}{ext}"
