*** Settings ***
Library         SeleniumLibrary
Library         String
Library         Screenshot
Library         Collections
Variables       ../variables.py
Resource        ../common_resource.robot


*** Variables ***
${REGISTER_LINK}            //a[@href='/register']
${LOGIN_LINK}               //a[@href='/login']
${LOGOUT_BTN_DISABLED}      //*[@id='appheader']/div//form/button[text()='Logout' and @disabled]


*** Keywords ***
User Inputs Username And Password
    [Arguments]    ${username}=${None}    ${password}=${None}
    ${gen_username}    ${gen_password}=    Generate Random Username And Password
    IF    '${username}'=='${None}'
        ${username}=    Set Variable    ${gen_username}
    END
    IF    '${password}'=='${None}'
        ${password}=    Set Variable    ${gen_password}
    END
    Input Text    username    ${username}
    Input Text    password    ${password}
    Click Button    ${SUBMIT_BTN}
    RETURN    ${username}    ${password}

User Is Redirected To Login
    Title Should Be    Login

User Should Not Be Able To Register With Invalid Username Or Password
    User Navigates To Register Page
    Register Page Should Be Open
    FOR    ${uname}    IN    @{NAIVE_INVALID_INPUTS_TO_USERNAME}
        User Inputs Username And Password    username=${uname}
        Register Page Should Be Open
    END
    FOR    ${pword}    IN    @{NAIVE_INVALID_INPUTS_TO_PASSWORD}
        User Inputs Username And Password    password=${pword}
        Register Page Should Be Open
    END

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

User Is Able To Go To Register Page By Link
    Login Page Should Be Open
    Click Link    ${REGISTER_LINK}
    Register Page Should Be Open

User Is Able To Go To Login Page By Link
    Register Page Should Be Open
    Click Link    ${LOGIN_LINK}
    Login Page Should Be Open

User Is Logged In
    Username Has Been Registered
    User Navigates To Login Page
    User Inputs Username And Password    ${UN}    ${PW}
    Landing Page Should Be Open

User Can Find Logout Button
    Page Should Contain Element    ${LOGOUT_BTN}

Pressing Logout Button Logs User Out Of The Application
    Click Element    ${LOGOUT_BTN}
    Login Page Should Be Open
    User Navigates To Landing Page
    Login Page Should Be Open
    Go Back
    Login Page Should Be Open

Logout Button Should Be Disabled
    Page Should Contain Element    ${LOGOUT_BTN_DISABLED}
