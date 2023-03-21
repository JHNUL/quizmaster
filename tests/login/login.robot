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
    Given Another User Has Registered A Username
    When User Inputs The Same Username
    Then User Stays On Register Page And Sees Error Message
