import psycopg2
import os

conn = psycopg2.connect(
    port=5555,
    host="localhost",
    database="quizdeveloper",
    user="postgres",
    password=os.environ.get("PG_PASSWORD")
)

cur = conn.cursor()
cur.execute("INSERT INTO \"quizuser\" (username, pw) VALUES (%s, %s)",
            ("testuser", "secret"))

cur.execute("INSERT INTO \"quiz\" (title, quiz_name) VALUES (%s, %s) RETURNING id",
            ("Test quiz", "Something about the quiz"))

quiz_id = cur.fetchone()[0]

cur.execute("INSERT INTO \"question\" (question_name) VALUES (%s) RETURNING id",
            ("Test question",))

question_id = cur.fetchone()[0]

cur.execute("INSERT INTO \"quiz_question\" (quiz_id, question_id) VALUES (%s, %s)",
            (quiz_id, question_id))


conn.commit()
conn.close()
