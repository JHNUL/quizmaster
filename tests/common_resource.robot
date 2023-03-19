*** Settings ***
Library         SeleniumLibrary
Library         Selenium.py
Variables       variables.py


*** Keywords ***
Open And Configure Browser
    ${options}=    Get Chrome Options
    Open Browser    browser=${BROWSER}    options=${options}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
