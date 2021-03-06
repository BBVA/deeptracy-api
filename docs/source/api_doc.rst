API
===

Versions
********
The current API version is 1. You can add more versions and endpoints through the module :meth:`deeptracy_api.api`

Authorization
*************
The API is not protected with auth so every endpoint is publicly accessible

Date formats and timezone
*************************
Dates are always in the same format YYYY-MM-DDTHH:mm:ss. Valid dates are

* 2017-01-25T10:12:148
* 2016-11-05T18:12:148

When running the CME one of the configuration options is the **timezone**. Refer to :ref:`usage`

Endpoints
*********

.. toctree::
    api/project_blueprint
    api/scan_blueprint
    api/webhook_blueprint
    api/delta_blueprint
