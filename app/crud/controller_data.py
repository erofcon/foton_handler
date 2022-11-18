from datetime import datetime, timedelta

from sqlalchemy import text

from app.models.database import database


async def get_controller_data_between_two_datetime(controller_id: int, start_datetime: datetime,
                                                   end_datetime: datetime):
    query = text(
        f"""SELECT vin, vout, temp, charge, relay, status, create_data_datetime
                FROM controller_data 
                WHERE controller_id={controller_id} and create_data_datetime >= '{start_datetime.date()}'
                AND create_data_datetime < '{(end_datetime + timedelta(days=1)).date()}' order by create_data_datetime
        """)

    return await database.fetch_all(query=query)
