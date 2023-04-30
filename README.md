[![system-tests](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml/badge.svg?branch=main)](https://github.com/JHNUL/quizmaster/actions/workflows/system-tests.yaml)

# Quizmaster

The application allows users to create, share and complete quizzes on various topics.

The deployed application is available at https://quizmastah.herokuapp.com/.

## Documentation

 - [Instructions to run locally](docs/dev.md)
 - [Database schema](docs/dbschema.md)
 - [CI/CD](docs/cicd.md)
 - [Instructions](docs/instructions.md)

## About the application

### Creating a quiz
Quizzes can consist of one to many questions each with two to five answer options. User can mark any of the answer options as correct or none of them. The application on purpose does not force the user to mark one answer option as correct, any number of answers or none can be correct as decided by the quiz author. User can create a quiz and test it before making it public to other users. An unpublished quiz is not accessible to any other user than its author. Published quizzes are visible to everyone and cannot be deleted or edited anymore.

### Filling a quiz
User can attempt any quiz that is visible in the list of quizzes. While in the quiz, user can select an answer and change it while still viewing that question. When navigating to the next question the answer is locked. User can only progress linearly through a quiz, already saved answers cannot be changed. If user navigates away from the quiz without completing it, the next time they start that same quiz it continues from the same place.

### Quiz results
One attempt of a quiz is a single instance, same quizzes can be filled many times, each saving the results as a new instance of that quiz for the user. Quiz attempts are timed and the results are shown to the user when finishing a quiz, including the time it took to answer the questions. There is a special statistics page where user can see overall stats about how many quizzes they have completed and what is the percentage of correctly answered questions.

## Known limitations

- There is no upper limit of questions in a quiz, in theory a user could add so many questions to one quiz that all the routes that get the full data of one quiz will be loading really large amounts of data in memory.
- Test coverage is lacking in many places, e.g malicious inputs are not extensively tested
- Although a question can be deleted if the quiz is not published, it cannot be edited.
