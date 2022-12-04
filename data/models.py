import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin):
    """Модель пользователя для работы с БД"""

    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    words = orm.relationship('Users_to_words', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Users_to_words(SqlAlchemyBase):
    __tablename__ = 'users_to_words'
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    word_id = sqlalchemy.Column(sqlalchemy.ForeignKey('words.id'))
    sqlalchemy.PrimaryKeyConstraint(user_id, word_id)

    user = orm.relationship('Users', back_populates='words')
    word = orm.relationship('Words', back_populates='users')


class Words(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "words"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    word_en = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False, unique=True)
    word_ru = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False, unique=True)

    users = orm.relationship('Users_to_words', back_populates='word')
