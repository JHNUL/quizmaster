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
    @{text_list}=    FakerLibrary.Words    nb=${words}
    ${txt}=    Catenate    @{text_list}
    IF    '${as_question}'=='${True}'
        ${txt}=    Set Variable    ${txt}?
    END
    RETURN    ${txt}

Create New Quiz
    User Navigates To Quiz Page
    Quiz Page Should Be Open
    ${quiz_title}=    Get Lorem Ipsum Text    words=${3}
    ${quiz_desc}=    Get Lorem Ipsum Text    words=${10}
    Input Text    quiztitle    ${quiz_title}
    Input Text    quizdescription    ${quiz_desc}
    Click Ok Button
    Quiz Details Page Should Be Open
    FOR    ${i}    IN RANGE    5
        Click Button    Add question
        ${question_name}=    Get Lorem Ipsum Text    as_question=${True}
        Input Text    questionname    ${question_name}
        Repeat Keyword    ${MAX_ANSWER_OPTIONS} times    Click Button    ${ADD_ANSWER_BTN}
        ${inputs}=    Get WebElements    ${ANSWER_INPUTS}
        FOR    ${input}    IN    @{inputs}
            ${answer}=    Get Lorem Ipsum Text
            Input Text    ${input}    ${answer}
        END
        ${checkboxes}    Get WebElements    ${ANSWER_CHECKBOXES}
        ${correct}    Get Random Element From List    ${checkboxes}
        Click Element    ${correct}
        Click Button    ${SAVE_QUESTION_BTN}
    END
    RETURN    ${quiz_title}    ${quiz_desc}

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
    [Arguments]    ${selectable_quizzes}=${None}
    User Navigates To Landing Page
    Landing Page Should Be Open
    IF    $selectable_quizzes==${None}
        ${selectable_quizzes}=    Get All Visible Quizzes From Landing Page
    END
    ${quiz}=    Get Random Element From List    ${selectable_quizzes}
    Click Button    //*[@id='quizlist']/div//h2[text()='${quiz}']/../../a/button[text()='Open']
