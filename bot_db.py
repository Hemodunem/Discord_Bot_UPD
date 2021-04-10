import sqlite3
import json

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# try:
#     cursor.execute("DROP TABLE activities")
# except:
#     pass


cursor.execute("""
CREATE TABLE IF NOT EXISTS activities
(user_id INTEGER UNIQUE, text_amount INTEGER, has_role BOOLEAN)
""")


# Заносим пользователя в базу

def activity_new(member_id, word_count):
    need_update_role = False
    try:
        amount = cursor.execute(f'''SELECT text_amount FROM activities WHERE user_id = {member_id} LIMIT 1''')
        amount = amount.fetchall()[0][0] + word_count
        if amount >= 50:
            cursor.execute(f"""
            UPDATE activities SET has_role = true WHERE user_id = {member_id}
            """)
            conn.commit()
            need_update_role = True
        cursor.execute(f"""
        UPDATE activities SET text_amount = {amount} WHERE user_id = {member_id}
        """)
        conn.commit()
    except:
        cursor.execute(f"""
        INSERT INTO activities (user_id, text_amount, has_role) VALUES ({member_id} , {word_count}, false);
        """)
        conn.commit()

    return need_update_role

# cursor.execute("""
# SELECT * FROM activities
# """)
#
# cool = []
#
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
#     if row[2] >= 50 and row[4] == 0:
#         cool.append((1, int(row[0])))
#
# print(json.dumps(cool))
#
# cursor.executemany("""UPDATE activities SET has_role = ? WHERE user_id = ?""", cool)
#
# conn.commit()
