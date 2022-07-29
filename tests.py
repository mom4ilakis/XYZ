import unittest
from unittest.mock import patch
from datetime import datetime
from decimal import Decimal

from peewee import SqliteDatabase

from models import Cities, NearestStore

from main import main
from utils import Point, calculate_distance

MODELS = [Cities, NearestStore]

in_mem_db = SqliteDatabase(':memory:')


def create_some_cities() -> None:
    rows = [
        (1, 'Andorra la Vella', 488, '07', 6, 'AD', Decimal('42.50779'), Decimal('1.52109'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q1863'),
        (2, 'Arinsal', 493, '04', 6, 'AD', Decimal('42.57205'), Decimal('1.48453'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q24554'),
        (3, 'Canillo', 489, '02', 6, 'AD', Decimal('42.5676'), Decimal('1.59756'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q24554'),
        (4, 'El Tarter', 489, '02', 6, 'AD', Decimal('42.57952'), Decimal('1.65362'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q24413'),
        (5, 'Encamp', 487, '03', 6, 'AD', Decimal('42.53474'), Decimal('1.58014'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q24413'),
        (6, 'Ordino', 491, '05', 6, 'AD', Decimal('42.55623'), Decimal('1.53319'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q3885480'),
        (7, 'Pas de la Casa', 487, '03', 6, 'AD', Decimal('42.54277'), Decimal('1.73361'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q24456'),
        (8, 'Sant Julià de Lòria', 490, '06', 6, 'AD', Decimal('42.46372'), Decimal('1.49129'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2020-05-01 18:52:33'), 1, 'Q1120573'),
        (9, 'la Massana', 493, '04', 6, 'AD', Decimal('42.54499'), Decimal('1.51483'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q3820973'),
        (10, 'les Escaldes', 492, '08', 6, 'AD', Decimal('42.50729'), Decimal('1.53414'),
         datetime.fromisoformat('2019-10-05 23:58:06'), datetime.fromisoformat('2019-10-05 23:58:06'), 1, 'Q1050185')
    ]
    fields = [
        Cities.id,
        Cities.name,
        Cities.state_id,
        Cities.state_code,
        Cities.country_id,
        Cities.country_code,
        Cities.latitude,
        Cities.longitude,
        Cities.created_at,
        Cities.updated_at,
        Cities.flag,
        Cities.wiki_data_id
    ]

    with in_mem_db.atomic():
        Cities.insert_many(rows, fields).execute()


class MyTestCase(unittest.IsolatedAsyncioTestCase):

    def test_calculate_distance(self) -> None:
        a, b = Point(0, 0), Point(0, 10)

        actual = calculate_distance(a, b)

        self.assertEqual(10, actual)

    @patch('main.database', in_mem_db)
    async def test_cities(self) -> None:
        with in_mem_db:
            in_mem_db.bind(MODELS)

            in_mem_db.create_tables(MODELS)

            create_some_cities()

            print("Coroutine test")

            targets = (['Encamp', 'Ordino', 'Arinsal'], [5, 6, 2])

            await main(targets[0])
            actual = NearestStore.select().tuples().execute()
            self.assertIsNotNone(actual)
            self.assertEqual(set(targets[1]), set([t[1] for t in actual]))

            in_mem_db.drop_tables(MODELS)


if __name__ == '__main__':
    unittest.main()
