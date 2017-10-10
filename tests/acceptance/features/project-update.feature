Feature: Update projects
  The API should be able to update existing projects

  Background: Database setup
    Given an empty project table in database

  Scenario Outline: Updates an existing project
    When the user makes a "UPDATE" request to "/api/1/project/" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>

    Examples:
      | payload                      | response_code | response                                              |
      | {"repo":"http://google.com"} | 201           | {"id": "ID", "repo": "http://google.com", "scans": 0} |
      | {"repo":""}                  | 400           | {"error": {"msg": "missing repo"}}                    |
      | {}                           | 400           | {"error": {"msg": "invalid payload"}}                 |
