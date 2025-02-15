from typing import Any, Optional, Type, List
from pydantic import BaseModel, ConfigDict
from .videojungle_basetool import VideoJungleApiBaseTool
import yt_dlp
import uuid
from datetime import datetime

class VideoJungleDownloadTool(VideoJungleApiBaseTool):
    """Tool for uploading video files and assets to Video Jungle"""
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, frozen=False
    )
    name: str = "Video Jungle Video Downloader"
    description: str = (
        "A tool to download and analyze videos on Video Jungle."
    )
    args_schema: Type[BaseModel] = VideoJungleApiBaseTool.VideoUploadSchema
    def _run(
        self,
        name: str,
        filename: str,
        upload_method: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Create and uplload a video file from a local file path or URL.
        Upload method must be 'url', and filename must contain the URL in order to download from a url.
        """
        try:
            if upload_method != 'url':
                self.client.video_files.create(name=name, filename=filename)
            elif upload_method == 'url':
                opts = {
                    'format': 'best',
                    'outtmpl': f'{str(uuid.uuid4())}.mp4'
                }
                with yt_dlp.YoutubeDL() as ydl:
                    ydl.download([filename])    
                
                self.client.video_files.create(name=name, filename=opts['outtmpl'])
            
        except Exception as e:
            return f"An error occurred during video edit creation: {str(e)}"