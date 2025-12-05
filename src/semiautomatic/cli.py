"""
semiautomatic CLI - Main entry point for all commands.

Usage:
    semiautomatic <command> [options]
    sa <command> [options]  # alias

Commands:
    process-image    Batch resize, convert, and compress images
"""

import sys
import argparse
from importlib.metadata import version


def setup_windows_encoding():
    """
    Configure UTF-8 encoding for Windows console output.

    Only called at CLI entry, never on library import.
    This ensures Unicode characters (checkmarks, etc.) display correctly.
    """
    if sys.platform != "win32":
        return

    import io

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)


def cmd_process_image(args):
    """Handler for 'process-image' command."""
    from semiautomatic.image.process import run_process_image
    return run_process_image(args)


def build_parser():
    """Build the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog='semiautomatic',
        description='AI automation tools for creative workflows',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--version', action='version',
        version=f'%(prog)s {version("semiautomatic")}'
    )

    subparsers = parser.add_subparsers(
        title='commands',
        dest='command',
        metavar='<command>',
    )

    # process-image command
    process_image_parser = subparsers.add_parser(
        'process-image',
        help='Batch resize, convert, and compress images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Size formats:
  1920x1080     Exact dimensions (width x height)
  0.5           Scale to 50% of original size
  2.0           Scale to 200% (upscale)
  1920x         Width-constrained (preserve aspect ratio)
  x1080         Height-constrained (preserve aspect ratio)

Examples:
  semiautomatic process-image --size 1920x1080
  semiautomatic process-image --size 0.5
  semiautomatic process-image --format png
  semiautomatic process-image --input photo.jpg --size 0.5
  semiautomatic process-image --max-size 5  # Compress for Claude Vision API
        """
    )
    process_image_parser.add_argument(
        '--size', type=str, default=None,
        help='Target size: WxH (1920x1080), scale (0.5), or constrained (1920x, x1080)'
    )
    process_image_parser.add_argument(
        '--format', choices=['auto', 'png', 'jpeg'], default='auto',
        help='Output format: auto (preserve source), png, or jpeg (default: auto)'
    )
    process_image_parser.add_argument(
        '--quality', type=int, default=85,
        help='JPEG quality 1-100 (default: 85)'
    )
    process_image_parser.add_argument(
        '--max-size', type=float, default=None,
        help='Maximum file size in MB (enables compression mode)'
    )
    process_image_parser.add_argument(
        '--input', type=str, default=None,
        help='Input image file (for single file processing)'
    )
    process_image_parser.add_argument(
        '--input-dir', type=str, default='./input',
        help='Input directory for batch processing (default: ./input)'
    )
    process_image_parser.add_argument(
        '--output-dir', type=str, default='./output',
        help='Output directory (default: ./output)'
    )
    process_image_parser.set_defaults(func=cmd_process_image)

    return parser


def main():
    """Main CLI entry point."""
    setup_windows_encoding()

    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    try:
        result = args.func(args)
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
