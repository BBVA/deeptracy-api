
Feature: Read projects
  The API should be able to read existing projects

  Background: Database setup
    Given an empty project table in database


  Scenario Outline: Get a project by id
    When a project with id "<project_id>" exists in the database
    And the user makes a "GET" request to "<endpoint>" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>

    Examples:
      | project_id      |  endpoint                          | response_code       |  response                                                                                     |  payload  |
      | 0000001         |  /api/1/project/0000001            | 200                 |  {"id": "ID", "repo": "http://test0000001.com", "scans": 0, "hookData": "", "hookType": ""}   |  empty    |
      | 0000001         |  /api/1/project/0000002            | 404                 |  {"error": {"msg": "Project 0000002 not found in database"}}                                  |  empty    |

  Scenario: Get projects
    When a project with id "0000001" exists in the database
    When the user makes a "GET" request to "/api/1/project/" endpoint with empty
    Then the api response code is 200
    And the api response payload is [{"repo": "http://test0000001.com", "scans": 0, "hookData": "", "hookType": ""}]
