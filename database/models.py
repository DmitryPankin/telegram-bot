from datetime import datetime
import peewee as orm

db = orm.SqliteDatabase('bot_hotels.db')


class BaseModel(orm.Model):
    created_request = orm.DateField(default=datetime.now())

    class Meta:
        database = db


class History(BaseModel):
    user_id = orm.TextField()
    request = orm.TextField()

    class Meta:
        order_by = 'user_id'


def db_create():
    with db:
        db.create_tables([History])


if __name__ == '__main__':
    db_create()
