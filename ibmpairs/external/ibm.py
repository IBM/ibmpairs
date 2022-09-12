"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
import os
from typing import List, Any
from pathlib import Path
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
import ibmpairs.constants as constants
import ibmpairs.common as common
from ibmpairs.logger import logger
import ibmpairs.messages as messages
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import ibm_boto3
from ibm_botocore.client import Config as IBMConfig
from ibm_botocore.client import ClientError as IBMClientError
import json
import requests
#}}}


class IBMCOSHMACKeys(object):
    #_access_key_id: str
    #_secret_access_key: str
    
    """
    An object to represent IBM Cloud Object Storage (COS) HMAC Keys.

    :param access_key_id:     Access key ID
    :type access_key_id:      str
    :param secret_access_key: Secret access key
    :type secret_access_key:  str
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return_dict = self.to_dict()
        
        if ("access_key_id" in return_dict):
            return_dict["access_key_id"] = "********"
        if ("secret_access_key" in return_dict):
            return_dict["secret_access_key"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return_dict = self.to_dict()
        
        if ("access_key_id" in return_dict):
            return_dict["access_key_id"] = "********"
        if ("secret_access_key" in return_dict):
            return_dict["secret_access_key"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
                        
    #
    def __init__(self,
                 access_key_id: str     = None,
                 secret_access_key: str = None
                ) -> None:
                    
        self._access_key_id     = access_key_id
        self._secret_access_key = secret_access_key
        
    #    
    def get_access_key_id(self):
        return self._access_key_id

    #
    def set_access_key_id(self, access_key_id):
        self._access_key_id = common.check_str(access_key_id)
        
    #    
    def del_access_key_id(self): 
        del self._access_key_id

    #    
    access_key_id = property(get_access_key_id, set_access_key_id, del_access_key_id)
    
    #    
    def get_secret_access_key(self):
        return self._secret_access_key

    #
    def set_secret_access_key(self, secret_access_key):
        self._secret_access_key = common.check_str(secret_access_key)
        
    #    
    def del_secret_access_key(self): 
        del self._secret_access_key

    #    
    secret_access_key = property(get_secret_access_key, set_secret_access_key, del_secret_access_key)
    
    #    
    def from_dict(cos_hmac_keys_dict: Any):
      
        """
        Create an IBMCOSHMACKeys object from a dictionary.
        
        :param cos_hmac_keys_dict:    A dictionary that contains the keys of an IBMCOSHMACKeys.
        :type cos_hmac_keys_dict:     Any             
        :rtype:                       ibmpairs.external.ibm.IBMCOSHMACKeys
        :raises Exception:            If not a dictionary.
        """
        
        access_key_id     = None
        secret_access_key = None
        
        common.check_dict(cos_hmac_keys_dict)
        if "access_key_id" in cos_hmac_keys_dict:
            if cos_hmac_keys_dict.get("access_key_id") is not None:
                access_key_id = common.check_str(cos_hmac_keys_dict.get("access_key_id"))
        if "secret_access_key" in cos_hmac_keys_dict:
            if cos_hmac_keys_dict.get("secret_access_key") is not None:
                secret_access_key = common.check_str(cos_hmac_keys_dict.get("secret_access_key"))
        return IBMCOSHMACKeys(access_key_id       = access_key_id,
                              secret_access_key = secret_access_key
                             )

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        cos_hmac_keys_dict: dict = {}
        if self._access_key_id is not None:
            cos_hmac_keys_dict["access_key_id"] = self._access_key_id
        if self._secret_access_key is not None:
            cos_hmac_keys_dict["secret_access_key"] = self._secret_access_key
        return cos_hmac_keys_dict

    #
    def from_json(cos_hmac_keys_json: Any):
      
        """
        Create an IBMCOSHMACKeys object from json (dictonary or str).
        
        :param cos_hmac_keys_json:        A json dictionary that contains the keys of an IBMCOSHMACKeys or a string representation of a json dictionary.
        :type cos_hmac_keys_json:         Any             
        :rtype:                           ibmpairs.external.ibm.IBMCOSHMACKeys
        :raises Exception:                If not a dictionary or a string.
        """

        if isinstance(cos_hmac_keys_json, dict):
            cos_hmac_keys = IBMCOSHMACKeys.from_dict(cos_hmac_keys_json)
        elif isinstance(cos_hmac_keys_json, str):
            cos_hmac_keys_dict = json.loads(cos_hmac_keys_json)
            cos_hmac_keys = IBMCOSHMACKeys.from_dict(cos_hmac_keys_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(cos_hmac_keys_json), "cos_hmac_keys_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return cos_hmac_keys

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())


class IBMCOSServiceCredentials(object):
    #_api_key: str
    #_cos_hmac_keys: IBMCOSHMACKeys
    #_endpoints: str
    #_iam_api_key_description: str
    #_iam_api_key_name: str
    #_iam_role_crn: str
    #_iam_service_id_crn: str
    #_resource_instance_id: str
    
    """
    An object to represent IBM Cloud Object Storage (COS) Service Credentials.

    :param api_key:                 API Key
    :type api_key:                  str
    :param cos_hmac_keys:           IBM COS HMAC Keys
    :type cos_hmac_keys:            ibmpairs.external.ibm.IBMCOSHMACKeys
    :param endpoints:               IBM Cloud Enpoints URL
    :type endpoints:                str
    :param iam_api_key_description: IAM API Key Description
    :type iam_api_key_description:  str
    :param iam_api_key_name:        IAM API Key Name
    :type iam_api_key_name:         str
    :param iam_role_crn:            IAM Role CRN
    :type iam_role_crn:             str
    :param iam_service_id_crn:      IAM Service ID CRN
    :type iam_service_id_crn:       str
    :param resource_instance_id:    Resource Instance ID
    :type resource_instance_id:     str
    :raises Exception:              If IBMCOSHMACKeys type is unknown.
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return_dict = self.to_dict()
        
        if ("api_key" in return_dict):
            return_dict["api_key"] = "********"
        elif ("apikey" in return_dict):
            return_dict["apikey"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return_dict = self.to_dict()
        
        if ("api_key" in return_dict):
            return_dict["api_key"] = "********"
        elif ("apikey" in return_dict):
            return_dict["apikey"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
    
    #
    def __init__(self,
                 api_key: str                 = None,
                 cos_hmac_keys                = None,
                 endpoints: str               = None,
                 iam_api_key_description: str = None,
                 iam_api_key_name: str        = None,
                 iam_role_crn: str            = None,
                 iam_service_id_crn: str      = None,
                 resource_instance_id: str    = None
                ) -> None:
                    
        self._api_key                = api_key
        if isinstance(cos_hmac_keys, IBMCOSHMACKeys):
            self._cos_hmac_keys      = cos_hmac_keys
        elif isinstance(cos_hmac_keys, dict):
            cos_hmac_keys_object     = IBMCOSHMACKeys()
            self._cos_hmac_keys      = cos_hmac_keys_object.from_dict(cos_hmac_keys)
        elif isinstance(cos_hmac_keys, str):
            cos_hmac_keys_object     = IBMCOSHMACKeys()
            self._cos_hmac_keys      = cos_hmac_keys_object.from_json(cos_hmac_keys)
        elif cos_hmac_keys is None:
            cos_hmac_keys_object     = IBMCOSHMACKeys()
        else:
            msg = messages.ERROR_AUTHENTICATION_IBM_COS_HMAC_KEYS_UNKNOWN_TYPE.format(str(type(cos_hmac_keys)))
            logger.error(msg)
            raise common.PAWException(msg)
        self._endpoints               = endpoints
        self._iam_api_key_description = iam_api_key_description
        self._iam_api_key_name        = iam_api_key_name
        self._iam_role_crn            = iam_role_crn
        self._iam_service_id_crn      = iam_service_id_crn
        self._resource_instance_id    = resource_instance_id

    #    
    def get_api_key(self):
        return self._api_key

    #
    def set_api_key(self, api_key):
        self._api_key = common.check_str(api_key)
        
    #    
    def del_api_key(self): 
        del self._api_key

    #    
    api_key = property(get_api_key, set_api_key, del_api_key)
    
    #    
    def get_cos_hmac_keys(self):
        return self._cos_hmac_keys

    #
    def set_cos_hmac_keys(self, cos_hmac_keys):
        self._cos_hmac_keys = common.check_class(cos_hmac_keys, IBMCOSHMACKeys)
        
    #    
    def del_cos_hmac_keys(self): 
        del self._cos_hmac_keys

    #    
    cos_hmac_keys = property(get_cos_hmac_keys, set_cos_hmac_keys, del_cos_hmac_keys)

    #    
    def get_endpoints(self):
        return self._endpoints

    #
    def set_endpoints(self, endpoints):
        self._endpoints = common.check_str(endpoints)
        
    #    
    def del_endpoints(self): 
        del self._endpoints

    #    
    endpoints = property(get_endpoints, set_endpoints, del_endpoints)

    #    
    def get_iam_api_key_description(self):
        return self._iam_api_key_description

    #
    def set_iam_api_key_description(self, iam_api_key_description):
        self._iam_api_key_description = common.check_str(iam_api_key_description)
        
    #    
    def del_iam_api_key_description(self): 
        del self._iam_api_key_description

    #    
    iam_api_key_description = property(get_iam_api_key_description, set_iam_api_key_description, del_iam_api_key_description)

    #    
    def get_iam_api_key_name(self):
        return self._iam_api_key_name

    #
    def set_iam_api_key_name(self, iam_api_key_name):
        self._iam_api_key_name = common.check_str(iam_api_key_name)
        
    #    
    def del_iam_api_key_name(self): 
        del self._iam_api_key_name

    #    
    iam_api_key_name = property(get_iam_api_key_name, set_iam_api_key_name, del_iam_api_key_name)

    #    
    def get_iam_role_crn(self):
        return self._iam_role_crn

    #
    def set_iam_role_crn(self, iam_role_crn):
        self._iam_role_crn = common.check_str(iam_role_crn)
        
    #    
    def del_iam_role_crn(self): 
        del self._iam_role_crn

    #    
    iam_role_crn = property(get_iam_role_crn, set_iam_role_crn, del_iam_role_crn)

    #    
    def get_iam_service_id_crn(self):
        return self._iam_service_id_crn

    #
    def set_iam_service_id_crn(self, iam_service_id_crn):
        self._iam_service_id_crn = common.check_str(iam_service_id_crn)
        
    #    
    def del_iam_service_id_crn(self): 
        del self._iam_service_id_crn

    #    
    iam_service_id_crn = property(get_iam_service_id_crn, set_iam_service_id_crn, del_iam_service_id_crn)

    #    
    def get_resource_instance_id(self):
        return self._resource_instance_id

    #
    def set_resource_instance_id(self, resource_instance_id):
        self._resource_instance_id = common.check_str(resource_instance_id)

    #    
    def del_resource_instance_id(self): 
        del self._resource_instance_id

    #    
    resource_instance_id = property(get_resource_instance_id, set_resource_instance_id, del_resource_instance_id)
    
    #    
    def from_dict(cos_service_credentials_dict: Any):
      
        """
        Create an IBMCOSServiceCredentials object from a dictionary.
        
        :param cos_service_credentials_dict:    A dictionary that contains the keys of an IBMCOSServiceCredentials.
        :type cos_service_credentials_dict:     Any             
        :rtype:                                 ibmpairs.external.ibm.IBMCOSServiceCredentials
        :raises Exception:                      If not a dictionary.
        """
        
        api_key                 = None
        cos_hmac_keys           = None
        endpoints               = None
        iam_api_key_description = None
        iam_api_key_name        = None
        iam_role_crn            = None
        iam_service_id_crn      = None
        resource_instance_id    = None
        
        common.check_dict(cos_service_credentials_dict)
        if "apikey" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("apikey") is not None:
                api_key = common.check_str(cos_service_credentials_dict.get("apikey"))
        elif "api_key" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("api_key") is not None:
                api_key = common.check_str(cos_service_credentials_dict.get("api_key"))
        if "cos_hmac_keys" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("cos_hmac_keys") is not None:
                cos_hmac_keys = IBMCOSHMACKeys.from_dict(cos_service_credentials_dict.get("cos_hmac_keys"))
        if "endpoints" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("endpoints") is not None:
                endpoints = common.check_str(cos_service_credentials_dict.get("endpoints"))
        if "iam_apikey_description" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("iam_apikey_description") is not None:
                iam_api_key_description = common.check_str(cos_service_credentials_dict.get("iam_apikey_description"))
        elif "iam_api_key_description" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("iam_api_key_description") is not None:
                iam_api_key_description = common.check_str(cos_service_credentials_dict.get("iam_api_key_description"))
        if "iam_apikey_name" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("iam_apikey_name") is not None:
                iam_api_key_name = common.check_str(cos_service_credentials_dict.get("iam_apikey_name"))
        elif "iam_api_key_name" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("iam_api_key_name") is not None:
                iam_api_key_name = common.check_str(cos_service_credentials_dict.get("iam_api_key_name"))
        if "iam_role_crn" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("iam_role_crn") is not None:
                iam_role_crn = common.check_str(cos_service_credentials_dict.get("iam_role_crn"))
        if "iam_serviceid_crn" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("iam_serviceid_crn") is not None:
                iam_service_id_crn = common.check_str(cos_service_credentials_dict.get("iam_serviceid_crn"))
        elif "iam_service_id_crn" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("iam_service_id_crn") is not None:
                iam_service_id_crn = common.check_str(cos_service_credentials_dict.get("iam_service_id_crn"))
        if "resource_instance_id" in cos_service_credentials_dict:
            if cos_service_credentials_dict.get("resource_instance_id") is not None:
                resource_instance_id = common.check_str(cos_service_credentials_dict.get("resource_instance_id"))
        return IBMCOSServiceCredentials(api_key                 = api_key,
                                        cos_hmac_keys           = cos_hmac_keys,
                                        endpoints               = endpoints,
                                        iam_api_key_description = iam_api_key_description,
                                        iam_api_key_name        = iam_api_key_name,
                                        iam_role_crn            = iam_role_crn,
                                        iam_service_id_crn      = iam_service_id_crn,
                                        resource_instance_id    = resource_instance_id
                                       )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.   
                 
        :rtype:                     dict
        """
        
        cos_service_credentials_dict: dict = {}
        if self._api_key is not None:
            cos_service_credentials_dict["api_key"] = self._api_key
        if self._cos_hmac_keys is not None:
            cos_service_credentials_dict["cos_hmac_keys"] = common.class_to_dict(self._cos_hmac_keys, IBMCOSHMACKeys)
        if self._endpoints is not None:
            cos_service_credentials_dict["endpoints"] = self._endpoints
        if self._iam_api_key_description is not None:
            cos_service_credentials_dict["iam_api_key_description"] = self._iam_api_key_description
        if self._iam_api_key_name is not None:
            cos_service_credentials_dict["iam_api_key_name"] = self._iam_api_key_name
        if self._iam_role_crn is not None:
            cos_service_credentials_dict["iam_role_crn"] = self._iam_role_crn
        if self._iam_service_id_crn is not None:
            cos_service_credentials_dict["iam_service_id_crn"] = self._iam_service_id_crn
        if self._resource_instance_id is not None:
            cos_service_credentials_dict["resource_instance_id"] = self._resource_instance_id
        return cos_service_credentials_dict
    
    
    #
    def from_json(cos_service_credentials_json: Any):
        
        """
        Create an IBMCOSServiceCredentials object from json (dictonary or str).
        
        :param cos_service_credentials_json:  A json dictionary that contains the keys of an IBMCOSServiceCredentials or a string representation of a json dictionary.
        :type cos_service_credentials_json:   Any             
        :rtype:                               ibmpairs.external.ibm.IBMCOSServiceCredentials
        :raises Exception:                    If not a dictionary or a string.
        """

        if isinstance(cos_service_credentials_json, dict):
            cos_service_credentials = IBMCOSServiceCredentials.from_dict(cos_service_credentials_json)
        elif isinstance(cos_service_credentials_json, str):
            cos_service_credentials_dict = json.loads(cos_service_credentials_json)
            cos_service_credentials = IBMCOSServiceCredentials.from_dict(cos_service_credentials_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(cos_service_credentials_json), "cos_service_credentials_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return cos_service_credentials

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.            
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())


class IBMCOSFile(object):
    #_iam_service_id: str
    #_ibm_api_key_id: str
    #_endpoint: str
    #_ibm_auth_endpoint: str
    #_bucket: str
    #_file: str
    
    """
    An object to represent IBM Cloud Object Storage (COS) File entry returned by Watson Studio.

    :param iam_service_id:    IAM Service ID.
    :type iam_service_id:     str
    :param ibm_api_key_id:    IBM API Key ID.
    :type ibm_api_key_id:     str
    :param endpoint:          Endpoint.
    :type endpoint:           str
    :param ibm_auth_endpoint: IBM Authentication Endpoint.
    :type ibm_auth_endpoint:  str
    :param bucket:            Bucket name.
    :type bucket:             str
    :param file:              File.
    :type file:               str
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return_dict = self.to_dict()
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return_dict = self.to_dict()
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
    
    def __init__(self, 
                 iam_service_id: str    = None,
                 ibm_api_key_id: str    = None,
                 endpoint: str          = None,
                 ibm_auth_endpoint: str = None,
                 bucket: str            = None,
                 file: str              = None
                ):
        self._iam_service_id    = iam_service_id
        self._ibm_api_key_id    = ibm_api_key_id
        self._endpoint          = endpoint
        self._ibm_auth_endpoint = ibm_auth_endpoint
        self._bucket            = bucket
        self._file              = file
    
    #    
    def get_iam_service_id(self):
        return self._iam_service_id

    #
    def set_iam_service_id(self, iam_service_id):
        self._iam_service_id = common.check_str(iam_service_id)

    #    
    def del_iam_service_id(self): 
        del self._iam_service_id

    #    
    iam_service_id = property(get_iam_service_id, set_iam_service_id, del_iam_service_id)
    
    #    
    def get_ibm_api_key_id(self):
        return self._ibm_api_key_id

    #
    def set_ibm_api_key_id(self, ibm_api_key_id):
        self._ibm_api_key_id = common.check_str(ibm_api_key_id)

    #    
    def del_ibm_api_key_id(self): 
        del self._ibm_api_key_id

    #    
    ibm_api_key_id = property(get_ibm_api_key_id, set_ibm_api_key_id, del_ibm_api_key_id)

    #    
    def get_endpoint(self):
        return self._endpoint

    #
    def set_endpoint(self, endpoint):
        self._endpoint = common.check_str(endpoint)

    #    
    def del_endpoint(self): 
        del self._endpoint

    #    
    endpoint = property(get_endpoint, set_endpoint, del_endpoint)

    #    
    def get_ibm_auth_endpoint(self):
        return self._ibm_auth_endpoint

    #
    def set_ibm_auth_endpoint(self, ibm_auth_endpoint):
        self._ibm_auth_endpoint = common.check_str(ibm_auth_endpoint)

    #    
    def del_ibm_auth_endpoint(self): 
        del self._ibm_auth_endpoint

    #    
    ibm_auth_endpoint = property(get_ibm_auth_endpoint, set_ibm_auth_endpoint, del_ibm_auth_endpoint)
    
    #    
    def get_bucket(self):
        return self._bucket

    #
    def set_bucket(self, bucket):
        self._bucket = common.check_str(bucket)

    #    
    def del_bucket(self): 
        del self._bucket

    #    
    bucket = property(get_bucket, set_bucket, del_bucket)
    
    #    
    def get_file(self):
        return self._file

    #
    def set_file(self, file):
        self._file = common.check_str(file)

    #    
    def del_file(self): 
        del self._file

    #    
    file = property(get_file, set_file, del_file)

    #    
    def from_dict(cos_file_dict: Any):
      
        """
        Create an IBMCOSFile object from a dictionary.
        
        :param cos_file_dict:    A dictionary that contains the keys of an IBMCOSFile.
        :type cos_file_dict:     Any             
        :rtype:                  ibmpairs.external.ibm.IBMCOSFile
        :raises Exception:       If not a dictionary.
        """
        
        iam_service_id    = None
        ibm_api_key_id    = None
        endpoint          = None
        ibm_auth_endpoint = None
        bucket            = None
        file_             = None
        
        common.check_dict(cos_file_dict)
        if "iam_service_id" in cos_file_dict:
            if cos_file_dict.get("iam_service_id") is not None:
                iam_service_id = common.check_str(cos_file_dict.get("iam_service_id"))
        if "ibm_api_key_id" in cos_file_dict:
            if cos_file_dict.get("ibm_api_key_id") is not None:
                ibm_api_key_id = common.check_str(cos_file_dict.get("ibm_api_key_id"))
        if "endpoint" in cos_file_dict:
            if cos_file_dict.get("endpoint") is not None:
                endpoint = common.check_str(cos_file_dict.get("endpoint"))
        if "ibm_auth_endpoint" in cos_file_dict:
            if cos_file_dict.get("ibm_auth_endpoint") is not None:
                ibm_auth_endpoint = common.check_str(cos_file_dict.get("ibm_auth_endpoint"))
        if "bucket" in cos_file_dict:
            if cos_file_dict.get("bucket") is not None:
                bucket = common.check_str(cos_file_dict.get("bucket"))
        if "file" in cos_file_dict:
            if cos_file_dict.get("file") is not None:
                file_ = common.check_str(cos_file_dict.get("file"))
        return IBMCOSServiceCredentials(iam_service_id    = iam_service_id,
                                        ibm_api_key_id    = ibm_api_key_id,
                                        endpoint          = endpoint,
                                        ibm_auth_endpoint = ibm_auth_endpoint,
                                        bucket            = bucket,
                                        file              = file_
                                       )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        cos_file_dict: dict = {}
        if self._iam_service_id is not None:
            cos_file_dict["iam_service_id"] = self._iam_service_id
        if self._ibm_api_key_id is not None:
            cos_file_dict["ibm_api_key_id"] = self._ibm_api_key_id
        if self._endpoint is not None:
            cos_file_dict["endpoint"] = self._endpoint
        if self._ibm_auth_endpoint is not None:
            cos_file_dict["ibm_auth_endpoint"] = self._ibm_auth_endpoint
        if self._bucket is not None:
            cos_file_dict["bucket"] = self._bucket
        if self._file is not None:
            cos_file_dict["file"] = self._file
        return cos_file_dict
    
    #
    def from_json(cos_file_json: Any):
        
        """
        Create an IBMCOSFile object from json (dictonary or str).
        
        :param cos_file_json:  A json dictionary that contains the keys of an IBMCOSFile or a string representation of a json dictionary.
        :type cos_file_json:   Any             
        :rtype:                ibmpairs.external.ibm.IBMCOSFile
        :raises Exception:     If not a dictionary or a string.
        """

        if isinstance(cos_file_json, dict):
            cos_file = IBMCOSFile.from_dict(cos_file_json)
        elif isinstance(cos_file_json, str):
            cos_file_dict = json.loads(cos_file_json)
            cos_file = IBMCOSFile.from_dict(cos_file_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(cos_file_json), "cos_file_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return cos_file

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())


# place an import try at the start, make import try determine if this object can be used
class IBMCOSResource:
    #_resource: ibm_boto3.resource
    
    #_api_key: str
    #_resource_instance_id: str
    #_ibm_auth_endpoint: str
    #_endpoint: str
    
    """
    An object to wrap the creation of an ibm_boto3.resource.

    :param api_key:              API Key.
    :type api_key:               str
    :param resource_instance_id: Resource Instance ID.
    :type resource_instance_id:  str
    :param ibm_auth_endpoint:    IBM Authentication Endpoint.
    :type ibm_auth_endpoint:     str
    :param endpoint:             Endpoint.
    :type endpoint:              str
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return_dict = self.to_dict()
        
        if ("api_key" in return_dict):
            return_dict["api_key"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return_dict = self.to_dict()
        
        if ("api_key" in return_dict):
            return_dict["api_key"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
    
    def __init__(self, 
                 api_key: str                = None,
                 resource_instance_id: str   = None,
                 ibm_auth_endpoint: str      = None,
                 endpoint: str               = None
                ):
        self._api_key              = api_key
        self._resource_instance_id = resource_instance_id
        self._ibm_auth_endpoint    = ibm_auth_endpoint
        self._endpoint             = endpoint
        
        self.set_resource(self._api_key, 
                          self._resource_instance_id, 
                          self._ibm_auth_endpoint, 
                          self._endpoint
                         )
        
    #
    def get_api_key(self):
        return self._api_key

    #
    def set_api_key(self, api_key):
        self._api_key = common.check_str(api_key)

    #
    def del_api_key(self):
        del self._api_key

    #
    api_key = property(get_api_key, set_api_key, del_api_key)
    
    #    
    def get_resource_instance_id(self):
        return self._resource_instance_id

    #
    def set_resource_instance_id(self, resource_instance_id):
        self._resource_instance_id = common.check_str(resource_instance_id)

    #    
    def del_resource_instance_id(self): 
        del self._resource_instance_id

    #    
    resource_instance_id = property(get_resource_instance_id, set_resource_instance_id, del_resource_instance_id)
    
    #    
    def get_ibm_auth_endpoint(self):
        return self._ibm_auth_endpoint

    #
    def set_ibm_auth_endpoint(self, ibm_auth_endpoint):
        self._ibm_auth_endpoint = common.check_str(ibm_auth_endpoint)

    #    
    def del_ibm_auth_endpoint(self): 
        del self._ibm_auth_endpoint

    #    
    ibm_auth_endpoint = property(get_ibm_auth_endpoint, set_ibm_auth_endpoint, del_ibm_auth_endpoint)
    
    #    
    def get_endpoint(self):
        return self._endpoint

    #
    def set_endpoint(self, endpoint):
        self._endpoint = common.check_str(endpoint)

    #    
    def del_endpoint(self): 
        del self._endpoint

    #    
    endpoint = property(get_endpoint, set_endpoint, del_endpoint)
    
    #    
    def from_dict(ibm_cos_resource_dict: Any):
        
        """
        Create an IBMCOSResource object from a dictionary.
        
        :param ibm_cos_resource_dict:    A dictionary that contains the keys of an IBMCOSResource.
        :type ibm_cos_resource_dict:     Any             
        :rtype:                          ibmpairs.external.ibm.IBMCOSResource
        :raises Exception:               If not a dictionary.
        """
        
        api_key              = None
        resource_instance_id = None
        ibm_auth_endpoint    = None
        endpoint             = None
        
        common.check_dict(ibm_cos_resource_dict)
        if "api_key" in ibm_cos_resource_dict:
            if ibm_cos_resource_dict.get("api_key") is not None:
                api_key = common.check_str(ibm_cos_resource_dict.get("api_key"))
        if "resource_instance_id" in ibm_cos_resource_dict:
            if ibm_cos_resource_dict.get("resource_instance_id") is not None:
                resource_instance_id = common.check_str(ibm_cos_resource_dict.get("resource_instance_id"))
        if "ibm_auth_endpoint" in ibm_cos_resource_dict:
            if ibm_cos_resource_dict.get("ibm_auth_endpoint") is not None:
                ibm_auth_endpoint = common.check_str(ibm_cos_resource_dict.get("ibm_auth_endpoint"))
        if "endpoint" in ibm_cos_resource_dict:
            if ibm_cos_resource_dict.get("endpoint") is not None:
                endpoint = common.check_str(ibm_cos_resource_dict.get("endpoint"))
        return IBMCOSResource(api_key              = api_key,
                              resource_instance_id = resource_instance_id,
                              ibm_auth_endpoint    = ibm_auth_endpoint,
                              endpoint             = endpoint
                             )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        ibm_cos_resource_dict: dict = {}
        if self._api_key is not None:
            ibm_cos_resource_dict["api_key"] = self._api_key
        if self._resource_instance_id is not None:
            ibm_cos_resource_dict["resource_instance_id"] = self._resource_instance_id
        if self._ibm_auth_endpoint is not None:
            ibm_cos_resource_dict["ibm_auth_endpoint"] = self._ibm_auth_endpoint
        if self._endpoint is not None:
            ibm_cos_resource_dict["endpoint"] = self._endpoint
        return ibm_cos_resource_dict
        
    #
    def from_json(cos_resource_json: Any):
        
        """
        Create an IBMCOSResource object from json (dictonary or str).
        
        :param cos_resource_json:  A json dictionary that contains the keys of an IBMCOSResource or a string representation of a json dictionary.
        :type cos_resource_json:   Any             
        :rtype:                    ibmpairs.external.ibm.IBMCOSResource
        :raises Exception:         If not a dictionary or a string.
        """

        if isinstance(cos_resource_json, dict):
            cos_resource = IBMCOSResource.from_dict(cos_resource_json)
        elif isinstance(cos_resource_json, str):
            cos_resource_dict = json.loads(cos_resource_json)
            cos_resource = IBMCOSResource.from_dict(cos_resource_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(cos_resource_json), "cos_resource_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return cos_resource

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
    
    def set_resource(self,
                     api_key: str              = None, 
                     resource_instance_id: str = None, 
                     ibm_auth_endpoint: str    = None, 
                     endpoint: str             = None
                    ):
                        
        """
        Creates an ibm_boto3.resource from attributes in the object.
        
        :param api_key:               API Key.
        :type api_key:                str      
        :param resource_instance_id:  Resource Instance ID.
        :type resource_instance_id:   str     
        :param ibm_auth_endpoint:     IBM Authentication Endpoint.
        :type ibm_auth_endpoint:      str     
        :param endpoint:              Endpoint.
        :type endpoint:               str            
        :raises Exception:            if ibm_boto3.resource could not be created.
        """

        if api_key is None:
            api_key = self._api_key

        if resource_instance_id is None:
            resource_instance_id = self._resource_instance_id

        if ibm_auth_endpoint is None:
            ibm_auth_endpoint = self._ibm_auth_endpoint

        if endpoint is None:
            endpoint = self._endpoint

        try:
            cos_resource = ibm_boto3.resource("s3",
                                              ibm_api_key_id          = api_key,
                                              ibm_service_instance_id = resource_instance_id,
                                              ibm_auth_endpoint       = ibm_auth_endpoint,
                                              config                  = IBMConfig(signature_version="oauth"),
                                              endpoint_url            = endpoint
                                             )
        except IBMClientError as e:
            msg = messages.ERROR_IBM_COS_RESOURCE_COULD_NOT_BE_CREATED.format(e)
            logger.error(msg)
            raise common.PAWException(msg)

        self._resource = cos_resource


class IBMCOSClient:
    #_client: ibm_boto3.client
    
    #_api_key: str
    #_access_key_id: str
    #_secret_access_key: str
    #_resource_instance_id: str
    #_ibm_auth_endpoint: str
    #_endpoint: str
    
    """
    An object to wrap the creation of an ibm_boto3.client.

    :param api_key:              API Key.
    :type api_key:               str
    :param access_key_id:        Access Key ID.
    :type access_key_id:         str
    :param secret_access_key:    Secret Access Key.
    :type secret_access_key:     str
    :param resource_instance_id: Resource Instance ID.
    :type resource_instance_id:  str
    :param ibm_auth_endpoint:    IBM Authentication Endpoint.
    :type ibm_auth_endpoint:     str
    :param endpoint:             Endpoint.
    :type endpoint:              str
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return_dict = self.to_dict()
        
        if ("access_key_id" in return_dict):
            return_dict["access_key_id"] = "********"
        
        if ("secret_access_key" in return_dict):
            return_dict["secret_access_key"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return_dict = self.to_dict()
        
        if ("access_key_id" in return_dict):
            return_dict["access_key_id"] = "********"
        
        if ("secret_access_key" in return_dict):
            return_dict["secret_access_key"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
    
    def __init__(self, 
                 api_key: str                = None,
                 access_key_id: str          = None,
                 secret_access_key: str      = None,
                 resource_instance_id: str   = None,
                 ibm_auth_endpoint: str      = None,
                 endpoint: str               = None
                ):

        self._api_key              = api_key
        self._access_key_id        = access_key_id
        self._secret_access_key    = secret_access_key
        self._resource_instance_id = resource_instance_id
        self._ibm_auth_endpoint    = ibm_auth_endpoint
        self._endpoint             = endpoint
        
        self.set_client(self._api_key,
                        self._access_key_id,
                        self._secret_access_key,
                        self._resource_instance_id, 
                        self._ibm_auth_endpoint, 
                        self._endpoint
                       )
    
    #
    def get_api_key(self):
      return self._api_key

    #
    def set_api_key(self, api_key):
      self._api_key = common.check_str(api_key)

    #
    def del_api_key(self):
      del self._api_key

    #
    api_key = property(get_api_key, set_api_key, del_api_key)
    
    #
    def get_access_key_id(self):
        return self._access_key_id

    #
    def set_access_key_id(self, access_key_id):
        self._access_key_id = common.check_str(access_key_id)

    #
    def del_access_key_id(self):
        del self._access_key_id

    #
    access_key_id = property(get_access_key_id, set_access_key_id, del_access_key_id)
    
    #
    def get_secret_access_key(self):
      return self._secret_access_key

    #
    def set_secret_access_key(self, secret_access_key):
      self._secret_access_key = common.check_str(secret_access_key)

    #
    def del_secret_access_key(self):
      del self._secret_access_key

    #
    secret_access_key = property(get_secret_access_key, set_secret_access_key, del_secret_access_key)
    
    #    
    def get_resource_instance_id(self):
        return self._resource_instance_id

    #
    def set_resource_instance_id(self, resource_instance_id):
        self._resource_instance_id = common.check_str(resource_instance_id)

    #    
    def del_resource_instance_id(self): 
        del self._resource_instance_id

    #    
    resource_instance_id = property(get_resource_instance_id, set_resource_instance_id, del_resource_instance_id)
    
    #    
    def get_ibm_auth_endpoint(self):
        return self._ibm_auth_endpoint

    #
    def set_ibm_auth_endpoint(self, ibm_auth_endpoint):
        self._ibm_auth_endpoint = common.check_str(ibm_auth_endpoint)

    #    
    def del_ibm_auth_endpoint(self): 
        del self._ibm_auth_endpoint

    #    
    ibm_auth_endpoint = property(get_ibm_auth_endpoint, set_ibm_auth_endpoint, del_ibm_auth_endpoint)
    
    #    
    def get_endpoint(self):
        return self._endpoint

    #
    def set_endpoint(self, endpoint):
        self._endpoint = common.check_str(endpoint)

    #    
    def del_endpoint(self): 
        del self._endpoint

    #    
    endpoint = property(get_endpoint, set_endpoint, del_endpoint)
    
    #    
    def from_dict(cos_client_dict: Any):
        
        """
        Create an IBMCOSClient object from a dictionary.
        
        :param cos_client_dict:    A dictionary that contains the keys of an IBMCOSClient.
        :type cos_client_dict:     Any             
        :rtype:                    ibmpairs.external.ibm.IBMCOSClient
        :raises Exception:         If not a dictionary.
        """
        
        api_key              = None
        access_key_id        = None
        secret_access_key    = None
        resource_instance_id = None
        ibm_auth_endpoint    = None
        endpoint             = None
        
        common.check_dict(cos_client_dict)
        if "api_key" in cos_client_dict:
          if cos_client_dict.get("api_key") is not None:
            api_key = common.check_str(cos_client_dict.get("api_key"))
        if "access_key_id" in cos_client_dict:
            if cos_client_dict.get("access_key_id") is not None:
                access_key_id = common.check_str(cos_client_dict.get("access_key_id"))
        if "secret_access_key" in cos_client_dict:
            if cos_client_dict.get("secret_access_key") is not None:
                secret_access_key = common.check_str(cos_client_dict.get("secret_access_key"))
        if "resource_instance_id" in cos_client_dict:
            if cos_client_dict.get("resource_instance_id") is not None:
                resource_instance_id = common.check_str(cos_client_dict.get("resource_instance_id"))
        if "ibm_auth_endpoint" in cos_client_dict:
            if cos_client_dict.get("ibm_auth_endpoint") is not None:
                ibm_auth_endpoint = common.check_str(cos_client_dict.get("ibm_auth_endpoint"))
        if "endpoint" in cos_client_dict:
            if cos_client_dict.get("endpoint") is not None:
                endpoint = common.check_str(cos_client_dict.get("endpoint"))
        return IBMCOSClient(api_key              = api_key,
                            access_key_id        = access_key_id,
                            secret_access_key    = secret_access_key,
                            resource_instance_id = resource_instance_id,
                            ibm_auth_endpoint    = ibm_auth_endpoint,
                            endpoint             = endpoint
                           )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.   
                 
        :rtype:                     dict
        """
        
        cos_client_dict: dict = {}
        if self._api_key is not None:
            cos_client_dict["api_key"] = self._api_key
        if self._access_key_id is not None:
            cos_client_dict["access_key_id"] = self._access_key_id
        if self._secret_access_key is not None:
            cos_client_dict["secret_access_key"] = self._secret_access_key
        if self._resource_instance_id is not None:
            cos_client_dict["resource_instance_id"] = self._resource_instance_id
        if self._ibm_auth_endpoint is not None:
            cos_client_dict["ibm_auth_endpoint"] = self._ibm_auth_endpoint
        if self._endpoint is not None:
            cos_client_dict["endpoint"] = self._endpoint
        return cos_client_dict

    #
    def from_json(cos_client_json: Any):
        
        """
        Create an IBMCOSClient object from json (dictonary or str).
        
        :param cos_client_json:    A json dictionary that contains the keys of an IBMCOSClient or a string representation of a json dictionary.
        :type cos_client_json:     Any             
        :rtype:                    ibmpairs.external.ibm.IBMCOSClient
        :raises Exception:         If not a dictionary or a string.
        """

        if isinstance(cos_client_json, dict):
            cos_client = IBMCOSClient.from_dict(cos_client_json)
        elif isinstance(cos_client_json, str):
            cos_client_dict = json.loads(cos_client_json)
            cos_client = IBMCOSClient.from_dict(cos_client_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(cos_client_json), "cos_client_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return cos_client

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
      
    def set_client(self,
                   api_key              = None,
                   access_key_id        = None, 
                   secret_access_key    = None, 
                   resource_instance_id = None,
                   ibm_auth_endpoint    = None,
                   endpoint             = None,
                  ):
                    
        """
        Creates an ibm_boto3.client from attributes in the object.
        
        :param api_key:               API Key.
        :type api_key:                str
        :param access_key_id:         Access Key ID.
        :type access_key_id:          str      
        :param secret_access_key:     Secret Access Key.
        :type secret_access_key:      str     
        :param resource_instance_id:  Resource Instance ID.
        :type resource_instance_id:   str   
        :param ibm_auth_endpoint:     IBM Authentication Endpoint.
        :type ibm_auth_endpoint:      str     
        :param endpoint:              Endpoint.
        :type endpoint:               str            
        :raises Exception:            if ibm_boto3.client could not be created.
        """
        
        if api_key is None:
            api_key = self._api_key

        if access_key_id is None:
            access_key_id = self._access_key_id

        if secret_access_key is None:
            secret_access_key = self._secret_access_key

        if resource_instance_id is None:
            resource_instance_id = self._resource_instance_id

        if ibm_auth_endpoint is None:
            ibm_auth_endpoint = self._ibm_auth_endpoint

        if endpoint is None:
            endpoint = self._endpoint  
            
        connection_type = None
        
        if ((self._access_key_id is not None) and (self._secret_access_key is not None)):
            connection_type = "s3v4"
        else:
            connection_type = "oauth"

        try:
            cos_client = ibm_boto3.client("s3", 
                                          ibm_api_key_id          = api_key,
                                          aws_access_key_id       = access_key_id,
                                          aws_secret_access_key   = secret_access_key,
                                          ibm_service_instance_id = resource_instance_id,
                                          ibm_auth_endpoint       = ibm_auth_endpoint,
                                          config                  = IBMConfig(signature_version = connection_type), 
                                          endpoint_url            = endpoint
                                         )
        except:
            msg = messages.ERROR_IBM_COS_CLIENT_COULD_NOT_BE_CREATED
            logger.error(msg)
            raise common.PAWException(msg)

        self._client = cos_client


class IBMCOSBucket(object):
    #_cos_resource: IBMCOSResource
    #_cos_client: IBMCOSClient
    #_api_key: str
    #_resource_instance_id: str
    #_ibm_auth_endpoint: str
    #_endpoint: str
    #_bucket: str
    #_access_key_id: str
    #_secret_access_key: str
    #_ibm_cos_service_credentials: IBMCOSServiceCredentials
    #_ibm_cos_file: IBMCOSFile
    
    """
    An object to represent an IBM Cloud Object Storage (COS) bucket.

    :param api_key:                     API Key.
    :type api_key:                      str
    :param resource_instance_id:        Resource Instance ID.
    :type resource_instance_id:         str
    :param ibm_auth_endpoint:           IBM Authentication Endpoint.
    :type ibm_auth_endpoint:            str
    :param endpoint:                    Endpoint.
    :type endpoint:                     str
    :param bucket:                      Bucket name.
    :type bucket:                       str
    :param access_key_id:               Access Key ID.
    :type access_key_id:                str
    :param secret_access_key:           Secret Access Key.
    :type secret_access_key:            str
    :param ibm_cos_service_credentials: An IBMCOSServiceCredentials instance.
    :type ibm_cos_service_credentials:  ibmpairs.external.ibm.IBMCOSServiceCredentials
    :param ibm_cos_file:                An IBMCOSFile instance.
    :type ibm_cos_file:                 ibmpairs.external.ibm.IBMCOSFile
    :raises Exception:                  If a client could not be found or created, 
                                        if a resource could not be found or created, 
                                        if ibm_cos_service_credentials provided but not valid, 
                                        if ibm_cos_file provided but not valid.
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
    
    #
    def __init__(self, 
                 api_key: str                                          = None,
                 resource_instance_id: str                             = None,
                 ibm_auth_endpoint: str                                = None,
                 endpoint: str                                         = None,
                 bucket: str                                           = None,
                 access_key_id: str                                    = None,
                 secret_access_key: str                                = None,
                 ibm_cos_service_credentials: IBMCOSServiceCredentials = None,
                 ibm_cos_file: IBMCOSFile                              = None,
                ):
        self._api_key              = api_key
        self._resource_instance_id = resource_instance_id
        self._ibm_auth_endpoint    = ibm_auth_endpoint
        # If the endpoint is a url, assign if it is a reference code e.g. 'us-geo' search endpoints url for the endpoint.
        if endpoint is not None:
            if endpoint.startswith("https://"):
                self._endpoint     = endpoint
            else:
                ep = get_cos_endpoint_by_region(endpoint)
                if ep is not None:
                    self._endpoint = ep
                else:
                    msg = messages.INFO_IBM_COS_BUCKET_NO_ENDPOINT.format("https://" + 
                                                                              constants.IBM_CLOUD_OBJECT_STORE_CONTROL_URL +
                                                                              constants.IBM_CLOUD_OBJECT_STORE_ENDPOINTS)
                    logger.info(msg)
        else:
            self._endpoint         = endpoint
        self._bucket               = bucket
        self._access_key_id        = access_key_id
        self._secret_access_key    = secret_access_key

        if ibm_cos_service_credentials is not None:
            # If assignation is None in the object attributes and ibm_cos_service_credentials is present, assign from one object to the other.
            if isinstance(ibm_cos_service_credentials, str):
                try:
                    ibm_cos_service_credentials = ibm_cos_service_credentials_from_json(ibm_cos_service_credentials)
                except:
                    msg = messages.ERROR_IBM_COS_BUCKET_UNKNOWN_SERVICE_CREDENTIALS_FORMAT.format('str', ibm_cos_service_credentials)
                    logger.error(msg)
                    raise common.PAWException(msg)

            if isinstance(ibm_cos_service_credentials, dict):
                try:
                    ibm_cos_service_credentials = ibm_cos_service_credentials_from_dict(ibm_cos_service_credentials)
                except:
                    msg = messages.ERROR_IBM_COS_BUCKET_UNKNOWN_SERVICE_CREDENTIALS_FORMAT.format('dict', ibm_cos_service_credentials)
                    logger.error(msg)
                    raise common.PAWException(msg)

            if isinstance(ibm_cos_service_credentials, IBMCOSServiceCredentials):
                if ((self._api_key is None) and (ibm_cos_service_credentials.api_key is not None)):
                    self._api_key = ibm_cos_service_credentials.api_key
                if ((self._resource_instance_id is None) and (ibm_cos_service_credentials.resource_instance_id is not None)):
                    self._resource_instance_id = ibm_cos_service_credentials.resource_instance_id
                if ((self._access_key_id is None) and (ibm_cos_service_credentials.cos_hmac_keys.access_key_id is not None)):
                    self._access_key_id = ibm_cos_service_credentials.cos_hmac_keys.access_key_id
                if ((self._secret_access_key is None) and (ibm_cos_service_credentials.cos_hmac_keys.secret_access_key is not None)):
                    self._secret_access_key = ibm_cos_service_credentials.secret_access_key
            else:
                msg = messages.ERROR_IBM_COS_BUCKET_UNKNOWN_SERVICE_CREDENTIALS_FORMAT.format(str(type(ibm_cos_service_credentials)), ibm_cos_service_credentials)
                logger.error(msg)
                raise common.PAWException(msg)
            
        if ibm_cos_file is not None:
            # If assignation is None in the object attributes and ibm_cos_file is present, assign from one object to the other.
            if isinstance(ibm_cos_file, str):
                try:
                    ibm_cos_file = ibm_cos_file_from_json(ibm_cos_file)
                except:
                    msg = messages.ERROR_IBM_COS_BUCKET_UNKNOWN_COS_FILE_FORMAT.format('str', ibm_cos_file)
                    logger.error(msg)
                    raise common.PAWException(msg)
            
            if isinstance(ibm_cos_file, dict):
                try:
                    ibm_cos_file = ibm_cos_file_from_dict(ibm_cos_file)
                except:
                    msg = messages.ERROR_IBM_COS_BUCKET_UNKNOWN_COS_FILE_FORMAT.format('dict', ibm_cos_file)
                    logger.error(msg)
                    raise common.PAWException(msg)
        
            if isinstance(ibm_cos_file, IBMCOSFile):
                if ((self._ibm_auth_endpoint is None) and (ibm_cos_file.ibm_auth_endpoint is not None)):
                    self._ibm_auth_endpoint = ibm_cos_file.ibm_auth_endpoint
                if ((self._endpoint is None) and (ibm_cos_file.endpoint is not None)):
                    self._endpoint = ibm_cos_file.endpoint
                if ((self._bucket is None) and (ibm_cos_file.bucket is not None)):
                    self._bucket = ibm_cos_file.bucket
            else:
                msg = messages.ERROR_IBM_COS_BUCKET_UNKNOWN_COS_FILE_FORMAT.format(str(type(ibm_cos_file)), ibm_cos_file)
                logger.error(msg)
                raise common.PAWException(msg)
        
        # If ibm_auth_endpoint remains unset by the user or in ibm_cos_file in the object, pull from endpoints().
        if ibm_auth_endpoint is None:
            self._ibm_auth_endpoint = get_cos_auth_endpoint()
            
        if ((self._api_key is not None) and (self._resource_instance_id is not None) and (self._ibm_auth_endpoint is not None) and (self._endpoint is not None)):

            self._cos_resource = IBMCOSResource(api_key              = self._api_key,
                                                resource_instance_id = self._resource_instance_id,
                                                ibm_auth_endpoint    = self._ibm_auth_endpoint,
                                                endpoint             = self._endpoint
                                               )
            
            self._cos_client = IBMCOSClient(api_key              = self._api_key,
                                            resource_instance_id = self._resource_instance_id,
                                            ibm_auth_endpoint    = self._ibm_auth_endpoint,
                                            endpoint             = self._endpoint
                                           )
        
        if ((self._access_key_id is not None) and (self._secret_access_key is not None) and (self._resource_instance_id is not None) and (self._ibm_auth_endpoint is not None) and (self._endpoint is not None)):

            self._cos_client = IBMCOSClient(access_key_id        = self._access_key_id,
                                            secret_access_key    = self._secret_access_key,
                                            resource_instance_id = self._resource_instance_id,
                                            ibm_auth_endpoint    = self._ibm_auth_endpoint,
                                            endpoint             = self._endpoint
                                           )
        

    #
    def get_api_key(self):
        return self._api_key

    #
    def set_api_key(self, api_key):
        self._api_key = common.check_str(api_key)

    #
    def del_api_key(self):
        del self._api_key

    #
    api_key = property(get_api_key, set_api_key, del_api_key)
    
    #    
    def get_resource_instance_id(self):
        return self._resource_instance_id

    #
    def set_resource_instance_id(self, resource_instance_id):
        self._resource_instance_id = common.check_str(resource_instance_id)

    #    
    def del_resource_instance_id(self): 
        del self._resource_instance_id

    #    
    resource_instance_id = property(get_resource_instance_id, set_resource_instance_id, del_resource_instance_id)
    
    #    
    def get_ibm_auth_endpoint(self):
        return self._ibm_auth_endpoint

    #
    def set_ibm_auth_endpoint(self, ibm_auth_endpoint):
        self._ibm_auth_endpoint = common.check_str(ibm_auth_endpoint)

    #    
    def del_ibm_auth_endpoint(self): 
        del self._ibm_auth_endpoint

    #    
    ibm_auth_endpoint = property(get_ibm_auth_endpoint, set_ibm_auth_endpoint, del_ibm_auth_endpoint)
    
    #    
    def get_endpoint(self):
        return self._endpoint

    #
    def set_endpoint(self, endpoint):
        self._endpoint = common.check_str(endpoint)

    #    
    def del_endpoint(self): 
        del self._endpoint

    #    
    endpoint = property(get_endpoint, set_endpoint, del_endpoint)
    
    #    
    def get_bucket(self):
        return self._bucket

    #
    def set_bucket(self, bucket):
        self._bucket = common.check_str(bucket)

    #    
    def del_bucket(self): 
        del self._bucket

    #    
    bucket = property(get_bucket, set_bucket, del_bucket)
    
    #    
    def get_access_key_id(self):
        return self._access_key_id

    #
    def set_access_key_id(self, access_key_id):
        self._access_key_id = common.check_str(access_key_id)

    #    
    def del_access_key_id(self): 
        del self._access_key_id

    #    
    access_key_id = property(get_access_key_id, set_access_key_id, del_access_key_id)
    
    #    
    def get_secret_access_key(self):
        return self._secret_access_key

    #
    def set_secret_access_key(self, secret_access_key):
        self._secret_access_key = common.check_str(secret_access_key)

    #    
    def del_secret_access_key(self): 
        del self._secret_access_key

    #    
    secret_access_key = property(get_secret_access_key, set_secret_access_key, del_secret_access_key)

    #
    def set_resource(self, 
                     api_key: str              = None,
                     resource_instance_id: str = None,
                     ibm_auth_endpoint: str    = None,
                     endpoint: str             = None,
                     resource                  = None
                    ):
                        
        """
        Populates the self._cos_resource attribute. If a resource is provided, the method uses this, if not, a new IBMCOSResource is created.
        
        :param api_key:               API Key.
        :type api_key:                str      
        :param resource_instance_id:  Resource Instance ID.
        :type resource_instance_id:   str     
        :param ibm_auth_endpoint:     IBM Authentication Endpoint.
        :type ibm_auth_endpoint:      str     
        :param endpoint:              Endpoint.
        :type endpoint:               str     
        :param resource:              An existing IBMCOSResource.
        :type resource:               ibmpairs.external.ibm.IBMCOSResource       
        :raises Exception:            If ibm_boto3.resource could not be created.
        """
        
        if api_key is not None:
            self._api_key = api_key
        if resource_instance_id is not None:
            self._resource_instance_id = resource_instance_id
        if ibm_auth_endpoint is not None:
            self._ibm_auth_endpoint = ibm_auth_endpoint
        if endpoint is not None:
            self._endpoint = endpoint
        
        if (resource is not None):
            if isinstance(resource, IBMCOSResource):
                self._cos_resource = resource
        else:
            self._cos_resource = IBMCOSResource(api_key              = self._api_key,
                                                resource_instance_id = self._resource_instance_id,
                                                ibm_auth_endpoint    = self._ibm_auth_endpoint,
                                                endpoint             = self._endpoint
                                               )

    #
    def set_client(self,
                   access_key_id: str        = None,
                   secret_access_key: str    = None,
                   resource_instance_id: str = None,
                   ibm_auth_endpoint: str    = None,
                   endpoint: str             = None,
                   client                    = None
                  ):
                    
        """
        Populates the self._cos_client attribute. If a client is provided, the method uses this, if not, a new IBMCOSClient is created.
        
        :param access_key_id:         Access Key ID.
        :type access_key_id:          str      
        :param secret_access_key:     Secret Access Key.
        :type secret_access_key:      str     
        :param resource_instance_id:  Resource Instance ID.
        :type resource_instance_id:   str   
        :param ibm_auth_endpoint:     IBM Authentication Endpoint.
        :type ibm_auth_endpoint:      str     
        :param endpoint:              Endpoint.
        :type endpoint:               str       
        :param client:                An existing IBMCOSClient.
        :type client:                 ibmpairs.external.ibm.IBMCOSClient
        :raises Exception:            If ibm_boto3.client could not be created.
        """
                    
        if access_key_id is not None:
            self._access_key_id = access_key_id
        if secret_access_key is not None:
            self._secret_access_key = secret_access_key
        if resource_instance_id is not None:
            self._resource_instance_id = resource_instance_id
        if ibm_auth_endpoint is not None:
            self._ibm_auth_endpoint = ibm_auth_endpoint
        if endpoint is not None:
            self._endpoint = endpoint
        
        if (client is not None):
            if isinstance(client, IBMCOSClient):
                self._cos_client = client
        else:
            self._cos_client = IBMCOSClient(access_key_id        = self._access_key_id,
                                            secret_access_key    = self._secret_access_key,
                                            resource_instance_id = self._resource_instance_id,
                                            ibm_auth_endpoint    = self._ibm_auth_endpoint,
                                            endpoint             = self._endpoint
                                           )
    
    #    
    def from_dict(cos_bucket_dict: Any):
        
        """
        Create an IBMCOSBucket object from a dictionary.
        
        :param cos_bucket_dict:    A dictionary that contains the keys of an IBMCOSBucket.
        :type cos_bucket_dict:     Any             
        :rtype:                    ibmpairs.external.ibm.IBMCOSBucket
        :raises Exception:         If not a dictionary.
        """
        
        api_key              = None
        resource_instance_id = None
        ibm_auth_endpoint    = None
        endpoint             = None
        bucket               = None
        access_key_id        = None
        secret_access_key    = None
        
        common.check_dict(cos_bucket_dict)
        if "api_key" in cos_bucket_dict:
            if cos_bucket_dict.get("api_key") is not None:
                api_key = common.check_str(cos_bucket_dict.get("api_key"))
        if "resource_instance_id" in cos_bucket_dict:
            if cos_bucket_dict.get("resource_instance_id") is not None:
                resource_instance_id = common.check_str(cos_bucket_dict.get("resource_instance_id"))
        if "ibm_auth_endpoint" in cos_bucket_dict:
            if cos_bucket_dict.get("ibm_auth_endpoint") is not None:
                ibm_auth_endpoint = common.check_str(cos_bucket_dict.get("ibm_auth_endpoint"))
        if "endpoint" in cos_bucket_dict:
            if cos_bucket_dict.get("endpoint") is not None:
                endpoint = common.check_str(cos_bucket_dict.get("endpoint"))
        if "bucket" in cos_bucket_dict:
            if cos_bucket_dict.get("bucket") is not None:
                bucket = common.check_str(cos_bucket_dict.get("bucket"))
        if "access_key_id" in cos_bucket_dict:
            if cos_bucket_dict.get("access_key_id") is not None:
                access_key_id = common.check_str(cos_bucket_dict.get("access_key_id"))
        if "secret_access_key" in cos_bucket_dict:
            if cos_bucket_dict.get("secret_access_key") is not None:
                secret_access_key = common.check_str(cos_bucket_dict.get("secret_access_key"))
        return IBMCOSBucket(api_key              = api_key,
                            resource_instance_id = resource_instance_id,
                            ibm_auth_endpoint    = ibm_auth_endpoint,
                            endpoint             = endpoint,
                            bucket               = bucket,
                            access_key_id        = access_key_id,
                            secret_access_key    = secret_access_key
                           )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype:                     dict
        """
        
        cos_bucket_dict: dict = {}
        if self._api_key is not None:
            cos_bucket_dict["api_key"] = self._api_key
        if self._resource_instance_id is not None:
            cos_bucket_dict["resource_instance_id"] = self._resource_instance_id
        if self._ibm_auth_endpoint is not None:
            cos_bucket_dict["ibm_auth_endpoint"] = self._ibm_auth_endpoint
        if self._endpoint is not None:
            cos_bucket_dict["endpoint"] = self._endpoint
        if self._bucket is not None:
            cos_bucket_dict["bucket"] = self._bucket
        if self._access_key_id is not None:
            cos_bucket_dict["access_key_id"] = self._access_key_id
        if self._secret_access_key is not None:
            cos_bucket_dict["secret_access_key"] = self._secret_access_key
        return cos_bucket_dict

    #
    def from_json(cos_bucket_json: Any):
        
        """
        Create an IBMCOSBucket object from json (dictonary or str).
        
        :param cos_client_json:    A json dictionary that contains the keys of an IBMCOSBucket or a string representation of a json dictionary.
        :type cos_client_json:     Any             
        :rtype:                    ibmpairs.external.ibm.IBMCOSBucket
        :raises Exception:         If not a dictionary or a string.
        """

        if isinstance(cos_bucket_json, dict):
            cos_bucket = IBMCOSBucket.from_dict(cos_bucket_json)
        elif isinstance(cos_bucket_json, str):
            cos_bucket_dict = json.loads(cos_bucket_json)
            cos_bucket = IBMCOSBucket.from_dict(cos_bucket_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(cos_bucket_json), "cos_bucket_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return cos_bucket

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
        
    #
    def get(self,
            key: str,
            bucket: str = None
           ):

        """
        Gets an object from a bucket.
        
        :param key:             Name of object in the bucket.
        :type key:              str 
        :param bucket:          (Optional) name of the bucket.
        :type bucket:           str 
        :raises Exception:      If operation fails.
        """
        
        if (bucket is None):
            bucket = self._bucket
        
        if self._cos_client is None:
            msg = messages.ERROR_NO_IBM_COS_CLIENT
            logger.error(msg)
            raise common.PAWException(msg)

        try:
            bucket_object = self._cos_client._client.get_object(Bucket = self._bucket, 
                                                                Key = key)
        except Exception as ex:
            msg = messages.ERROR_IBM_COS_ERROR.format('GET', self._bucket, key, ex)
            logger.info(msg)
            raise common.PAWException(msg)

        return bucket_object

    #
    def upload(self, 
               file_name: str, 
               key: str      = None,
               bucket: str   = None
              ):
        """
        Stores the local file `file_name` in bucket as `key`. 
        Will raise an exception of `file_name` if the file does not exist.
        
        :param file_name:   Name of (data) file to ingest.
        :type file_name:    str
        :param key:         (Optional) name of file in bucket. `file_name`
                            without parent directories will be used if not
                            provided.
        :type key:          str
        :param bucket:      (Optional) name of the bucket.
        :type bucket:       str
        :raises Exception:  If upload fails with an IBMClientError, 
                            if upload operation fails.
        """
                
        if self._cos_resource is None:
            msg = messages.ERROR_NO_IBM_COS_RESOURCE
            logger.error(msg)
            raise common.PAWException(msg)
        
        try:
            file_name = Path(file_name)
                
            if (key is None):
                key = file_name.name
                
            if (bucket is None):
                bucket = self._bucket

            # Set 50 MB chunks
            part_size = constants.IBM_COS_UPLOAD_PART_SIZE

            # Set threshold to 50 MB
            file_threshold = constants.IBM_COS_UPLOAD_FILE_THRESHOLD

            # Set the transfer threshold and chunk size
            transfer_config = ibm_boto3.s3.transfer.TransferConfig(multipart_threshold = file_threshold,
                                                                   multipart_chunksize = part_size
            )

            # The upload_fileobj method will automatically execute a multi-part upload
            # in part_size chunks for all files over file_threshold
            msg = messages.DEBUG_IBM_COS_UPLOADING.format(file_name.name, key, bucket)
            logger.debug(msg)
            
            with open(file_name, "rb") as f:
                self._cos_resource._resource.Object(bucket, key).upload_fileobj(
                    Fileobj = f,
                    Config = transfer_config
                )

            msg = messages.DEBUG_IBM_COS_UPLOAD_SUCCESS.format(file_name.name, key, bucket)
            logger.debug(msg)
            
        except IBMClientError as e:
            msg = messages.ERROR_IBM_COS_UPLOAD_CLIENT_ERROR.format(file_name, e)
            logger.error(msg)
            raise common.PAWException(msg)
        except Exception as e:
            msg = messages.ERROR_IBM_COS_UPLOAD_ERROR.format(file_name, e)
            logger.error(msg)
            raise common.PAWException(msg)
            
    #
    def download(self,
                 key: str,
                 download_path = 'download',
                 bucket: str   = None
                ):
        """
        Downloads the `key` in bucket to local. 
        Will raise an exception of `file_name` if the file does not exist.
        
        :param file_name:   Name of (data) file to download.
        :type file_name:    str
        :param key:         (Optional) name of the file in the bucket.
        :type key:          str
        :param bucket:      (Optional) name of the bucket.
        :type bucket:       str
        :raises Exception:  If upload fails with an IBMClientError, 
                            if upload operation fails.
        """
                
        if self._cos_resource is None:
            msg = messages.ERROR_NO_IBM_COS_RESOURCE
            logger.error(msg)
            raise common.PAWException(msg)
        
        try:
            # TODO:
            # Need to handle case where key has / by grabbing final name after last /.
                
            if (bucket is None):
                bucket = self._bucket
            
            # Check download_path exists as relative, fixed or create.
            if os.path.exists(os.path.join(os.getcwd(), download_path)):
                download_path = os.path.join(os.getcwd(), download_path) + '/'
            elif os.path.exists(download_path):
                download_path = download_path + '/'
            else:
                msg = messages.DEBUG_IBM_COS_CREATING_DIRECTORY.format(download_path)
                logger.debug(msg)
                os.makedirs(os.path.join(os.getcwd(), download_path))
                download_path = os.path.join(os.getcwd(), download_path) + '/'

            # Set 50 MB chunks
            part_size = constants.IBM_COS_DOWNLOAD_PART_SIZE

            # Set threshold to 50 MB
            file_threshold = constants.IBM_COS_DOWNLOAD_FILE_THRESHOLD

            # Set the transfer threshold and chunk size
            transfer_config = ibm_boto3.s3.transfer.TransferConfig(multipart_threshold = file_threshold,
                                                 multipart_chunksize = part_size
            )

            # The download_fileobj method will automatically execute a multi-part download
            # in part_size chunks for all files over file_threshold
            msg = messages.DEBUG_IBM_COS_DOWNLOADING.format(key, bucket, download_path, key)
            logger.debug(msg)

            with open(download_path + key, "wb") as f:
                self._cos_resource._resource.Object(bucket, key).download_fileobj(
                    Fileobj = f,
                    Config = transfer_config
                )
                #self._cos_resource._resource.Object(bucket, key).download_fileobj(bucket, key, f)
                #f.write()

            msg = messages.DEBUG_IBM_COS_DOWNLOAD_SUCCESS.format(key, bucket, download_path, key)
            logger.debug(msg)
            
        except IBMClientError as e:
            msg = messages.ERROR_IBM_COS_DOWNLOAD_CLIENT_ERROR.format(key, bucket, download_path, key, e)
            logger.error(msg)
            raise common.PAWException(msg)
        except Exception as e:
            msg = messages.ERROR_IBM_COS_DOWNLOAD_ERROR.format(key, bucket, download_path, key, e)
            logger.error(msg)
            raise common.PAWException(msg)

    #
    def delete(self, 
               key: str,
               bucket: str = None
              ):
        """
        Deletes a (data) object from the IBM COS bucket
        
        :param key:    Name of (data) object to be deleted
        :type key:     str
        :param bucket: (Optional) name of the bucket.
        :type bucket:  str
        """
        
        if (bucket is None):
            bucket = self._bucket
        
        if self._cos_client is None:
            msg = messages.ERROR_NO_IBM_COS_CLIENT
            logger.error(msg)
            raise common.PAWException(msg)

        msg = messages.DEBUG_IBM_COS_DELETING.format(key, bucket)
        logger.debug(msg)
        
        try:
            self._cos_client._client.head_object(Bucket = bucket, 
                                                 Key    = key
                                                )
            self._cos_client._client.delete_objects(Bucket = bucket,
                                                    Delete = {'Objects' : [{'Key' : key}]}
                                                   )
        except Exception as ex:
            msg = messages.ERROR_IBM_COS_ERROR.format('DELETE', self._bucket, key, ex)
            logger.error(msg)
            raise common.PAWException(msg)
        
        msg = messages.DEBUG_IBM_COS_DELETE_SUCCESS.format(key, bucket)
        logger.debug(msg)

    #
    def get_presigned_url(self, 
                          key: str,
                          bucket: str          = None,
                          expiration_time: int = constants.IBM_COS_PRESIGNED_URL_EXPIRY_TIME
                         ):
        """
        Generates a presigned URL for the object `key`.
        
        :param key:             Name of object in the bucket.
        :type key:              str
        :param bucket:          (Optional) name of the bucket.
        :type bucket:           str
        :param expiration_time: Expiration time of the URL (in seconds).
        :type expiration_time:  int
        """
        
        if (bucket is None):
            bucket = self._bucket
        
        if self._cos_client is None:
            msg = messages.ERROR_NO_IBM_COS_CLIENT
            logger.error(msg)
            raise common.PAWException(msg)
        
        try:
            presigned_url = self._cos_client._client.generate_presigned_url('get_object', 
                                                                            Params = {'Bucket': bucket,
                                                                                      'Key': key
                                                                                     },
                                                                            ExpiresIn = expiration_time
                                                                           )
        except Exception as ex:
            msg = messages.ERROR_IBM_COS_ERROR.format('GENERATE PRESIGNED URL', self._bucket, key, ex)
            logger.error(msg)
            raise common.PAWException(msg)

        return presigned_url

#
def get_cos_auth_endpoint():
    
    """
    A helper function to get IBM COS Authentication Endpoint.
    
    :returns:          The current IBM COS Authentication Endpoint.
    :rtype:            str
    :raises Exception: If endpoint not found.
    """

    response = requests.get("https://" + 
                            constants.IBM_CLOUD_OBJECT_STORE_CONTROL_URL +
                            constants.IBM_CLOUD_OBJECT_STORE_ENDPOINTS
                           )
    
    if response.status_code != 200:
        msg = messages.ERROR_IBM_CLOUD_OBJECT_STORE_CONTROL_FAIL.format("https://" + 
                                                                            constants.IBM_CLOUD_OBJECT_STORE_CONTROL_URL +
                                                                            constants.IBM_CLOUD_OBJECT_STORE_ENDPOINTS, 
                                                                        response.status_code
                                                                       )
        logger.error(msg)
        raise common.PAWException(msg)
    else:
        endpoints = response.json()
    
        if endpoints["identity-endpoints"] is not None:
            if endpoints["identity-endpoints"]["iam-token"] is not None:
                auth_endpoint = "https://" + endpoints["identity-endpoints"]["iam-token"] + "/oidc/token"
                
        if auth_endpoint is None:
            msg = messages.ERROR_IBM_CLOUD_OBJECT_AUTH_ENDPOINT_NOT_FOUND
            logger.error(msg)
            raise common.PAWException(msg)
    
        return auth_endpoint


#
def get_cos_endpoint_by_region(region: str,
                               interface: str = "public", # ["public", "private", "direct"]
):
    
    """
    A helper function to get an IBM COS bucket endpoint by region.
    
    :param region:          Region signifier (e.g. 'us-south').
    :type region:           str
    :param interface:       A choice of endpoint type- 'public' or 'private' or 'direct'.
    :type interface:        str
    :returns:               The current IBM COS bucket endpoint.
    :rtype:                 str or None
    :raises Exception:      If response is not 200.
    """
    
    if interface not in ["public", "private", "direct"]:
        msg = messages.ERROR_IBM_INTERFACE_NOT_RECOGNIZED.format(interface)
        logger.error(msg)
        raise common.PAWException(msg)

    response = requests.get("https://" + 
                            constants.IBM_CLOUD_OBJECT_STORE_CONTROL_URL +
                            constants.IBM_CLOUD_OBJECT_STORE_ENDPOINTS
                           )
    
    if response.status_code != 200:
        msg = messages.ERROR_IBM_CLOUD_OBJECT_STORE_CONTROL_FAIL.format("https://" + 
                                                                            constants.IBM_CLOUD_OBJECT_STORE_CONTROL_URL +
                                                                            constants.IBM_CLOUD_OBJECT_STORE_ENDPOINTS, 
                                                                        response.status_code
                                                                       )
        logger.error(msg)
        raise common.PAWException(msg)
        
    else:
        endpoints = response.json()
    
        eps = dict()

        if endpoints["service-endpoints"] is not None:
            for region_type in endpoints["service-endpoints"]:
                for region_id in endpoints["service-endpoints"][region_type]:
                    for route in endpoints["service-endpoints"][region_type][region_id]:
                        if route == interface:
                            for k,v in endpoints["service-endpoints"][region_type][region_id][route].items():
                                eps[k] = v
    
        endpoint = None
    
        try:
            endpoint = eps[region]
        except:
            endpoint = None
        
        return "https://" + endpoint


#
def get_data_asset(project, source_filename, destination_filename = None, destination_directory_path = None):
    if destination_filename is None:
        destination_filename = source_filename

#TODO: Properly deal with / etc...
    if destination_directory_path is not None:
        if not os.path.isdir(destination_directory_path):
            os.mkdir(destination_directory_path)

#TODO: TRY EXCEPT
    readfile = project.get_file(source_filename)
    writefile = open(destination_filename, 'wb')
    writefile.write(readfile.read())
    writefile.close()

#
def ibm_cos_hmac_keys_from_dict(ibm_cos_hmac_keys_dictionary: dict):
    """
    The function converts a dictionary of IBMCOSHMACKeys to a IBMCOSHMACKeys object.
    
    :param ibm_cos_hmac_keys_dict:    A dictionary that contains the keys of a IBMCOSHMACKeys.
    :type ibm_cos_hmac_keys_dict:     dict             
    :rtype:                           ibmpairs.external.ibm.IBMCOSHMACKeys
    :raises Exception:                if not a dict.
    """
    ibm_cos_hmac_keys = IBMCOSHMACKeys.from_dict(ibm_cos_hmac_keys_dictionary)
        
    return ibm_cos_hmac_keys

#
def ibm_cos_hmac_keys_to_dict(ibm_cos_hmac_keys: IBMCOSHMACKeys):
    """
    The function converts an object of IBMCOSHMACKeys to a dict.
    
    :param ibm_cos_hmac_keys:    A IBMCOSHMACKeys object.
    :type ibm_cos_hmac_keys:     ibmpairs.external.ibm.IBMCOSHMACKeys             
    :rtype:                      dict
    """
    return IBMCOSHMACKeys.to_dict(ibm_cos_hmac_keys)

#
def ibm_cos_hmac_keys_from_json(ibm_cos_hmac_keys_json: Any):
    """
    The function converts a dictionary or json string of IBMCOSHMACKeys to a IBMCOSHMACKeys object.
    
    :param ibm_cos_hmac_keys_json:    A dictionary or json string that contains the keys of a IBMCOSHMACKeys.
    :type ibm_cos_hmac_keys_json:     Any             
    :rtype:                           ibmpairs.external.ibm.IBMCOSHMACKeys
    :raises Exception:                if not a dict or a str.
    """
    ibm_cos_hmac_keys = IBMCOSHMACKeys.from_json(ibm_cos_hmac_keys_json)
    return ibm_cos_hmac_keys

#
def ibm_cos_hmac_keys_to_json(ibm_cos_hmac_keys: IBMCOSHMACKeys):
    """
    The function converts an object of IBMCOSHMACKeys to a json string.
    
    :param ibm_cos_hmac_keys:    A IBMCOSHMACKeys object.
    :type ibm_cos_hmac_keys:     ibmpairs.external.ibm.IBMCOSHMACKeys             
    :rtype:                      str
    """
    return IBMCOSHMACKeys.to_json(ibm_cos_hmac_keys)

#
def ibm_cos_service_credentials_from_dict(ibm_cos_service_credentials_dictionary: dict):
    """
    The function converts a dictionary of IBMCOSServiceCredentials to a IBMCOSServiceCredentials object.
    
    :param ibm_cos_service_credentials_dict:    A dictionary that contains the keys of a IBMCOSServiceCredentials.
    :type ibm_cos_service_credentials_dict:     dict             
    :rtype:                                     ibmpairs.external.ibm.IBMCOSServiceCredentials
    :raises Exception:                          if not a dict.
    """
    ibm_cos_service_credentials = IBMCOSServiceCredentials.from_dict(ibm_cos_service_credentials_dictionary)
        
    return ibm_cos_service_credentials

#
def ibm_cos_service_credentials_to_dict(ibm_cos_service_credentials: IBMCOSServiceCredentials):
    """
    The function converts an object of IBMCOSServiceCredentials to a dict.
    
    :param ibm_cos_service_credentials:    A IBMCOSServiceCredentials object.
    :type ibm_cos_service_credentials:     ibmpairs.external.ibm.IBMCOSServiceCredentials             
    :rtype:                                dict
    """
    return IBMCOSServiceCredentials.to_dict(ibm_cos_service_credentials)

#
def ibm_cos_service_credentials_from_json(ibm_cos_service_credentials_json: Any):
    """
    The function converts a dictionary or json string of IBMCOSServiceCredentials to a IBMCOSServiceCredentials object.
    
    :param ibm_cos_service_credentials_json:    A dictionary or json string that contains the keys of a IBMCOSServiceCredentials.
    :type ibm_cos_service_credentials_json:     Any             
    :rtype:                                     ibmpairs.external.ibm.IBMCOSServiceCredentials
    :raises Exception:                          if not a dict or a str.
    """
    ibm_cos_service_credentials = IBMCOSServiceCredentials.from_json(ibm_cos_service_credentials_json)
    return ibm_cos_service_credentials

#
def ibm_cos_service_credentials_to_json(ibm_cos_service_credentials: IBMCOSServiceCredentials):
    """
    The function converts an object of IBMCOSServiceCredentials to a json string.
    
    :param ibm_cos_service_credentials:    A IBMCOSServiceCredentials object.
    :type ibm_cos_service_credentials:     ibmpairs.external.ibm.IBMCOSServiceCredentials             
    :rtype:                                str
    """
    return IBMCOSServiceCredentials.to_json(ibm_cos_service_credentials)

#
def ibm_cos_file_from_dict(ibm_cos_file_dictionary: dict):
    """
    The function converts a dictionary of IBMCOSFile to a IBMCOSFile object.
    
    :param ibm_cos_file_dict:    A dictionary that contains the keys of a IBMCOSFile.
    :type ibm_cos_file_dict:     dict             
    :rtype:                      ibmpairs.external.ibm.IBMCOSFile
    :raises Exception:           if not a dict.
    """
    ibm_cos_file = IBMCOSFile.from_dict(ibm_cos_file_dictionary)
        
    return ibm_cos_file

#
def ibm_cos_file_to_dict(ibm_cos_file: IBMCOSFile):
    """
    The function converts an object of IBMCOSFile to a dict.
    
    :param ibm_cos_file:    A IBMCOSFile object.
    :type ibm_cos_file:     ibmpairs.external.ibm.IBMCOSFile             
    :rtype:                 dict
    """
    return IBMCOSFile.to_dict(ibm_cos_file)

#
def ibm_cos_file_from_json(ibm_cos_file_json: Any):
    """
    The function converts a dictionary or json string of IBMCOSFile to a IBMCOSFile object.
    
    :param ibm_cos_file_json:    A dictionary or json string that contains the keys of a IBMCOSFile.
    :type ibm_cos_file_json:     Any             
    :rtype:                      ibmpairs.external.ibm.IBMCOSFile
    :raises Exception:           if not a dict or a str.
    """
    ibm_cos_file = IBMCOSFile.from_json(ibm_cos_file_json)
    return ibm_cos_file

#
def ibm_cos_file_to_json(ibm_cos_file: IBMCOSFile):
    """
    The function converts an object of IBMCOSFile to a json string.
    
    :param ibm_cos_file:    A IBMCOSFile object.
    :type ibm_cos_file:     ibmpairs.external.ibm.IBMCOSFile             
    :rtype:                 str
    """
    return IBMCOSFile.to_json(ibm_cos_file)

#
def ibm_cos_resource_from_dict(ibm_cos_resource_dictionary: dict):
    """
    The function converts a dictionary of IBMCOSResource to a IBMCOSResource object.
    
    :param ibm_cos_resource_dict:    A dictionary that contains the keys of a IBMCOSResource.
    :type ibm_cos_resource_dict:     dict             
    :rtype:                          ibmpairs.external.ibm.IBMCOSResource
    :raises Exception:               if not a dict.
    """
    ibm_cos_resource = IBMCOSResource.from_dict(ibm_cos_resource_dictionary)
        
    return ibm_cos_resource

#
def ibm_cos_resource_to_dict(ibm_cos_resource: IBMCOSResource):
    """
    The function converts an object of IBMCOSResource to a dict.
    
    :param ibm_cos_resource:    A IBMCOSResource object.
    :type ibm_cos_resource:     ibmpairs.external.ibm.IBMCOSResource             
    :rtype:                     dict
    """
    return IBMCOSResource.to_dict(ibm_cos_resource)

#
def ibm_cos_resource_from_json(ibm_cos_resource_json: Any):
    """
    The function converts a dictionary or json string of IBMCOSResource to a IBMCOSResource object.
    
    :param ibm_cos_resource_json:    A dictionary or json string that contains the keys of a IBMCOSResource.
    :type ibm_cos_resource_json:     Any             
    :rtype:                          ibmpairs.external.ibm.IBMCOSResource
    :raises Exception:               if not a dict or a str.
    """
    ibm_cos_resource = IBMCOSResource.from_json(ibm_cos_resource_json)
    return ibm_cos_resource

#
def ibm_cos_resource_to_json(ibm_cos_resource: IBMCOSResource):
    """
    The function converts an object of IBMCOSResource to a json string.
    
    :param ibm_cos_resource:    A IBMCOSResource object.
    :type ibm_cos_resource:     ibmpairs.external.ibm.IBMCOSResource             
    :rtype:                     str
    """
    return IBMCOSResource.to_json(ibm_cos_resource)

#
def ibm_cos_client_from_dict(ibm_cos_client_dictionary: dict):
    """
    The function converts a dictionary of IBMCOSClient to a IBMCOSClient object.
    
    :param ibm_cos_client_dict:    A dictionary that contains the keys of a IBMCOSClient.
    :type ibm_cos_client_dict:     dict             
    :rtype:                        ibmpairs.external.ibm.IBMCOSClient
    :raises Exception:             if not a dict.
    """
    ibm_cos_client = IBMCOSClient.from_dict(ibm_cos_client_dictionary)
        
    return ibm_cos_client

#
def ibm_cos_client_to_dict(ibm_cos_client: IBMCOSClient):
    """
    The function converts an object of IBMCOSClient to a dict.
    
    :param ibm_cos_client:    A IBMCOSClient object.
    :type ibm_cos_client:     ibmpairs.external.ibm.IBMCOSClient             
    :rtype:                   dict
    """
    return IBMCOSClient.to_dict(ibm_cos_client)

#
def ibm_cos_client_from_json(ibm_cos_client_json: Any):
    """
    The function converts a dictionary or json string of IBMCOSClient to a IBMCOSClient object.
    
    :param ibm_cos_client_json:    A dictionary or json string that contains the keys of a IBMCOSClient.
    :type ibm_cos_client_json:     Any             
    :rtype:                        ibmpairs.external.ibm.IBMCOSClient
    :raises Exception:             if not a dict or a str.
    """
    ibm_cos_client = IBMCOSClient.from_json(ibm_cos_client_json)
    return ibm_cos_client

#
def ibm_cos_client_to_json(ibm_cos_client: IBMCOSClient):
    """
    The function converts an object of IBMCOSClient to a json string.
    
    :param ibm_cos_client:    A IBMCOSClient object.
    :type ibm_cos_client:     ibmpairs.external.ibm.IBMCOSClient             
    :rtype:                   str
    """
    return IBMCOSClient.to_json(ibm_cos_client)

#
def ibm_cos_bucket_from_dict(ibm_cos_bucket_dictionary: dict):
    """
    The function converts a dictionary of IBMCOSBucket to a IBMCOSBucket object.
    
    :param ibm_cos_bucket_dict:    A dictionary that contains the keys of a IBMCOSBucket.
    :type ibm_cos_bucket_dict:     dict             
    :rtype:                        ibmpairs.external.ibm.IBMCOSBucket
    :raises Exception:             if not a dict.
    """
    ibm_cos_bucket = IBMCOSBucket.from_dict(ibm_cos_bucket_dictionary)
        
    return ibm_cos_bucket

#
def ibm_cos_bucket_to_dict(ibm_cos_bucket: IBMCOSBucket):
    """
    The function converts an object of IBMCOSBucket to a dict.
    
    :param ibm_cos_bucket:    A IBMCOSBucket object.
    :type ibm_cos_bucket:     ibmpairs.external.ibm.IBMCOSBucket             
    :rtype:                   dict
    """
    return IBMCOSBucket.to_dict(ibm_cos_bucket)

#
def ibm_cos_bucket_from_json(ibm_cos_bucket_json: Any):
    """
    The function converts a dictionary or json string of IBMCOSBucket to a IBMCOSBucket object.
    
    :param ibm_cos_bucket_json:    A dictionary or json string that contains the keys of a IBMCOSBucket.
    :type ibm_cos_bucket_json:     Any             
    :rtype:                        ibmpairs.external.ibm.IBMCOSBucket
    :raises Exception:             if not a dict or a str.
    """
    ibm_cos_bucket = IBMCOSBucket.from_json(ibm_cos_bucket_json)
    return ibm_cos_bucket

#
def ibm_cos_bucket_to_json(ibm_cos_bucket: IBMCOSBucket):
    """
    The function converts an object of IBMCOSBucket to a json string.
    
    :param ibm_cos_bucket:    A IBMCOSBucket object.
    :type ibm_cos_bucket:     ibmpairs.external.ibm.IBMCOSBucket             
    :rtype:                   str
    """
    return IBMCOSBucket.to_json(ibm_cos_bucket)
