#!/usr/bin/python3
"""The View for Review Object"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def get_reviews(place_id):
    """Get reviews of a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        props = request.get_json()
        if "user_id" not in props:
            abort(400, "Missing user_id")
        if "text" not in props:
            abort(400, "Missing text")

        user = storage.get(User, props["user_id"])
        if user is None:
            abort(404)
        new_review = Review(**props)
        new_review.user_id = user_id
        storage.new(new_review)
        storage.save()

        return jsonify(new_review), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def get_review(review_id):
    """Get a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()

        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "not a JSON")
        props = request.get_json()
        for key, value in props.items():
            if key not in ["id", "user_id", "place_id", "created_at",
                    "updated_at"]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
