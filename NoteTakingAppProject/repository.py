import sqlite3
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class Repository(object):

    def __init__(self):
        self.__conn = sqlite3.connect(r'C:\Users\Brock\Desktop\NoteTakingAppProject\NoteTakingAppProject\data.sqlite')
        # if you drag the project to your D: drive it will be :
        # 'D:\Python\Project\NoteTakingAppProject\NoteTakingAppProject\data.sqlite'

    def __del__(self):
        self.__conn.close()

    def create_users_table(self):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("create table if not exists Users (User_ID INTEGER PRIMARY KEY AUTOINCREMENT, User_Name VARCHAR)")
        except Exception as e:
            print(e)
            raise

    def create_subject_table(self, subject):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("create table if not exists {} (Topic VARCHAR, Notes VARCHAR, User_ID INTEGER)".format(subject))
        except Exception as e:
            print(e)
            raise

    def add_new_user(self, user_name, password): 
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("INSERT INTO Users (User_Name, Password) values (?,?)".format(user_name),(user_name, generate_password_hash(password)))
        except Exception as e:
            print(e)
            print("In Repository for add_new_user")
            raise

    def check_password(self, user_name, password):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                temp_tuple = cursor.execute("SELECT Password FROM Users WHERE User_Name = ?",(user_name,)).fetchone()
                temp_tuple = [i for i in temp_tuple]
                hashed_pw = temp_tuple[0]
                is_same = check_password_hash(hashed_pw, password)
                return is_same
        except Exception as e:
            print(e)
            raise

    def add_to_subject_table(self, subject, topic_submit, notes_submit, submit_ID): 
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("insert into {} (Topic, Notes, User_ID) values (?, ?, ?)".format(subject),(topic_submit, notes_submit, submit_ID))
        except Exception as e:
            print("Problem in add_to_subject_table")
            print(e)
            raise
        
    def get_user_id(self, user_name):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                results = cursor.execute("SELECT User_ID FROM Users WHERE User_Name = ?",(user_name,)).fetchone()
                results = [i for i in results]
                s = results[0]
                return s
        except Exception as e:
            print(e)
            raise

    def get_topics(self,subject_table_name, user_id):
        try:
            cursor = self.__conn.cursor()
            results = cursor.execute("select Topic from {} where User_ID = ?".format(subject_table_name),(user_id,))
            s =[]
            s = results.fetchall()
            return s
        except Exception as e:
            print(e)
            raise

    def check_topics(self,subject_table_name, user_id, topic_name):
        try:
            isThere = False
            cursor = self.__conn.cursor()
            results = cursor.execute("select Topic from {} where User_ID = ?".format(subject_table_name),(user_id,))
            s =[]
            s = results.fetchall()
            for i in s:
                if topic_name == i[0]:
                    isThere = True
            return isThere
        except Exception as e:
            print(e)
            raise

    def get_notes(self,subject_table_name, user_id):
        try:
            cursor = self.__conn.cursor()
            results = cursor.execute("select Notes from {} where User_ID = ?".format(subject_table_name),(user_id,))
            s =[]
            s = results.fetchall()
            return s
        except Exception as e:
            print(e)
            raise

    def update_notes(self, subject_submit, topic_submit, notes_submit, submit_ID):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("update {} set Notes =? where Topic =? and User_ID =?".format(subject_submit),(notes_submit, topic_submit, submit_ID))
        except Exception as e:
            print("Problem in update_notes")
            print(e)
            raise


    def delete_topic(self, subject_submit, topic_submit, submit_ID):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("delete from {} where Topic =? and User_ID =?".format(subject_submit),(topic_submit, submit_ID))
        except Exception as e:
            print("Problem in delete_topic")
            print(e)
            raise