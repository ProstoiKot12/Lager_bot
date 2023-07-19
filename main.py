import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from files.config import TOKEN, ADMIN_ID
from utils.commands import set_commands
from request.sql_request import create_table
from user.user_handler import start_handler, main_menu
from user.user_callback import authenticated_test_name, Form, test_state_1, test_state_2, test_state_3, test_state_4, \
                               character_test_call, character_test_1, character_test_2, character_test_3, \
                               character_test_4, character_test_5, character_test_6, character_test_7, \
                               character_test_8, character_test_9, character_test_10, character_test_11, \
                               character_test_12, character_test_13, character_test_14, character_test_15, \
                               character_test_16, character_test_17, character_test_18, what_scoring, \
                               what_scoring_remove, main_menu_call, my_points, my_character, universe_rules
from admin.admin_handler import admin_panel
from admin.admin_callback import admin_add, Admin_Form, admin_add_state, admin_panel_call, admin_remove, \
                                 admin_remove_state, children_list, delete_children, children_delete_state, \
                                 view_childrens_points, view_children_points, view_children_state, \
                                 children_points_plus_state_1, children_points_plus_state_2, children_points_plus, \
                                 children_points_plus_state_3, children_points_minus, children_points_minus_state_1, \
                                 children_points_minus_state_2, children_points_minus_state_3

router = Router()

async def start_bot(bot: Bot):
    await set_commands(bot)
    await create_table()
    await bot.send_message(ADMIN_ID, text='Бот запущен!')

async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(TOKEN, parse_mode="HTML")

    dp.startup.register(start_bot)

    dp.message.register(start_handler, Command('start'))
    dp.message.register(main_menu, Command('main'))
    dp.message.register(admin_panel, Command('admin'))

    dp.message.register(test_state_1, Form.test_state_1)
    dp.message.register(test_state_2, Form.test_state_2)
    dp.message.register(test_state_3, Form.test_state_3)
    dp.message.register(test_state_4, Form.test_state_4)

    dp.message.register(character_test_1, Form.character_test_1)
    dp.message.register(character_test_2, Form.character_test_2)
    dp.message.register(character_test_3, Form.character_test_3)
    dp.message.register(character_test_4, Form.character_test_4)
    dp.message.register(character_test_5, Form.character_test_5)
    dp.message.register(character_test_6, Form.character_test_6)
    dp.message.register(character_test_7, Form.character_test_7)
    dp.message.register(character_test_8, Form.character_test_8)
    dp.message.register(character_test_9, Form.character_test_9)
    dp.message.register(character_test_10, Form.character_test_10)
    dp.message.register(character_test_11, Form.character_test_11)
    dp.message.register(character_test_12, Form.character_test_12)
    dp.message.register(character_test_13, Form.character_test_13)
    dp.message.register(character_test_14, Form.character_test_14)
    dp.message.register(character_test_15, Form.character_test_15)
    dp.message.register(character_test_16, Form.character_test_16)
    dp.message.register(character_test_17, Form.character_test_17)
    dp.message.register(character_test_18, Form.character_test_18)

    dp.message.register(admin_add_state, Admin_Form.admin_add_state)
    dp.message.register(admin_remove_state, Admin_Form.admin_remove_state)
    dp.message.register(children_delete_state, Admin_Form.children_delete_state)
    dp.message.register(view_children_state, Admin_Form.view_children_state)

    dp.message.register(children_points_minus_state_1, Admin_Form.children_points_minus_state_1)
    dp.message.register(children_points_minus_state_2, Admin_Form.children_points_minus_state_2)
    dp.message.register(children_points_minus_state_3, Admin_Form.children_points_minus_state_3)

    dp.message.register(children_points_plus_state_1, Admin_Form.children_points_plus_state_1)
    dp.message.register(children_points_plus_state_2, Admin_Form.children_points_plus_state_2)
    dp.message.register(children_points_plus_state_3, Admin_Form.children_points_plus_state_3)

    dp.callback_query.register(authenticated_test_name, F.data.startswith('callback_authenticated'))
    dp.callback_query.register(character_test_call, F.data.startswith('callback_character_test'))
    dp.callback_query.register(universe_rules, F.data.startswith('universe_rules'))
    dp.callback_query.register(my_character, F.data.startswith('my_character'))
    dp.callback_query.register(my_points, F.data.startswith('my_points'))
    dp.callback_query.register(main_menu_call, F.data.startswith('return'))
    dp.callback_query.register(what_scoring_remove, F.data.startswith('what_scoring_remove'))
    dp.callback_query.register(what_scoring, F.data.startswith('what_scoring'))

    dp.callback_query.register(view_childrens_points, F.data.startswith('view_childrens_points'))
    dp.callback_query.register(view_children_points, F.data.startswith('view_children_points'))
    dp.callback_query.register(admin_add, F.data.startswith('admin_add'))
    dp.callback_query.register(admin_remove, F.data.startswith('admin_remove'))
    dp.callback_query.register(admin_panel_call, F.data.startswith('panel_return'))
    dp.callback_query.register(children_list, F.data.startswith('children_list'))
    dp.callback_query.register(delete_children, F.data.startswith('delete_children'))
    dp.callback_query.register(children_points_plus, F.data.startswith('children_points_plus'))
    dp.callback_query.register(children_points_minus, F.data.startswith('children_points_minus'))

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
