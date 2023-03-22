*** Settings ***
Library         SeleniumLibrary
Library         String
Library         LoginLibrary.py
Library         Screenshot
Library         ../../.venv/lib/python3.11/site-packages/robot/libraries/Collections.py
Variables       ../variables.py


*** Keywords ***
Register Page Should Be Open
    Title Should Be    Register

Login Page Should Be Open
    Title Should Be    Login

Landing Page Should Be Open
    Title Should Be    Langing page

User Navigates To ${target} Page
    ${url}=    Get From Dictionary    ${ROUTES_DICT}    ${target}
    Go To    ${url}

User Inputs Username And Password
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

Username Has Been Registered
    User Navigates To Register Page
    ${UN}    ${PW}=    User Inputs Username And Password
    Set Test Variable    ${UN}
    Set Test Variable    ${PW}

User Inputs The Same Username
    User Navigates To Register Page
    User Inputs Username And Password    ${UN}    ${PW}

User Stays On Register Page And Sees Error Message
    Register Page Should Be Open
    Page Should Contain    Username not available!
    Capture Page Screenshot

User Is Directed To Landingpage
    Landing Page Should Be Open

User Stays On Login Page And Sees Error Message
    [Arguments]    ${msg}
    Login Page Should Be Open
    Page Should Contain    ${msg}
    Capture Page Screenshot
