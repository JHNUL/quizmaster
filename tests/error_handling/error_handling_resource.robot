*** Settings ***
Library     SeleniumLibrary
Library     Screenshot
Resource    ../common_resource.robot


*** Keywords ***
Error Handling Suite Setup
    ${SUITE_USERNAME}    ${SUITE_PASSWORD}    Create User
    ${SUITE_USER_QUIZZES}    Create List
    FOR    ${i}    IN RANGE    3
        ${quiz}    Create Quiz With Api
        ...    ${SUITE_USERNAME}
        ...    ${SUITE_PASSWORD}
        Append To List    ${SUITE_USER_QUIZZES}    ${quiz}
    END
    Set Suite Variable    ${SUITE_USERNAME}
    Set Suite Variable    ${SUITE_PASSWORD}
    Set Suite Variable    ${SUITE_USER_QUIZZES}

Login As Suite User
    Open And Configure Browser
    User Navigates To Login Page
    Input Text    username    ${SUITE_USERNAME}
    Input Text    password    ${SUITE_PASSWORD}
    Click Button    ${SUBMIT_BTN}
    Landing Page Should Be Open

Error Page When Trying To Start Non Existing Quiz
    ${attempt_url}    Get From Dictionary    ${ROUTES_DICT}    Attempt
    Go To    ${attempt_url}/-999
    Not Found Page Should Be Open
