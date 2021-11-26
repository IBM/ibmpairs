"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
from datetime import datetime
import json
import re
from typing import List, Any
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
import ibmpairs.common as common
import ibmpairs.constants as constants
import ibmpairs.client as client_module
import ibmpairs.query as query_module
import ibmpairs.messages as messages
from ibmpairs.logger import logger
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
#}}}

class QueryRegistrationReturn:
    #_analytics_uuid: str
    #_layer_id: str
    #_base_computation_id: str
    
    """
    An object to represent the return from an IBM Environmental Intelligence Suite (EIS) Query Registration call.

    :param analytics_uuid:              Analytics UUID.
    :type analytics_uuid:               str
    :param layer_id:                    EIS Dashboard Layer ID.
    :type layer_id:                     str
    :param base_computation_id:         Base Computation ID.
    :type base_computation_id:          str
    """
    
    #
    def __str__(self):

        """
        The method creates a string representation of the internal class structure.
        
        :returns: A string representation of the internal class structure.
        :rtype:   str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):

        """
        The method creates a dict representation of the internal class structure.
        
        :returns: A dict representation of the internal class structure.
        :rtype:   dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    def __init__(self,
                 analytics_uuid: str      = None,
                 layer_id: str            = None,
                 base_computation_id: str = None
                ):

        self._analytics_uuid = analytics_uuid
        self._layer_id = layer_id
        self._base_computation_id = base_computation_id

    def get_analytics_uuid(self):
        return self._analytics_uuid
        
    def set_analytics_uuid(self, analytics_uuid):
        self._analytics_uuid = common.check_str(analytics_uuid)
        
    def del_analytics_uuid(self):
        del self._analytics_uuid
        
    analytics_uuid = property(get_analytics_uuid, set_analytics_uuid, del_analytics_uuid)

    def get_layer_id(self):
        return self._layer_id
        
    def set_layer_id(self, layer_id):
        self._layer_id = common.check_str(layer_id)
        
    def del_layer_id(self):
        del self._layer_id
        
    layer_id = property(get_layer_id, set_layer_id, del_layer_id)

    def get_base_computation_id(self):
        return self._base_computation_id
        
    def set_base_computation_id(self, base_computation_id):
        self._base_computation_id = common.check_str(base_computation_id)
        
    def del_base_computation_id(self):
        del self._base_computation_id
        
    base_computation_id = property(get_base_computation_id, set_base_computation_id, del_base_computation_id)

    #
    def from_dict(query_registration_return_dict: Any):
      
        """
        Create a QueryRegistrationReturn object from a dictionary.
        
        :param query_registration_return_dict: A dictionary that contains the keys of a QueryRegistrationReturn.
        :type query_registration_return_dict:  Any             
        :rtype:                                ibmpairs.dashboard.QueryRegistrationReturn
        """
      
        analytics_uuid      = None
        layer_id            = None
        base_computation_id = None

        #common.check_dict(query_dict)
        if "analyticsUuid" in query_registration_return_dict:
            if query_registration_return_dict.get("analyticsUuid") is not None:
                analytics_uuid = common.check_str(query_registration_return_dict.get("analyticsUuid"))
        if "layerId" in query_registration_return_dict:
            if query_registration_return_dict.get("layerId") is not None:
                layer_id = common.check_str(query_registration_return_dict.get("layerId"))
        if "baseComputationId" in query_registration_return_dict:
            if query_registration_return_dict.get("baseComputationId") is not None:
                base_computation_id = common.check_str(query_registration_return_dict.get("baseComputationId"))
        return QueryRegistrationReturn(analytics_uuid      = analytics_uuid,
                                       layer_id            = layer_id,
                                       base_computation_id = base_computation_id
                                      )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        query_registration_return_dict: dict = {}
        if self._analytics_uuid is not None:
            query_registration_return_dict["analytics_uuid"] = self._analytics_uuid
        if self._layer_id is not None:
            query_registration_return_dict["layer_id"] = self._layer_id
        if self._base_computation_id is not None:
            query_registration_return_dict["base_computation_id"] = self._base_computation_id
        return query_registration_return_dict
        
    #
    def from_json(query_registration_return_json: Any):
        
        """
        Create an QueryRegistrationReturn object from json (dictonary or str).
        
        :param query_registration_return_json:  A json dictionary that contains the keys of an QueryRegistrationReturn or a string representation of a json dictionary.
        :type query_registration_return_json:   Any             
        :rtype:                                 ibmpairs.dashboard.QueryRegistrationReturn
        :raises Exception:                      if not a dictionary or a string.
        """

        if isinstance(query_registration_return_json, dict):
            query_registration_return = QueryRegistrationReturn.from_dict(query_registration_return_json)
        elif isinstance(query_registration_return_json, str):
            query_registration_return_dict = json.loads(query_registration_return_json)
            query_registration_return = QueryRegistrationReturn.from_dict(query_registration_return_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_registration_return_json), "query_registration_return_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_registration_return

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
def register_query(query,
                   query_name: str,
                   client: client_module.Client = None,
                   host: str                    = None
                  ):
                    
    """
    A method to register a PAIRS Query with the IBM Environmental Intelligence Suite (EIS) dashboard.

    :param query:        A PAIRS Query.
    :type query:         ibmpairs.query.Query or dict or str
    :param query_name:   A query name.
    :type query_name:    str
    :param client:       (Optional) An IBM PAIRS Client.
    :type client:        ibmpairs.client.Client
    :param host:         (Optional) A host for the registration.
    :type host:          str
    :returns:            A QueryRegistrationReturn and a Query.
    :rtype:              ibmpairs.dashboard.QueryRegistrationReturn, ibmpairs.query.Query
    :raises Exception:   If no client is provided or found Globally in the environment, 
                         if query type is not ibmpairs.query.Query or dict or str, 
                         if response is not 200, 
                         if object conversions fail.
    """        
                    
    if (host is None):
        host = constants.EIS_REGISTER_QUERY_URL

    if (client is None):
        client = common.set_client(input_client  = client,
                                   global_client = client_module.GLOBAL_PAIRS_CLIENT)

    client.set_host(host)

    if isinstance(query, query_module.Query):
        query_body = query.to_json()
    elif isinstance(query, dict):
        query_body = json.dumps(query)
    elif isinstance(query, str):
        query_body = query
    else:
        msg = messages.ERROR_QUERY_TYPE_NOT_RECOGNIZED.format(type(query))
        logger.error(msg)
        raise common.PAWException(msg)

    bodyJson = {"pairsPayload": query_body,
                "analyticsName": query_name }
    bodyJsonString = json.dumps(bodyJson)
    try:
        response = client.post(host,
                                body = bodyJsonString
                                )
        if response.status_code != 200:
            try:
                msg = json.dumps(response.json())
            except :
                msg = str(response.status_code)
            logger.error(msg)
            raise common.PAWException(msg)

        query_registration =  QueryRegistrationReturn.from_dict(response.json()[0])
        query_return = query_module.QueryResponse(id = query_registration.base_computation_id)
        if isinstance(query, query_module.Query):
            query_obj = query
        elif isinstance(query, dict):
            query_obj = query_module.query_from_dict(query)
        else: 
            query_obj = query_module.query_from_dict(query)
        query_obj.submit_response = query_return
        query_obj.id = query_registration.base_computation_id
        #query_result = query_module.QueryResult(client=client, query=query_obj, query_return=query_return)
        return query_registration, query_obj
    except Exception as ex:
        raise ex
    finally:
        # set client back to pointing at PAIRS
        client.set_host(constants.CLIENT_PAIRS_URL)


