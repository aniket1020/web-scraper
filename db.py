import sqlite3

if __name__ == '__main__':
    try:
        db = sqlite3.connect('jobs.db')
        print("Connected to the database successfully")
    except:
        print("Error occurred when connecting to the database")
        exit()

    result = db.execute(
        'SELECT * FROM JOBS'
    ).fetchall()
    for res in result:
        for it in res:
            print(it)
        print("--------------------")
