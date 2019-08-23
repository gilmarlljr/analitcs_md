from datetime import datetime

import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase

from core.path import Path
from core.util import CustomEnum

db = PostgresqlExtDatabase('amd_tcc', user='amd_tcc', password='123',
                           host='localhost', port=5432,autorollback=True)



class BaseModel(peewee.Model):
    class Meta:
        database = db

    def to_dict(self):
        insert_dict = {}
        fields = self.__class__._meta.fields
        for attr, value in self.__data__.items():
            if type(fields[attr]) is peewee.ForeignKeyField:
                insert_dict[attr + "_id"] = value
            else:
                insert_dict[attr] = value

        return insert_dict


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


class User(BaseModel):
    class SOCIAL_MEDIAS(CustomEnum):
        TWITTER = ('T', 'twitter'),
        REDDIT = ('R', 'reddit')

    class GENDERS(CustomEnum):
        MALE = ('M', 'Male')
        FEMALE = ('F', 'Female')
        UNDEFINED = ('U', 'Undefined')
        NONE = ('N', 'None')

    username = peewee.CharField(max_length=50, primary_key=True)
    display_name = peewee.CharField(max_length=50, null=True)
    about = peewee.TextField(null=True)
    social_media = peewee.CharField(max_length=1)
    gender = peewee.CharField(max_length=1, default=GENDERS.NONE)


class Post(BaseModel):
    md5 = peewee.CharField(max_length=32, primary_key=True, index=True, null=False)
    user = peewee.ForeignKeyField(User)
    title = peewee.CharField(max_length=50, null=True)
    content = peewee.TextField(null=True)
    date_time = peewee.DateTimeField(null=True, default=datetime.now())
    likes_score = peewee.IntegerField(null=True)
    url = peewee.CharField(max_length=250, null=True)
    main_url = peewee.CharField(max_length=250, null=True)


class Embendding(BaseModel):
    post = peewee.ForeignKeyField(Post)
    characters_count = peewee.IntegerField()
    words_count = peewee.IntegerField()
    stopwords_count = peewee.IntegerField()
    numerics_count = peewee.IntegerField()
    uppercase_count = peewee.IntegerField()
    average_word_length = peewee.FloatField()
    content_cleaned = peewee.TextField()
    empath = peewee.TextField()
    word_to_vec = peewee.TextField()
