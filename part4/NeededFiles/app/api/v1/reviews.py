#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask_jwt_extended import jwt_required
from app.models.review import Review

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'id': fields.String(readOnly=True),
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String,
    'place_id': fields.String
})

review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()

    @api.expect(review_input_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        return facade.create_review(api.payload), 201

@api.route('/<string:id>')
@api.param('id', 'The review identifier')
@api.response(404, 'Review not found')
class Review(Resource):
    @api.marshal_with(review_model)
    def get(self, id):
        """Get a review by ID"""
        review = facade.get_review_by_id(id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.expect(review_input_model)
    @api.marshal_with(review_model)
    def put(self, id):
        """Update a review by ID"""
        try:
            return facade.update_review(id, api.payload)
        except ValueError as e:
            api.abort(404, str(e))

    def delete(self, id):
        """Delete a review by ID"""
        try:
            facade.delete_review(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))
