import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
        self.create_table_user()
        self.create_table_flag()
        self.create_table_user_flags()

    def create_table_user(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS user (
                    user_id INTEGER PRIMARY KEY,
                    points INTEGER DEFAULT 0)''')

    def create_table_flag(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS flags (
                    flag TEXT NOT NULL,
                    points INTEGER,
                    PRIMARY KEY (flag))''')

    def create_table_user_flags(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS user_flags (
                    user_id INTEGER,
                    flag TEXT,
                    FOREIGN KEY (user_id) REFERENCES user(user_id),
                    FOREIGN KEY (flag) REFERENCES flags(flag),
                    UNIQUE (user_id, flag))''')
            

    def clear_tables(self):
        try:
            with self.conn:
                self.conn.execute('DELETE FROM user_flags')
                self.conn.execute('DELETE FROM user')
                self.conn.execute('DELETE FROM flags')
            return True
        except sqlite3.Error:
            return False
    

    def add_user(self, user_id: int):
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT OR IGNORE INTO user (user_id) VALUES (?)", (user_id,))
            return True
        except sqlite3.IntegrityError:
            return False
    

    def get_all_users(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM user')
            result = cursor.fetchall()
            users = [{'user_id': row[0], 'points': row[1]} for row in result]
            return users


    def update_user_points(self, user_id: int, points: int):
        with self.conn:
            cursor = self.conn.execute(
                'UPDATE user SET points = points + ? WHERE user_id = ?', (points, user_id))
            return cursor.rowcount > 0
        
        
    def get_users_sorted_by_points(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM user ORDER BY points DESC')
            result = cursor.fetchall()
            users = [{'user_id': row[0], 'points': row[1]} for row in result]
            return users
        

    def get_user_points(self, user_id: int):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                'SELECT points FROM user WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        

    def get_flag_points(self, flag: str):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT points FROM flags WHERE flag = ?', (flag,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        
        
    def update_flag_points(self, flag: str, points: int):
        with self.conn:
            self.conn.execute('UPDATE flags SET points = ? WHERE flag = ?', (points, flag))
    
    
    def add_user_flag(self, user_id: int, flag: str):
        flag_points = self.get_flag_points(flag)
        if flag_points is None:
            return False,0
        new_points = max(1, flag_points - 1)
        self.update_flag_points(flag, new_points)
        try:
            with self.conn:
                self.conn.execute('INSERT INTO user_flags (user_id, flag) VALUES (?, ?)', (user_id, flag))
                self.update_user_points(user_id, flag_points)
            return True, flag_points
        except sqlite3.IntegrityError:
            return False,0
        

    def add_flag(self, flag: str, points: int):
        try:
            with self.conn:
                self.conn.execute(
                    'INSERT INTO flags (flag, points) VALUES (?, ?)', (flag, points))
            return True
        except sqlite3.IntegrityError:
            return False
        

    def get_flag(self, flag: str):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM flags WHERE flag = ?', (flag,))
            result = cursor.fetchone()
            if result:
                return {'flag': result[0], 'points': result[1]}
            return None


    def get_all_flags(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM flags')
            flags = [{'flag': row[0], 'points': row[1]} for row in cursor.fetchall()]
            return flags


    def delete_flag(self, flag: str):
        with self.conn:
            cursor = self.conn.execute(
                'DELETE FROM flags WHERE flag = ?', (flag,))
            return cursor.rowcount > 0

