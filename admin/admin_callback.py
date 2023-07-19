import time

from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.admin_keyboards import panel_return_kb, admin_panel_kb
from request.sql_request import insert_admin_id, delete_admin, get_admin_id, get_children_list, delete_children1, \
                                get_children_points, get_child_points, read_children_points, plus_points_children, \
                                get_user_name, minus_points_children


class Admin_Form(StatesGroup):
    admin_add_state = State()
    admin_remove_state = State()
    children_delete_state = State()
    view_children_state = State()

    children_points_plus_state_1 = State()
    children_points_plus_state_2 = State()
    children_points_plus_state_3 = State()

    children_points_minus_state_1 = State()
    children_points_minus_state_2 = State()
    children_points_minus_state_3 = State()


user_name = ''
user_name_minus = ''
child_point = ''
child_point_minus = ''

async def admin_add(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    admin_id = await get_admin_id()
    for row in admin_id:
        admin_id_value = row[0]
        if call.from_user.id == admin_id_value:
            await call.message.answer('Напиши его id в телеграмм, только цифры\n'
                                      'Его можно узнать тут @getmyid_bot\n'
                                      'Чтобы узнать его перешлите любое сообщение человека в @getmyid_bot\n'
                                      'Нужны только цифры после Forwarded from: ➡️<b>317717074</b>⬅️', reply_markup=panel_return_kb)
            await state.set_state(Admin_Form.admin_add_state)

async def admin_add_state(message: Message, state: FSMContext):
    admin_id = message.text.strip()
    if admin_id.isdigit():
        admin = await insert_admin_id(admin_id)
        if admin == True:
            await message.answer(f'<b>Готово</b>✅\n'
                                 f'Человек с id <b>{admin_id}</b> добавлен в админы', reply_markup=panel_return_kb)
            await state.clear()
        else:
            await message.answer('Человек с таким id уже добавлен в админы')
    else:
        await message.answer('В id должны быть только цифры')

async def admin_remove(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    admin_id = await get_admin_id()
    for row in admin_id:
        admin_id_value = row[0]
        if call.from_user.id == admin_id_value:
            await call.message.answer('Введите id того кого вы хотите удалить из админов', reply_markup=panel_return_kb)
            await state.set_state(Admin_Form.admin_remove_state)

async def admin_remove_state(message: Message, state: FSMContext):
    admin_id = message.text.strip()
    admin_delete = await delete_admin(admin_id)
    if admin_delete == True:
        await message.answer(f"<b>Готово</b>✅\n"
                             f"Человек с id <b>{admin_id}</b> был удален из админов", reply_markup=panel_return_kb)
        await state.clear()
    elif admin_delete == False:
        await message.answer(f'<b>Неудача</b>❌\n'
                             f'Человека с id <b>{admin_id}</b> не было найдено среди админов', reply_markup=panel_return_kb)

async def admin_panel_call(call: CallbackQuery):
    await call.answer('')
    admin_id = await get_admin_id()
    for row in admin_id:
        admin_id_value = row[0]
        if call.from_user.id == admin_id_value:
            await call.message.answer('<b>Админ панель</b>', reply_markup=admin_panel_kb)

async def children_list(call: CallbackQuery):
    await call.answer('')
    admin_id = await get_admin_id()
    for row1 in admin_id:
        admin_id_value = row1[0]
        if call.from_user.id == admin_id_value:

            children_list1 = await get_children_list()
            children_info = '<b>Список детей</b>\n\n'
            counter = 1
            message_limit = 4000
            message = ''

            for row in children_list1:
                child_info = f'<b>{counter}.</b> <b>{row[2]}</b>\n' \
                             f'Имя <b>{row[3]}</b>\n' \
                             f'Фамилия <b>{row[4]}</b>\n' \
                             f'Отчество <b>{row[5]}</b>\n' \
                             f'Возраст <b>{row[6]}</b>\n' \
                             f'№ комнаты <b>{row[8]}</b>\n' \
                             f'№ телефона <code>{row[7]}</code>\n\n'

                if len(message) + len(child_info) <= message_limit:
                    message += child_info
                else:
                    time.sleep(0.5)
                    await call.message.answer(message, reply_markup=panel_return_kb)
                    message = child_info

                counter += 1

            if message:
                await call.message.answer(message, reply_markup=panel_return_kb)

async def delete_children(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    admin_id = await get_admin_id()
    for row1 in admin_id:
        admin_id_value = row1[0]
        if call.from_user.id == admin_id_value:
            await call.message.answer('Введите User_name ребенка которого вы хотите удалить\n'
                                      'Пример: @Имя ребенка', reply_markup=panel_return_kb)
            await state.set_state(Admin_Form.children_delete_state)

async def children_delete_state(message: Message, state: FSMContext):
    children_user_name = message.text.strip()
    if children_user_name.startswith('@'):
        resualt = await delete_children1(children_user_name)
        if resualt == True:
            await message.answer(f'Готово ребенок с user_name {children_user_name} был удален', reply_markup=panel_return_kb)
            await state.set_state()
        elif resualt == False:
            await message.answer(f'Ребенка с user_name {children_user_name} небыло найдено', reply_markup=panel_return_kb)
    else:
        await message.answer('Неверный формат user_name. Пожалуйста, введите user_name, начинающийся с символа "@"', reply_markup=panel_return_kb)

async def view_childrens_points(call: CallbackQuery):
    await call.answer('')
    admin_id = await get_admin_id()
    for row1 in admin_id:
        admin_id_value = row1[0]
        if call.from_user.id == admin_id_value:

            children_points = await get_children_points()
            counter = 1

            for row in children_points:
                children_info = f'<b>Навыки {row[1]}</b>\n\n'
                children_info += f'Имя: <b>{row[3]}</b>\n' \
                                 f'Фамилия: <b>{row[4]}</b>\n' \
                                 f'Отчество: <b>{row[5]}</b>\n' \
                                 f'Персонаж: <b>{row[6]}</b>\n' \
                                 f'Общение: <b>{row[7]}</b>\n' \
                                 f'Открытость: <b>{row[8]}</b>\n' \
                                 f'Раскрепощение: <b>{row[9]}</b>\n' \
                                 f'Доброжелательность: <b>{row[10]}</b>\n' \
                                 f'Креативность: <b>{row[11]}</b>\n' \
                                 f'Сила духа: <b>{row[13]}</b>\n' \
                                 f'Энергия: <b>{row[14]}</b>\n' \
                                 f'Пунктуальность: <b>{row[15]}</b>\n\n'

                time.sleep(0.5)
                await call.message.answer(children_info)
                counter += 1

async def view_children_points(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    admin_id = await get_admin_id()
    for row1 in admin_id:
        admin_id_value = row1[0]
        if call.from_user.id == admin_id_value:

            await call.message.answer('Введите Фамилию ребенка')
            await state.set_state(Admin_Form.view_children_state)

async def view_children_state(message: Message, state: FSMContext):
        children_user_name = message.text.strip()
        child_points = await get_child_points(children_user_name)
        if child_points == False:
            await message.answer('Ребернка с таким user_name не было найдено')
        else:
            child_points = child_points[0]
            children_info = f'<b>Навыки {child_points[1]}</b>\n\n' \
                             f'Имя: <b>{child_points[3]}</b>\n' \
                             f'Фамилия: <b>{child_points[4]}</b>\n' \
                             f'Отчество: <b>{child_points[5]}</b>\n' \
                             f'Персонаж: <b>{child_points[6]}</b>\n' \
                             f'Общение: <b>{child_points[7]}</b>\n' \
                             f'Открытость: <b>{child_points[8]}</b>\n' \
                             f'Раскрепощение: <b>{child_points[9]}</b>\n' \
                             f'Доброжелательность: <b>{child_points[10]}</b>\n' \
                             f'Креативность: <b>{child_points[11]}</b>\n' \
                             f'Сила духа: <b>{child_points[13]}</b>\n' \
                             f'Энергия: <b>{child_points[14]}</b>\n' \
                             f'Пунктуальность: <b>{child_points[15]}</b>\n\n'
            await message.answer(children_info, reply_markup=panel_return_kb)
            await state.clear()

async def children_points_plus(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    admin_id = await get_admin_id()
    for row1 in admin_id:
        admin_id_value = row1[0]
        if call.from_user.id == admin_id_value:

            children_points = await get_children_points()

            children_info = 'Введите фамилию того ребенка, к которому вы хотите прибавить навык\n\n'
            counter = 1

            for row in children_points:
                children_info += f'{counter}. <code>{row[1]}</code>\n'
                counter += 1

            await call.message.answer("Введите фамилию того ребенка, к которому вы хотите прибавить навык")
            await state.set_state(Admin_Form.children_points_plus_state_1)

async def children_points_plus_state_1(message: Message, state: FSMContext):
        global user_name
        user_name = message.text.strip()

        result = await get_user_name(user_name)
        if result == True:
            await message.answer('Введите какой навык вы хотите прибавить\n\n'
                                 '<code>Общение</code>\n'
                                 '<code>Открытость</code>\n'
                                 '<code>Раскрепощение</code>\n'
                                 '<code>Доброжелательность</code>\n'
                                 '<code>Креативность</code>\n'
                                 '<code>Сила духа</code>\n'
                                 '<code>Энергия</code>\n'
                                 '<code>Пунктуальность</code>', reply_markup=panel_return_kb)
            await state.set_state(Admin_Form.children_points_plus_state_2)
        elif result == False:
            await message.answer('Ребенка с такой фамилией не было найдено')

async def children_points_plus_state_2(message: Message, state: FSMContext):
    global child_point
    child_point = message.text
    if child_point == 'Общение':
        result = await read_children_points(user_name, 'Общение')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Общение: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

    elif child_point == 'Открытость':
        result = await read_children_points(user_name, 'Открытость')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Открытость: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

    elif child_point == 'Раскрепощение':
        result = await read_children_points(user_name, 'Раскрепощение')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Раскрепощение: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

    elif child_point == 'Доброжелательность':
        result = await read_children_points(user_name, 'Доброжелательность')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Доброжелательность: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

    elif child_point == 'Креативность':
        result = await read_children_points(user_name, 'Креативность')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Креативность: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

    elif child_point == 'Сила духа':
        result = await read_children_points(user_name, 'Сила духа')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Сила духа: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

    elif child_point == 'Энергия':
        result = await read_children_points(user_name, 'Энергия')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Энергия: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

    elif child_point == 'Пунктуальность':
        result = await read_children_points(user_name, 'Пунктуальность')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Пунктуальность: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_plus_state_3)

async def children_points_plus_state_3(message: Message, state: FSMContext):
    plus_point = message.text.strip()
    if plus_point.isdigit():
        try:
            await plus_points_children(user_name, child_point, plus_point)
            await message.answer(f'Отлично, к <b>{user_name}</b> прибавилось <b>{plus_point}</b> навыков <b>{child_point}</b>', reply_markup=panel_return_kb)
            await state.clear()
        except:
            await message.answer('Ошибка')
    else:
        await message.answer('Введите число')

async def children_points_minus(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    admin_id = await get_admin_id()
    for row1 in admin_id:
        admin_id_value = row1[0]
        if call.from_user.id == admin_id_value:

            children_points = await get_children_points()

            children_info = 'Введите фамилию того ребенка, у которого вы хотите убрать навык\n\n'
            counter = 1

            for row in children_points:
                children_info += f'{counter}. <code>{row[1]}</code>\n'
                counter += 1

            await call.message.answer('Введите фамилию того ребенка, у которого вы хотите убрать навык')
            await state.set_state(Admin_Form.children_points_minus_state_1)

async def children_points_minus_state_1(message: Message, state: FSMContext):
        global user_name_minus
        user_name_minus = message.text.strip()
        result = await get_user_name(user_name_minus)
        if result == True:
            await message.answer('Введите какой навык вы хотите убрать\n\n'
                                 '<code>Общение</code>\n'
                                 '<code>Открытость</code>\n'
                                 '<code>Раскрепощение</code>\n'
                                 '<code>Доброжелательность</code>\n'
                                 '<code>Креативность</code>\n'
                                 '<code>Сила духа</code>\n'
                                 '<code>Энергия</code>\n'
                                 '<code>Пунктуальность</code>', reply_markup=panel_return_kb)
            await state.set_state(Admin_Form.children_points_minus_state_2)
        elif result == False:
            await message.answer('Ребенка с таким user_name не было найдено')

async def children_points_minus_state_2(message: Message, state: FSMContext):
    global child_point_minus
    child_point_minus = message.text.strip()
    if child_point_minus == 'Общение':
        result = await read_children_points(user_name, 'Общение')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Общение: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите убавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

    elif child_point_minus == 'Открытость':
        result = await read_children_points(user_name, 'Открытость')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Открытость: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите убавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

    elif child_point_minus == 'Раскрепощение':
        result = await read_children_points(user_name, 'Раскрепощение')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Раскрепощение: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите убавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

    elif child_point_minus == 'Доброжелательность':
        result = await read_children_points(user_name, 'Доброжелательность')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Доброжелательность: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите убавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

    elif child_point_minus == 'Креативность':
        result = await read_children_points(user_name, 'Креативность')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Креативность: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите убавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

    elif child_point_minus == 'Сила духа':
        result = await read_children_points(user_name, 'Сила духа')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Сила духа: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите убавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

    elif child_point_minus == 'Энергия':
        result = await read_children_points(user_name, 'Энергия')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Энергия: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите убавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

    elif child_point_minus == 'Пунктуальность':
        result = await read_children_points(user_name, 'Пунктуальность')
        await message.answer(f'Сейчас у <b>{user_name}</b>\n'
                             f'Пунктуальность: {result[0][0]}\n\n'
                             f'Введите сколько вы хотите прибавить')
        await state.set_state(Admin_Form.children_points_minus_state_3)

async def children_points_minus_state_3(message: Message, state: FSMContext):
    minus_point = message.text.strip()
    if minus_point.isdigit():
        try:
            await minus_points_children(user_name_minus, child_point_minus, minus_point)
            await message.answer(f'Отлично, у <b>{user_name}</b> убавилось <b>{minus_point}</b> навыков <b>{child_point}</b>', reply_markup=panel_return_kb)
            await state.clear()
        except:
            await message.answer('Ошибка')
    else:
        await message.answer('Введите число')