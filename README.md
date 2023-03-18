# Quizmaster

The application allows users to create, share and complete quizzes on various topics.

## Technical documentation

 - [Developing and testing](docs/Howto.md)
 - [Database schema](docs/Dbschema.md)

## Quiz

Quizzes can consist of one to many questions each with three to five(?) answer options, only one of which is correct. Upon answering a question, user should see the correct answer and possibly extra info on the selected answer if it was incorrect. User can only progress linearly through a quiz, no backsies. Quiz attempts are timed and some score on a quiz is calculated based on how many correct answers there were and how quick they were answered.

Quizzes can be created, edited, deleted and attemped by any registered user. Some data about attempts are collected per user that only the user themselves and admin can see. User cannot edit or delete another users quizzes. User should not see other users' scores on quizzes.

## Roles

### User

Can:
  - create username and password
  - log in
  - see list of existing published quizzes from everyone
  - complete any quiz in the list
  - create a new quiz
  - delete a quiz that belongs to the user (note that quiz might be used while deleting)
  - publish a quiz or keep it private
  - see all quizzes that they have created, attempted and completed

### Admin

Can:
 - see some aggregated data of usage, e.g. how many quizzes created at any given period of time, what percentage is private/published etc.
