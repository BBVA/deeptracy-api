
Feature: Read scan vulnerabilities
  The API should be able to read scan vulnerabilities

  Background: Database setup
    Given an empty system

  Scenario Outline: Get  scan vulnerabilities
    Given a database ready to receive scans
    When the scan with id "<scan_id>" has vulnerabilities
    And the user makes a "GET" request to "<endpoint>" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>

    Examples:
      | scan_id      |  endpoint                                    | response_code       |  response                                                                                                                           |  payload  |
      | 0000001          |  /api/1/scan/0000001/vulnerabilities     | 200                 |  [{"id": "0000001", "scan_id": "0000001", "library": "tar", "version": "1.0.3", "severity": "1", "summary": "", "advisory": "" }] |  empty    |
      | 0000001          |  /api/1/scan/0000002/vulnerabilities     | 404                 |  {"error": {"msg": "Scan 0000002 not found in database"}}                                                                        |  empty    |
