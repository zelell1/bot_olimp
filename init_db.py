import sqlite3


# создаем класс пользователя
class User:
    def __init__(self, id, first_name, last_name, username, olimpiads):       
        self.con = sqlite3.connect("Bot_users.db")
        self.id = id
        self.fr = first_name
        self.lr = last_name
        self.username = username
        self.olimps = []

    # добавляем нового пользователя
    def add_user(self):
        cur = self.con.cursor()
        users_id = list(map(lambda x: x[0], cur.execute(f"SELECT user_id from users").fetchall()))
        if self.id not in users_id:
            cur.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?)", (self.id, self.fr, self.lr , self.username, ''))
            self.olimps = []
            self.con.commit()
            return True
            
        else:
            self.olimps = list(set("".join(map(lambda x: x[0], cur.execute("SELECT olimpiads from users WHERE user_id = (?)", (str(self.id), )).fetchall())).split(';')))
            return False


    # обновляем информацию об олимпиадах пользователя
    def update_info_user(self, olimps):
        self.olimps += list(set(olimps))
        st = ";".join(set(self.olimps))
        cur = self.con.cursor()
        cur.execute(f"""UPDATE users SET olimpiads = (?) WHERE user_id = (?)""", (st, self.id))
        self.con.commit()
    

    # берем список из олимпиад пользователя
    def get_list(self):
        cur = self.con.cursor()
        return list(set("".join(map(lambda x: x[0], cur.execute("SELECT olimpiads from users WHERE user_id = (?)", (str(self.id), )).fetchall())).split(';')))


    # получаем ник пользователя
    def usernam(self):
        cur = self.con.cursor()
        usersn = list(map(lambda x: x[0], cur.execute(f"""SELECT username from users WHERE user_id = '{self.id}'""").fetchall()))
        return usersn[0]
    

def get_users():
    con = sqlite3.connect("Bot_users.db")
    cur = con.cursor()
    users = list(cur.execute(f"""SELECT user_id, first_name, last_name, username from users""").fetchall())
    return users

