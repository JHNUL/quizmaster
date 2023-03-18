*** Settings ***
Library     SeleniumLibrary
Library     LoginLibrary.py


*** Variables ***
${SERVER}           localhost:5000
${BROWSER}          chrome
${DELAY}            0.2 seconds
${HOME_URL}         http://${SERVER}
${REGISTER_URL}     http://${SERVER}/register


*** Keywords ***
Open And Configure Browser
    Open Browser    browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Register Page Should Be Open
    Title Should Be    Register

User Can Navigate To Register Page
    Go To    ${REGISTER_URL}
    Register Page Should Be Open

User Inputs Valid Username And Password
    Input Text    username    RobotUser
    Input Text    password    RobotPassword
    Click Button    Submit

User Is Registered To The Application
    Pass Execution    Not implemented
