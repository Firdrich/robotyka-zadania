import sqlite3

class DataBase():

    def __init__(self):
        self.conn = None
        self.connect()
        self.cursor = self.get_cursor()
        self.conn.commit()

    def connect(self):
        self.conn = sqlite3.connect('database1.db')

    def get_cursor(self):
        return self.conn.cursor()

    def get_account(self,username):
        self.cursor.execute("SELECT * FROM users WHERE username=\"%s\"" % username)
        user = self.cursor.fetchone()
        return user

    def get_user_username(self,username):
        self.cursor.execute("SELECT username FROM users WHERE username=\"%s\"" % username)
        username = self.cursor.fetchone()
        return username

    def get_user_id(self,username):
        self.cursor.execute("SELECT user_id FROM users WHERE username=\"%s\"" % username)
        user_id = self.cursor.fetchone()
        return int(user_id[0])

    def get_user_password(self,username):
        self.cursor.execute("SELECT password FROM users WHERE username=\"%s\"" % username)
        password = self.cursor.fetchone()
        return str(password[0])

    def get_user_admin(self,username): #check if user is admin
        self.cursor.execute("SELECT admin FROM users WHERE username=\"%s\"" % username)
        admin = self.cursor.fetchone()[0]
        return admin #returns either 0 or 1

    def login_to_account(self,username,password):
        user = self.get_account(username)
        if user == None:
            return False
        elif str(user[1]) == username and str(user[2]) == password:
            return True

    def add_account(self,username,password,email):
        if self.get_user_username(username) is not None:
            return False
        else:
            self.cursor.execute("INSERT INTO users(username, password, email) VALUES(\"%s\", \"%s\", \"%s\")" % (username, password, email))
            self.cursor.execute("INSERT INTO settings(user_id,name,surname,age,sex) VALUES(\"%i\",\"%s\",\"%s\",\"%i\",\"%s\")" % (self.get_user_id(username),"Name","Surname",0,"Sex"))
            self.conn.commit()
            return True

    def change_setting(self,parameter,name,username):
        if type(name) == int:
            self.cursor.execute("UPDATE settings SET \"%s\"=\"%i\" WHERE user_id=\"%i\"" % (parameter,name,self.get_user_id(username)))
        else:
            self.cursor.execute("UPDATE settings SET \"%s\"=\"%s\" WHERE user_id=\"%i\"" % (parameter,name,self.get_user_id(username)))
        self.conn.commit()

    def change_email(self,newmail,username):
        self.cursor.execute("UPDATE users SET email=\"%s\" WHERE username=\"%s\"" % (newmail,username))
        self.conn.commit()

    def change_password(self,newpassword,username):
        self.cursor.execute("UPDATE users SET password=\"%s\" WHERE username=\"%s\"" % (newpassword,username))
        self.conn.commit()

    def add_exercise(self,time,exercise,header):
        """Adds new exercise time and content into the database"""
        self.cursor.execute("INSERT INTO exercises(time_answers, content, title) VALUES(\"%s\", \"%s\", \"%s\")" % (time, exercise, header))
        self.conn.commit()

    def delete_exercise(self,id):
        """Deletes exercise from database"""
        self.cursor.execute("DELETE FROM exercises WHERE id=\"%s\"" % id)
        self.conn.commit()

    def get_all_exercises():
        """Gets all exercises"""
        self.cursor.execute("SELECT title, content, time_answers FROM exercises")
        exercise = self.cursor.fetchall()
        return exercise
        # Object reational mapper, flask

    def get_exercise(self, id):
        """Gets exercise from database by id"""
        self.cursor.execute("SELECT * FROM exercises WHERE id=\"%s\"" % id)
        exercise = self.cursor.fetchone()
        return exercise

    def get_exercise_id(self):
        """Gets all exercise ids"""
        self.cursor.execute("SELECT id FROM exercises")
        id = self.cursor.fetchall()
        id =  list(map(lambda id_tuple: id_tuple[0], id))
        return id

    def get_exercise_titles(self):
        """Gets all exercise titles"""
        self.cursor.execute("SELECT title FROM exercises")
        title = self.cursor.fetchall()
        title = list(map(lambda id_tuple: id_tuple[0], title))
        return title

    def get_exercise_content(self):
        """Gets all exercise contents"""
        self.cursor.execute("SELECT content FROM exercises")
        content = self.cursor.fetchall()
        content = list(map(lambda id_tuple: id_tuple[0], content))
        return content

    def get_exercise_time(self):
        """Gets all exercises times to answer"""
        self.cursor.execute("SELECT time_answers FROM exercises")
        time_answers = self.cursor.fetchall()
        time_answers = list(map(lambda id_tuple: id_tuple[0], time_answers))
        return time_answers

    def getone_exercise_time(id):
        """Gets time of one exercise from exercises"""
        self.cursor.execute("SELECT time_answers FROM exercises WHERE id=\"%s\"" % id)
        time_answers = self.cursor.fetchone()[0]
        return time_answers

    def start_exercise(self, user_id, exercise_id, exercise_time, system_time):
        """Matches user to exercise, takes time calculates and adds to database"""
        time_till_answer = system_time + exercise_time
        self.cursor.execute("INSERT INTO user_exercises(user, exercise, unlock_day) VALUES(\"%s\", \"%s\", \"%s\")" % (user_id, exercise_id, time_till_answer))
        self.conn.commit()

    def get_time_till_answer(self, user, exercise):
        """Gets time the exercise's answer unlocks"""
        self.cursor.execute("SELECT unlock_day FROM user_exercises WHERE user=\"%s\" AND exercise=\"%s\"" % (user, exercise))
        time = self.cursor.fetchone()[0]
        return time

    def get_exercise_answer(self, id):
        """Gets answer of the exercise"""
        #WARNING DATABASE NOT UPDATED TO SUPPORT THIS
        self.cursor.execute("SELECT answer FROM exercises WHERE id=\"%s\"" % id)
        answer = self.cursor.fetchone()[0]
        return answer
