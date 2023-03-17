import psycopg2
import os
import random

conn = psycopg2.connect(
    port=5555,
    host="localhost",
    database="quizdeveloper",
    user="postgres",
    password=os.environ.get("PGPASSWORD")
)

cur = conn.cursor()

# User
cur.execute("INSERT INTO \"quizuser\" (username, pw) VALUES (%s, %s)",
            ("testuser", "secret"))

# Quiz
cur.execute("INSERT INTO \"quiz\" (title, quiz_description) VALUES (%s, %s) RETURNING id",
            ("Test quiz", "Something about the quiz"))
quiz_id = cur.fetchone()[0]

# Question
cur.execute("INSERT INTO \"question\" (question_name) VALUES (%s) RETURNING id",
            ("Test question",))
question_id = cur.fetchone()[0]

answers = []
correct = random.randint(1, 5)
for i in range(5):
    answers.append((f"Option {i+1}", i+1 == correct))

# Create answers
cur.execute("INSERT INTO \"answer\" (answer_text, is_correct) VALUES %s RETURNING id",
            ((answers,)))
answer_ids = cur.fetchall()

for answer_id in answer_ids:
    # Link answer to question
    cur.execute("INSERT INTO \"question_answer\" (question_id, answer_id) VALUES (%s, %s)",
                (question_id, answer_id))

# Link question to quiz
cur.execute("INSERT INTO \"quiz_question\" (quiz_id, question_id) VALUES (%s, %s)",
            (quiz_id, question_id))


conn.commit()
conn.close()
