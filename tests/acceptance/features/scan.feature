
Feature: Create new scans
  The API should be able to create new scans

  Background: Database setup
    Given an empty system
    And a database ready to receive scans
  @demo
  Scenario Outline: Create scan
    When the user makes a "POST" request to "/api/1/scan/" endpoint with <payload>
    Then the api response code is <response_code>
    And the api response payload is <response>
    And <created> scans are in the database
    And <created> celery tasks of type prepare_scan are in the broker

    Examples:
      | payload                                     | response_code | response                                                                                                                                                                                     | created |
      | {"project_id":"123", "lang": "lang"}        | 201           | {"project_id": "123", "lang": "lang", "state": "PENDING", "branch": "master", "scan_analysis": [], "analysis_count": 0, "analysis_done": 0, "total_packages": 0, "total_vulnerabilities": 0} | 1       |
      | {"project_id":"123"}                        | 201           | {"project_id": "123", "lang": null, "state": "PENDING", "branch": "master", "scan_analysis": [], "analysis_count": 0, "analysis_done": 0, "total_packages": 0, "total_vulnerabilities": 0}   | 1       |
      | {"project_id":"123", "branch": "develop"}   | 201           | {"project_id": "123", "lang": null, "state": "PENDING", "branch": "develop", "scan_analysis": [], "analysis_count": 0, "analysis_done": 0, "total_packages": 0, "total_vulnerabilities": 0}   | 1       |
      | {"lang": "lang"}                            | 400           | {"error": {"msg": "missing project_id"}}                                                                                                                                                     | 0       |
      | {}                                          | 400           | {"error": {"msg": "invalid payload"}}                                                                                                                                                        | 0       |

  @only
  Scenario: Create scan with max allowed per period
    Given a scan created 3 mins ago exists in the database for a project
    And the ALLOWED_SCANS_PER_PERIOD config is set to 1
    And the ALLOWED_SCANS_CHECK_PERIOD config is set to 5
    When the user makes a "POST" request to "/api/1/scan/" endpoint with {"project_id":"123"}
    Then the api response code is 403


  @only
  Scenario Outline: Get Scans by Project Id
    When the user makes a "POST" request to "/api/1/scan/" endpoint with {"project_id":"123", "lang": "lang"}
    And  the user makes a "GET" request to "<endpoint>" endpoint with "empty"
    Then the api response code is <response_code>
    And the api response payload is <response>


    Examples:
      | endpoint                   | response_code | response                                                                                                                                                                                       |
      | /api/1/project/123/scans   | 200           | [{"analysis_count": 0, "analysis_done": 0, "lang": "lang", "branch": "master", "project_id": "123", "scan_analysis": [], "state": "PENDING", "total_packages": 0, "total_vulnerabilities": 0}] |
      | /api/1/project/400/scans   | 404           | {"error": {"msg": "Project 400 not found in database"}}                                                                                                                                        |
