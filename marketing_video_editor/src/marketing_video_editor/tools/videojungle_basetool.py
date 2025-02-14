import os
import re
from typing import Any, Optional, Union

from crewai.tools import BaseTool

class VideoJungleApiBaseTool(BaseTool):
    """Base class for SerpApi functionality with shared capabilities."""

    client: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            from videojungle import ApiClient,  VideoSearch, VideoFile, VideoEditAsset, VideoEditCreate  # type: ignore
        except ImportError:
            import click

            if click.confirm(
                "You are missing the 'videojungle' package. Would you like to install it?"
            ):
                import subprocess

                subprocess.run(["uv", "add", "videojungle"], check=True)
                from videojungle import ApiClient, VideoSearch, VideoFile, VideoEditAsset, VideoEditCreate 
            else:
                raise ImportError(
                    "`videojungle` package not found, please install with `uv add videojungle`"
                )
        api_key = os.getenv("VJ_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing API key, you can get the key from https://www.video-jungle.com/profile/settings"
            )
        self.client = ApiClient(token=api_key)
        self.VideoSearch = VideoSearch
        self.VideoFile = VideoFile
        self.VideoEditAsset = VideoEditAsset
        self.VideoEdit = VideoEditCreate

    def _omit_fields(self, data: Union[dict, list], omit_patterns: list[str]) -> None:
        if isinstance(data, dict):
            for field in list(data.keys()):
                if any(re.compile(p).match(field) for p in omit_patterns):
                    data.pop(field, None)
                else:
                    if isinstance(data[field], (dict, list)):
                        self._omit_fields(data[field], omit_patterns)
        elif isinstance(data, list):
            for item in data:
                self._omit_fields(item, omit_patterns)
