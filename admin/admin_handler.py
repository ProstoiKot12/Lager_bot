from aiogram.types import Message

from files.config import ADMIN_ID
from keyboards.admin_keyboards import admin_panel_kb
from request.sql_request import get_admin_id

async def admin_panel(message: Message):
    admin_id = await get_admin_id()
    for row in admin_id:
        admin_id_value = row[0]
        if message.from_user.id == admin_id_value:
            await message.answer('<b>Админ панель</b>', reply_markup=admin_panel_kb)
