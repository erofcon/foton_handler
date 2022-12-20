from datetime import datetime, timedelta

from sqlalchemy import text

from app.models.database import database


async def get_controller_data_between_two_datetime(controller_id: int, start_datetime: datetime,
                                                   end_datetime: datetime):
    step = 1
    delta = end_datetime - start_datetime

    if delta.days > 7:
        step = 2

    if delta.days > 30:
        step = 3

    if delta.days > 60:
        step = 4

    query = text(
        f"""
        SELECT id, vin, vout, temp, charge, relay, create_data_datetime
        FROM controller_data 
        WHERE controller_id={controller_id}
        AND create_data_datetime >= '{start_datetime.date()}'
        AND create_data_datetime < '{(end_datetime + timedelta(days=1)).date()}' 
        AND status=true 
        AND id%{step} = 0
        ORDER BY create_data_datetime
        """
    )

    return await database.fetch_all(query=query)
