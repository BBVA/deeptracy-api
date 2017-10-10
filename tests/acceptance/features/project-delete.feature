
Feature: Delete projects
  The API should be able to delete existing projects

  Background: Database setup
    Given an empty project table in database

  @only
  Scenario Outline: Delete project by id
    When a project with id "<project_id>" exists in the database
    And the user makes a "DELETE" request to "<endpoint>" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>
    And project with id "<project_id>" is not in the database

    Examples:
      | project_id               |  endpoint                          | response_code       |  response                                 |  payload       |
      | 0000001                  |  /api/1/project/0000002            | 404                 |  {"error": {"msg": "project not found"}}  |  empty         |
      | 0000001                  |  /api/1/project/0000001            | 204                 |  empty                                    |  empty         |

  Scenario Outline: Delete projects
    When the user makes a "DELETE" request to "<endpoint>" endpoint
    Then the api response code is <response_code>
    And the api response payload is <response>
    And table projects is empty

    Examples:
      |  endpoint                          | response_code       |   response   |
      |  /api/1/project/                   | 204                 |   empty      |
