import psycopg2
import os
import random
import argparse
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser(description='Seed data details.')
parser.add_argument('-u', '--users', type=int,
                    help='how many users to create', required=True)
parser.add_argument('-z', '--quizzes', type=int,
                    help='how many quizzes per user', required=True)
parser.add_argument('-q', '--questions', type=int,
                    help='how many questions in each quiz', required=True)

args = parser.parse_args()

print(
    f"Creating {args.users} users, with {args.quizzes} quizzes and {args.questions} questions each")

conn = psycopg2.connect(
    port=5555,
    host="localhost",
    database="quizdeveloper",
    user="postgres",
    password=os.environ.get("PG_PASSWORD"),
)

cur = conn.cursor()

for i in range(args.users):

    # User
    user_sql = "INSERT INTO quizuser (username, pw) VALUES (%s, %s) RETURNING id"
    cur.execute(user_sql, (f"Testuser_{i+1}", f"secret_{i+1}"))
    user_id = cur.fetchone()[0]

    for j in range(args.quizzes):

        # Quiz
        quiz_sql = "INSERT INTO quiz (title, quiz_description, quizuser_id) VALUES (%s, %s, %s) RETURNING id"
        cur.execute(
            quiz_sql, (f"Test quiz {j+1} for user {user_id}", f"Something about the quiz {j+1}", user_id))
        quiz_id = cur.fetchone()[0]

        for k in range(args.questions):

            # Question
            question_sql = "INSERT INTO question (question_name) VALUES (%s) RETURNING id"
            cur.execute(question_sql, (f"Test question {k+1} of quiz {quiz_id}",))
            question_id = cur.fetchone()[0]

            answers = []
            correct = random.randint(1, 5)
            for i in range(5):
                answers.append((f"Q {k+1} Option {i+1}", i+1 == correct))

            answer_ids = []
            answer_sql = "INSERT INTO answer (answer_text, is_correct) VALUES (%s, %s) RETURNING id"
            for answer in answers:
                # Create answers
                cur.execute(answer_sql, (answer))
                answer_ids.append(cur.fetchone()[0])

            qa_sql = "INSERT INTO question_answer (question_id, answer_id) VALUES (%s, %s)"
            for answer_id in answer_ids:
                # Link answer to question
                cur.execute(qa_sql, (question_id, answer_id))

            # Link question to quiz
            qq_sql = "INSERT INTO quiz_question (quiz_id, question_id) VALUES (%s, %s)"
            cur.execute(qq_sql, (quiz_id, question_id))


conn.commit()
conn.close()
