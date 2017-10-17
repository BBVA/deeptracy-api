.. http:post:: /project/

   Creates a new project in database.

   **Example request**:

   .. sourcecode:: http

      POST /api/1/project HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
        "project_id": 00001,
        "repo": http://github.com/mirepo,
        "repo_auth": "auth",
        "repo_auth_type": "auth_type"
      }

   :statuscode 200: A new project inserted



.. http:get:: /project/

   Retrieves a list of all projects on database

   **Example request**:

   .. sourcecode:: http

      GET /api/1/project HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      [
        {
          "project_id": 00001,
          "repo": http://github.com/mirepo,
          "repo_auth": "auth",
          "repo_auth_type": "auth_type"
        },
        {
          "project_id": 00002,
          "repo": http://bitbucket.com/mirepo,
          "repo_auth": "auth",
          "repo_auth_type": "auth_type"
        }
      ]

   :statuscode 200: An array of projects


.. http:get:: /project/(int:project_id)

   The posts tagged with `tag` that the user (`user_id`) wrote.

   **Example request**:

   .. sourcecode:: http

      GET /api/1/project HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
        "project_id": 12345,
        "repo": http://github.com/mirepo,
        "repo_auth": "auth",
        "repo_auth_type": "auth_type"
      }

   :statuscode 200: A project
   :statuscode 404: Project not found


.. http:put:: /project/(int:project_id)

   Update an existing project with aditional data.

   **Example request**:

   .. sourcecode:: http

      PUT /api/1/project HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
        "project_id": 12345,
        "repo": http://github.com/mirepo,
        "repo_auth": "auth",
        "repo_auth_type": "auth_type"
      }

   :statuscode 200: A project with the updated data
   :statuscode 404: Project not found


.. http:delete:: /project/

   Delete a list of all projects on database

   **Example request**:

   .. sourcecode:: http

      DELETE /api/1/project HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      [
        {
          "project_id": 00001,
          "repo": http://github.com/mirepo,
          "repo_auth": "auth",
          "repo_auth_type": "auth_type"
        },
        {
          "project_id": 00002,
          "repo": http://bitbucket.com/mirepo,
          "repo_auth": "auth",
          "repo_auth_type": "auth_type"
        }
      ]

   :statuscode 200: An array of projects


.. http:delete:: /project/(int:project_id)

   Remove Requested Project

   **Example request**:

   .. sourcecode:: http

      DELETE /api/1/project HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 204 OK
      Vary: Accept
      Content-Type: no-content

   :statuscode 204: No content. Project removed successfully
   :statuscode 404: Project not found
