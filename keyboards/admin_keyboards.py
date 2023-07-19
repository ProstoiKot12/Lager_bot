from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


panel_return_button = [
    [InlineKeyboardButton(text='◀️Админ панель', callback_data='panel_return')]
]

panel_return_kb = InlineKeyboardMarkup(inline_keyboard=panel_return_button)


admin_panel_button = [
    [InlineKeyboardButton(text='📃‍Список детей', callback_data='children_list')],
    [InlineKeyboardButton(text='➕Прибавить навык ребенку', callback_data='children_points_plus')],
    [InlineKeyboardButton(text='➖Убавить навык ребенку', callback_data='children_points_minus')],
    [InlineKeyboardButton(text='🤹‍Посмотреть навыки детей', callback_data='view_childrens_points')],
    [InlineKeyboardButton(text='🧒‍Посмотреть опр ребенка', callback_data='view_children_points')],
    [InlineKeyboardButton(text='🟥Удалить ребенка из списка', callback_data='delete_children')],
    [InlineKeyboardButton(text='👮‍♂️Добавить админа', callback_data='admin_add')],
    [InlineKeyboardButton(text='🧹Убрать админа', callback_data='admin_remove')]
]

admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=admin_panel_button)
