import peewee

MAX_MEDIUM_UNSIGNED_INT = 16777215
MIN_UNSIGNED_INT = 0
MAX_TINY_INT = 255


class MediumUnsignedInt(peewee.IntegerField):
    field_type = 'mediumint unsigned'

    def db_value(self, value: int):
        if not MIN_UNSIGNED_INT <= value <= MAX_MEDIUM_UNSIGNED_INT:
            raise ValueError(f"{value} outside interval: Min: {MIN_UNSIGNED_INT},  Max:{MAX_MEDIUM_UNSIGNED_INT}")
        return super(MediumUnsignedInt, self).db_value(value)

    def python_value(self, value):
        return super(MediumUnsignedInt, self).python_value(value)


class TinyInt(peewee.IntegerField):
    field_type = 'tinyint'

    def db_value(self, value):
        if not MIN_UNSIGNED_INT <= value <= MAX_TINY_INT:
            raise ValueError(f"{value} outside interval: Min: {MIN_UNSIGNED_INT},  Max: {MAX_TINY_INT}")
        return super(TinyInt, self).db_value(value)

    def python_value(self, value):
        return super(TinyInt, self).python_value(value)