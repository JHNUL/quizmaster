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
    Click Button    ${SUBMIT_BTN}
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
    Click Button    ${SUBMIT_BTN}
    Landing Page Should Be Open
    Quizzes Should Be Listed On Landing Page    ${names}

User Clicks To Start Quiz
    Start Quiz From Landing Page    ${QUIZ_NAMES}

User Can See Quiz Front Page
    Quiz Start Page Should Be Open
    Capture Page Screenshot

Choose Answer Option
    ${all_options}    Get WebElements    ${ANSWER_OPTIONS}
    ${selected_option}    Get Random Element From List    ${all_options}
    Click Element    ${selected_option}
    ${option_text}    Get Text    ${selected_option}
    RETURN    ${option_text}

User Can Click Through Questions
    Quiz Start Page Should Be Open
    Capture Page Screenshot
    Click Button    ${START_QUIZ_BUTTON}
    ${sanity}    Set Variable    ${20}
    ${count}    Get Element Count    ${NEXT_QUESTION_BTN}
    ${SELECTED_ANSWERS}    Create List
    WHILE    $count == 1 and $sanity > 0
        ${selected_answer}    Choose Answer Option
        Append To List    ${SELECTED_ANSWERS}    ${selected_answer}
        Capture Page Screenshot
        ${next_btn}    Get WebElement    ${NEXT_QUESTION_BTN}
        Click Button    ${next_btn}
        ${count}    Get Element Count    ${NEXT_QUESTION_BTN}
        ${sanity}    Evaluate    ${sanity}-1
    END
    Set Test Variable    ${SELECTED_ANSWERS}
    Quiz Results Page Should Be Open

Final Page Shows Quiz Results
    FOR    ${answer}    IN    @{SELECTED_ANSWERS}
        Page Should Contain    ${answer}
    END
    Capture Page Screenshot
