from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('username', String(), unique=True),
              Column('password', String()),
              Column('is_super_user', Boolean(), default=False)
              )
