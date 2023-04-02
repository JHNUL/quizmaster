# Todos

This is mainly to show progress below the main functionality level. These are not refined or prioritized, and serve mostly as a way to keep track of what details still need to be implemented.

 - create username and password DONE
  - log in DONE
  - unauthenticated user should be redirected to login page when trying to go to
    landing page DONE
  - there should be links between register and login <-> DONE
  - user should be able to logout DONE
  - create a new quiz DONE
  - after creating new question to quiz, question is listed and possible to add more DONE
  - see list of quizzes in the system on landingpage DONE
  - complete any quiz in the list DONE
    - Quiz in list is clickable DONE
    - Clicking quiz takes to "attempt quiz" view DONE
    - User can go through the quiz by selecting one answer out of answer options DONE
    - Main view of that page shows description of the quiz and allows to press start DONE
    - An answer should be made in order to go forward DONE
    - After selection the answer is locked for this attempt DONE
    - Final page should show stats about the completed quiz DONE
    - Final page should have link to go to main page DONE
    - Handle quiz with no questions DONE
  - answer can be defined correct (no limitation at first) DONE
  - deploy to fly.io or somewhere, integrate deployment to pipeline DONE
  - user existence should be checked from DB in login_required decorator DONE
  - integrate some style library DONE
  - save timestamps in ISO8601 format
  - show timestamps in client local tz
  - answers can be deleted, not just added
  - transactionality at logical level -> cannot create e.g. 3 out of 5 intended answers
    for a question, all succeed or none do
  - common error message logic
  - possible to navigate away from quiz and question creation
  - possible to edit existing quiz if not public
  - possible to edit existing question along with its answers if not public in quiz
  - unique constraint to connection tables based on compound key
  - shorter session length
  - delete a quiz that belongs to the user (note that quiz might be used while deleting)
  - publish a quiz or keep it private
  - user sees all quizzes that they have created, attempted and completed
  - errorhandler with not found tpl
  - change all urls to use url_for
  - comb through all todos in the code
  - make UI look better IN PROGRESS