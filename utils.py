from math import sqrt
from collections import namedtuple

from peewee import ModelSelect

from models import Cities
import store_locator

Point = namedtuple('Point', ['x', 'y'])


def calculate_distance(point_a: Point, point_b: Point) -> float:
    return round(sqrt((point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2), 2)


def db_cities_paginated_iterator(city_names: list, page_size=100) -> ModelSelect:
    page = 1
    while record := Cities.select().where(Cities.name.in_(city_names)).paginate(page, page_size):
        yield from record
        page += 1


async def locate_nearest_store(city_location: Point) -> dict:
    return store_locator.get_nearest_store(city_location.x, city_location.y)


async def distance_to_nearest_shop(city: Cities) -> tuple:
    city_point = Point(float(city.longitude), float(city.latitude))

    nearest_store = await locate_nearest_store(city_point)

    distance = calculate_distance(city_point, Point(nearest_store['latitude'], nearest_store['longitude']))

    return city.id, nearest_store['store_id'], distance
