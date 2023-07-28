import sqlite3
from utils import *

def connection():
    return sqlite3.connect('dbt.db')

def create_table_user():
    con = connection()
    cur = con.cursor()
    cur.execute("""
        create table if not exists user(
                userID integer not null primary key autoincrement,
                first_name varchar(30),
                last_name varchar(30),
                birth_day date,
                phone varchar(13),
                username varchar(50),
                password varchar(150),
                is_admin boolean default false
        )
    """)
    con.commit()
    con.close()


def create_user_course():
    con = connection()
    cur = con.cursor()
    cur.execute("""
        create table if not exists user_course(
                id integer not null primary key autoincrement,
                user_id int,
                course_id int,
                datetime datetime
        )
    """)
    con.commit()
    con.close()


def create_table_courses():
    con = connection() 
    cur = con.cursor()
    cur.execute("""
        create table if not exists courses(
                courceID integer not null primary key autoincrement,
                name varchar(50),
                number_of_students int,
                is_active boolean default true
        )
    """)
    con.commit()
    con.close()


def add_course(data: dict):
    con = connection()
    cur = con.cursor()
    query = """
        insert into courses(
        name,
        number_of_students,
        is_active
        ) values
        (?, ?, ?)
    """
    values = tuple(data.values())
    cur.execute(query, values)
    con.commit()
    con.close()


def add_user_course(data: dict):
    con = connection()
    cur = con.cursor()
    query = """
        insert into user_course(
        user_id,
        cource_id
        ) values
        (?, ?)
    """
    values = tuple(data.values())
    cur.execute(query, values)
    con.commit()
    con.close()


def update(table, part, new_data, username):
    con = connection()
    cur = con.cursor()
    cur.execute(f"""
        update {table}
        set {part}='{new_data}'
        where `username`='{username}'
    """)
    con.commit()


def login(username: str, password: str):
    con = connection()
    cur = con.cursor()
    hashed_password = hash_password(password)
    query = """
        select * from user
        where username=? and password=?
    """
    value = (username, hashed_password)
    cur.execute(query, value)
    return bool(cur.fetchone())


def is_admin(username):
    con=connection()
    cur=con.cursor()
    cur.execute("""
    select * from user
    """)
    rows = cur.fetchall()
    arr=[]
    for row in rows:
        arr.append(row)
    for i in arr:
        if i[5]==username:
            b=i[7]

    return b


def add_user(data: dict):
    con = connection()
    cur = con.cursor()
    hashed_password = hash_password(data['password'])
    data['password'] = hashed_password
    query = """
        insert into user(
        first_name,
        last_name,
        birth_day, 
        phone,
        username,
        password
        ) values
        (?, ?, ?, ?, ?, ?)
    """
    values = tuple(data.values())
    cur.execute(query, values)
    con.commit()
    con.close()


def admin_menu():
    print("Admin menusi!")
    n=input('1.Add course \n2.View students \nChoose: ')
    if n=='1':
        name=input("Course name: ")
        number_of_students=input("Number students: ")

        data=dict(
            name=name,
            number_of_students=number_of_students,
            is_active=True
        )

        add_course(data)
        print('Success')
        admin_menu()

    elif n=='2':
        con=connection()
        cur=con.cursor()
        cur.execute("""
        select * from user_course
        """)
        rows = cur.fetchall()
        for row in rows:
            print(row)



def pupil_menu(username):
    print("pupil menu")
    n=input("""
1.Aktiv kurslar ro'yhatini ko'rish;
2. Aktiv kurslarga yozilish;
3. O'zi yozilgan kurslar ro'yhatini ko'rish;
Tanlang: """)

    if n=='1':
        con=connection()
        cur=con.cursor()
        cur.execute("""
        select * from courses
        """)
        rows = cur.fetchall()
        arr=[]
        for row in rows:
            arr.append(row)

        for i in arr:
            if i[3]:
                print(i)
        

    elif n=='2':
        course=input("Qaysi kursga yozilasiz: ")

        con=connection()
        cur=con.cursor()
        cur.execute("""
        select * from courses
        """)
        rows = cur.fetchall()
        arr=[]
        for row in rows:
            arr.append(row)
        for i in arr:
            if i[1]==course:
                print(i)
        a=input('Kursga yozilish(+): ')

        if a=='+':
            #user_id
            con=connection()
            cur=con.cursor()
            cur.execute("""
            select * from user
            """)
            rows = cur.fetchall()
            arr=[]
            for row in rows:
                arr.append(row)
            for i in arr:
                if i[5]==username:
                    user_id=i[0]


            #course_id
            con=connection()
            cur=con.cursor()
            cur.execute("""
            select * from courses
            """)
            rows = cur.fetchall()
            arr=[]
            for row in rows:
                arr.append(row)
            for i in arr:
                if i[1]==course:
                    course_id=i[0]

            data=dict(
                user_id=user_id,
                course_id=course_id
            )
            add_user_course(data)
            print("Kursga muvaffaqiyatli yozildingiz!")


create_user_course()