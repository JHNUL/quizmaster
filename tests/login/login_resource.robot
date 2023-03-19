*** Settings ***
Library         SeleniumLibrary
Library         LoginLibrary.py
Variables       ../variables.py


*** Variables ***
${REGISTER_URL}     ${BASE_URL}/register


*** Keywords ***
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
