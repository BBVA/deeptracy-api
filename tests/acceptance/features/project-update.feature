Feature: Update projects
  The API should be able to update existing projects

  Background: Database setup
    Given an empty project table in database

  Scenario Outline: Updates an existing project
    When a project with id "0000001" exists in the database
    When the user makes a "PUT" request to "/api/1/project/0000001" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>

    Examples:
      | payload                                                   | response_code | response                                                                                                          |
      | {"hook_type":"slack"}                                     | 201           | {"id": "ID", "repo": "http://test0000001.com", "scans": 0, "hookData": "", "hookType": "slack"}                   |
      | {"hook_type": "slack", "hook_data": "slack.com/0000001"}  | 201           | {"id": "ID", "repo": "http://test0000001.com", "scans": 0, "hookData": "slack.com/0000001", "hookType": "slack"}  |
      | {}                                                        | 400           | {"error": {"msg": "invalid payload"}}                                                                             |
