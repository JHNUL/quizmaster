*** Settings ***
Resource            login_resource.robot

Suite Setup         Open And Configure Browser
Suite Teardown      Close Browser


*** Test Cases ***
User Can Register To The Application
    Given User Can Navigate To Register Page
    When User Inputs Valid Username And Password
    Then User Is Registered To The Application
