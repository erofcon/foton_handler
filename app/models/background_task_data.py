from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, DateTime, String

metadata = MetaData()

background_task_data = Table('background_task_data', metadata,
                             Column('id', Integer(), primary_key=True),
                             Column('task_id', String()),
                             Column('status', String(10)),
                             Column('task_create_datetime', DateTime(), default=datetime.now())
                             )
