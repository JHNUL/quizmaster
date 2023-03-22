*** Settings ***
Resource            login_resource.robot
Resource            ../common_resource.robot

Test Setup          Open And Configure Browser
Test Teardown       Close Browser


*** Test Cases ***
User Can Register To The Application
    Given User Can Navigate To Register Page
    When User Inputs Valid Username And Password
    Then User Is Redirected To Login

Usernames Are Unique
    Given Username Has Been Registered
    When User Inputs The Same Username
    Then User Stays On Register Page And Sees Error Message

User Can Login To The Application
    Given Username Has Been Registered
    When User Can Navigate To Login Page
    And User Inputs Valid Username And Password
    ...    username=${UN}    password=${PW}
    Then User Is Directed To Landing Page
