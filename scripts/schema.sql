CREATE DATABASE quizdeveloper;

\c quizdeveloper;

CREATE TABLE quizuser (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  pw VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  logged_at TIMESTAMPTZ
);

CREATE TABLE quiz (
  id SERIAL PRIMARY KEY,
  quizuser_id INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  quiz_description TEXT,
  public BOOLEAN NOT NULL DEFAULT FALSE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ,
  FOREIGN KEY(quizuser_id) REFERENCES quizuser(id)
);

CREATE TABLE question (
  id SERIAL PRIMARY KEY,
  question_name TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE quiz_question (
  quiz_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  FOREIGN KEY(quiz_id) REFERENCES quiz(id),
  FOREIGN KEY(question_id) REFERENCES question(id),
  UNIQUE (quiz_id, question_id)
);

CREATE TABLE answer (
  id SERIAL PRIMARY KEY,
  answer_text TEXT NOT NULL,
  is_correct BOOLEAN,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE question_answer (
  question_id INTEGER NOT NULL,
  answer_id INTEGER NOT NULL,
  FOREIGN KEY(question_id) REFERENCES question(id),
  FOREIGN KEY(answer_id) REFERENCES answer(id),
  UNIQUE (question_id, answer_id)
);

CREATE TABLE quiz_instance (
  id SERIAL PRIMARY KEY,
  quizuser_id INTEGER NOT NULL,
  quiz_id INTEGER NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  finished_at TIMESTAMPTZ,
  FOREIGN KEY(quizuser_id) REFERENCES quizuser(id),
  FOREIGN KEY(quiz_id) REFERENCES quiz(id)
);

CREATE TABLE question_instance (
  id SERIAL PRIMARY KEY,
  quizuser_id INTEGER NOT NULL,
  quiz_instance_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  answer_id INTEGER NOT NULL,
  answered_at TIMESTAMPTZ NOT NULL,
  FOREIGN KEY(quizuser_id) REFERENCES quizuser(id),
  FOREIGN KEY(quiz_instance_id) REFERENCES quiz_instance(id),
  FOREIGN KEY(question_id) REFERENCES question(id),
  FOREIGN KEY(answer_id) REFERENCES answer(id),
  UNIQUE (quiz_instance_id, question_id)
);
