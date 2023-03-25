*** Settings ***
Library     SeleniumLibrary
Library     Screenshot
Resource    ../common_resource.robot


*** Variables ***
${ANSWER_INPUTS}    //*[@id="answeropts"]/input[contains(@id,'answeropt')]


*** Keywords ***
User Should Be Able To Create A New Quiz
    Input Text    quiztitle    Stellar quiz
    Input Text    quizdescription    This will test knowledge about astronomy
    Click Button    Create
    Quiz Details Page Should Be Open

Add Maximum Number Of Answers
    ${answers}    Get Element Count    ${ANSWER_INPUTS}
    Should Be Equal As Integers    ${answers}    ${DEFAULT_ANSWER_OPTIONS}
    ${over_max}    Evaluate    ${MAX_ANSWER_OPTIONS}+10
    Repeat Keyword    ${over_max} times    Click Button    Add answer
    ${answers_after}    Get Element Count    ${ANSWER_INPUTS}
    Should Be Equal As Integers    ${answers_after}    ${MAX_ANSWER_OPTIONS}
    Capture Page Screenshot

Add Text To All Visible Empty Answers
    @{inputs}    Get WebElements    ${ANSWER_INPUTS}
    FOR    ${input}    IN    @{inputs}
        Input Text    ${input}    foo
    END
    Capture Page Screenshot

User Should Be Able To Add A Question With Answer Options
    Input Text    questionname    What's the square root of a potato?
    Add Maximum Number Of Answers
    Add Text To All Visible Empty Answers
