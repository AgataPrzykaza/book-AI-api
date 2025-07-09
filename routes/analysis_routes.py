from flask import Blueprint, request, jsonify
from services.book_service import BookService
from models.book import BookRecommendation
import traceback

analysis_bp = Blueprint('analysis', __name__)
book_service = BookService()

@analysis_bp.route('/api/analyze/reading-patterns', methods=['POST'])
def analyze_reading_patterns():
    """Analizuj wzorce czytania użytkownika"""
    try:
        data = request.get_json()
        read_books_data = data.get('read_books', [])
        
        if not read_books_data:
            return jsonify({"error": "read_books list is required"}), 400
        
        # Konwertuj dane na obiekty Book
        read_books = []
        for book_data in read_books_data:
            if 'title' in book_data and 'author' in book_data:
                read_books.append(BookRecommendation(book_data['title'], book_data['author']))
            else:
                return jsonify({"error": "Each book must have 'title' and 'author'"}), 400
        
        # Wywołaj analizę wzorców
        patterns = book_service.analyze_reading_patterns(read_books)
        
        return jsonify({
            "analyzed_books_count": len(read_books),
            "patterns": patterns
        })
    
    except Exception as e:
        print(f"Error in reading patterns analysis: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500