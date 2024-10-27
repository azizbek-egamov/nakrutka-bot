import sqlite3


def sql_connect():
    try:
        connection = sqlite3.connect("sqlite3.db")  # SQLite3 bazasiga bog'lanish
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False


def sql_connection():
    connection = sqlite3.connect("sqlite3.db")  # SQLite3 bazasiga bog'lanish
    connection.commit()
    return connection


def CreateTableUsers():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid BIGINT NOT NULL,
                full_name TEXT NOT NULL,
                username TEXT,
                balance BIGINT NOT NULL,
                orders BIGINT NOT NULL,
                payment BIGINT NOT NULL,
                offer BIGINT NOT NULL,
                ban TEXT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTableAPI():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE api_key (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid BIGINT NOT NULL,
                api_key TEXT NOT NULL,
                url TEXT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTableOrderTemp():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE order_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid BIGINT NOT NULL,
                service_id BIGINT NOT NULL,
                soni TEXT NOT NULL,
                narx TEXT NOT NULL,
                url TEXT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTable_NakCategory():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTableRef():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE referal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid BIGINT NOT NULL,
                ref_id BIGINT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTable_NakService():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service INTEGER NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                rate TEXT NOT NULL,
                min INTEGER NOT NULL,
                max INTEGER NOT NULL,
                dripfeed TEXT NOT NULL,
                refill TEXT NOT NULL,
                cancel TEXT NOT NULL,
                category TEXT NOT NULL,
                category_id INTEGER NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTableOrders():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid BIGINT NOT NULL,
                order_id TEXT NOT NULL,
                base_id BIGINT NOT NULL,
                service_id BIGINT NOT NULL,
                name TEXT NOT NULL,
                narx BIGINT NOT NULL,
                soni BIGINT NOT NULL,
                url TEXT NOT NULL,
                send_status TEXT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTablePaymentCards():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE pay_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                card BIGINT NOT NULL,
                info BIGINT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def CreateTableOrderDeleteMessage():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE order_delete_message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid BIGINT NOT NULL,
                message_id BIGINT NOT NULL,
                text TEXT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


try:
    CreateTableOrderDeleteMessage()
    print("CreateTableOrderDeleteMessage() Yaratildi")
except:
    print("CreateTableOrderDeleteMessage() Yaratilgan")

try:
    CreateTablePaymentCards()
    print("CreateTablePaymentCards() Yaratildi")
except:
    print("CreateTablePaymentCards() Yaratilgan")

try:
    CreateTableRef()
    print("CreateTableRef() Yaratildi")
except:
    print("CreateTableRef() Yaratilgan")

try:
    CreateTableOrders()
    print("CreateTableOrders() Yaratildi")
except:
    print("CreateTableOrders() Yaratilgan")


try:
    CreateTableOrderTemp()
    print("CreateTableOrderTemp() Yaratildi")
except:
    print("CreateTableOrderTemp() Yaratilgan")


try:
    CreateTable_NakCategory()
    print("CreateTable_NakCategory() Yaratildi")
except:
    print("CreateTable_NakCategory() Yaratilgan")

try:
    CreateTable_NakService()
    print("CreateTable_NakService() Yaratildi")
except:
    print("CreateTable_NakService() Yaratilgan")

try:
    CreateTableUsers()
    print("CreateTableUsers() Yaratildi")
except:
    print("CreateTableUsers() Yaratilgan")

try:
    CreateTableAPI()
    print("CreateTableAPI() Yaratildi")
except:
    print("CreateTableAPI() Yaratilgan")


def AddOrders(uid, order_id, base_id, service_id, name, narx, soni, url, send_status):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO orders (uid, order_id,base_id, service_id, name, narx, soni, url, send_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    uid,
                    order_id,
                    base_id,
                    service_id,
                    name,
                    narx,
                    soni,
                    url,
                    send_status,
                ),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def AddOrderDeleteMessage(uid, mes_id, text):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO order_delete_message (uid, message_id, text) VALUES (?, ?)""",
                (
                    uid,
                    mes_id,
                    text,
                ),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def AddRef(uid, ref_id):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO referal (uid, ref_id) VALUES (?, ?)""",
                (
                    uid,
                    ref_id,
                ),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def AddPayCard(name, card, info):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO pay_card (name, card, info) VALUES (?, ?, ?)""",
                (name, card, info),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def AddOrderTemp(uid, service_id, soni, narxi, url):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO order_temp (uid, service_id, soni, narx, url) VALUES (?, ?, ?, ?, ?)""",
                (
                    uid,
                    service_id,
                    soni,
                    narxi,
                    url,
                ),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def AddNakCategory(name):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO category (name) VALUES (?)""",
                (name,),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def AddNakServices(
    service, name, type, rate, min, max, dripfeed, refill, cancel, category, category_id
):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO services (service, name, type, rate, min, max, dripfeed, refill, cancel, category, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    service,
                    name,
                    type,
                    rate,
                    min,
                    max,
                    dripfeed,
                    refill,
                    cancel,
                    category,
                    category_id,
                ),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def add_information(uid, full_name, username, balance, orders, payment, offer, ban):
    conn = sql_connection()
    if conn:
        try:
            r = one_table_info("users", "uid", uid)
            if r == False:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO users (uid, full_name, username, balance, orders, payment, offer, ban) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (uid, full_name, username, balance, orders, payment, offer, ban),
                )
                conn.commit()
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()
    return False


def add_phone(uid, full_name, username):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO phone (uid, p) VALUES (?, ?, ?)""",
                (uid, full_name, username),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def select_info(id):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {id}")

        res = cursor.fetchall()
        conn.commit()
        l = list()
        if not res:
            return False
        else:
            for i in res:
                l.append(i)
            return l
    else:
        return False


def dalete_info(id):

    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {id}")

            conn.commit()
            conn.close
            return True
        except:
            return False
    else:
        return False


def delete_table(da, ta, keys):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {da} WHERE {ta} = {keys}")
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def drop_table(keys):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            cursor.execute(f"drop table {keys}")
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def UpdateRaferalCount(id, count):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET offer = ? WHERE uid = ?", (count, id))
            con.commit()
            print(f"Updated ID: {id} with offer: {count}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def UpdateOrderSendStatus(id, status):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE orders SET send_status = ? WHERE id = ?", (status, id))
            con.commit()
            print(f"Updated ID: {id} with status: {status}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def UpdatePoll(ball, code):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE poll SET ball = ? WHERE user_code = ?", (ball, code))
            con.commit()
            print("Фамилия обновлена")
    except sqlite3.Error as err:
        print(f"Возникла ошибка при обновлении: {err}")


def UpdateVoted(code, uid):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO voted (uid, quote_code) VALUES (?, ?)", (uid, code)
            )
            con.commit()
            print("Фамилия обновлена")
    except sqlite3.Error as err:
        print(f"Возникла ошибка при обновлении: {err}")


