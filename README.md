[![system-tests](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml/badge.svg?branch=main)](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml)

# Quizmaster

The application allows users to create, share and complete quizzes on various topics.

The deployed application is available at https://quizmastah.herokuapp.com/.

## Documentation

 - [Instructions to run locally](docs/dev.md)
 - [Database schema](docs/dbschema.md)
 - [CI/CD](docs/cicd.md)
 - [Todos](docs/todos.md)

## About the application (Draft)


### Creating a quiz
Quizzes can consist of one to many questions each with two to five answer options. User can create a quiz and test it before making it public to other users. An unpublished quiz is not accessible to any other user that its author. Published quizzes are visible to everyone and cannot be deleted or edited anymore.

### Filling a quiz
User can attempt any quiz that is visible in the list of quizzes. While in the quiz, user can select an answer and change it while still viewing that question. When navigating to the next question the answer is locked. User can only progress linearly through a quiz, already saved answers cannot be changed. If user navigates away from the quiz without completing it, the next time they start that same quiz it continues from the same place.

### Quiz results
One attempt of a quiz is a single instance, same quizzes can be filled many times, each saving the results as a new instance of that quiz for the user. Quiz attempts are timed and the results are shown to the user when finishing a quiz, including the time it took to answer the questions. There is a special statistics page where user can see overall stats about how many quizzes they have completed and what is the percentage of correctly answered questions.

## Functionality (updated 23 Apr)

*High level functionality* that the course reviewers should expect to be there when trying it out. The user experience is still somewhat awful at this point.

Robot Framework test suite tags are there for convenience, should you want to run relevant tests and see things happening in the browser.

As these are very high level, more techical and detailed tasks on how the development is going are recorded [here](docs/todos.md).

|MVP|Role|Functionality|Status|Robot tags|
|---|---|---|---|---|
|Yes|User|create username and password|DONE|registerORlogin|
|Yes|User|login and logout|DONE|loginORlogout|
|Yes|User|see list of quizzes|DONE|quiz_creationORquestion_creation|
|Yes|User|create a new quiz|DONE|quiz_creationORquestion_creation|
|Yes|User|complete a quiz|DONE|quiz_usage|
|Yes|User|edit or delete own quiz while it is not yet published|DONE|quiz_usageORdelete_quiz|
|Yes|User|see data about quizzes that they've completed|DONE||
|No|User|can filter and search quizzes by some categories||
|No|User|can give score to a quiz||
|No|User|can comment on a quiz||
