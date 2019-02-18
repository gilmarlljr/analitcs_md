from datetime import datetime

import peewee

from core.path import Path
from core.util import md5_text, CustomEnum

db = peewee.SqliteDatabase(Path.db)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class VersionControl(BaseModel):
    app_version = peewee.IntegerField(null=False)


class RedditConfig(BaseModel):
    client_id = peewee.CharField(max_length=14, null=True)
    client_secret = peewee.CharField(max_length=27, null=True)
    username = peewee.CharField(max_length=250, null=True)
    password = peewee.CharField(max_length=250, null=True)
    user_agent = peewee.CharField(max_length=250, null=True)


class RedditPage(BaseModel):
    url = peewee.CharField(max_length=250, primary_key=True, null=True)
    reddit_config = peewee.ForeignKeyField(RedditConfig)


class Config(BaseModel):
    md5 = peewee.CharField(max_length=32, null=True)
    reddit_config = peewee.ForeignKeyField(RedditConfig)


class Post(BaseModel):
    class SOCIAL_MEDIAS(CustomEnum):
        TWITTER = ('T', 'twitter'),
        REDDIT = ('R', 'reddit')

    class GENDERS(CustomEnum):
        MALE = ('M', 'Male')
        FEMALE = ('F', 'Female')
        UNDEFINED = ('U', 'Undefined')
        NONE = ('N', 'None')

    username = peewee.CharField(max_length=50, null=True)
    title = peewee.CharField(max_length=50, null=True)
    content = peewee.TextField(null=True)
    social_media = peewee.CharField(max_length=1)
    gender = peewee.CharField(max_length=1, default=GENDERS.NONE)
    date_time = peewee.DateTimeField(null=True, default=datetime.now())
    likes_score = peewee.IntegerField(null=True)
    url = peewee.CharField(max_length=250, null=True)
    md5 = peewee.CharField(max_length=32,unique=True,index=True,null=False)
    main_url = peewee.CharField(max_length=250, null=True)
