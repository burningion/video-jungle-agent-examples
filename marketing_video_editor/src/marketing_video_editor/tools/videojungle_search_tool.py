from typing import Any, Optional, Type, List
from pydantic import BaseModel, ConfigDict
from .videojungle_basetool import VideoJungleApiBaseTool
from datetime import datetime

class VideoJungleSearchTool(VideoJungleApiBaseTool):
    """Tool for searching for video files and assets on Video Jungle"""
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, frozen=False
    )
    name: str = "Video Jungle Search"
    description: str = (
        "A tool to perform to perform searches on your Video Jungel library."
    )
    args_schema: Type[BaseModel] =VideoJungleApiBaseTool.VideoSearchSchema
def _run(
    self,
    query: Optional[str] = None,
    limit: int = 10,
    project_id: Optional[str] = None,
    duration_min: Optional[float] = None,
    duration_max: Optional[float] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    tags: Optional[List[str]] = None,
    min_relevance: Optional[float] = None,
    include_segments: bool = True,
    include_related: bool = False,
    query_audio: Optional[str] = None,
    query_img: Optional[str] = None,
    **kwargs: Any,
) -> Any:
    try:
        search_params = {
            "query": query,
            "limit": limit,
            "project_id": project_id,
            "duration_min": duration_min,
            "duration_max": duration_max,
            "created_after": created_after,
            "created_before": created_before,
            "tags": tags,
            "min_relevance": min_relevance,
            "include_segments": include_segments,
            "include_related": include_related,
            "query_audio": query_audio,
            "query_img": query_img
        }
        
        # Remove None values to avoid sending unnecessary parameters
        search_params = {k: v for k, v in search_params.items() if v is not None}
        
        results = self.client.video_files.search(**search_params).as_dict()
        return results
    except Exception as e:
        return f"An error occurred: {str(e)}. Some parameters may be invalid."