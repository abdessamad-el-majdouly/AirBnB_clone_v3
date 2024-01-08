#!/usr/bin/python3
""" Endpoints for place_amenity related interactions """

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', strict_slashes=False, methods=['GET'])
def place_amenities(place_id):
    """ Retrieve the list of all Amenity objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE', 'POST'])
def update_place_amenities(place_id, amenity_id):
    """ Delete, or link/unlink Amenity to/from Place based on the HTTP method """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    env = getenv('HBNB_TYPE_STORAGE')

    if place is None or amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)

    elif request.method == 'POST':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)

    place.save()
    return make_response(jsonify(amenity.to_dict()), 200 if request.method == 'DELETE' else 201)
