import json
import sqlite3
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    url: str
    run: int
    cars: list[str]


class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('user_data.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id INTEGER PRIMARY KEY,
                url TEXT,
                run INTEGER,
                cars TEXT
            )
        """)
        self.conn.commit()

    def add_user(self, user: User):
        user_cars_json = json.dumps(user.cars)
        self.cur.execute("""
            INSERT INTO user_data (user_id, url, run, cars)
            VALUES (?, ?, ?, ?)
        """, (user.user_id, user.url, user.run, user_cars_json))
        self.conn.commit()

    def get_user(self, user_id) -> User | None:
        self.cur.execute("""
            SELECT * FROM user_data
            WHERE user_id = ?
        """, (user_id,))

        user_data = self.cur.fetchone()
        if not user_data:
            return None
        user_id, url_to_scrape, run, cars = user_data

        user_data = User(user_id, url_to_scrape, run, json.loads(cars))

        return user_data

    def get_all_users(self) -> list[User]:
        self.cur.execute("""
            SELECT * FROM user_data
        """)
        users = self.cur.fetchall()

        users = [User(user_id, url_to_scrape, run, json.loads(cars)) for user_id, url_to_scrape, run, cars in users]

        return users

    def update_url(self, user_id, url):
        self.cur.execute("""
            UPDATE user_data
            SET url = ?
            WHERE user_id = ?
        """, (url, user_id))
        self.conn.commit()

    def update_cars(self, user_id, cars):
        cars_json = json.dumps(cars)
        self.cur.execute("""
            UPDATE user_data
            SET cars = ?
            WHERE user_id = ?
        """, (cars_json, user_id))
        self.conn.commit()

    def update_run(self, user_id, run):
        self.cur.execute("""
            UPDATE user_data
            SET run = ?
            WHERE user_id = ?
        """, (run, user_id))
        self.conn.commit()


user_db = UserDatabase()
