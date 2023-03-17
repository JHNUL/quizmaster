DROP DATABASE IF EXISTS quizdeveloper;

CREATE DATABASE quizdeveloper;

\c quizdeveloper;

CREATE TABLE quizuser (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  pw VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  logged_at TIMESTAMP
);

CREATE TABLE quiz (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  quiz_description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP
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
