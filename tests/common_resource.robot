*** Settings ***
Library         SeleniumLibrary
Library         RequestsLibrary
Library         Collections
Library         FakerLibrary
Library         Selenium.py
Library         Common.py
Variables       variables.py


*** Keywords ***
Register Page Should Be Open
    Title Should Be    Register

Login Page Should Be Open
    Title Should Be    Login

Landing Page Should Be Open
    Title Should Be    Quizmaster

Quiz Page Should Be Open
    Title Should Be    New quiz

Edit Quiz Page Should Be Open
    Title Should Be    Edit quiz

Quiz Details Page Should Be Open
    Title Should Be    Quiz detail

Quiz Start Page Should Be Open
    Title Should Be    Start quiz

Quiz Question Page Should Be Open
    Title Should Be    Question time!

Quiz Results Page Should Be Open
    Title Should Be    Quiz stats

Not Found Page Should Be Open
    Title Should Be    Not found
    Page Should Contain    404 Not Found

User Navigates To ${target} Page
    ${url}=    Get From Dictionary    ${ROUTES_DICT}    ${target}
    Go To    ${url}

Click Ok Button
    Click Button    OK

Click Cancel Button
    Click Button    Cancel

Open And Configure Browser
    ${options}=    Get Chrome Options
    Open Browser    browser=${BROWSER}    options=${options}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Create User And Login
    ${username}    ${password}=    Generate Random Username And Password
    ${data}=    Create Dictionary
    ...    username=${username}
    ...    password=${password}
    ${url}=    Get From Dictionary    ${ROUTES_DICT}    Register
    ${res}=    POST    ${url}    data=${data}
    Status Should Be    200    ${res}
    Open And Configure Browser
    User Navigates To Login Page
    Input Text    username    ${USERNAME}
    Input Text    password    ${PASSWORD}
    Click Button    ${SUBMIT_BTN}
    Landing Page Should Be Open
    Set Suite Variable    ${USERNAME}
    Set Suite Variable    ${PASSWORD}
    RETURN    ${USERNAME}    ${PASSWORD}

Get Lorem Ipsum Text
    [Arguments]    ${words}=${5}    ${as_question}=${False}
    ${text_list}=    FakerLibrary.Words    nb=${words}
    ${txt}=    Catenate    @{text_list}
    IF    '${as_question}'=='${True}'
        ${txt}=    Set Variable    ${txt}?
    END
    RETURN    ${txt}

Create New Quiz
    [Arguments]    ${publish}=${True}    ${questions}=${5}
    User Navigates To Quiz Page
    Quiz Page Should Be Open
    ${quiz_title}=    Get Lorem Ipsum Text    words=${3}
    ${quiz_desc}=    Get Lorem Ipsum Text    words=${10}
    Input Text    quiztitle    ${quiz_title}
    Input Text    quizdescription    ${quiz_desc}
    Click Ok Button
    Quiz Details Page Should Be Open
    ${url}    Get Location
    ${quiz_id}    Get Quiz Id From Url    ${url}
    ${quiz}    Create Dictionary
    ...    quiz_id=${quiz_id}
    ...    quiz_title=${quiz_title}
    ...    quiz_description=${quiz_desc}
    FOR    ${i}    IN RANGE    ${questions}
        Click Button    Add question
        ${question_name}=    Get Lorem Ipsum Text    as_question=${True}
        Input Text    questionname    ${question_name}
        Repeat Keyword    ${MAX_ANSWER_OPTIONS} times    Click Button    ${ADD_ANSWER_BTN}
        ${inputs}=    Get WebElements    ${ANSWER_INPUTS}
        FOR    ${input}    IN    @{inputs}
            ${answer}=    Get Lorem Ipsum Text
            Input Text    ${input}    ${answer}
        END
        ${checkboxes}=    Get WebElements    ${ANSWER_CHECKBOXES}
        ${correct}=    Get Random Element From List    ${checkboxes}
        Click Element    ${correct}
        Click Button    ${SAVE_QUESTION_BTN}
    END
    Click Button    ${QUIZ_DONE_BTN}
    IF    $publish == True
        Click Button    id:publish_quiz_${quiz_id}
    END
    RETURN    ${quiz}

Get All Visible Quizzes From Landing Page
    User Navigates To Landing Page
    Landing Page Should Be Open
    ${quizzes}=    Get WebElements    ${VISIBLE_QUIZZES}
    ${quizzes_text}=    Create List
    FOR    ${quiz}    IN    @{quizzes}
        Append To List    ${quizzes_text}    ${quiz.text}
    END
    RETURN    ${quizzes_text}

Start Quiz From Landing Page
    [Arguments]    ${selectable_quizzes}
    User Navigates To Landing Page
    Landing Page Should Be Open
    ${quiz}=    Get Random Element From List    ${selectable_quizzes}
    Click Button    id:open_quiz_${quiz["quiz_id"]}
