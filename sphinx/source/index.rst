IBM Environmental Intelligence: Geospatial APIs SDK (ibmpairs)
===============================================================
   
Getting started
---------------

To get started using IBM Environmental Intelligence: Geospatial APIs SDK (ibmpairs), take a look at the tutorials.

What's new
----------

June 14, 2024
*************

- **3.1.3** Fix in AOI.get in :mod:`query`.

May 24, 2024
************

- **3.1.2** Added QueryJob.message in :mod:`query`. Fix (unit -> units) in DataLayer.display in :mod:`catalog`.

March 28, 2024
**************

- **3.1.1** Added constants.CLIENT_TOKEN_REFRESH_MESSAGE_APIC to improve accuracy of authenticaion retry attempt in the Client object in :mod:`client`. Fix in Query.point_data_as_dataframe in :mod:`query`.

March 11, 2024
**************

- **3.1.0** Added v4 support in :mod:`query`, :mod:`authentication` and :mod:`client`.

January 24, 2024
****************

- **3.0.9** Fix in Query.async_download in :mod:`query`.

January 22, 2024
****************

- **3.0.8** Added support for online queries that are automatically converted to batch in :mod:`query`.

January 5, 2024
***************

- **3.0.7** Fixes for add_dashboard_layer in :mod:`dashboard`.

December 15, 2023
*****************

- **3.0.6** Added additional csv format support. Fixes for Client init in :mod:`client`.

December 6, 2023
****************

- **3.0.5** Pinned version of Pillow. Optional verify fix for DataLayers.create in :mod:`catalog`.

November 8, 2023
****************

- **3.0.4** Fixes for AOIs.search and Query.download in :mod:`query`.

September 22, 2023
******************

- **3.0.3** Fixes to :mod:`dashboard`.

September 8, 2023
*****************

- **3.0.2** Added eis_get_auth_token() authentication into :mod:`authentication`.

September 5, 2023
*****************

- **3.0.1** Added catalog.search into :mod:`catalog`

August 15, 2023
***************

- **3.0.0** Added capability for /v3/ endpoints.

June 26, 2023
*************

- **0.2.10** Added new authentication options for /v3/ endpoints.

June 13, 2023
*************

- **0.2.8** Added an environment selector, added IBM API Connect authentication into :mod:`authentication`.

March 15, 2023
**************

- **0.2.7** Added a new default timeout in :mod:`client`.

January 18, 2023
****************

- **0.2.6** A fix to a data type in :mod:`paw`.

November 8, 2022
****************

- **0.2.5** A fix to allow existing script loggers in :mod:`config`.

September 12, 2022
******************

- **0.2.4** Added api_key as an alternative for authentication to :mod:`external.ibm` IBMCOSClient.

May 18, 2022
************

- **0.2.3** A maintenance fix to token refresh in the :mod:`authentication` OAuth2 class.

December 9, 2021
****************

- **0.2.2** Added :mod:`query` functionality- 'alias' attribute to query.QueryResponseData and 'expression' attribute to query.Filter. Please see Reference for more details.

December 1, 2021
****************

- **0.2.1** The SDK removed some mandatory requirements to improve the experience of setup on Windows.

December 1, 2021
*****************

- **0.2.0** The SDK now includes new :mod:`catalog`, :mod:`client`, :mod:`dashboard`, :mod:`query` and :mod:`upload` modules as well as updates to :mod:`authentication`. Please see Reference for more details.

February 24, 2021
*****************

- **0.1.3** :mod:`paw` now supports OAuth 2.0 authentication by use of a `Geospatial Analytics API key <https://ibm.github.io/Environmental-Intelligence-Suite/geospatial-api.html#authentication>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   installation
   tutorials/index
   reference/index
   examples
