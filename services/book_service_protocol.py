from typing import Dict, List, Optional
from abc import ABC,abstractmethod

class BookServiceProtocol(ABC):
    @abstractmethod
    def get_book_genre(self, title: str, author: str) -> str:
        """Get precise genre for a book"""
        pass

    @abstractmethod
    def get_similar_books(self, title: str, author: str) -> List[str]:
        """Get 3 similar book recommendations"""
        pass

    
    @abstractmethod
    def get_books_for_trope(self, trope: str, count: int = 5, genre: Optional[str] = None) -> List:
        """Get book recommendations based on ttrope"""
        pass

    @abstractmethod
    def get_book_spice_level(self, title: str, author: str) -> dict: 
        """Get spice level and content warnings for a book"""
        pass

    
    @abstractmethod
    def get_book_tags(self, title: str, author: str, count: int = 10) -> List[str]:
        """Get tags for a book"""
        pass

    @abstractmethod
    def get_recommendations_from_history(self, 
                                       read_books: List,
                                       count: int = 5,
                                       preferred_genres: Optional[List[str]] = None,
                                       exclude_authors: Optional[List[str]] = None) -> List:
        """Get book recommendations based on reading history"""
        pass