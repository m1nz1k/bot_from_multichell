from sqlalchemy import Column, BigInteger, Boolean, String, sql
from utils.db_api.db_gino import TimedBaseModel


# Основная таблица в БД для хранения данных пользователя.
class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    status = Column(String(30))
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    query: sql.select