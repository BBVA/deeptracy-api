
Feature: Delete projects
  The API should be able to delete existing projects

  Background: Database setup
    Given an empty system

  Scenario: Delete project by id
    When a project with id "0000001" exists in the database
    And the user makes a "DELETE" request to "/api/1/project/0000001" endpoint with empty
    Then the api response code is 204
    And the api response payload is empty
    And project with id "0000001" is not in the database

  Scenario: Try to delete project that does not exist
    When a project with id "0000001" exists in the database
    And the user makes a "DELETE" request to "/api/1/project/0000002" endpoint with empty
    Then the api response code is 404
    And the api response payload is {"error": {"msg": "project not found"}}

   Scenario: Delete projects
    When a project with id "0000001" exists in the database
    And a project with id "0000002" exists in the database
    When the user makes a "DELETE" request to "/api/1/project/" endpoint with empty
    Then the api response code is 204
    And the api response payload is empty
    And table projects is empty
