
Feature: Read projects
  The API should be able to read existing projects

  Background: Database setup
    Given an empty project table in database

  Scenario Outline: Get a project by id
    When a project with id "<project_id>" exists in the database
    And the user makes a "GET" request to "<endpoint>" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>
    And project with id "<project_id>" is not in the database

    Examples:
      | project_id        |  endpoint                          | response_code       |  response                                                |  payload  |
      | "0000001"         |  /api/1/project/0000001            | 200                 |  {"id": "ID", "repo": "http://google.com", "scans": 0}   |  empty    |
      | "0000001"         |  /api/1/project/0000002            | 404                 |  {"error": {"msg": "project not found"}}                 |  empty    |

  Scenario Outline: Get projects
    When the user makes a "GET" request to "<endpoint>" endpoint
    Then the api response code is <response_code>
    And the api response payload is <response>

    Examples:
      | response_code | response                                                |
      | 200           | [{"id": "ID", "repo": "http://google.com", "scans": 0}] |

