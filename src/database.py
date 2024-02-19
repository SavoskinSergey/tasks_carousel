import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()


DEBUG = False
db_name = 'my_database.sqlite'
# Создаем таблицу Users
with DatabaseManager(db_name) as cursor:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tasks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    priority INTEGER
    )
    ''')


if DEBUG:
    with DatabaseManager(db_name) as cursor:
        for i in range(5):
            task_name = 'task' + str(i)
            task_description = 'task' + str(i) + '_description'
            task_priority = i
            query = 'INSERT INTO Tasks (name, description, priority) VALUES (?, ?, ?)'
            cursor.execute(query, (task_name, task_description, task_priority))
            # cursor.execute(
            # 'INSERT INTO Tasks (name, description, priority) VALUES (?, ?, ?)',
            # ('task2', 'task2_description', 2))

with DatabaseManager(db_name) as cursor:
    cursor.execute('SELECT * FROM Tasks')
    tasks = cursor.fetchall()
    # Выводим результаты
    for task in tasks:
        print(task)


def get_tasks():
    with DatabaseManager(db_name) as cursor:
        cursor.execute('SELECT * FROM Tasks')
        tasks = cursor.fetchall()
        return tasks


def add_task(name: str, comment: str, priority: int) -> None:
    with DatabaseManager(db_name) as cursor:
        query = 'INSERT INTO Tasks (name, description, priority) VALUES (?, ?, ?)'
        cursor.execute(query, (name, comment, priority))
        cursor.execute('SELECT * FROM Tasks')
        tasks = cursor.fetchall()
        print(tasks, ' from db after add task')
