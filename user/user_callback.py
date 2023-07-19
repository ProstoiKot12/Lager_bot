import re
import time

from aiogram.types import Message, CallbackQuery
from random import randint

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from request.sql_request import insert_table_data, insert_children_character, read_us_id_user_table, \
                                read_us_id_points_table, read_points
from keyboards.user_keyboards import character_test_kb, return_kb, main_menu_kb


class Form(StatesGroup):
    test_state_1 = State()
    test_state_2 = State()
    test_state_3 = State()
    test_state_4 = State()

    character_test_1 = State()
    character_test_2 = State()
    character_test_3 = State()
    character_test_4 = State()
    character_test_5 = State()
    character_test_6 = State()
    character_test_7 = State()
    character_test_8 = State()
    character_test_9 = State()
    character_test_10 = State()
    character_test_11 = State()
    character_test_12 = State()
    character_test_13 = State()
    character_test_14 = State()
    character_test_15 = State()
    character_test_16 = State()
    character_test_17 = State()
    character_test_18 = State()
    character_test_19 = State()


user_id: int
user_name: str
children_surname: str
children_name: str
children_patronymic: str
children_year: int
children_room_number: int
test_points_yes = 0
test_points_probably_yes = 0
test_points_no = 0

async def authenticated_test_name(call: CallbackQuery, state: FSMContext):
    await call.answer('')

    testing = await read_us_id_user_table(call.from_user.id)

    if testing == True:
        await call.message.answer("Введите своё ФИО:\n\n"
                                  "✅Иванов Иван Иванович\n\n"
                                  "❌ыфф23дльзы")
        await state.set_state(Form.test_state_1)
    elif testing == False:
        await call.message.answer("Вы уже индефицировали себя")

async def test_state_1(message: Message, state: FSMContext):
    try:
        global user_id, user_name, children_name, children_surname, children_patronymic

        user_id = message.from_user.id
        user_name = f'@{message.from_user.username}'
        name_parts = message.text.split()
        children_surname = name_parts[0]
        children_name = name_parts[1]
        children_patronymic = name_parts[2]

        if len(name_parts) != 3:
            raise ValueError('Неверный формат ФИО')

        name_pattern = re.compile(r'^[А-ЯЁа-яё]+$')
        if not all(name_pattern.match(name) for name in name_parts):
            raise ValueError('Неверный формат ФИО')

        await message.answer('Хорошо 👍, теперь введите то сколько вам полных лет:\n\n'
                             '✅14\n\n'
                             '❌12312978')

        await state.set_state(Form.test_state_2)
    except:
        await message.answer('Вы неверно ввели ФИО 😡')

async def test_state_2(message: Message, state: FSMContext):
    try:
        age = int(message.text.strip())

        if age <= 90:
            global children_year
            children_year = message.text.strip()
            await message.answer('Введите номер своей комнаты')
            await state.set_state(Form.test_state_3)
        else:
            await message.answer('Вы неверно ввели свой возраст 😡')
    except ValueError:
        await message.answer('Вы неверно ввели свой возраст 😡')

async def test_state_3(message: Message, state: FSMContext):
    try:
        global children_room_number
        children_room_number = message.text

        if not children_room_number.isdigit():
            await message.answer('Вы неверно ввели номер своей комнаты 😡')
            return

        await message.answer('Введите свой номер телефона в формате 81234567890')
        await state.set_state(Form.test_state_4)
    except:
        await message.answer('Вы неверно ввели номер своеё комнаты 😡')

def format_phone_number(phone_number):
    digits = ''.join(filter(str.isdigit, phone_number))

    if len(digits) != 11:
        return phone_number

    country_code = digits[1:4]
    first_part = digits[4:7]
    second_part = digits[7:9]
    last_part = digits[9:]

    formatted_number = f"8 {country_code} {first_part} {second_part}-{last_part}"
    return formatted_number

