*** Settings ***
Resource            quiz_results_resource.robot

Test Setup          Create User And Login
Test Teardown       Close Browser


*** Test Cases ***
Quiz Results Show Results Correctly (All Correct)
    [Tags]    quiz_results
    Given User Has Finished A Quiz
    When User Is At Quiz Results Page
    Then Results Are Shown Correctly For All Correct Answers

Quiz Results Show Results Correctly (Some Correct)
    [Tags]    quiz_results
    Given User Has Finished A Quiz With Some Correct Answers
    When User Is At Quiz Results Page
    Then Results Are Shown Correctly For Some Correct Answers

Quiz Results Show Results Correctly (None Correct)
    [Tags]    quiz_results
    Given User Has Finished A Quiz With No Correct Answers
    When User Is At Quiz Results Page
    Then Results Are Shown Correctly For No Correct Answers

User Quiz Statistics Do Not Show Inactive Quiz Results
    [Tags]    quiz_results    user_stats
    Given User Has Finished An Unpublished Quiz
    And Statistics Include Correct Quiz Results
    And User Has Deleted The Quiz
    Then Quiz Stats Page Should Show No Statistics

User Quiz Statistics Shows Correct Statistics After One Quiz
    [Tags]    quiz_results    user_stats
    Given User Has Finished A Quiz With Some Correct Answers
    And User Navigates To Stats Page
    Then Statistics Are Shown Correctly For One Quiz

User Quiz Statistics Shows Correct Statistics After Multiple Quizzes
    [Tags]    quiz_results    user_stats
    Given User Has Finished A Quiz
    Given User Has Finished A Quiz With Some Correct Answers
    Given User Has Finished A Quiz With No Correct Answers
    And User Navigates To Stats Page
    Then Statistics Are Shown Correctly For Multiple Quizzes
