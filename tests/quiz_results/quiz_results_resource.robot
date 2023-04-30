*** Settings ***
Library     SeleniumLibrary
Library     Screenshot
Resource    ../common_resource.robot


*** Keywords ***
User Has Finished A Quiz
    ${QUIZ}    Create New Quiz
    Start Quiz From Landing Page    ${QUIZ}
    Complete Quiz With Specific Answers    ${QUIZ["correct_answers"]}
    Set Test Variable    ${QUIZ}

User Has Finished A Quiz With Some Correct Answers
    ${QUIZ}    Create New Quiz
    Start Quiz From Landing Page    ${QUIZ}
    ${answers}    Shuffle Every Other Value    ${QUIZ["correct_answers"]}
    Complete Quiz With Specific Answers    ${answers}
    Set Test Variable    ${QUIZ}

User Has Finished A Quiz With No Correct Answers
    ${QUIZ}    Create New Quiz
    Start Quiz From Landing Page    ${QUIZ}
    ${answers}    Shuffle Every Value    ${QUIZ["correct_answers"]}
    Complete Quiz With Specific Answers    ${answers}
    Set Test Variable    ${QUIZ}

User Is At Quiz Results Page
    Quiz Results Page Should Be Open
    Capture Page Screenshot

Loop And Expect ${result}
    ${questions}    Get From Dictionary    ${QUIZ}    questions
    FOR    ${question}    IN    @{questions}
        ${elem}    Get WebElement    //*[@id="content"]//h3[text()='${question}']/following-sibling::div//span
        Should Be Equal As Strings    ${elem.text}    ${result}
    END

Results Are Shown Correctly For All Correct Answers
    Loop And Expect Correct

Results Are Shown Correctly For No Correct Answers
    Loop And Expect Incorrect

Results Are Shown Correctly For Some Correct Answers
    ${questions}    Get From Dictionary    ${QUIZ}    questions
    ${counter}    Set Variable    ${0}
    FOR    ${question}    IN    @{questions}
        ${result}    Get WebElement    //*[@id="content"]//h3[text()='${question}']/following-sibling::div//span
        IF    $counter % 2 == 1
            Should Be Equal As Strings    ${result.text}    Correct
        ELSE
            Should Be Equal As Strings    ${result.text}    Incorrect
        END
        ${counter}    Evaluate    ${counter}+1
    END

Complete Quiz With Specific Answers
    [Arguments]    ${answers_to_select}
    Quiz Start Page Should Be Open
    Click Button    ${START_QUIZ_BUTTON}
    ${counter}    Set Variable    ${0}
    ${count}    Get Element Count    ${NEXT_QUESTION_BTN}
    ${SELECTED_ANSWERS}    Create List
    WHILE    $count == 1 and $counter < 20
        ${all_options}    Get WebElements    ${ANSWER_OPTIONS}
        ${index}    Get From List    ${answers_to_select}    ${counter}
        ${selected_option}    Get From List    ${all_options}    ${index}
        Click Element    ${selected_option}
        ${option_text}    Get Text    ${selected_option}
        Append To List    ${SELECTED_ANSWERS}    ${option_text}
        ${next_btn}    Get WebElement    ${NEXT_QUESTION_BTN}
        Click Button    ${next_btn}
        ${count}    Get Element Count    ${NEXT_QUESTION_BTN}
        ${counter}    Evaluate    ${counter}+1
    END
    Set Test Variable    ${SELECTED_ANSWERS}

User Has Finished An Unpublished Quiz
    ${QUIZ}    Create New Quiz    publish=${False}
    Start Quiz From Landing Page    ${QUIZ}
    Complete Quiz With Specific Answers    ${QUIZ["correct_answers"]}
    Quiz Results Page Should Be Open
    Set Test Variable    ${QUIZ}

Check Stats
    [Arguments]    ${quizzes}    ${questions}    ${correct}    ${duration}=${None}
    ${total_quizzes}    Get Text    id:stats_total_quizzes
    ${total_answers}    Get Text    id:stats_total_answers
    ${total_correct}    Get Text    id:stats_total_correct
    ${avg_duration}    Get Text    id:stats_avg_duration
    Should Be Equal As Strings    ${total_quizzes}    ${quizzes}
    Should Be Equal As Strings    ${total_answers}    ${questions}
    Should Be Equal As Strings    ${total_correct}    ${correct}
    IF    $duration != None
        Should Be Equal As Strings    ${avg_duration}    ${duration}
    END

Statistics Include Correct Quiz Results
    User Navigates To Stats Page
    Stats Page Should Be Open
    Page Should Contain    Statistics for user ${USERNAME}
    Check Stats    quizzes=1    questions=5    correct=100.0%

User Has Deleted The Quiz
    User Navigates To Landing Page
    Landing Page Should Be Open
    Page Should Contain    ${QUIZ["quiz_title"]}
    Click Button    id:delete_quiz_${QUIZ["quiz_id"]}
    Wait Until Page Does Not Contain    ${QUIZ["quiz_title"]}    timeout=1 second
    Landing Page Should Be Open

Quiz Stats Page Should Show No Statistics
    User Navigates To Stats Page
    Stats Page Should Be Open
    Page Should Contain    Statistics for user ${USERNAME}
    Check Stats    quizzes=0    questions=0    correct=0.0%    duration=0 seconds

Statistics Are Shown Correctly For One Quiz
    Stats Page Should Be Open
    Page Should Contain    Statistics for user ${USERNAME}
    Check Stats    quizzes=1    questions=5    correct=40.0%

Statistics Are Shown Correctly For Multiple Quizzes
    # 3 quizzes, 5 questions each
    # 1st quiz all correct
    # 2nd quiz 2 correct
    # 3rd quiz 0 correct
    # 7/15 ~= 46.7 %
    Stats Page Should Be Open
    Page Should Contain    Statistics for user ${USERNAME}
    Check Stats    quizzes=3    questions=15    correct=46.7%
