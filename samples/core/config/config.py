import peewee
from core.persistence.db import db


class RedditConfig(peewee.Model):
    client_id = peewee.CharField(max_length=50, null=True)
    client_secret = peewee.CharField(max_length=250, null=True)
    password = peewee.CharField(max_length=250, null=True)
    user_agent = peewee.CharField(max_length=250, null=True)
    username = peewee.CharField(max_length=250, null=True)

    class Meta:
        database = db


class Config(peewee.Model):
    reddit_config = peewee.ForeignKeyField(RedditConfig)

    class Meta:
        database = db


if __name__ == '__main__':
    try:
        RedditConfig.create_table()
    except peewee.OperationalError:
        print('Tabela Author ja existe!')
    try:
        Config.create_table()
    except peewee.OperationalError:
        print('Tabela Author ja existe!')

    rc =  RedditConfig.create(client_id='123',
                        client_secret='AWDAS',
                        password='QWEQW',
                        user_agent='QWEQW',
                        username='QWEQWE')

    config = Config.create(reddit_config=rc)
