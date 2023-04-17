import sqlite3

class User:
    def __init__(self, id, first_name, last_name, username):       
        self.con = sqlite3.connect("Bot_users.db")
        self.id = id
        self.fr = first_name
        self.lr = last_name
        self.username = username
            
    def add_user(self):
        cur = self.con.cursor()
        users_id = list(map(lambda x: x[0], cur.execute(f"SELECT user_id from users").fetchall()))
        if self.id not in users_id:
            cur.execute(f"INSERT INTO users VALUES(?, ?, ?, ?)", (self.id, self.fr, self.lr , self.username))
            self.con.commit()
            

    def usernam(self):
        cur = self.con.cursor()
        usersn = list(map(lambda x: x[0], cur.execute(f"""SELECT username from users WHERE user_id = '{self.id}'""").fetchall()))
        return usersn[0]