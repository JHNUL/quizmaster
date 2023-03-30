[![system-tests](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml/badge.svg?branch=main)](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml)

# Quizmaster

The application allows users to create, share and complete quizzes on various topics.

The deployed application is available at https://quizmaster.fly.dev/

## Documentation

 - [Instructions to run locally](docs/dev.md)
 - [Database schema](docs/dbschema.md)
 - [CI/CD](docs/cicd.md)
 - [Todos](docs/todos.md)

## About the application (Draft)

Quizzes can consist of one to many questions each with two to five answer options, only one of which is correct. User can select the answer and change it while still viewing that question. When navigating to the next question the answer is locked. User can only progress linearly through a quiz, already saved answers cannot be changed. One attempt of a quiz is a single instance, same quizzes can be filled many times each saving the results as a new instance of that quiz for the user. Quiz attempts are timed and some score on a quiz is calculated based on how many correct answers there were and how quick they were answered.

## Functionality

High level functionality that can be tested by course reviewers. Everything looks awful because function takes priority over form at this point, styles are added in the end if time permits. Robot Framework test suite tags are there for convenience, should you want to run relevant tests and see things happening in the browser. As these are very high level, more techical and detailed tasks on how the development is going are recorded [here](docs/todos.md).

List is likely to grow once development goes further but at least the non-optionals here are required for MVP.

|Optional|Role|Functionality|Status|Robot tags|
|---|---|---|---|---|
|No|User|create username and password|DONE|registerORlogin|
|No|User|login and logout|DONE|loginORlogout|
|No|User|see list of quizzes|DONE|quiz_creationORquestion_creation|
|No|User|create a new quiz|DONE|quiz_creationORquestion_creation|
|No|User|complete a quiz||
|No|User|can filter and search quizzes by some categories||
|No|User|edit or delete own quiz while it is not yet published||
|No|User|see data about quizzes that they've completed||
|Yes|User|can give score to a quiz||
|Yes|User|can comment on a quiz||
