from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, DateTime, ForeignKey, Boolean
from .controllers import controllers

metadata = MetaData()

controller_data = Table('controller_data', metadata,
                        Column('id', Integer(), primary_key=True),
                        Column('vin', Integer()),
                        Column('vout', Integer()),
                        Column('temp', Integer()),
                        Column('charge', Integer()),
                        Column('relay', Integer()),
                        Column('year', Integer()),
                        Column('month', Integer()),
                        Column('date', Integer()),
                        Column('hour', Integer()),
                        Column('min', Integer()),
                        Column('sec', Integer()),
                        Column('status', Boolean(), default=False),
                        Column('create_data_datetime', DateTime(), default=datetime.utcnow()),
                        Column('controller_id', Integer(), ForeignKey(controllers.c.id, ondelete='CASCADE'))
                        )
