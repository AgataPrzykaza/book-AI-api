from flask import Blueprint, request, jsonify
from services.book_service import BookService
from models.book import BookRecommendation

book_bp = Blueprint('book', __name__)
book_service = BookService()

@book_bp.route('/api/book/genre', methods=['POST'])
def get_book_genre():
    """Pobierz gatunek książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        genre = book_service.get_book_genre(title, author)
        return jsonify({
            "title": title,
            "author": author,
            "genre": genre
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@book_bp.route('/api/book/genre/<title>/<author>', methods=['GET'])
def get_book_genre_url(title, author):
    """Pobierz gatunek książki przez URL"""
    try:
        genre = book_service.get_book_genre(title, author)
        return jsonify({
            "title": title,
            "author": author,
            "genre": genre
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@book_bp.route('/api/book/similar', methods=['POST'])
def get_similar_books():
    """Pobierz podobne książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        similar_books = book_service.get_similar_books(title, author)
        return jsonify({
            "original_book": {"title": title, "author": author},
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in similar_books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@book_bp.route('/api/book/similar/<title>/<author>', methods=['GET'])
def get_similar_books_url(title, author):
    """Pobierz podobne książki przez URL"""
    try:
        similar_books = book_service.get_similar_books(title, author)
        return jsonify({
            "original_book": {"title": title, "author": author},
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in similar_books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@book_bp.route('/api/book/spice-level', methods=['POST'])
def get_spice_level():
    """Pobierz poziom pikantności książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        spice_data = book_service.get_book_spice_level(title, author)
        return jsonify({
            "title": title,
            "author": author,
            "spice_level": spice_data.get("spice_level", 0),
            "content_warnings": spice_data.get("content_warnings", [])
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@book_bp.route('/api/book/spice-level/<title>/<author>', methods=['GET'])
def get_spice_level_url(title, author):
    """Pobierz poziom pikantności książki przez URL"""
    try:
        spice_data = book_service.get_book_spice_level(title, author)
        return jsonify({
            "title": title,
            "author": author,
            "spice_level": spice_data.get("spice_level", 0),
            "content_warnings": spice_data.get("content_warnings", [])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@book_bp.route('/api/book/tags/<title>/<author>', methods=['GET'])
@book_bp.route('/api/book/tags/<title>/<author>/<int:count>', methods=['GET'])
def get_book_tags_url(title, author, count=10):
    """Pobierz tagi książki przez URL"""
    try:
        tags = book_service.get_book_tags(title, author, count)
        return jsonify({
            "title": title,
            "author": author,
            "count": count,
            "tags": tags
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@book_bp.route('/api/book/tags', methods=['POST'])
def get_book_tags():
    """Pobierz tagi książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        count = data.get('count', 10)
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        tags = book_service.get_book_tags(title, author, count)
        return jsonify({
            "title": title,
            "author": author,
            "tags": tags
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500