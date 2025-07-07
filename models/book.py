from dataclasses import dataclass
from typing import List, Optional

@dataclass
class BookRecommendation:
    title: str
    author: str
    
    @classmethod
    def from_string(cls, book_string: str):
        """Parse 'Title by Author' format"""
        if ' by ' in book_string:
            title, author = book_string.split(' by ', 1)
            return cls(title.strip(), author.strip())
        return cls(book_string.strip(), "Unknown")