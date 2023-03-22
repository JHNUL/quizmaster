*** Settings ***
Library         SeleniumLibrary
Library         String
Library         LoginLibrary.py
Library         Screenshot
Variables       ../variables.py


*** Variables ***
${REGISTER_URL}     ${BASE_URL}/register
${LOGIN_URL}        ${BASE_URL}/login


*** Keywords ***
Register Page Should Be Open
    Title Should Be    Register
    Capture Page Screenshot

Login Page Should Be Open
    Title Should Be    Login
    Capture Page Screenshot

Landing Page Should Be Open
    Title Should Be    Langing page

User Can Navigate To Register Page
    Go To    ${REGISTER_URL}
    Register Page Should Be Open

User Can Navigate To Login Page
    Go To    ${LOGIN_URL}
    Login Page Should Be Open

User Inputs Valid Username And Password
    [Arguments]    ${username}=${None}    ${password}=${None}
    IF    '${username}'=='${None}'
        ${rnd}=    Generate Random String    8    [LOWER]
        ${username}=    Set Variable    ${rnd}@quiztester.dev
    END
    IF    '${password}'=='${None}'
        ${password}=    Generate Random String    15    [NUMBERS][LOWER]
    END
    Input Text    username    ${username}
    Input Text    password    ${password}
    Click Button    Submit
    RETURN    ${username}    ${password}

User Is Redirected To Login
    Title Should Be    Login
    Capture Page Screenshot

Username Has Been Registered
    User Can Navigate To Register Page
    ${UN}    ${PW}=    User Inputs Valid Username And Password
    Set Test Variable    ${UN}
    Set Test Variable    ${PW}

User Inputs The Same Username
    User Can Navigate To Register Page
    User Inputs Valid Username And Password    ${UN}    ${PW}

User Stays On Register Page And Sees Error Message
    Register Page Should Be Open
    Page Should Contain    Username not available!

User Is Directed To Landingpage
    Landing Page Should Be Open
