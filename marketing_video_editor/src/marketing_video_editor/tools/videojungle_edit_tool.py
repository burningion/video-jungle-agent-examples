from typing import Any, Optional, Type, List
from pydantic import BaseModel, ConfigDict
from .videojungle_basetool import VideoJungleApiBaseTool
from videojungle import VideoEditAsset, VideoEditAudioAsset
from datetime import datetime

class VideoJungleEditTool(VideoJungleApiBaseTool):
    """Tool for editing video files and assets on Video Jungle"""
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, frozen=False
    )
    name: str = "Video Jungle Edit"
    description: str = (
        "A tool to perform edits on your Video Jungle library."
    )
    args_schema: Type[BaseModel] = VideoJungleApiBaseTool.VideoEditSchema
    def _run(
        self,
        project_id: str,
        video_edit_version: str,
        video_output_format: str,
        video_output_resolution: str,
        video_output_fps: float,
        video_output_filename: str,
        video_series_sequential: List[VideoEditAsset],
        audio_overlay: Optional[List[VideoEditAudioAsset]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Run a video edit operation using the Video Jungle API.
        
        Args:
            project_id: The project identifier
            video_edit_version: Version identifier for this edit configuration
            video_output_format: Desired output video format (e.g., 'mp4', 'mov')
            video_output_resolution: Desired output resolution (e.g., '1920x1080')
            video_output_fps: Desired output frames per second
            video_output_filename: Desired filename for the output video
            video_series_sequential: Ordered list of video assets for the edit
            audio_overlay: Optional list of audio assets to overlay
        """
        try:
            create_edit = {
                "video_edit_version": video_edit_version,
                "video_output_format": video_output_format,
                "video_output_resolution": video_output_resolution,
                "video_output_fps": video_output_fps,
                "video_output_filename": video_output_filename,
                "video_series_sequential": [asset.dict() for asset in video_series_sequential],
                "audio_overlay": [audio.dict() for audio in (audio_overlay or [])]
            }
            
            return self.client.render_edit(project_id=project_id, create_edit=create_edit)
        except Exception as e:
            return f"An error occurred during video edit creation: {str(e)}"