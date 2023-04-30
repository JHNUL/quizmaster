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

Define Random Answer As Correct
    ${checkboxes}    Get WebElements    ${ANSWER_CHECKBOXES}
    ${correct}    ${index}    Get Random Element From List    ${checkboxes}
    Click Element    ${correct}

Define Specific Answer As Correct
    [Arguments]    ${index}
    ${checkboxes}    Get WebElements    ${ANSWER_CHECKBOXES}
    ${correct}    Get From List    ${checkboxes}    ${index}
    Click Element    ${correct}

User Should Be Able To Add A Question With Answer Options
    [Arguments]    ${correct_index}=${-1}
    ${question_name}    Get Lorem Ipsum Text    as_question=${True}
    Click Button    Add question
    Input Text    questionname    ${question_name}
    Add Maximum Number Of Answers
    Add Text To All Visible Empty Answers
    IF    $correct_index >= 0
        Define Specific Answer As Correct    ${correct_index}
    ELSE
        Define Random Answer As Correct
    END
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

User Adds Questions To Quiz
    User Has Created A Quiz
    ${q1}    User Should Be Able To Add A Question With Answer Options
    ...    correct_index=${0}
    ${q2}    User Should Be Able To Add A Question With Answer Options
    ...    correct_index=${1}
    ${q3}    User Should Be Able To Add A Question With Answer Options
    ...    correct_index=${4}
    ${FLOW_QUESTIONS}    Create List    ${None}    ${q1}    ${q2}    ${q3}
    ${CORRECT_ANSWERS}    Create List    ${None}    ${0}    ${1}    ${4}
    Set Test Variable    ${FLOW_QUESTIONS}
    Set Test Variable    ${CORRECT_ANSWERS}

Get Visible Questions From Question Flow
    ${count}    Get Element Count    //*[@id="question_flow"]/div[@class='bg-white rounded-md shadow-md p-4']
    ${names}    Create List
    FOR    ${i}    IN RANGE    ${1}    ${count+1}
        ${question_elem}    Get WebElement
        ...    //*[@id="question_flow"]/div[@class='bg-white rounded-md shadow-md p-4'][${i}]/div[1]
        Append To List    ${names}    ${question_elem.text}
    END
    RETURN    ${names}

Questions Show In The Question Flow
    ${count}    Get Element Count    //*[@id="question_flow"]/div[@class='bg-white rounded-md shadow-md p-4']
    FOR    ${i}    IN RANGE    ${1}    ${count+1}
        ${question_elem}    Get WebElement
        ...    //*[@id="question_flow"]/div[@class='bg-white rounded-md shadow-md p-4'][${i}]/div[1]
        ${question}    Get From List    ${FLOW_QUESTIONS}    ${i}
        Should Be Equal As Strings    ${question}    ${question_elem.text}
        ${answer_idx}    Get From List    ${CORRECT_ANSWERS}    ${i}
        ${correct_answer}    Get WebElement
        ...    //*[@id="question_flow"]/div[@class='bg-white rounded-md shadow-md p-4'][${i}]/div[1]/following-sibling::div/p[${answer_idx+1}]
        String Should Contain Substring    ${correct_answer.text}    (Correct)
    END

Questions Can Be Deleted From Question Flow
    ${names}    Get Visible Questions From Question Flow
    Length Should Be    ${names}    ${3}
    Click Button
    ...    //*[@id="question_flow"]/div[@class='bg-white rounded-md shadow-md p-4'][2]/div[1]/following-sibling::div//button
    ${names}    Get Visible Questions From Question Flow
    Length Should Be    ${names}    ${2}
    Should Be Equal As Strings    ${FLOW_QUESTIONS[1]}    ${names[0]}
    Should Be Equal As Strings    ${FLOW_QUESTIONS[3]}    ${names[1]}
