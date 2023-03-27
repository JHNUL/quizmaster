DROP DATABASE IF EXISTS quizdeveloper;

CREATE DATABASE quizdeveloper;

\c quizdeveloper;

CREATE TABLE quizuser (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  pw VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  logged_at TIMESTAMP
);

CREATE TABLE quiz (
  id SERIAL PRIMARY KEY,
  quizuser_id INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  quiz_description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP,
  FOREIGN KEY(quizuser_id) REFERENCES quizuser(id)
);

CREATE TABLE question (id SERIAL PRIMARY KEY, question_name TEXT);

CREATE TABLE quiz_question (
  quiz_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  FOREIGN KEY(quiz_id) REFERENCES quiz(id),
  FOREIGN KEY(question_id) REFERENCES question(id)
);

CREATE TABLE answer (
  id SERIAL PRIMARY KEY,
  answer_text TEXT NOT NULL,
  is_correct BOOLEAN
);

CREATE TABLE question_answer (
  question_id INTEGER NOT NULL,
  answer_id INTEGER NOT NULL,
  FOREIGN KEY(question_id) REFERENCES question(id),
  FOREIGN KEY(answer_id) REFERENCES answer(id)
);

CREATE TABLE quiz_instance (
  quizuser_id INTEGER NOT NULL,
  quiz_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  answer_id INTEGER NOT NULL,
  started_at TIMESTAMP NOT NULL DEFAULT NOW(),
  finished_at TIMESTAMP,
  FOREIGN KEY(quizuser_id) REFERENCES quizuser(id),
  FOREIGN KEY(quiz_id) REFERENCES quiz(id),
  FOREIGN KEY(question_id) REFERENCES question(id),
  FOREIGN KEY(answer_id) REFERENCES answer(id)
);
