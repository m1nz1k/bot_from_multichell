from sqlalchemy import Column, BigInteger, Sequence, Float, String, sql

from utils.db_api.db_gino import  TimedBaseModel

# Таблица в БД для хранения заявок на оплату.
class Product(TimedBaseModel):
    __tablename__ = 'products'
    id = Column(BigInteger, Sequence('product_id_seq'), primary_key=True)
    name = Column(String)
    size = Column(String)
    color = Column(String(30))
    status = Column(String(60))
    rent_user_id = Column(BigInteger)
    photo_id = Column(String(500))
    query: sql.select