def add_dashboard_layer(query_registration: QueryRegistrationReturn,
                        name: str,
                        client         = None,
                        headers        = None,
                        host           = None,
                        style_properties = {'palette': {'COLOR_STEPS': [ { 'step': -1, 'rgba': [ 0, 0, 8, 255 ] },
                                                                         { 'step': 0, 'rgba': [ 11, 0, 251, 255 ] },
                                                                         { 'step': .2, 'rgba': [ 236, 0, 34, 255 ] },
                                                                         { 'step': .4, 'rgba': [ 250, 93, 7, 255 ] },
                                                                         { 'step': .6, 'rgba': [ 250, 249, 0, 255 ] },
                                                                         { 'step': .8, 'rgba': [ 0, 239, 0, 255 ] },
                                                                         { 'step': 1, 'rgba': [ 1, 49, 1, 255 ] } 
                                                                       ] 
                                                       },
                                            'unit': 'C',
                                            'isInterpolated': True,
                                            'extendMinimumColor': False,
                                            'extendMaximumColor': True,
                                            'invalidDataValue': -9999
                                           }
                        ):
    
    """
    A method to add a dashboard layer to the IBM Environmental Intelligence Suite (EIS) dashboard.

    :param query_registration: A query registration result from a successful EIS registration.
    :type query_registration:  ibmpairs.dashboard.QueryRegistrationReturn
    :param name:               A dashboard layer name.
    :type name:                str
    :param client:             (Optional) An IBM PAIRS Client.
    :type client:              ibmpairs.client.Client
    :param headers:            (Optional) Headers for the request.
    :type headers:             str
    :param host:               (Optional) A host for the registration.
    :type host:                str
    :param style_properties:   (Optional) A dictionary of style properties for the dashboard layer.
    :type style_properties:    dict
    :raises Exception:         If no client is provided or found Globally in the environment, 
                               if response is not 200.
    """ 

    if (headers is None):
        headers = constants.CLIENT_JSON_HEADER

    if (host is None):
        host = constants.PHOENIX_ADD_DASHBOARD_LAYER

    if (client is None):
        client = common.set_client(input_client  = client,
                                   global_client = client_module.GLOBAL_PAIRS_CLIENT)

    client.set_host(host)

    bodyJson = { 'VIEWERSHIP_ROLE' : 'ALL',
                 'CONFIG_BLOCK': { 'id': name,
                                   'modelRegistryId': None,
                                   'displayName': name,
                                   'provider': None,
                                   'layerType': 'grid',
                                   'isSelected': False,
                                   'isActive': False,
                                   'enableValidity': False,
                                   'lastUpdatedUtc': None,
                                   'coverageArea': 'Custom',
                                   'dataAttributes': { 'url': 'https://foundation.agtech.ibm.com/v2',
                                                       'uuid': query_registration.analytics_uuid 
                                                     },
                                  'menuIconUrl': None,
                                  'legendUrl': '',
                                  'styleProperties': style_properties
                                }
               }

    bodyJsonString = json.dumps(bodyJson)

    try:
        response = client.put(host,
                              body = bodyJsonString,
                              headers = headers
                             )
        if response.status_code != 200:
            try:
                msg = json.dumps(response.json())
            except :
                msg = str(response.status_code)
                logger.error(msg)
            raise common.PAWException(msg)
    except Exception as ex:
        raise ex
    finally:
        # set client back to pointing at PAIRS
        client.set_host(constants.CLIENT_PAIRS_URL)

