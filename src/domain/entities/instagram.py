from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class InstagramPost:
    post_id: str
    url: str
    caption: Optional[str] = None
    video_url: Optional[str] = None
    download_status: str = 'pending'
    error_message: Optional[str] = None
    created_at: datetime = None
    downloaded_at: Optional[datetime] = None
    file_path: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InstagramProfile:
    username: str
    total_posts: int
    bio: Optional[str] = None
    followers: Optional[int] = None
    following: Optional[int] = None
