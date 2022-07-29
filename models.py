from peewee import *

from fields import MediumUnsignedInt, TinyInt

database = SqliteDatabase('task.db')


class BaseModel(Model):
    class Meta:
        database = database


class Cities(BaseModel):
    id = MediumUnsignedInt(primary_key=True)  # mediumint unsigned
    name = CharField()
    state_id = MediumUnsignedInt()  # mediumint unsigned
    state_code = CharField()
    country_id = MediumUnsignedInt()  # mediumint unsigned
    country_code = CharField()
    latitude = DecimalField()
    longitude = DecimalField()
    created_at = TimestampField()  # timestamp
    updated_at = TimestampField()  # timestamp
    flag = TinyInt(default=1)  # tinyint(1)
    wiki_data_id = CharField(column_name='wikiDataId', null=True)

    class Meta:
        table_name = 'cities'


class NearestStore(BaseModel):
    city_id = ForeignKeyField(Cities)
    store_id = IntegerField()
    distance = DecimalField(help_text='Distance between city and nearest store in a straight line in kilometers')


def clear_db():
    with database:
        database.drop_tables([NearestStore, Cities])


def init_db():
    with database:
        database.create_tables([NearestStore, Cities])


if __name__ == '__main__':
    init_db()