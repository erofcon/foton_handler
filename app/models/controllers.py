from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

controllers = Table('controllers', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('controller_address', String(20)),
                    Column('login', String(20)),
                    Column('password', String(20))
                    )
