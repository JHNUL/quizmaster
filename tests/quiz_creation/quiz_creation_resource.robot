*** Settings ***
Library     SeleniumLibrary
Library     Screenshot
Resource    ../common_resource.robot


*** Keywords ***
User Should Be Able To Create A New Quiz
    ${quiz_title}    Get Lorem Ipsum Text    words=${3}
    ${quiz_desc}    Get Lorem Ipsum Text    words=${10}
    Input Text    quiztitle    ${quiz_title}
    Input Text    quizdescription    ${quiz_desc}
    Click Ok Button
    Quiz Details Page Should Be Open

User Should Be Able To Start And Cancel Quiz Creation
    ${quiz_title}    Get Lorem Ipsum Text    words=${3}
    ${quiz_desc}    Get Lorem Ipsum Text    words=${10}
    Input Text    quiztitle    ${quiz_title}
    Input Text    quizdescription    ${quiz_desc}
    Click Cancel Button
    Landing Page Should Be Open

Add Maximum Number Of Answers
    ${answers}    Get Element Count    ${ANSWER_INPUTS}
    Should Be Equal As Integers    ${answers}    ${DEFAULT_ANSWER_OPTIONS}
    ${over_max}    Evaluate    ${MAX_ANSWER_OPTIONS}+1
    Repeat Keyword    ${over_max} times    Click Button    ${ADD_ANSWER_BTN}
    ${answers_after}    Get Element Count    ${ANSWER_INPUTS}
    Should Be Equal As Integers    ${answers_after}    ${MAX_ANSWER_OPTIONS}

Add Text To All Visible Empty Answers
    ${inputs}    Get WebElements    ${ANSWER_INPUTS}
    FOR    ${input}    IN    @{inputs}
        ${answer}    Get Lorem Ipsum Text
        Input Text    ${input}    ${answer}
    END

Define Random Question As Correct
    ${checkboxes}    Get WebElements    ${ANSWER_CHECKBOXES}
    ${correct}    Get Random Element From List    ${checkboxes}
    Click Element    ${correct}

User Should Be Able To Add A Question With Answer Options
    ${question_name}    Get Lorem Ipsum Text    as_question=${True}
    Click Button    Add question
    Input Text    questionname    ${question_name}
    Add Maximum Number Of Answers
    Add Text To All Visible Empty Answers
    Define Random Question As Correct
    Capture Page Screenshot
    Click Button    ${SAVE_QUESTION_BTN}
    RETURN    ${question_name}

User Has Added Multiple Questions To Quiz
    [Arguments]    ${question_amount}=${5}
    User Navigates To Quiz Page
    Quiz Page Should Be Open
    User Should Be Able To Create A New Quiz
    ${QUESTION_NAMES}    Create List
    FOR    ${i}    IN RANGE    5
        ${q_name}    User Should Be Able To Add A Question With Answer Options
        Append To List    ${QUESTION_NAMES}    ${q_name}
    END
    Set Test Variable    ${QUESTION_NAMES}

Created Questions Are Visible On Page
    FOR    ${question}    IN    @{QUESTION_NAMES}
        Page Should Contain    ${question}
    END
    Capture Page Screenshot

User Has Created A Quiz
    User Navigates To Quiz Page
    Quiz Page Should Be Open
    User Should Be Able To Create A New Quiz

User Can Adjust The Amount Of Answer Options
    Click Button    Add question
    ${answers}    Get Element Count    ${ANSWER_INPUTS}
    Should Be Equal As Integers    ${answers}    ${DEFAULT_ANSWER_OPTIONS}
    Repeat Keyword    2 times    Click Button    ${ADD_ANSWER_BTN}
    ${answers_after}    Get Element Count    ${ANSWER_INPUTS}
    Should Be Equal As Integers    ${answers_after}    ${4}
    Click Button    ${REMOVE_ANSWER_BTN}
    ${answers_after}    Get Element Count    ${ANSWER_INPUTS}
    Should Be Equal As Integers    ${answers_after}    ${3}

User Can Cancel Question Creation
    ${attr}    SeleniumLibrary.Get Element Attribute    id:add_question_form    style
    Should Be Equal As Strings    ${attr}    display: block;
    Click Cancel Button
    ${attr}    SeleniumLibrary.Get Element Attribute    id:add_question_form    style
    Should Be Equal As Strings    ${attr}    display: none;
