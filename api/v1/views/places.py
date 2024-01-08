#!/usr/bin/python3
"""Module to handle API actions related to Place objects"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for places based on JSON data in the request body"""
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Not a JSON"}), 400

    if not data or not any(data.values()):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])

    if not isinstance(states, list) or not isinstance(cities, list) or not isinstance(amenities, list):
        return jsonify({"error": "Invalid data format"}), 400

    place_ids = set()

    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            place_ids.update([place.id for city in state.cities for place in city.places])

    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            place_ids.update([place.id for place in city.places])

    if amenities:
        amenities_set = set(amenities)
        place_ids = [place_id for place_id in place_ids if amenities_set.issubset(place.amenities)]

    places = [storage.get(Place, place_id) for place_id in place_ids if storage.get(Place, place_id)]

    return jsonify([place.to_dict() for place in places])


if __name__ == "__main__":
    pass
