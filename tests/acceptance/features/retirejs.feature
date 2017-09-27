
Feature: Create new projects
  The API should be able to create new projects

  Scenario Outline: Create project endpoint
    Given there are no projects in the database
    When the user makes a "POST" request to "/project/" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>
    And the new project is created in the database if the response is 201

    Examples:
      | payload                      | response_code | response                                  |
      | {"repo":"http://google.com"} | 201           | {"id": "ID", "repo": "http://google.com"} |
      | {"repo":""}                  | 400           | {"error": {"msg": "invalid repo"}}        |
      | {}                           | 400           | {"error": {"msg": "invalid payload"}}     |
