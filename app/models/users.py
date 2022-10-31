from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('username', String(20), unique=True),
              Column('password', String(20)),
              Column('is_super_user', Boolean(), default=False)
              )
