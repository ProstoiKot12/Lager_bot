from aiogram.types import Message

from keyboards.user_keyboards import authenticated_kb, main_menu_kb
from request.sql_request import read_us_id_user_table, read_us_id_points_table, get_admin_id


async def start_handler(message: Message):
    admin_id = await get_admin_id()
    await message.answer('''Привет! 👋На связи главный Маэстро параллельной вселенной <b>АРT-V.</b>

☺️<b>В АRT-V ВСЕЛЕННОЙ каждый персонаж обладает особыми качествами, каждый класс персонажей называется по-своему:</b>

✊ Свершитель, 
🫴Интеллигент,
🙌Телепат, 
🤝Друг, 
👌Деятель,
🤟Виртуоз, 

Прежде чем начать побеждать пустоты и освобождать Вселенную, вам необходимо пройти идентификацию личности! Удачи! 🔥🔥🔥🍀''', reply_markup=authenticated_kb)
    for row in admin_id:
        admin_id_value = row[0]
        if message.from_user.id == admin_id_value:
            await message.answer('Привет админ, чтобы включить админ панель пропиши /admin')

async def main_menu(message: Message):
    wall = await read_us_id_user_table(message.from_user.id)
    wall1 = await read_us_id_points_table(message.from_user.id)
    if wall == True:
        await message.answer('Вам нужно пройти индефицировать себя')
        if wall1 == True:
            await message.answer('Вам нужно пройти тест')
    elif wall == False:
        await message.answer('<b>Главное меню</b>', reply_markup=main_menu_kb)
