from psched.post import Post
import sqlite3
from datetime import datetime
import os
import os.path

DB_PATH = "./posts.db"

def create_database():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE posts(id INTEGER PRIMARY KEY ASC,
        title TEXT, content TEXT, create_date NOT NULL, modify_date, post_date)""")


def create_database_if_not_exist():
    if not os.path.exists(DB_PATH):
        create_database()

def format_date(d: datetime) -> str:
    return d.isoformat()

def unformat_date(s: str | None) -> datetime:
    if s is not None:
        return datetime.fromisoformat(s)
    else:
        return None
        

def create_post_entry(p: Post):
    assert(p.post_id is None)
    
    currdate = datetime.now()
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        print(repr(format_date(currdate)))
        con.execute("INSERT INTO posts(title, content, create_date) VALUES (?,?,?)",
                    (
                        p.title, p.content,
                        format_date(currdate)
                    ))

        p.create_date = currdate
        

def return_next_post_entry(amount = 1) -> list[Post]:

    def rows_to_post(r):
        postid, title, content, cdate, mdate, pdate = r
        return Post(title=title, content=content,
                    create_date=unformat_date(cdate),
                    modify_date=unformat_date(mdate),
                    post_date=unformat_date(pdate),
                    post_id=postid)

    
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        return [rows_to_post(r) for r in con.execute(
            "SELECT id, title, content, create_date, modify_date, post_date " +
            "FROM posts WHERE post_date IS NULL ORDER BY id ASC LIMIT ?", (amount,))]
        



def update_post_entry_content(p: Post, title: str, content: str):
    assert(p.post_id is not None)
    assert(p.post_date is None)
    
    currdate = datetime.now()
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        con.execute("UPDATE posts SET title=?, content=?, modify_date=? WHERE id=? " +
                    "", (
                        p.title, p.content,
                        format_date(currdate),
                        p.post_id
                    ))

        p.title = title
        p.content = content
        p.modify_date = currdate
        

def submit_post_entry(p: Post):
    assert(p.post_id is not None)
    assert(p.post_date is None)

    currdate = datetime.now()
    
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        con.execute("UPDATE posts SET post_date=? where id=? " +
                    "", (currdate, p.post_id))

        p.post_date = currdate
        
