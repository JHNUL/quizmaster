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
    Title Should Be    Langing page

Quiz Page Should Be Open
    Title Should Be    New quiz

Quiz Details Page Should Be Open
    Title Should Be    Quiz detail

User Navigates To ${target} Page
    ${url}=    Get From Dictionary    ${ROUTES_DICT}    ${target}
    Go To    ${url}

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
    Input Text    username    ${username}
    Input Text    password    ${password}
    Click Button    Submit
    Landing Page Should Be Open

Get Lorem Ipsum Text
    [Arguments]    ${words}=${5}    ${as_question}=${False}
    @{text_list}=    FakerLibrary.Words    nb=${words}
    ${txt}=    Catenate    @{text_list}
    IF    '${as_question}'=='${True}'
        ${txt}=    Set Variable    ${txt}?
    END
    RETURN    ${txt}
