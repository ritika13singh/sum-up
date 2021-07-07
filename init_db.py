import sqlite3 as sql

def init_db():
    con = sql.connect("users.db")
    cur= con.cursor()

    cur.execute("create table users('user_id', 'user_name')")
    cur.execute("create table user_emails('user_id', 'email')")
    cur.execute("create table summaries('summary_id', 'user_id', 'summary')")
    cur.execute("create table user_passwords('user_id', 'password')")
    return

if __name__ == "__main__":
    init_db()


