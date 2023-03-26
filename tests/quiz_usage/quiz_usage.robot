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