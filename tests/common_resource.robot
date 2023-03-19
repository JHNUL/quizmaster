*** Settings ***
Library         SeleniumLibrary
Variables       variables.py


*** Keywords ***
Open And Configure Browser
    Open Browser    browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
