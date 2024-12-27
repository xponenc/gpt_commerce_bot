from datetime import datetime

from db_models.db_models import GPTHistory
from db_start import async_session


async def write_data_to_table(data: list):
    async with async_session() as session:
        for item in data:
            new_gpt_msg = GPTHistory(user_id=item.get("user_id"),
                                     date_time=item.get("date_time"),
                                     is_bot_msg=item.get("is_bot_msg", False),
                                     message=item.get("message")
                                     )

            session.add(new_gpt_msg)
        await session.commit()
