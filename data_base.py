import sqlite3


class User:
    def __init__(self, database):
        self.connect = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.bad_advice = []
        self.rest = []
        self.helper = []
        self.choice_advice = []
        self.resume = []

    def add_id_to_db(self, user_id):
        with self.connect:
            self.cursor.execute("INSERT INTO user (id) values (?)", (user_id,))
            self.connect.commit()

    def get_all_id(self, user_id):
        with self.connect:
            result = self.cursor.execute("SELECT id FROM user WHERE `id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_stat(self, stat, user_id):
        with self.connect:
            result = self.cursor.execute("INSERT INTO user (stat) values (?) WHERE id = (?)", (stat, user_id))
            self.connect.commit()
            return result

    def update_stat(self, stat, user_id):
        with self.connect:
            result = self.cursor.execute("UPDATE user SET stat = ? WHERE id = ?", (stat, user_id))
            self.connect.commit()
            return result

    def get_stat(self, user_id):
        with self.connect:
            result = self.cursor.execute("SELECT stat FROM user WHERE id = (?)", (user_id,))
            return result


    def copy_bad_advice(self):
        with self.connect:
            request = "SELECT * FROM Bad_advice"
            get_back = self.cursor.execute(request).fetchall()
            for reply in get_back:
                self.bad_advice.append(reply)
            return self.bad_advice

    def copy_choice_advice(self):
        with self.connect:
            request = "SELECT * FROM Choice_advice"
            get_back = self.cursor.execute(request).fetchall()
            for reply in get_back:
                self.choice_advice.append(reply)
            return self.choice_advice

    def copy_rest(self):
        with self.connect:
            request = "SELECT description, sources FROM Rest"
            get_back = self.cursor.execute(request).fetchall()
            for reply in get_back:
                self.rest.append(reply)
            return self.rest

    def copy_helper(self):
        with self.connect:
            request = "SELECT description FROM Helper"
            get_back = self.cursor.execute(request).fetchall()
            for reply in get_back:
                self.helper.append(reply)
        return self.helper

    def get_resumes(self):
        with self.connect:
            request = "SELECT description FROM Resume"
            get_back = self.cursor.execute(request).fetchall()
            for reply in get_back:
                self.resume.append(reply)
            return self.resume

    def list1(self):
        return [1, 2, 3]
