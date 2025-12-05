"""
semiautomatic.image - Image processing utilities.

Public API:
    compress_for_api    Compress image for size-limited APIs (e.g., Claude Vision)
    compress_to_size    Progressive compression with full control
    process_single_image    Resize, convert, or compress a single image

Data classes:
    CompressionResult   Result of compression operation
    SizeSpec           Parsed size specification
"""

from semiautomatic.image.process import (
    # Main functions
    compress_for_api,
    compress_to_size,
    process_single_image,
    # Utilities
    parse_size,
    calculate_dimensions,
    find_images,
    get_unique_path,
    # Data classes
    CompressionResult,
    SizeSpec,
    # Constants
    DEFAULT_MAX_SIZE_BYTES,
    IMAGE_EXTENSIONS,
)

__all__ = [
    'compress_for_api',
    'compress_to_size',
    'process_single_image',
    'parse_size',
    'calculate_dimensions',
    'find_images',
    'get_unique_path',
    'CompressionResult',
    'SizeSpec',
    'DEFAULT_MAX_SIZE_BYTES',
    'IMAGE_EXTENSIONS',
]
