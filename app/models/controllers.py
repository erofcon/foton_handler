from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime

metadata = MetaData()

controllers = Table('controllers', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('controller_address', String()),
                    Column('login', String()),
                    Column('password', String()),
                    Column('create_date_time', DateTime(), default=datetime.utcnow())
                    )
