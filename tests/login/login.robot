*** Settings ***
Resource            login_resource.robot

Test Setup          Open And Configure Browser
Test Teardown       Close Browser


*** Test Cases ***
User Can Register To The Application
    [Tags]    register
    Given User Navigates To Register Page
    And Register Page Should Be Open
    When User Inputs Username And Password
    Then User Is Redirected To Login

User Cannot Register To The Application With Invalid Username Or Password
    [Tags]    register
    User Should Not Be Able To Register With Invalid Username Or Password

Usernames Are Unique
    [Tags]    register
    Given Username Has Been Registered
    When User Inputs The Same Username
    Then User Stays On Register Page And Sees Error Message

User Can Login To The Application
    [Tags]    login
    Given Username Has Been Registered
    When User Navigates To Login Page
    And Login Page Should Be Open
    And User Inputs Username And Password
    ...    username=${UN}    password=${PW}
    Then User Is Directed To Landing Page

User Cannot Login To The Application With Incorrect Password
    [Tags]    login
    Given Username Has Been Registered
    When User Navigates To Login Page
    And Login Page Should Be Open
    And User Inputs Username And Password
    ...    username=${UN}    password=qwerty12345
    Then User Stays On Login Page And Sees Error Message
    ...    Incorrect password!

User Cannot Login To The Application With Incorrect Username
    [Tags]    login
    Given Username Has Been Registered
    When User Navigates To Login Page
    And Login Page Should Be Open
    And User Inputs Username And Password
    ...    username=qwerty12345    password=${PW}
    Then User Stays On Login Page And Sees Error Message
    ...    Username not found!

User Cannot Access Application Unless Logged In
    [Tags]    login
    Given User Navigates To Landing Page
    Then User Is Redirected To Login
    And User Navigates To Quiz Page
    Then User Is Redirected To Login

There Should Be A Link To Register From Login
    [Tags]    login
    Given User Navigates To Login Page
    Then User Is Able To Go To Register Page By Link

There Should Be A Link To Login From Register
    [Tags]    login
    Given User Navigates To Register Page
    Then User Is Able To Go To Login Page By Link

User Should Be Able To Logout From The Application
    [Tags]    logout
    Given User Is Logged In
    Then User Can Find Logout Button
    And Pressing Logout Button Logs User Out Of The Application

Login Button Should Be Disabled If User Is Not Logged In
    [Tags]    logout
    Given User Navigates To Login Page
    Then User Can Find Logout Button
    And Logout Button Should Be Disabled
    Then User Navigates To Register Page
    And User Can Find Logout Button
    And Logout Button Should Be Disabled
