import argparse
import asyncio

from models import NearestStore, database
from utils import distance_to_nearest_shop, db_cities_paginated_iterator


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [Cities}",
        description='Calculate and save the distance to nearest shop for each city'
    )

    parser.add_argument('-c', '--cities', nargs='*', help='Names of cities')

    return parser


async def main(cities: list) -> None:
    tasks = [distance_to_nearest_shop(city) for city in db_cities_paginated_iterator(cities)]

    rows = await asyncio.gather(*tasks)

    with database.atomic():
        NearestStore.insert_many(rows, [NearestStore.city_id, NearestStore.store_id, NearestStore.distance]).execute()


if __name__ == '__main__':
    parser = init_argparse()

    args = parser.parse_args()

    print(args.cities)

    asyncio.run(main(cities=args.cities))



