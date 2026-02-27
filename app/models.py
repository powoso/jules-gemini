from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SocialMediaPost(BaseModel):
    id: str
    source: str  # "reddit" or "twitter"
    author: str
    content: str
    url: str
    timestamp: Optional[str] = None
    media_url: Optional[str] = None
    avatar_url: Optional[str] = None
