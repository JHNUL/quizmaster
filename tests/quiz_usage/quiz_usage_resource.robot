*** Settings ***
Library     SeleniumLibrary
Library     Screenshot
Resource    ../common_resource.robot


*** Keywords ***
Quiz Usage Suite Setup
    ${SUITE_USERNAME}    ${SUITE_PASSWORD}    Create User
    ${SUITE_USER_QUIZZES}    Create List
    ${UNPUBLISHED_QUIZZES}    Create List
    FOR    ${i}    IN RANGE    6
        ${do_publish}    Evaluate    ${i} > 2
        ${quiz}    Create Quiz With Api
        ...    ${SUITE_USERNAME}
        ...    ${SUITE_PASSWORD}
        ...    publish=${do_publish}
        IF    $do_publish == True
            Append To List    ${SUITE_USER_QUIZZES}    ${quiz}
        ELSE
            Append To List    ${UNPUBLISHED_QUIZZES}    ${quiz}
        END
    END
    Set Suite Variable    ${UNPUBLISHED_QUIZZES}
    Set Suite Variable    ${SUITE_USERNAME}
    Set Suite Variable    ${SUITE_PASSWORD}
    Set Suite Variable    ${SUITE_USER_QUIZZES}

Login As Test User
    Open And Configure Browser
    User Navigates To Login Page
    Input Text    username    ${SUITE_USERNAME}
    Input Text    password    ${SUITE_PASSWORD}
    Click Button    ${SUBMIT_BTN}
    Landing Page Should Be Open

Quizzes Should Be Listed On Landing Page
    [Arguments]    ${expected_quizzes}=${SUITE_USER_QUIZZES}
    User Navigates To Landing Page
    FOR    ${quiz}    IN    @{expected_quizzes}
        Page Should Contain    ${quiz["quiz_title"]}
    END
    Capture Page Screenshot

Quizzes Created By Other User Should Be Listed On Landing Page
    ${quiz}    Create New Quiz    questions=${1}
    ${quizzes}    Copy List    ${SUITE_USER_QUIZZES}
    Append To List    ${quizzes}    ${quiz}
    Quizzes Should Be Listed On Landing Page    ${quizzes}
    Click Element    ${LOGOUT_BTN}
    Login Page Should Be Open
    Input Text    username    ${SUITE_USERNAME}
    Input Text    password    ${SUITE_PASSWORD}
    Click Button    ${SUBMIT_BTN}
    Landing Page Should Be Open
    Quizzes Should Be Listed On Landing Page    ${quizzes}

Unpublished Quizzes Created By Others Are Not Visible
    Click Element    ${LOGOUT_BTN}
    Login Page Should Be Open
    Input Text    username    ${USERNAME}
    Input Text    password    ${PASSWORD}
    Click Button    ${SUBMIT_BTN}
    Landing Page Should Be Open
    ${visible_quizzes}    Get All Visible Quizzes From Landing Page
    FOR    ${quiz}    IN    @{UNPUBLISHED_QUIZZES}
        List Should Not Contain Value    ${visible_quizzes}    ${quiz["quiz_title"]}
    END

User Clicks To Start Quiz
    Start Random Quiz From Landing Page    ${SUITE_USER_QUIZZES}

User Can See Quiz Front Page
    Quiz Start Page Should Be Open
    Capture Page Screenshot

Choose Answer Option
    ${all_options}    Get WebElements    ${ANSWER_OPTIONS}
    ${selected_option}    ${index}    Get Random Element From List    ${all_options}
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

Click Delete Quiz
    [Arguments]    ${quiz}
    Click Button    id:delete_quiz_${quiz["quiz_id"]}

Click Edit Quiz
    [Arguments]    ${quiz}
    Click Button    id:edit_quiz_${quiz["quiz_id"]}
    Edit Quiz Page Should Be Open

Quiz Should Not Have Edit Button
    [Arguments]    ${quiz}
    Page Should Contain Element    id:open_quiz_${quiz["quiz_id"]}
    Page Should Not Contain Element    id:edit_quiz_${quiz["quiz_id"]}

User Should Only Be Able To Edit Own Unpublished Quizzes
    FOR    ${quiz}    IN    @{UNPUBLISHED_QUIZZES}
        Click Edit Quiz    ${quiz}
        Capture Page Screenshot
        User Navigates To Landing Page
    END

User Clicks To Edit A Quiz They Created
    ${own_quiz}    ${index}    Get Random Element From List    ${UNPUBLISHED_QUIZZES}
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

User Has An Unpublished Quiz
    ${DELETABLE_QUIZ}    Create New Quiz    questions=${1}    publish=${False}
    Set Test Variable    ${DELETABLE_QUIZ}

User Is Able To Delete Quiz
    Page Should Contain    ${DELETABLE_QUIZ["quiz_title"]}
    Click Delete Quiz    ${DELETABLE_QUIZ}
    Wait Until Page Does Not Contain    ${DELETABLE_QUIZ["quiz_title"]}    timeout=1 second
    Landing Page Should Be Open

User Has Filled That Quiz
    Start Quiz From Landing Page    ${DELETABLE_QUIZ}
    User Can Click Through Questions
    User Navigates To Landing Page
