*** Settings ***
Resource            quiz_creation_resource.robot

Test Setup          Create User And Login
Test Teardown       Close Browser


*** Test Cases ***
User Can Create A New Quiz
    [Tags]    quiz_creation
    Given User Navigates To Quiz Page
    And Quiz Page Should Be Open
    Then User Should Be Able To Create A New Quiz

User Can Cancel Quiz Creation
    [Tags]    quiz_creation
    Given User Navigates To Quiz Page
    And Quiz Page Should Be Open
    Then User Should Be Able To Start And Cancel Quiz Creation

User Can Add Question To Quiz
    [Tags]    quiz_creation    question_creation
    Given User Navigates To Quiz Page
    And Quiz Page Should Be Open
    And User Should Be Able To Create A New Quiz
    Then User Should Be Able To Add A Question With Answer Options

Questions Included In Quiz Are Listed
    [Tags]    quiz_creation    question_creation
    Given User Has Added Multiple Questions To Quiz
    Then Created Questions Are Visible On Page

Answer Options Can Be Added And Removed
    [Tags]    quiz_creation    question_creation
    Given User Has Created A Quiz
    Then User Can Adjust The Amount Of Answer Options
    And User Can Cancel Question Creation
