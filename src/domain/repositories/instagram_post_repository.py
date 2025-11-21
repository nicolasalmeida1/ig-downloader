from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.instagram import InstagramPost


class InstagramPostRepository(ABC):
    
    @abstractmethod
    def save(self, post: InstagramPost) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, post_id: str) -> Optional[InstagramPost]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[InstagramPost]:
        pass
    
    @abstractmethod
    def update(self, post: InstagramPost) -> None:
        pass
    
    @abstractmethod
    def delete(self, post_id: str) -> None:
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[InstagramPost]:
        pass
