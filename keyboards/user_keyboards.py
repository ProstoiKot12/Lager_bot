from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

authenticated_button = [
    [InlineKeyboardButton(text='🔍Пройти идентификацию', callback_data='callback_authenticated')]
]
authenticated_kb = InlineKeyboardMarkup(inline_keyboard=authenticated_button)

character_test_button = [
    [InlineKeyboardButton(text='Начать тест😀', callback_data='callback_character_test')]
]

character_test_kb = InlineKeyboardMarkup(inline_keyboard=character_test_button)

main_menu_button = [
    [InlineKeyboardButton(text='🦸Мой персонаж', callback_data='my_character')],
    [InlineKeyboardButton(text='💪Мои навыки', callback_data='my_points')],
    [InlineKeyboardButton(text='📜Правила Вселенной АРТ-V', callback_data='universe_rules')],
    [InlineKeyboardButton(text='👍За что начисляются навыки', callback_data='what_scoring')],
    [InlineKeyboardButton(text='🙁За что могут забрать навыки', callback_data='what_scoring_remove')]
]

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=main_menu_button)

return_button = [
    [InlineKeyboardButton(text='◀️Назад', callback_data='return')]
]

return_kb = InlineKeyboardMarkup(inline_keyboard=return_button)