async def test_state_4(message: Message, state: FSMContext):
    try:
        children_phone = message.text.strip()

        phone_pattern = re.compile(r'^\d{11}$')
        match_result = phone_pattern.match(children_phone)
        if match_result is None:
            await message.answer('Неверный формат номера телефона. Пожалуйста, введите номер в формате 81234567890')
            return

        formatted_phone = '+7 ' + children_phone[1:4] + ' ' + children_phone[4:7] + ' ' + children_phone[7:9] + '-' + children_phone[9:11]

        await message.answer('Готово👌, вы прошли идентификацию, теперь вам нужно пройти <b>тест</b>\n'
                             'Чтобы определить персонажа который подходит именно <b>тебе</b>', reply_markup=character_test_kb)
        await insert_table_data(user_id, user_name, children_name, children_surname, children_patronymic, children_year, formatted_phone, children_room_number)
    except:
        await message.answer('Вы неверно ввели свой номер телефона 😡')
        await state.clear()

async def character_test_call(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    result = await read_us_id_user_table(call.from_user.id)

    if result == False:
        await call.message.answer('Ты должен ответить на вопросы такими утверждения как:\n'
                                  '<code>1 (Да)</code>\n'
                                  '<code>2 (Нет)</code>\n'
                                  'Ты должен(а) ответить цифрами')
        time.sleep(1)
        await call.message.answer('Я настойчивый(ая) и упорный (упорная)')
        await state.set_state(Form.character_test_1)
    if result == True:
        await call.message.answer('Вы уже прошли тест')

async def character_test_1(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я планирую мои дела ежедневно')
        await state.set_state(Form.character_test_2)
    elif message.text.strip() == "31":
        test_points_probably_yes += 1
        await message.answer('Я планирую мои дела ежедневно')
        await state.set_state(Form.character_test_2)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я планирую мои дела ежедневно')
        await state.set_state(Form.character_test_2)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_2(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я умею действовать, несмотря на страх')
        await state.set_state(Form.character_test_3)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я умею действовать, несмотря на страх')
        await state.set_state(Form.character_test_3)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я умею действовать, несмотря на страх')
        await state.set_state(Form.character_test_3)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_3(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Даже если задача трудная, я стараюсь не сдаваться и пробую ее решить')
        await state.set_state(Form.character_test_4)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Даже если задача трудная, я стараюсь не сдаваться и пробую ее решить')
        await state.set_state(Form.character_test_4)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Даже если задача трудная, я стараюсь не сдаваться и пробую ее решить')
        await state.set_state(Form.character_test_4)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_4(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Мои знакомые считают меня надежным человеком')
        await state.set_state(Form.character_test_5)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Мои знакомые считают меня надежным человеком')
        await state.set_state(Form.character_test_5)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Мои знакомые считают меня надежным человеком')
        await state.set_state(Form.character_test_5)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_5(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я не могу перейти к другому делу, если не завершил(а) предыдущее')
        await state.set_state(Form.character_test_6)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я не могу перейти к другому делу, если не завершил(а) предыдущее')
        await state.set_state(Form.character_test_6)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я не могу перейти к другому делу, если не завершил(а) предыдущее')
        await state.set_state(Form.character_test_6)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_6(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Большинству людей я нравлюсь')
        await state.set_state(Form.character_test_7)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Большинству людей я нравлюсь')
        await state.set_state(Form.character_test_7)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Большинству людей я нравлюсь')
        await state.set_state(Form.character_test_7)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_7(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я приятный человек')
        await state.set_state(Form.character_test_8)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я приятный человек')
        await state.set_state(Form.character_test_8)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я приятный человек')
        await state.set_state(Form.character_test_8)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_8(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Другим со мной интересно')
        await state.set_state(Form.character_test_9)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Другим со мной интересно')
        await state.set_state(Form.character_test_9)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Другим со мной интересно')
        await state.set_state(Form.character_test_9)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_9(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('У меня много друзей')
        await state.set_state(Form.character_test_10)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('У меня много друзей')
        await state.set_state(Form.character_test_10)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('У меня много друзей')
        await state.set_state(Form.character_test_10)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_10(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('У меня есть близкие друзья')
        await state.set_state(Form.character_test_11)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('У меня есть близкие друзья')
        await state.set_state(Form.character_test_11)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('У меня есть близкие друзья')
        await state.set_state(Form.character_test_11)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_11(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я чувствую, что заряжен энергией')
        await state.set_state(Form.character_test_12)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я чувствую, что заряжен энергией')
        await state.set_state(Form.character_test_12)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я чувствую, что заряжен энергией')
        await state.set_state(Form.character_test_12)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_12(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я полон энергии и решимости')
        await state.set_state(Form.character_test_13)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я полон энергии и решимости')
        await state.set_state(Form.character_test_13)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я полон энергии и решимости')
        await state.set_state(Form.character_test_13)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_13(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я почти всегда бодр и готов действовать')
        await state.set_state(Form.character_test_14)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я почти всегда бодр и готов действовать')
        await state.set_state(Form.character_test_14)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я почти всегда бодр и готов действовать')
        await state.set_state(Form.character_test_14)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_14(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Мне есть на кого положиться')
        await state.set_state(Form.character_test_15)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Мне есть на кого положиться')
        await state.set_state(Form.character_test_15)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Мне есть на кого положиться')
        await state.set_state(Form.character_test_15)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_15(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я люблю заниматься творчеством')
        await state.set_state(Form.character_test_16)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я люблю заниматься творчеством')
        await state.set_state(Form.character_test_16)
    elif message.text.strip() == "1":
        test_points_no += 1
        await message.answer('Я люблю заниматься творчеством')
        await state.set_state(Form.character_test_16)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_16(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('Я - творческий человек')
        await state.set_state(Form.character_test_17)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('Я - творческий человек')
        await state.set_state(Form.character_test_17)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('Я - творческий человек')
        await state.set_state(Form.character_test_17)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_17(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('У меня всегда много идей')
        await state.set_state(Form.character_test_18)
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('У меня всегда много идей')
        await state.set_state(Form.character_test_18)
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('У меня всегда много идей')
        await state.set_state(Form.character_test_18)
    else:
        await message.answer('Введите 1 или 2')

async def character_test_18(message: Message, state: FSMContext):
    global test_points_probably_yes, test_points_yes, test_points_no
    random = randint(1, 6)
    us_id = message.from_user.id
    if message.text.strip() == "1":
        test_points_yes += 1
        await message.answer('И твой персонаж...')
        time.sleep(2)
        if random == 1:
            await message.answer('''✊<b>Свершитель</b> 

⚡️<b>Основные навыки:</b> раскрепощение, смелость.

🪄<b>Индивидуальные свойства:</b>

-Побеждает пустоты при равенсиве сил.
-Может пользоваться рисунками на щите (футболка).  

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы-нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Свершитель')
        elif random == 2:
            await message.answer('''🫴<b>Интеллигент</b> 

⚡️<b>Основной навык:</b>   аккуратность

🪄<b>Индивидуальные своства:</b>  

-Может применять волшебные предметы против злых духов. (предметы на карточках сокровищ)

-Может пользоваться рисунками на щите (футболка). 

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Интеллегнт')
        elif random == 3:
            await message.answer('''🙌<b>Телепат</b>  

⚡️<b>Основной навык:</b> доброжелательность.

🪄<b>Индивидуальные свойства:</b> 
-Обладает гипнозом. Если имеет специальное кольцо, то может загипнотизировать злых духов и забрать сокровища. 

- Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b> 
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Телепат')
        elif random == 4:
            await message.answer('''🤝<b>Друг</b>  

⚡️<b>Основной навык:</b>  общение

🪄<b>Индивидуальные свойства:</b>  
-Может восстанавивать только что потерянный навык у других.

-Может пользоваться рисунками на щите (футболка) 


❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Друг')
        elif random == 5:
            await message.answer('''👌<b>Деятель</b>  

⚡️<b>Основной навык:</b>  Сила духа, энергия

🪄<b>Индивидуальные свойства:</b>  

-Может использовать против злого духа любые сокровища.  Пожертвовав одно сокровище- побеждает. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Деятель')
        elif random == 6:
            await message.answer('''🤟<b>Виртуоз</b>  

⚡️<b>Основной навык:</b>  креативность

🪄<b>Индивидуальные свойства:</b>  

-Обладает волшебной пыльцой, которая позволяет скрыться от пустот. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Виртуоз')
        await state.clear()
    elif message.text.strip() == "Скорее да":
        test_points_probably_yes += 1
        await message.answer('И твой персонаж...')
        time.sleep(2)
        if random == 1:
            await message.answer('''✊<b>Свершитель</b> 

⚡️<b>Основные навыки:</b> раскрепощение, смелость.

🪄<b>Индивидуальные свойства:</b>

-Побеждает пустоты при равенстве сил.
-Может пользоваться рисунками на щите (футболка).  

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Свершитель')
        elif random == 2:
            await message.answer('''🫴<b>Интеллигент</b> 

⚡️<b>Основной навык:</b>   аккуратность

🪄<b>Индивидуальные своства:</b>  

-Может применять волшебные предметы против злых духов. (предметы на карточках сокровищ)

-Может пользоваться рисунками на щите (футболка). 

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Интеллегнт')
        elif random == 3:
            await message.answer('''🙌<b>Телепат</b>  

⚡️<b>Основной навык:</b> доброжелательность.

🪄<b>Индивидуальные свойства:</b> 
-Обладает гипнозом. Если имеет специальное кольцо, то может загипнотизировать злых духов и забрать сокровища. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b> 
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Телепат')
        elif random == 4:
            await message.answer('''🤝<b>Друг</b>  

⚡️<b>Основной навык:</b>  общение

🪄<b>Индивидуальные свойства:</b>  
-Может восстанавивать только что потерянный навык у других.

-Может пользоваться рисунками на щите (футболка) 


❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Друг')
        elif random == 5:
            await message.answer('''👌<b>Деятель</b>  

⚡️<b>Основной навык:</b>  Сила духа, энергия

🪄<b>Индивидуальные свойства:</b>  

-Может использовать против злого духа любые сокровища.  Пожертвовав одно сокровище - побеждает. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Деятель')
        elif random == 6:
            await message.answer('''🤟<b>Виртуоз</b>  

⚡️<b>Основной навык:</b>  креативность

🪄<b>Индивидуальные свойства:</b>  

-Обладает волшебной пыльцой, которая позволяет скрыться от пустот. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Виртуоз')
        await state.clear()
    elif message.text.strip() == "2":
        test_points_no += 1
        await message.answer('И твой персонаж...')
        time.sleep(2)
        if random == 1:
            await message.answer('''✊<b>Свершитель</b> 

⚡️<b>Основные навыки:</b> раскрепощение, смелость.

🪄<b>Индивидуальные свойства:</b>

-Побеждает пустоты при равенсиве сил.
-Может пользоваться рисунками на щите (футболка).  

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Свершитель')
        elif random == 2:
            await message.answer('''🫴<b>Интеллигент</b> 

⚡️<b>Основной навык:</b>   аккуратность

🪄<b>Индивидуальные своства:</b>  

-Может применять волшебные предметы против злых духов. (предметы на карточках сокровищ)

-Может пользоваться рисунками на щите (футболка). 

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Интеллегнт')
        elif random == 3:
            await message.answer('''🙌<b>Телепат</b>  

⚡️<b>Основной навык:</b> доброжелательность.

🪄<b>Индивидуальные свойства:</b> 
-Обладает гипнозом. Если имеет специальное кольцо, то может загипнотизировать злых духов и забрать сокровища. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b> 
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Телепат')
        elif random == 4:
            await message.answer('''🤝<b>Друг</b>  

⚡️<b>Основной навык:</b>  общение

🪄<b>Индивидуальные свойства:</b>  
-Может восстанавивать только что потерянный навык у других.

-Может пользоваться рисунками на щите (футболка) 


❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Друг')
        elif random == 5:
            await message.answer('''👌<b>Деятель</b>  

⚡️<b>Основной навык:</b>  Сила духа, энергия

🪄<b>Индивидуальные свойства:</b>  

-Может использовать против злого духа любые сокровища.  Пожертвовав одно сокровище - побеждает. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Деятель')
        elif random == 6:
            await message.answer('''🤟<b>Виртуоз</b>  

⚡️<b>Основной навык:</b>  креативность

🪄<b>Индивидуальные свойства:</b>  

-Обладает волшебной пыльцой, которая позволяет скрыться от пустот. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''')
            await insert_children_character(us_id, 'Виртуоз')
        await state.clear()

async def what_scoring(call: CallbackQuery):
    await call.answer('')
    await call.message.answer('<b>За что начисляютя навыки</b>\n\n'
                              'Личные достижения\n'
                              'Активное участие на мастер-классах, увлеченность деятельностью\n'
                              'Скрытые достижения\n'
                              'Чистота в номере\n'
                              'Помощь Маэстро\n'
                              'Зарядка. Проведение зарядки\n'
                              'Пунктуальность\n'
                              'Сюрпризы друг другу\n'
                              'Активность, креативность\n'
                              'Лидерство, заряд позитива\n'
                              'Победа над пустотами', reply_markup=return_kb)

async def what_scoring_remove(call: CallbackQuery):
    await call.answer('')
    await call.message.answer('<b>За что могут забарть навыки</b>\n\n'
                              'Опоздания\n'
                              'Хулиганство\n' 
                              'Нецензурная брань\n'
                              'Грязные комнаты\n'
                              'Пропуск зарядки\n'
                              'Нарушение правил Вселенной\n'
                              'Поражение Пустот', reply_markup=return_kb)

async def universe_rules(call: CallbackQuery):
    await call.answer('')
    await call.message.answer('<b>Правила Вселенной АРТ-V</b>\n\n'
'''1. Не навреди 
Ни словом, ни поступком. Ни себе, ни ближнему своему.) На любом мероприятии, деле, приеме пищи, 24/7 мы в ответе за свои действия и поступки как перед собой, так и перед окружающими. Имущество вселенной и организаторов, тоже входит сюда.  

2. Предупреждай 
Пространство нашей вселенной свободно для выражения собственных действий.
 Но если ты решил отлучиться куда-либо на территории базы сообщи любому маэстро. Самовольное покидание базы несет за собой ответственность вплоть до исключения из программы.  

3. Говори 
Ты можешь спокойно выражать свое собственное мнение на русском или английских языках. Любые конфликты решаются путем мирных переговоров. Давай не захламлять пространство нецензурной бранью, за этим следует предупреждение и санкции. 

4. Здоровье 
СРАЗУ! Необходимо сообщить наставнику о плохом самочувствие, или травме. На базе есть врач, мы обязаны будем оказать первую помощь! 

5. Купание
Мы купаемся в водоеме по 15 минут, с перерывом. Если нам мало этого времени будет, то вместе будем пересматривать время на это. Самостоятельное купание запрещено. 

6. Распорядок 
Каждое утро мы проговариваем план на день, и вывешиваем его. Мы самостоятельно приходим на те или иные дела, мероприятия и тренировки. У нас есть тихое время, когда нам позволено заниматься своими делами, в этот час запрещено шуметь, это посвящено общему отдыху. 

7. Еда
Ты – то что ты ешь. Можно даже просить добавку. Но, вход в блок питания только по графику приема пищи. Не поел – плохо откатал, заповедь райдера.

8. Взаимодействие 
С участниками вне нашей вселенной мы взаимодействуем мирно. Если у вас, то или иное занятие или мастер-класс в какой-либо аудитории, а она занята, то спокойно и вежливо уточняем по какой причине и сообщаем маэстро. 

9. Телефон 
Использовать можно в любое СВОБОДНОЕ время. Отбой не считается свободным временем, после него использование телефонов запрещено. После первого предупреждения на время отбоя телефон будет сдаваться наставнику. Брать телефон в катер разрешено. Все телефоны под личной ответственностью владельца. 

10. Комнаты
Необходимо содержать в ежедневной чистоте. После подъема заправить кровать и убрать пространство всеми проживающими в этой комнате. Будут ревизорро. Ключи от комнат не терять. 
Под ответственностью у каждого участника нашего проекта. Необходимо договариваться где вы их храните со своим соседом. 

11. Маэстро
Во вселенной есть маэстро. Они транслируют свои знания тебе, поэтому только от тебя зависит насколько ты готов впитать в себя их. Маэстро может предложить тебе по-другому посмотреть на твою комнату, на то, как ты питаешься, на твое поведение. Прислушайся!

12. Свободное время, тихое время
В это время от занятий вы можете гулять по территории со своими друзьями или самостоятельно, но ОБЯЗАТЕЛЬНО предупредить маэстро или написать в общий чат! 📲
За самовольное покидание номера в тихое время, без предупреждения следуют санкции!''')

async def my_points(call: CallbackQuery):
    await call.answer('')
    children_points = await read_points(call.from_user.id)
    children_points = children_points[0]
    await call.message.answer(f'<b>Твои навыки:</b>\n\n'
                              f'Общение: {children_points[7]}\n'
                              f'Отркытость: {children_points[8]}\n'
                              f'Раскрепощение: {children_points[9]}\n'
                              f'Доброжелательность: {children_points[10]}\n'
                              f'Креативность: {children_points[11]}\n'
                              f'Сила духа: {children_points[13]}\n'
                              f'Энергия: {children_points[14]}\n'
                              f'Пунктуальность: {children_points[15]}', reply_markup=return_kb)

async def my_character(call: CallbackQuery):
    await call.answer('')
    children_characters = await read_points(call.from_user.id)
    children_characters = children_characters[0][6]

    if children_characters == 'Свершитель':
        await call.message.answer('''✊<b>Свершитель</b> 

⚡️<b>Основные навыки:</b> раскрепощение, смелость.

🪄<b>Индивидуальные свойства:</b>

-Побеждает пустоты при равенстве сил.
-Может пользоваться рисунками на щите (футболка).  

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''', reply_markup=return_kb)

    elif children_characters == 'Интеллегнт':
        await call.message.answer('''🫴<b>Интеллигент</b> 

⚡️<b>Основной навык:</b>   аккуратность

🪄<b>Индивидуальные своства:</b>  

-Может применять волшебные предметы против злых духов. (предметы на карточках сокровищ)

-Может пользоваться рисунками на щите (футболка). 

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''', reply_markup=return_kb)

    elif children_characters == 'Телепат':
        await call.message.answer('''🙌<b>Телепат</b>  

⚡️<b>Основной навык:</b> доброжелательность.

🪄<b>Индивидуальные свойства:</b> 
-Обладает гипнозом. Если имеет специальное кольцо, то может загипнотизировать злых духов и забрать сокровища. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b> 
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b> 
Щит с рисунками дает + 3 любых навыка при столкновении ✅''', reply_markup=return_kb)

    elif children_characters == 'Друг':
        await call.message.answer('''🤝<b>Друг</b>  

⚡️<b>Основной навык:</b>  общение

🪄<b>Индивидуальные свойства:</b>  
-Может восстанавивать только что потерянный навык у других.

-Может пользоваться рисунками на щите (футболка) 


❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''', reply_markup=return_kb)

    elif children_characters == 'Деятель':
        await call.message.answer('''👌<b>Деятель</b>  

⚡️<b>Основной навык:</b>  Сила духа, энергия

🪄<b>Индивидуальные свойства:</b>  

-Может использовать против злого духа любые сокровища.  Пожертвовав одно сокровище- побеждает. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''', reply_markup=return_kb)

    elif children_characters == 'Виртуоз':
        await call.message.answer('''🤟<b>Виртуоз</b>  

⚡️<b>Основной навык:</b>  креативность

🪄<b>Индивидуальные свойства:</b>  

-Обладает волшебной пыльцой, которая позволяет скрыться от пустот. 

-Может пользоваться рисунками на щите (футболка)

❗️<b>Про щит:</b>  
После прохождения идентификации выдается щит, чтобы нарисовать на нем элементы - нужно ПОБЕДИТЬ пустоты и получить от них сокровища  

<b>СВОЙСТВА ЩИТА:</b>  
Щит с рисунками дает + 3 любых навыка при столкновении ✅''', reply_markup=return_kb)

async def main_menu_call(call: CallbackQuery):
    await call.answer('')
    await call.message.answer('<b>Главное меню</b>', reply_markup=main_menu_kb)
