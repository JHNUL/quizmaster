*** Settings ***
Library     SeleniumLibrary
Library     Screenshot
Resource    ../common_resource.robot


*** Keywords ***
Quiz Usage Suite Setup
    ${SUITE_USERNAME}    ${SUITE_PASSWORD}    Create User And Login
    ${QUIZ_NAMES}    Create List
    FOR    ${i}    IN RANGE    3
        ${quiz_title}    ${quiz_desc}    Create New Quiz
        Append To List    ${QUIZ_NAMES}    ${quiz_title}
    END
    Set Suite Variable    ${SUITE_USERNAME}
    Set Suite Variable    ${SUITE_PASSWORD}
    Set Suite Variable    ${QUIZ_NAMES}
    Click Element    ${LOGOUT_BTN}
    Close All Browsers

Login As Test User
    Open And Configure Browser
    User Navigates To Login Page
    Input Text    username    ${SUITE_USERNAME}
    Input Text    password    ${SUITE_PASSWORD}
    Click Button    Submit
    Landing Page Should Be Open

Quizzes Should Be Listed On Landing Page
    [Arguments]    ${expected_quizzes}=${QUIZ_NAMES}
    User Navigates To Landing Page
    FOR    ${quiz}    IN    @{expected_quizzes}
        Page Should Contain    ${quiz}
    END
    Capture Page Screenshot

Quizzes Created By Other User Should Be Listed On Landing Page
    ${quiz_title}    ${quiz_desc}    Create New Quiz
    ${names}    Copy List    ${QUIZ_NAMES}
    Append To List    ${names}    ${quiz_title}
    Quizzes Should Be Listed On Landing Page    ${names}
    Click Element    ${LOGOUT_BTN}
    Login Page Should Be Open
    Input Text    username    ${SUITE_USERNAME}
    Input Text    password    ${SUITE_PASSWORD}
    Click Button    Submit
    Landing Page Should Be Open
    Quizzes Should Be Listed On Landing Page    ${names}
