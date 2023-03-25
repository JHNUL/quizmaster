*** Settings ***
Resource            quiz_resource.robot

Test Setup          Create User And Login
Test Teardown       Close Browser


*** Test Cases ***
User Can Create A New Quiz
    [Tags]    quiz_creation
    Given User Navigates To Quiz Page
    And Quiz Page Should Be Open
    Then User Should Be Able To Create A New Quiz
