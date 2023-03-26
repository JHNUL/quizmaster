[![system-tests](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml/badge.svg?branch=main)](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml)

# Quizmaster

The application allows users to create, share and complete quizzes on various topics.

## Technical documentation

 - [Developing and testing](docs/Howto.md)
 - [Database schema](docs/Dbschema.md)

## Quiz

Quizzes can consist of one to many questions each with three to five(?) answer options, only one of which is correct. Upon answering a question, user should see the correct answer and possibly extra info on the selected answer if it was incorrect. User can only progress linearly through a quiz, no backsies. Quiz attempts are timed and some score on a quiz is calculated based on how many correct answers there were and how quick they were answered.

Quizzes can be created, edited, deleted and attemped by any registered user. Some data about attempts are collected per user that only the user themselves and admin can see. User cannot edit or delete another users quizzes. User should not see other users' scores on quizzes.

## Functionality

High level functionality from user role perspective that can be tested at this point by course reviewers. Everything looks awful because function takes priority over form at this point, styles are added in the end if time permits. Robot Framework test suite tags are there for convenience, should you want to run relevant tests with the browser. See instructions in [Developing and testing](docs/Howto.md).

|Role|Functionality|Status|Robot tags|
|---|---|---|---|
|User|create username and password|DONE|loginORlogout|
|User|login and logout|DONE|loginORlogout|
|User|see list of quizzes|DONE|quiz_creationORquestion_creation|
|User|create a new quiz|DONE|quiz_creationORquestion_creation|
|User|complete a quiz||
|User|edit or delete own quiz||
|User|see data on own completed quizzes||
|Admin|(TBC, not included in MVP)||
