import psycopg2


class Connection:
    connection = None

    def __init__(self):
        self.connection = psycopg2.connect(user='postgres', password='Pa$$w0rd', host='localhost', port='5432',
                                           database='python_login_api')

    def verify_user(self, username, password):
        cursor = self.connection.cursor()
        sql = "SELECT id, username, first_name, last_name FROM tbl_users WHERE username=%s and password = %s"
        param = (username, password)
        cursor.execute(sql, param)
        users = cursor.fetchone()
        res = {'isValid': False, 'userData': None}
        if users is not None:
            u = User(users[0], users[1], users[2], users[3])
            res['isValid'] = True
            res['userData'] = u.toDic()
        return res

class User:
    def __init__(self, user_id=None, username=None, first_name=None, last_name=None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def toDic(self):
        return {'user_id': self.user_id, 'username' : self.username, "first_name": self.first_name, 'last_name': self.last_name}

    @staticmethod
    def get_all_user():
        cursor = Connection().connection.cursor()
        sql = "SELECT * FROM tbl_users"
        cursor.execute(sql)
        users = cursor.fetchall()
        insert_object = []
        column_names = [column[0] for column in cursor.description]
        for record in users:
            insert_object.append(dict(zip(column_names, record)))
        return insert_object

    @staticmethod
    def get_user_by_username(username):
        cursor = Connection().connection.cursor()
        sql = "SELECT * FROM tbl_users WHERE username=%s"
        param = (username, )
        cursor.execute(sql, param)
        users = cursor.fetchone()
        column_names = [column[0] for column in cursor.description]
        return dict(zip(column_names, users))

    def set_user_by_username(self, username):
        cursor = Connection().connection.cursor()
        sql = "SELECT * FROM tbl_users WHERE username=%s"
        param = (username,)
        cursor.execute(sql, param)
        users = cursor.fetchone()
        if users is None:
            return False
        else:
            self.__init__(users[0], users[1], users[2], users[3])
            return True


    def change_password(self, new_password):
        con = Connection().connection
        cursor = con.cursor()
        sql = "UPDATE tbl_users SET password=%s WHERE id=%s"
        param = (new_password, self.user_id)
        cursor.execute(sql, param)
        rows = cursor.rowcount
        con.commit()
        return rows > 0


