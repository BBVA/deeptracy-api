
Feature: Create new scans
  The API should be able to create new scans

  Background: Database setup
    Given an empty system
    And a database ready to receive scans

  Scenario Outline: Create scan endpoint
    When the user makes a "POST" request to "/api/1/scan/" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>
    And <created> scans are in the database
    And <created> celery tasks of type start_scan are in the broker

    Examples:
      | payload                              | response_code | response                                                                                                                | created |
      | {"project_id":"123", "lang": "lang"} | 201           | {"project_id": "123", "lang": "lang", "state": "PENDING", "scan_analysis": [], "analysis_count": 0, "analysis_done": 0} | 1       |
      | {"project_id":"123"}                 | 201           | {"project_id": "123", "lang": null, "state": "PENDING", "scan_analysis": [], "analysis_count": 0, "analysis_done": 0}   | 1       |
      | {"lang": "lang"}                     | 400           | {"error": {"msg": "missing project_id"}}                                                                                | 0       |
      | {}                                   | 400           | {"error": {"msg": "invalid payload"}}                                                                                   | 0       |
