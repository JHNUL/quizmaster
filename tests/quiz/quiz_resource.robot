*** Settings ***
Library     SeleniumLibrary
Resource    ../common_resource.robot


*** Keywords ***
User Should Be Able To Create A New Quiz
    Input Text    quiztitle    Stellar quiz
    Input Text    quizdescription    This will test knowledge about astronomy
    Click Button    Create
    # TODO: currently just ends there
