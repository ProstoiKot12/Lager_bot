import sqlite3


con = sqlite3.connect("User.db")
cur = con.cursor()

async def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS user_table("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER, "
                "user_name TEXT, "
                "children_name TEXT, "
                "children_surname TEXT,"
                "children_patronymic TEXT, "
                "children_year INTEGER,"
                "children_phone INTEGER,"
                "children_room_number INTEGER)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS points_table("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_name TEXT, "
                "user_id INTEGER, "
                "children_name TEXT, "
                "children_surname TEXT,"
                "children_patronymic TEXT, "
                "children_character TEXT, "
                "communication_points INTEGER, "
                "openness_points INTEGER, "
                "liberation_points INTEGER, "
                "goodwill_points INTEGER, "
                "creativity_points INTEGER, "
                "neatness_points INTEGER, "
                "fortitude_points INTEGER, "
                "energy_points INTEGER, "
                "punctuality_points INTEGER)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS admin_table("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "admin_user_name TEXT, "
                "admin_id INTEGER)")
    con.commit()

async def insert_table_data(user_id, user_name, children_name, children_surname, children_patronymic, children_year, children_phone, children_room_number):
    cur.execute("SELECT * FROM user_table WHERE user_id = ?", (user_id,))
    det = cur.fetchall()
    if not det:
        cur.execute("INSERT INTO user_table ("
                    "user_id, "
                    "user_name, "
                    "children_name, "
                    "children_surname, "
                    "children_patronymic, "
                    "children_year, "
                    "children_phone, "
                    "children_room_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id,
                     user_name,
                     children_name,
                     children_surname,
                     children_patronymic,
                     children_year,
                     children_phone,
                     children_room_number))
        con.commit()
        cur.execute("INSERT INTO points_table "
                    "(user_name, "
                    "user_id, "
                    "children_name, "
                    "children_surname, "
                    "children_patronymic) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (user_name, user_id, children_name, children_surname, children_patronymic))
        con.commit()

async def insert_children_character(us_id, child_char):
        if child_char == 'Свершитель':
            cur.execute('UPDATE points_table SET '
                        'communication_points = ?, '
                        'openness_points = ?, '
                        'liberation_points = ?, '
                        'goodwill_points = ?, '
                        'creativity_points = ?, '
                        'fortitude_points = ?, '
                        'energy_points = ?, '
                        'punctuality_points = ?, '
                        'children_character = ? '
                        'WHERE user_id = ?',
                        (0, 0, 1, 0, 0, 0, 0, 0, child_char, us_id))
            con.commit()
        elif child_char == 'Интеллегнт':
            cur.execute('UPDATE points_table SET '
                        'communication_points = ?, '
                        'openness_points = ?, '
                        'liberation_points = ?, '
                        'goodwill_points = ?, '
                        'creativity_points = ?, '
                        'fortitude_points = ?, '
                        'energy_points = ?, '
                        'punctuality_points = ?, '
                        'children_character = ? '
                        'WHERE user_id = ?',
                        (0, 0, 0, 1, 0, 0, 0, 0, child_char, us_id))
            con.commit()
        elif child_char == 'Телепат':
            cur.execute('UPDATE points_table SET '
                        'communication_points = ?, '
                        'openness_points = ?, '
                        'liberation_points = ?, '
                        'goodwill_points = ?, '
                        'creativity_points = ?, '
                        'fortitude_points = ?, '
                        'energy_points = ?, '
                        'punctuality_points = ?, '
                        'children_character = ? '
                        'WHERE user_id = ?',
                        (0, 0, 0, 1, 0, 0, 0, 0, child_char, us_id))
            con.commit()
        elif child_char == 'Друг':
            cur.execute('UPDATE points_table SET '
                        'communication_points = ?, '
                        'openness_points = ?, '
                        'liberation_points = ?, '
                        'goodwill_points = ?, '
                        'creativity_points = ?, '
                        'fortitude_points = ?, '
                        'energy_points = ?, '
                        'punctuality_points = ?, '
                        'children_character = ? '
                        'WHERE user_id = ?',
                        (5, 2, 0, 2, 0, 1, 0, 0, child_char, us_id))
            con.commit()
        elif child_char == 'Деятель':
            cur.execute('UPDATE points_table SET '
                        'communication_points = ?, '
                        'openness_points = ?, '
                        'liberation_points = ?, '
                        'goodwill_points = ?, '
                        'creativity_points = ?, '
                        'fortitude_points = ?, '
                        'energy_points = ?, '
                        'punctuality_points = ?, '
                        'children_character = ? '
                        'WHERE user_id = ?',
                        (0, 0, 1, 0, 0, 0, 0, 0, child_char, us_id))
            con.commit()
        elif child_char == 'Виртуоз':
            cur.execute('UPDATE points_table SET '
                        'communication_points = ?, '
                        'openness_points = ?, '
                        'liberation_points = ?, '
                        'goodwill_points = ?, '
                        'creativity_points = ?, '
                        'fortitude_points = ?, '
                        'energy_points = ?, '
                        'punctuality_points = ?, '
                        'children_character = ? '
                        'WHERE user_id = ?',
                        (0, 0, 0, 0, 1, 0, 0, 0, child_char, us_id))
            con.commit()

async def read_us_id_user_table(user_id):
    cur.execute('SELECT user_id FROM user_table WHERE user_id = ?', (user_id,))
    det = cur.fetchall()
    if not det:
        return True
    else:
        return False

async def read_us_id_points_table(user_id):
    cur.execute('SELECT user_id FROM points_table WHERE user_id = ?', (user_id,))
    det = cur.fetchall()
    if not det:
        return True
    else:
        return False

async def read_points(user_id):
    cur.execute('SELECT * FROM points_table WHERE user_id = ?', (user_id,))
    character_points = cur.fetchall()
    return character_points

async def get_admin_id():
    cur.execute('SELECT admin_id FROM admin_table')
    admin_id = cur.fetchall()
    return admin_id

async def insert_admin_id(admin_id):
    cur.execute('SELECT admin_id FROM admin_table WHERE admin_id = ?', (admin_id,))
    det = cur.fetchall()
    if not det:
        cur.execute('INSERT INTO admin_table (admin_id) VALUES (?)', (admin_id,))
        con.commit()
        return True

async def delete_admin(admin_id):
    cur.execute('SELECT admin_id FROM admin_table WHERE admin_id = ?', (admin_id,))
    det = cur.fetchall()
    if not det:
        return False
    else:
        cur.execute('DELETE FROM admin_table WHERE admin_id = ?', (admin_id,))
        con.commit()
        return True

async def get_children_list():
    cur.execute('SELECT * FROM user_table')
    children_list = cur.fetchall()
    return children_list

async def get_children_points():
    cur.execute('SELECT * FROM points_table')
    children_points = cur.fetchall()
    return children_points

async def get_child_points(children_user_name):
    cur.execute('SELECT * FROM points_table WHERE children_surname = ?', (children_user_name,))
    children_points = cur.fetchall()
    if not children_points:
        return False
    else:
        return children_points

async def delete_children1(children_user_name):
    cur.execute('SELECT user_name FROM user_table WHERE user_name = ?', (children_user_name,))
    det = cur.fetchall()
    if not det:
        return False
    else:
        cur.execute('DELETE FROM user_table WHERE user_name = ?', (children_user_name,))
        con.commit()
        cur.execute('DELETE FROM points_table WHERE user_name = ?', (children_user_name,))
        con.commit()
        return True

async def read_children_points(user_name, skill):
    if skill == 'Общение':
        cur.execute('SELECT communication_points FROM points_table WHERE children_surname = ?', (user_name,))
        communication = cur.fetchall()
        return communication
    elif skill == 'Открытость':
        cur.execute('SELECT openness_points FROM points_table WHERE children_surname = ?', (user_name,))
        openness = cur.fetchall()
        return openness
    elif skill == 'Раскрепощение':
        cur.execute('SELECT liberation_points FROM points_table WHERE children_surname = ?', (user_name,))
        liberation = cur.fetchall()
        return liberation
    elif skill == 'Доброжелательность':
        cur.execute('SELECT goodwill_points FROM points_table WHERE children_surname = ?', (user_name,))
        goodwill = cur.fetchall()
        return goodwill
    elif skill == 'Креативность':
        cur.execute('SELECT creativity_points FROM points_table WHERE children_surname = ?', (user_name,))
        creativity = cur.fetchall()
        return creativity
    elif skill == 'Сила духа':
        cur.execute('SELECT neatness_points FROM points_table WHERE children_surname = ?', (user_name,))
        neatness = cur.fetchall()
        return neatness
    elif skill == 'Энергия':
        cur.execute('SELECT energy_points FROM points_table WHERE children_surname = ?', (user_name,))
        energy = cur.fetchall()
        return energy
    elif skill == 'Пунктуальность':
        cur.execute('SELECT punctuality_points FROM points_table WHERE children_surname = ?', (user_name,))
        punctuality = cur.fetchall()
        return punctuality

async def plus_points_children(user_name, skill, plus_point):
    if skill == 'Общение':
        cur.execute('UPDATE points_table SET communication_points = communication_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Открытость':
        cur.execute('UPDATE points_table SET openness_points = openness_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Раскрепощение':
        cur.execute('UPDATE points_table SET liberation_points = liberation_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Доброжелательность':
        cur.execute('UPDATE points_table SET goodwill_points = goodwill_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Креативность':
        cur.execute('UPDATE points_table SET creativity_points = creativity_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Сила духа':
        cur.execute('UPDATE points_table SET fortitude_points = fortitude_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Энергия':
        cur.execute('UPDATE points_table SET energy_points = energy_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Пунктуальность':
        cur.execute('UPDATE points_table SET punctuality_points = punctuality_points + ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

async def minus_points_children(user_name, skill, plus_point):
    if skill == 'Общение':
        cur.execute('UPDATE points_table SET communication_points = communication_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Открытость':
        cur.execute('UPDATE points_table SET openness_points = openness_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Раскрепощение':
        cur.execute('UPDATE points_table SET liberation_points = liberation_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Доброжелательность':
        cur.execute('UPDATE points_table SET goodwill_points = goodwill_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Креативность':
        cur.execute('UPDATE points_table SET creativity_points = creativity_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Сила духа':
        cur.execute('UPDATE points_table SET fortitude_points = fortitude_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Энергия':
        cur.execute('UPDATE points_table SET energy_points = energy_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()

    elif skill == 'Пунктуальность':
        cur.execute('UPDATE points_table SET punctuality_points = punctuality_points - ? WHERE children_surname = ?',
                    (plus_point, user_name))
        con.commit()


async def get_user_name(user_name):
    cur.execute('SELECT children_surname FROM points_table WHERE children_surname = ?', (user_name,))
    det = cur.fetchall()
    if not det:
        return False
    else:
        return True
