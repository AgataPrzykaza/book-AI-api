from flask import Blueprint, request, jsonify
from services.book_service import BookService
from models.book import BookRecommendation
import traceback

recommendation_bp = Blueprint('recommendation', __name__)
book_service = BookService()

@recommendation_bp.route('/api/books/by-trope', methods=['POST'])
def get_books_by_trope():
    """Pobierz książki według tropu"""
    try:
        data = request.get_json()
        trope = data.get('trope')
        count = data.get('count', 5)
        genre = data.get('genre')
        
        if not trope:
            return jsonify({"error": "Trope is required"}), 400
        
        books = book_service.get_books_for_trope(trope, count, genre)
        return jsonify({
            "trope": trope,
            "genre": genre,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recommendation_bp.route('/api/books/by-trope/<trope>', methods=['GET'])
@recommendation_bp.route('/api/books/by-trope/<trope>/<int:count>', methods=['GET'])
@recommendation_bp.route('/api/books/by-trope/<trope>/<int:count>/<genre>', methods=['GET'])
def get_books_by_trope_url(trope, count=5, genre=None):
    """Pobierz książki według tropu przez URL"""
    try:
        books = book_service.get_books_for_trope(trope, count, genre)
        return jsonify({
            "trope": trope,
            "count": count,
            "genre": genre,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@recommendation_bp.route('/api/books/by-mood', methods=['POST'])
def get_books_by_mood():
    """Pobierz książki według nastroju"""
    try:
        data = request.get_json()
        mood = data.get('mood')
        read_books_data = data.get('read_books', [])
        count = data.get('count', 5)
        preferred_genres = data.get('preferred_genres')
        spice_level = data.get('spice_level')
        avoid_triggers = data.get('avoid_triggers')
        audience = data.get('audience')
        
        if not mood:
            return jsonify({"error": "Mood is required"}), 400
        
    
        read_books = []
        for book_data in read_books_data:
            if 'title' in book_data and 'author' in book_data:
                read_books.append(BookRecommendation(book_data['title'], book_data['author']))
            else:
                return jsonify({"error": "Each book must have 'title' and 'author'"}), 400
        
        recommendations = book_service.get_books_by_mood(
            mood, read_books, count, preferred_genres, spice_level, avoid_triggers, audience
        )
        
        return jsonify({
            "mood": mood,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in recommendations
            ]
        })
    
    except Exception as e:
        print(f"Error in mood recommendations: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@recommendation_bp.route('/api/books/by-mood/<mood>', methods=['GET'])
@recommendation_bp.route('/api/books/by-mood/<mood>/<int:count>', methods=['GET'])
def get_books_by_mood_url(mood, count=5):
    """Pobierz książki według nastroju przez URL"""
    try:
        recommendations = book_service.get_books_by_mood(mood, count=count)
        return jsonify({
            "mood": mood,
            "count": count,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in recommendations
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@recommendation_bp.route('/api/recommendations/history', methods=['POST'])
def get_recommendations_from_history():
    """Pobierz rekomendacje na podstawie historii czytania"""
    try:
        data = request.get_json()
        read_books_data = data.get('read_books', [])
        count = data.get('count', 5)
        preferred_genres = data.get('preferred_genres')
        exclude_authors = data.get('exclude_authors')
        
        if not read_books_data:
            return jsonify({"error": "read_books list is required"}), 400
        
     
        read_books = []
        for book_data in read_books_data:
            if 'title' in book_data and 'author' in book_data:
                read_books.append(BookRecommendation(book_data['title'], book_data['author']))
            else:
                return jsonify({"error": "Each book must have 'title' and 'author'"}), 400
        
        recommendations = book_service.get_recommendations_from_history(
            read_books, count, preferred_genres, exclude_authors
        )
        
        return jsonify({
            "based_on_books": [
                {"title": book.title, "author": book.author}
                for book in read_books
            ],
            "preferred_genres": preferred_genres,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in recommendations
            ]
        })
    
    except Exception as e:
        print(f"Error in history recommendations: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500