import argparse
import asyncio

from logger import logger
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

    models = await asyncio.gather(*tasks)
    with database.atomic():
        rows_updated = NearestStore.bulk_update(
            models,
            [NearestStore.city_id, NearestStore.store_id, NearestStore.distance]
        )
        logger.info(f'Updated {rows_updated} rows')


if __name__ == '__main__':
    parser = init_argparse()

    args = parser.parse_args()

    asyncio.run(main(cities=args.cities))



