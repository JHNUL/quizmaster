*** Settings ***
Resource            quiz_usage_resource.robot

Suite Setup         Quiz Usage Suite Setup
Test Setup          Login As Test User
Test Teardown       Close All Browsers


*** Test Cases ***
Quizzes Are Listed On Landing Page
    [Tags]    quiz_usage
    Given User Navigates To Landing Page
    Then Quizzes Should Be Listed On Landing Page

Quizzes Created By Other Users Are Visible On Landing Page
    [Tags]    quiz_usage
    [Setup]    Create User And Login
    Given User Navigates To Landing Page
    Then Quizzes Created By Other User Should Be Listed On Landing Page

Quiz Can Be Started
    [Tags]    quiz_usage
    Given User Navigates To Landing Page
    And Quizzes Should Be Listed On Landing Page
    When User Clicks To Start Quiz
    Then User Can See Quiz Front Page

Quiz Can Be Completed
    [Tags]    quiz_usage
    Given User Navigates To Landing Page
    And Quizzes Should Be Listed On Landing Page
    When User Clicks To Start Quiz
    Then User Can Click Through Questions
    And Final Page Shows Quiz Results

Quiz Details Should Show Correct Creator For Quiz
    [Tags]    quiz_usage
    [Setup]    Create User And Login
    When User Starts A Quiz Created By Another User
    Then Quiz Front Page Should Show Correct Creator For Quiz

User Can Edit Quiz That They Created
    [Tags]    quiz_usage    edit_quiz
    Given User Navigates To Landing Page
    Then User Should Only Be Able To Edit Own Quizzes

User Can Edit Title And Description Of Created Quiz
    [Tags]    quiz_usage    edit_quiz
    Given User Navigates To Landing Page
    And User Clicks To Edit A Quiz They Created
    Then It Is Possible To Edit Title And Description
