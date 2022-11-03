from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, DateTime, ForeignKey
from .controllers import controllers

metadata = MetaData()

controller_data = Table('controller_data', metadata,
                        Column('id', Integer(), primary_key=True),
                        Column('vout', Integer()),
                        Column('temp', Integer()),
                        Column('charge', Integer()),
                        Column('relay', Integer()),
                        Column('vch', Integer()),
                        Column('data_datetime', DateTime(), default=datetime.utcnow()),
                        Column('controller_id', Integer(), ForeignKey(controllers.c.id))
                        )
