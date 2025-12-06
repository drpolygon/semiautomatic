"""
Video processing module for semiautomatic.

Provides video manipulation tools including speed adjustment, zoom effects,
resize, trim, and frame extraction operations.

Library usage:
    from semiautomatic.video import process_video, extract_frame_from_video

    # Process video with speed and zoom
    output = process_video(
        Path('input.mp4'),
        Path('./output'),
        speed=1.5,
        zoom_h=(100, 150)
    )

    # Extract a single frame
    frame = extract_frame_from_video(
        Path('video.mp4'),
        Path('./output'),
        frame_position='last'
    )

CLI usage:
    semiautomatic process-video --speed 1.25
    semiautomatic process-video --zoom 100:150
    semiautomatic process-video --extract-frame last
"""

from semiautomatic.video.process import (
    process_video,
    run_process_video,
    ProcessingResult,
)
from semiautomatic.video.frames import (
    extract_frame_from_video,
    extract_single_frame,
    extract_frames,
    process_frames_with_zoom,
    create_speed_ramped_frames,
    FrameExtractionResult,
)
from semiautomatic.video.info import (
    get_video_info,
    get_unique_output_path,
    find_videos,
    parse_size,
    parse_zoom,
    VideoInfo,
    ZoomSpec,
)
from semiautomatic.video.easing import (
    apply_easing_curve,
    EASING_CURVES,
)
from semiautomatic.video.ffmpeg import (
    build_ffmpeg_filter,
    assemble_video,
    process_video_simple,
)

__all__ = [
    # Main processing
    "process_video",
    "run_process_video",
    "ProcessingResult",
    # Frame operations
    "extract_frame_from_video",
    "extract_single_frame",
    "extract_frames",
    "process_frames_with_zoom",
    "create_speed_ramped_frames",
    "FrameExtractionResult",
    # Video info
    "get_video_info",
    "get_unique_output_path",
    "find_videos",
    "parse_size",
    "parse_zoom",
    "VideoInfo",
    "ZoomSpec",
    # Easing
    "apply_easing_curve",
    "EASING_CURVES",
    # FFmpeg
    "build_ffmpeg_filter",
    "assemble_video",
    "process_video_simple",
]