# def update_data(table_name, variable, content1, element, content2):

#     if sql_connect() == True:
#         try:
#             conn = sql_connection()
#             cursor = conn.cursor()

#             cursor.execute(f"""UPDATE {table_name} SET {variable} = '{content1}' WHERE {element} = {content2}""")

#             conn.commit()
#             conn.close()
#             return True
#         except sqlite3.Error as e:
#             print(e)
#             return False
#     else:
#         return False


# update_data(table_name="poll", variable="ball", element="user_code", content1=1, content2="6672bf3f738d7a")
def table_info(ab, ba, id):
    if sql_connect() == True:

        conn = sql_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {ab} WHERE {ba} = ?", (id,))

        res = cursor.fetchall()
        conn.commit()

        if not res:
            return False
        else:
            return res
    else:
        return False


def one_table_info(ab, ba, id):
    if sql_connect() == True:

        conn = sql_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {ab} WHERE {ba} = ?", (id,))

        res = cursor.fetchone()
        conn.commit()

        if not res:
            return False
        else:
            return res
    else:
        return False


def step(id):
    if sql_connect() == True:

        conn = sql_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM step WHERE uid = ?", (id))

        res = cursor.fetchall()
        conn.commit()

        if not res:
            return False
        else:
            return res
    else:
        return False


def StepAdd(uid, txt):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO step (uid, txt) VALUES (?, ?)""",
                (uid, txt),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def TempAdd(uid, txt, code):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO temp (uid, txt, code) VALUES (?, ?, ?)""",
                (uid, txt, code),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def AddChannel(uid, channel_id):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO channels (uid, channel_id) VALUES (?, ?)""",
                (uid, channel_id),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def AddApi(uid, api_key, url):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO api_key (uid, api_key, url) VALUES (?, ?, ?)""",
                (uid, api_key, url),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def Statistic(name):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                f"""SELECT COUNT() FROM {name}""",
            )
            soni = cursor.fetchone()[0]
            conn.commit()
            return soni
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


from fuzzywuzzy import process


def get_all_names():
    conn = sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM services")
    names = cursor.fetchall()
    conn.close()
    return [name[0] for name in names]


def search_info(id_part):
    if sql_connect():
        all_names = get_all_names()
        best_match = process.extract(id_part, all_names, limit=len(all_names))

        if best_match:
            matched_names = [
                match[0] for match in best_match if match[1] >= 80
            ]  # 80 va undan yuqori o'xshashlik darajasi qabul qilinadi
            conn = sql_connection()
            cursor = conn.cursor()
            placeholders = ",".join("?" for _ in matched_names)
            query = f"SELECT * FROM services WHERE name IN ({placeholders})"
            cursor.execute(query, matched_names)
            res = cursor.fetchall()
            conn.close()

            if not res:
                return False
            else:
                return res
    else:
        return False


def UpdateUsersOrder(id, count):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET orders = ? WHERE uid = ?", (count, id))
            con.commit()
            print(f"Updated ID: {id} with order: {count}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def UpdateUsersPayment(id, count):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET payment = ? WHERE uid = ?", (count, id))
            con.commit()
            print(f"Updated ID: {id} with payment: {count}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def UpdateUsersBalance(id, count):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET balance = ? WHERE uid = ?", (count, id))
            con.commit()
            print(f"Updated ID: {id} with balance: {count}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def AddPayments(name, card, info):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO pay_cards (name, card, info) VALUES (?, ?, ?)""",
                (name, card, info),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False
