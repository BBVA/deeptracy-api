
Feature: Read scan vulnerabilities
  The API should be able to read scan vulnerabilities

  Background: Database setup
    Given an empty system

  Scenario Outline: Get  scan
    When a scan with id "<scan_id>" exists in the database
    And the user makes a "GET" request to "<endpoint>" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>

    Examples:
      | scan_id      |  endpoint                            | response_code       |  response                                                                                                              |  payload  |
      | 0000001      |  /api/1/scan/0000001/vulnerabilities | 200                 |  {"id": "ID", "repo": "http://test0000001.com", "scans": 0, "hookData": "", "hookType": "NONE", "authType": "PUBLIC"}  |  empty    |
      | 0000001      |  /api/1/scan/0000002/vulnerabilities | 404                 |  {"error": {"msg": "Project 0000002 not found in database"}}                                                           |  empty    |
