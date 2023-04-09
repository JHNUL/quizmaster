*** Settings ***
Resource            error_handling_resource.robot

Suite Setup         Error Handling Suite Setup
Test Setup          Login As Suite User
Test Teardown       Close All Browsers


*** Test Cases ***
Not Found Page
    [Tags]    error_handling
    Error Page When Trying To Start Non Existing Quiz
