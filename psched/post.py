
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    title: str
    content: str    
    create_date: datetime | None = None
    modify_date: datetime | None = None
    post_date: datetime | None = None
    post_id: int | None = None

    @staticmethod
    def create(title: str, content: str):
        return Post(
            title=title,
            content=content
        )

