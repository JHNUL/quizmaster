*** Settings ***
Library     SeleniumLibrary
Library     Screenshot
Resource    ../common_resource.robot


*** Keywords ***
Quiz Usage Suite Setup
    ${SUITE_USERNAME}    ${SUITE_PASSWORD}    Create User And Login
    ${SUITE_USER_QUIZ_NAMES}    Create List
    FOR    ${i}    IN RANGE    3
        ${quiz_title}    ${quiz_desc}    Create New Quiz
        Append To List    ${SUITE_USER_QUIZ_NAMES}    ${quiz_title}
    END
    Set Suite Variable    ${SUITE_USERNAME}
    Set Suite Variable    ${SUITE_PASSWORD}
    Set Suite Variable    ${SUITE_USER_QUIZ_NAMES}
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
    [Arguments]    ${expected_quizzes}=${SUITE_USER_QUIZ_NAMES}
    User Navigates To Landing Page
    FOR    ${quiz}    IN    @{expected_quizzes}
        Page Should Contain    ${quiz}
    END
    Capture Page Screenshot

Quizzes Created By Other User Should Be Listed On Landing Page
    ${quiz_title}    ${quiz_desc}    Create New Quiz
    ${names}    Copy List    ${SUITE_USER_QUIZ_NAMES}
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
    Start Quiz From Landing Page    ${SUITE_USER_QUIZ_NAMES}

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

User Starts A Quiz Created By Another User
    User Clicks To Start Quiz
    Quiz Start Page Should Be Open

Quiz Front Page Should Show Correct Creator For Quiz
    Page Should Contain    ${SUITE_USERNAME}
    Page Should Not Contain    ${USERNAME}

Click Edit Quiz
    [Arguments]    ${quiz_name}
    Click Button    //*[@id='quizlist']/div//h2[text()='${quiz_name}']/../../a/button[text()='Edit']
    Edit Quiz Page Should Be Open

Quiz Should Not Have Edit Button
    [Arguments]    ${quiz_name}
    Page Should Contain Element    //*[@id='quizlist']/div//h2[text()='${quiz_name}']/../../a/button[text()='Open']
    Page Should Not Contain Element    //*[@id='quizlist']/div//h2[text()='${quiz_name}']/../../a/button[text()='Edit']

User Should Only Be Able To Edit Own Quizzes
    ${all_quizzes}    Get All Visible Quizzes From Landing Page
    ${total_count}    Set Variable    ${0}
    FOR    ${quiz}    IN    @{all_quizzes}
        ${count}    Get Match Count    ${SUITE_USER_QUIZ_NAMES}    ${quiz}
        IF    $count > 0
            Click Edit Quiz    ${quiz}
            ${total_count}    Evaluate    ${total_count}+1
            User Navigates To Landing Page
            Capture Page Screenshot
        ELSE
            Quiz Should Not Have Edit Button    ${quiz}
        END
    END
    ${suite_user_expected_quiz_count}    Get Length    ${SUITE_USER_QUIZ_NAMES}
    Should Be Equal As Integers    ${suite_user_expected_quiz_count}    ${total_count}

User Clicks To Edit A Quiz They Created
    ${own_quiz}    Get Random Element From List    ${SUITE_USER_QUIZ_NAMES}
    Click Edit Quiz    ${own_quiz}

It Is Possible To Edit Title And Description
    ${old_title}    Get Value    //*[@id="quiztitle"]
    ${old_desc}    Get Text    //*[@id="quizdescription"]
    ${new_title}    Get Lorem Ipsum Text    words=${3}
    ${new_desc}    Get Lorem Ipsum Text    words=${10}
    Input Text    quiztitle    ${new_title}
    Input Text    quizdescription    ${new_desc}
    Click Ok Button
    Quiz Details Page Should Be Open
    Page Should Contain    ${new_title}
    Page Should Contain    ${new_desc}
    Page Should Not Contain    ${old_title}
    Page Should Not Contain    ${old_desc}
    Capture Page Screenshot
