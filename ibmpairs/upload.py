"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
import os
import json
import warnings
from typing import List, Any
from pathlib import Path
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
import ibmpairs.client as cl
import ibmpairs.common as common
import ibmpairs.constants as constants
from ibmpairs.logger import logger
import ibmpairs.messages as messages
import ibmpairs.external.ibm as ibm_cos
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import requests
import asyncio
import aiohttp
#}}}

UPLOAD_DEFAULT_WORKERS         = int(os.environ.get('UPLOAD_DEFAULT_WORKERS', 1))
UPLOAD_MAX_WORKERS             = int(os.environ.get('UPLOAD_MAX_WORKERS', 8))
UPLOAD_MIN_STATUS_INTERVAL     = int(os.environ.get('UPLOAD_MIN_STATUS_INTERVAL', 30))
UPLOAD_STATUS_CHECK_INTERVAL   = int(os.environ.get('UPLOAD_STATUS_CHECK_INTERVAL', 60))

#
class ServiceParameters:
    #_uploader_id: int
    #_max_bytes_per_call: int
    
    """
    A representation of an Upload ServiceParameters.
    
    :param uploader_id:        The ID of an uploader.
    :type uploader_id:         int
    :param max_bytes_per_call: The maximum bytes per call.
    :type max_bytes_per_call:  int
    """
    
    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    def __init__(self, 
                 uploader_id: int        = None, 
                 max_bytes_per_call: int = None
                ):
        self._uploader_id        = uploader_id
        self._max_bytes_per_call = max_bytes_per_call
        
    #    
    def get_uploader_id(self):
        return self._uploader_id

    #
    def set_uploader_id(self, uploader_id):
        self._uploader_id = common.check_int(uploader_id)
        
    #    
    def del_uploader_id(self): 
        del self._uploader_id

    #    
    uploader_id = property(get_uploader_id, set_uploader_id, del_uploader_id)
    
    #    
    def get_max_bytes_per_call(self):
        return self._max_bytes_per_call

    #
    def set_max_bytes_per_call(self, max_bytes_per_call):
        self._max_bytes_per_call = common.check_int(max_bytes_per_call)
        
    #    
    def del_max_bytes_per_call(self): 
        del self._max_bytes_per_call

    #    
    max_bytes_per_call = property(get_max_bytes_per_call, set_max_bytes_per_call, del_max_bytes_per_call)
    
    #    
    def from_dict(service_parameters_dict: Any):
      
        """
        Create a ServiceParameters object from a dictionary.
        
        :param service_parameters_dict:    A dictionary that contains the keys of a ServiceParameters.
        :type service_parameters_dict:     Any             
        :rtype:                            ibmpairs.upload.ServiceParameters
        :raises Exception:                 if not a dictionary.
        """
        
        uploader_id    = None
        max_bytes_per_call = None
        
        common.check_dict(service_parameters_dict)
        if "uploader_id" in service_parameters_dict:
            if service_parameters_dict.get("uploader_id") is not None:
                uploader_id = common.check_int(service_parameters_dict.get("uploader_id"))
        if "max_bytes_per_call" in service_parameters_dict:
            if service_parameters_dict.get("max_bytes_per_call") is not None:
                max_bytes_per_call = common.check_int(service_parameters_dict.get("max_bytes_per_call"))
        return ServiceParameters(uploader_id        = uploader_id,
                                 max_bytes_per_call = max_bytes_per_call
                                )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.     
               
        :rtype:                     dict
        """
        
        service_parameters_dict: dict = {}
        if self._uploader_id is not None:
            service_parameters_dict["uploader_id"] = self._uploader_id
        if self._max_bytes_per_call is not None:
            service_parameters_dict["max_bytes_per_call"] = self._max_bytes_per_call
        return service_parameters_dict
        
    #
    def from_json(service_parameters_json: Any):

        """
        Create a ServiceParameters object from json (dictonary or str).
        
        :param service_parameters_dict:        A json dictionary that contains the keys of a ServiceParameters or a string representation of a json dictionary.
        :type service_parameters_dict:         Any             
        :rtype:                                ibmpairs.upload.ServiceParameters
        :raises Exception:                     if not a dictionary or a string.
        """

        if isinstance(service_parameters_json, dict):
            service_parameters = ServiceParameters.from_dict(service_parameters_json)
        elif isinstance(service_parameters_json, str):
            service_parameters_dict = json.loads(service_parameters_json)
            service_parameters = ServiceParameters.from_dict(service_parameters_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(service_parameters_json), "service_parameters_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return service_parameters

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """        
        
        return json.dumps(self.to_dict())


#
class UploadInfo:
    #_status: str
    #_maintainer: str
    #_copyright: str
    #_service_parameters: ServiceParameters
    #_contact: str
    #_version: str
    
    """
    A representation of an Upload UploadInfo.
    
    :param status:             Status.
    :type status:              int
    :param maintainer:         Maintainer.
    :type maintainer:          int
    :param copyright:          Copyright.
    :type copyright:           int
    :param service_parameters: A ServiceParameters object.
    :type service_parameters:  ibmpairs.catalog.ServiceParameters
    :param contact:            Contact.
    :type contact:             str
    :param version:            Version.
    :type version:             str
    """
    
    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                            indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                            sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                            indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                            sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 status: str                           = None, 
                 maintainer: str                       = None, 
                 copyright: str                        = None, 
                 service_parameters: ServiceParameters = None, 
                 contact: str                          = None, 
                 version: str                          = None
                ):
        self._status             = status
        self._maintainer         = maintainer
        self._copyright          = copyright
        self._service_parameters = service_parameters
        self._contact            = contact
        self._version            = version
        
    #    
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_str(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)
    
    #    
    def get_maintainer(self):
        return self._maintainer

    #
    def set_maintainer(self, maintainer):
        self._maintainer = common.check_str(maintainer)
        
    #    
    def del_maintainer(self): 
        del self._maintainer

    #    
    maintainer = property(get_maintainer, set_maintainer, del_maintainer)

    #    
    def get_copyright(self):
        return self._copyright

    #
    def set_copyright(self, copyright):
        self._copyright = common.check_str(copyright)
        
    #    
    def del_copyright(self): 
        del self._copyright

    #    
    copyright = property(get_copyright, set_copyright, del_copyright)
    
    #    
    def get_service_parameters(self):
        return self._service_parameters

    #
    def set_service_parameters(self, service_parameters):
        self._service_parameters = common.check_class(service_parameters, ServiceParameters)
        
    #    
    def del_service_parameters(self): 
        del self._service_parameters

    #    
    service_parameters = property(get_service_parameters, set_service_parameters, del_service_parameters)
    
    #    
    def get_contact(self):
        return self._contact

    #
    def set_contact(self, contact):
        self._contact = common.check_str(contact)
        
    #    
    def del_contact(self): 
        del self._contact

    #    
    contact = property(get_contact, set_contact, del_contact)

    #    
    def get_version(self):
        return self._version

    #
    def set_version(self, version):
        self._version = common.check_str(version)
        
    #    
    def del_version(self): 
        del self._version

    #    
    version = property(get_version, set_version, del_version)

    #    
    def from_dict(upload_info_dict: Any):

        """
        Create an UploadInfo object from a dictionary.
        
        :param upload_info_dict:    A dictionary that contains the keys of an UploadInfo.
        :type upload_info_dict:     Any             
        :rtype:                     ibmpairs.upload.UploadInfo
        :raises Exception:          if not a dictionary.
        """
        
        status             = None
        maintainer         = None
        copyright          = None
        service_parameters = None
        contact            = None
        version            = None
        
        common.check_dict(upload_info_dict)
        if "status" in upload_info_dict:
            if upload_info_dict.get("status") is not None:
                status = common.check_str(upload_info_dict.get("status"))
        if "maintainer" in upload_info_dict:
            if upload_info_dict.get("maintainer") is not None:
                maintainer = common.check_str(upload_info_dict.get("maintainer"))
        if "copyright" in upload_info_dict:
            if upload_info_dict.get("copyright") is not None:
                copyright = common.check_str(upload_info_dict.get("copyright"))
        if "service_parameters" in upload_info_dict:
            if upload_info_dict.get("service_parameters") is not None:
                service_parameters = ServiceParameters.from_dict(upload_info_dict.get("service_parameters"))
        if "contact" in upload_info_dict:
            if upload_info_dict.get("contact") is not None:
                contact = common.check_str(upload_info_dict.get("contact"))
        if "version" in upload_info_dict:
            if upload_info_dict.get("version") is not None:
                version = common.check_str(upload_info_dict.get("version"))
        return UploadInfo(status             = status,
                          maintainer         = maintainer,
                          copyright          = copyright,
                          service_parameters = service_parameters,
                          contact            = contact,
                          version            = version
                         )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        upload_info_dict: dict = {}
        if self._status is not None:
            upload_info_dict["status"] = self._status
        if self._maintainer is not None:
            upload_info_dict["maintainer"] = self._maintainer
        if self._copyright is not None:
            upload_info_dict["copyright"] = self._copyright
        if self._service_parameters is not None:
            upload_info_dict["service_parameters"] = self._service_parameters
        if self._contact is not None:
            upload_info_dict["contact"] = self._contact
        if self._version is not None:
            upload_info_dict["version"] = self._version
        return upload_info_dict
        
    #
    def from_json(upload_info_json: Any):

        """
        Create an UploadInfo object from json (dictonary or str).
        
        :param upload_info_dict:        A json dictionary that contains the keys of an UploadInfo or a string representation of a json dictionary.
        :type upload_info_dict:         Any             
        :rtype:                         ibmpairs.upload.UploadInfo
        :raises Exception:              if not a dictionary or a string.
        """

        if isinstance(upload_info_json, dict):
            upload_info = UploadInfo.from_dict(upload_info_json)
        elif isinstance(upload_info_json, str):
            upload_info_dict = json.loads(upload_info_json)
            upload_info = UploadInfo.from_dict(upload_info_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(upload_info_json), "upload_info_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return upload_info

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Summary:
    #_status: float
    #_last_updated: str
    #_details: str
    #_raw_filename: str
    
    """
    A representation of an Upload Summary.
    
    :param status:       The status of the file upload.
    :type status:        float
    :param last_updated: The date at which the summary for the file was last updated.
    :type last_updated:  str
    :param details:      Details.
    :type details:       str
    :param raw_filename: The raw file name of the upload.
    :type raw_filename:  str
    """
    
    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 status: float     = None, 
                 last_updated: str = None, 
                 details: str      = None, 
                 raw_filename: str = None
                ):
        self._status       = status
        self._last_updated = last_updated
        self._details      = details
        self._raw_filename = raw_filename
    
    #    
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_float(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)
    
    #    
    def get_last_updated(self):
        return self._last_updated

    #
    def set_last_updated(self, last_updated):
        self._last_updated = common.check_str(last_updated)
        
    #    
    def del_last_updated(self): 
        del self._last_updated

    #    
    last_updated = property(get_last_updated, set_last_updated, del_last_updated)
    
    #    
    def get_details(self):
        return self._details

    #
    def set_details(self, details):
        self._details = common.check_str(details)
        
    #    
    def del_details(self): 
        del self._details

    #    
    details = property(get_details, set_details, del_details)
    
    #    
    def get_raw_filename(self):
        return self._raw_filename

    #
    def set_raw_filename(self, raw_filename):
        self._raw_filename = common.check_str(raw_filename)
        
    #    
    def del_raw_filename(self): 
        del self._raw_filename

    #    
    raw_filename = property(get_raw_filename, set_raw_filename, del_raw_filename)

    #    
    def from_dict(summary_dict: Any):

        """
        Create a Summary object from a dictionary.
        
        :param summary_dict:    A dictionary that contains the keys of a Summary.
        :type summary_dict:     Any             
        :rtype:                 ibmpairs.upload.Summary
        :raises Exception:      if not a dictionary.
        """
        
        status       = None
        last_updated = None
        details      = None
        raw_filename = None
        
        common.check_dict(summary_dict)
        if "status" in summary_dict:
            if summary_dict.get("status") is not None:
                status = common.check_float(summary_dict.get("status"))
        if "last_updated" in summary_dict:
            if summary_dict.get("last_updated") is not None:
                last_updated = common.check_str(summary_dict.get("last_updated"))
        if "details" in summary_dict:
            if summary_dict.get("details") is not None:
                details = common.check_str(summary_dict.get("details"))
        if "raw_filename" in summary_dict:
            if summary_dict.get("raw_filename") is not None:
                raw_filename = common.check_str(summary_dict.get("raw_filename"))
        return Summary(status       = status,
                       last_updated = last_updated,
                       details      = details,
                       raw_filename = raw_filename
                      )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        summary_dict: dict = {}
        if self._status is not None:
            summary_dict["status"] = self._status
        if self._last_updated is not None:
            summary_dict["last_updated"] = self._last_updated
        if self._details is not None:
            summary_dict["details"] = self._details
        if self._raw_filename is not None:
            summary_dict["raw_filename"] = self._raw_filename
        return summary_dict

    #
    def from_json(summary_json: Any):

        """
        Create a Summary object from json (dictonary or str).
        
        :param summary_dict:        A json dictionary that contains the keys of a Summary or a string representation of a json dictionary.
        :type summary_dict:         Any             
        :rtype:                     ibmpairs.upload.Summary
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(summary_json, dict):
            summary = Summary.from_dict(summary_json)
        elif isinstance(summary_json, str):
            summary_dict = json.loads(summary_json)
            summary = Summary.from_dict(summary_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(summary_json), "summary_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return summary

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class UploadResponse:
    #_id: str
    #_message: str
    
    """
    A representation of a response to an Upload.
    
    :param id:      Upload ID.
    :type id:       str
    :param message: A message for the request.
    :type message:  str
    """
    
    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 id: str      = None, 
                 message: str = None
                ):
        self._id      = id
        self._message = message
        
    #    
    def get_id(self):
        return self._id

    #
    def set_id(self, id):
        self._id = common.check_str(id)
        
    #    
    def del_id(self): 
        del self._id

    #    
    id = property(get_id, set_id, del_id)
        
    #    
    def get_message(self):
        return self._message

    #
    def set_message(self, message):
        self._message = common.check_str(message)
        
    #    
    def del_message(self): 
        del self._message

    #    
    message = property(get_message, set_message, del_message)
    
    #    
    def from_dict(upload_response_dict: Any):
        
        """
        Create an UploadResponse object from a dictionary.
        
        :param upload_response_dict:    A dictionary that contains the keys of an UploadResponse.
        :type upload_response_dict:     Any             
        :rtype:                         ibmpairs.upload.UploadResponse
        :raises Exception:              if not a dictionary.
        """
        
        id      = None
        message = None
        
        common.check_dict(upload_response_dict)
        if "id" in upload_response_dict:
            if upload_response_dict.get("id") is not None:
                id = common.check_str(upload_response_dict.get("id"))
        if "message" in upload_response_dict:
            if upload_response_dict.get("message") is not None:
                message = common.check_str(upload_response_dict.get("message"))
        return UploadResponse(id      = id,
                              message = message
                             )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        upload_response_dict: dict = {}
        if self._id is not None:
            upload_response_dict["id"] = self._id
        if self._message is not None:
            upload_response_dict["message"] = self._message
        return upload_response_dict

    #
    def from_json(upload_response_json: Any):

        """
        Create an UploadResponse object from json (dictonary or str).
        
        :param upload_response_dict:        A json dictionary that contains the keys of an UploadResponse or a string representation of a json dictionary.
        :type upload_response_dict:         Any             
        :rtype:                             ibmpairs.upload.UploadResponse
        :raises Exception:                  if not a dictionary or a string.
        """

        if isinstance(upload_response_json, dict):
            upload_response = UploadResponse.from_dict(upload_response_json)
        elif isinstance(upload_response_json, str):
            upload_response_dict = json.loads(upload_response_json)
            upload_response = UploadResponse.from_dict(upload_response_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(upload_response_json), "upload_response_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return upload_response

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class UploadStatusResponse:
    #_status: str
    #_last_updated: str
    #_summary: List[Summary]
    #_tracking_id: str
    #_progress: int
    #_user_tag: str
    
    """
    A representation of a response to an Upload Status call.
    
    :param status:       The status of the upload.
    :type status:        str
    :param last_updated: The last time the status was updated.
    :type last_updated:  str
    :param summary:      A summary of the uploaded files.
    :type summary:       List[ibmpairs.upload.Summary]
    :param tracking_id:  A tracking ID for the upload.
    :type tracking_id:   str
    :param progress:     A progress percentage for the upload.
    :type progress:      int
    :param user_tag:     A user tag assigned to the upload.
    :type user_tag:      str
    """
    
    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 status: str            = None, 
                 last_updated: str      = None, 
                 summary: List[Summary] = None, 
                 tracking_id: str       = None, 
                 progress: int          = None, 
                 user_tag: str          = None
                ):
        self._status       = status
        self._last_updated = last_updated
        self._summary      = summary
        self._tracking_id  = tracking_id
        self._progress     = progress
        self._user_tag     = user_tag
        
    #    
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_str(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)

    #    
    def get_last_updated(self):
        return self._last_updated

    #
    def set_last_updated(self, last_updated):
        self._last_updated = common.check_str(last_updated)
        
    #    
    def del_last_updated(self): 
        del self._last_updated

    #    
    last_updated = property(get_last_updated, set_last_updated, del_last_updated)

    #
    def get_summary(self):
        return self._summary

    #
    def set_summary(self, summary):
        self._summary = common.check_class(summary, List[Summary])

    #    
    def del_summary(self): 
        del self._summary

    #    
    summary = property(get_summary, set_summary, del_summary)

    #    
    def get_tracking_id(self):
        return self._tracking_id

    #
    def set_tracking_id(self, tracking_id):
        self._tracking_id = common.check_str(tracking_id)
        
    #    
    def del_tracking_id(self): 
        del self._tracking_id

    #    
    tracking_id = property(get_tracking_id, set_tracking_id, del_tracking_id)

    #    
    def get_progress(self):
        return self._progress

    #
    def set_progress(self, progress):
        self._progress = common.check_int(progress)
        
    #    
    def del_progress(self): 
        del self._progress

    #    
    progress = property(get_progress, set_progress, del_progress)
    
    #    
    def get_user_tag(self):
        return self._user_tag

    #
    def set_user_tag(self, user_tag):
        self._user_tag = common.check_str(user_tag)
        
    #    
    def del_user_tag(self): 
        del self._user_tag

    #    
    user_tag = property(get_user_tag, set_user_tag, del_user_tag)

    #    
    def from_dict(upload_status_response_dict: Any):
        
        """
        Create an UploadStatusResponse object from a dictionary.
        
        :param upload_status_response_dict:    A dictionary that contains the keys of an UploadStatusResponse.
        :type upload_status_response_dict:     Any             
        :rtype:                                ibmpairs.upload.UploadStatusResponse
        :raises Exception:                     if not a dictionary.
        """
        
        status       = None
        last_updated = None
        summary      = None
        tracking_id  = None
        progress     = None
        user_tag     = None
        
        common.check_dict(upload_status_response_dict)
        if "status" in upload_status_response_dict:
            if upload_status_response_dict.get("status") is not None:
                status = common.check_str(upload_status_response_dict.get("status"))
        if "last_updated" in upload_status_response_dict:
            if upload_status_response_dict.get("last_updated") is not None:
                last_updated = common.check_str(upload_status_response_dict.get("last_updated"))
        if "summary" in upload_status_response_dict:
            if upload_status_response_dict.get("summary") is not None:
                summary = common.from_list(upload_status_response_dict.get("summary"), Summary.from_dict)
        if "tracking_id" in upload_status_response_dict:
            if upload_status_response_dict.get("tracking_id") is not None:
                tracking_id = common.check_str(upload_status_response_dict.get("tracking_id"))
        if "progress" in upload_status_response_dict:
            if upload_status_response_dict.get("progress") is not None:
                progress = common.check_int(upload_status_response_dict.get("progress"))
        if "user_tag" in upload_status_response_dict:
            if upload_status_response_dict.get("user_tag") is not None:
                user_tag = common.check_str(upload_status_response_dict.get("user_tag"))
        return UploadStatusResponse(status       = status,
                                    last_updated = last_updated,
                                    summary      = summary,
                                    tracking_id  = tracking_id,
                                    progress     = progress,
                                    user_tag     = user_tag
                                   )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        upload_status_response_dict: dict = {}
        if self._status is not None:
            upload_status_response_dict["status"] = self._status
        if self._last_updated is not None:
            upload_status_response_dict["last_updated"] = self._last_updated
        if self._summary is not None:
            upload_status_response_dict["summary"] = common.from_list(self._summary, lambda item: common.class_to_dict(item, Summary))
        if self._tracking_id is not None:
            upload_status_response_dict["tracking_id"] = self._tracking_id
        if self._progress is not None:
            upload_status_response_dict["progress"] = self._progress
        if self._user_tag is not None:
            upload_status_response_dict["user_tag"] = self._user_tag
        return upload_status_response_dict

    #
    def from_json(upload_status_response_json: Any):

        """
        Create an UploadStatusResponse object from json (dictonary or str).
        
        :param upload_status_response_dict:        A json dictionary that contains the keys of an UploadStatusResponse or a string representation of a json dictionary.
        :type upload_status_response_dict:         Any             
        :rtype:                                    ibmpairs.upload.UploadStatusResponse
        :raises Exception:                         if not a dictionary or a string.
        """

        if isinstance(upload_status_response_json, dict):
            upload_status_response = UploadStatusResponse.from_dict(upload_status_response_json)
        elif isinstance(upload_status_response_json, str):
            upload_status_response_dict = json.loads(upload_status_response_json)
            upload_status_response = UploadStatusResponse.from_dict(upload_status_response_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(upload_status_response_json), "upload_status_response_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return upload_status_response

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.   
                 
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())


#
class ConvParamsDict:
    #_lin_conv_offset: float
    #_lin_conv_slope: float
    #_non_lin_param1: float
    #_non_lin_param2: float
    
    """
    A representation of an Upload Conversion Parameters Dict (ConvParamsDict).
    
    :param lin_conv_offset: lin conv offset.
    :type lin_conv_offset:  float
    :param lin_conv_slope:  lin conv slope.
    :type lin_conv_slope:   float
    :param non_lin_param1:  non lin param1.
    :type non_lin_param1:   float
    :param non_lin_param2:  non lin param2.
    :type non_lin_param2:   float
    """

    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 lin_conv_offset: float = None, 
                 lin_conv_slope: float  = None, 
                 non_lin_param1: float  = None, 
                 non_lin_param2: float  = None
                ):
        self._lin_conv_offset = lin_conv_offset
        self._lin_conv_slope  = lin_conv_slope
        self._non_lin_param1  = non_lin_param1
        self._non_lin_param2  = non_lin_param2
    
    #    
    def get_lin_conv_offset(self):
        return self._lin_conv_offset

    #
    def set_lin_conv_offset(self, lin_conv_offset):
        self._lin_conv_offset = common.check_float(lin_conv_offset)
    
    #    
    def del_lin_conv_offset(self): 
        del self._lin_conv_offset

    #    
    lin_conv_offset = property(get_lin_conv_offset, set_lin_conv_offset, del_lin_conv_offset)
    
    #    
    def get_lin_conv_slope(self):
        return self._lin_conv_slope

    #
    def set_lin_conv_slope(self, lin_conv_slope):
        self._lin_conv_slope = common.check_float(lin_conv_slope)
    
    #    
    def del_lin_conv_slope(self): 
        del self._lin_conv_slope

    #    
    lin_conv_slope = property(get_lin_conv_slope, set_lin_conv_slope, del_lin_conv_slope)
    
    #    
    def get_non_lin_param1(self):
        return self._non_lin_param1

    #
    def set_non_lin_param1(self, non_lin_param1):
        self._non_lin_param1 = common.check_float(non_lin_param1)
    
    #    
    def del_non_lin_param1(self): 
        del self._non_lin_param1

    #    
    non_lin_param1 = property(get_non_lin_param1, set_non_lin_param1, del_non_lin_param1)
    
    #    
    def get_non_lin_param2(self):
        return self._non_lin_param2

    #
    def set_non_lin_param2(self, non_lin_param2):
        self._non_lin_param2 = common.check_float(non_lin_param2)
    
    #    
    def del_non_lin_param2(self): 
        del self._non_lin_param2

    #    
    non_lin_param2 = property(get_non_lin_param2, set_non_lin_param2, del_non_lin_param2)

    #    
    def from_dict(conv_params_dict_dict: Any):
        
        """
        Create a ConvParamsDict object from a dictionary.
        
        :param conv_params_dict_dict:    A dictionary that contains the keys of a ConvParamsDict.
        :type conv_params_dict_dict:     Any             
        :rtype:                          ibmpairs.upload.ConvParamsDict
        :raises Exception:               if not a dictionary.
        """
        
        lin_conv_offset = None
        lin_conv_slope  = None
        non_lin_param1  = None
        non_lin_param2  = None
    
        common.check_dict(conv_params_dict_dict)
        if "lin-conv-offset" in conv_params_dict_dict:
            if conv_params_dict_dict.get("lin-conv-offset") is not None:
                lin_conv_offset = common.check_float(conv_params_dict_dict.get("lin-conv-offset"))
        elif "lin_conv_offset" in conv_params_dict_dict:
            if conv_params_dict_dict.get("lin_conv_offset") is not None:
                lin_conv_offset = common.check_float(conv_params_dict_dict.get("lin_conv_offset"))
        if "lin-conv-slope" in conv_params_dict_dict:
            if conv_params_dict_dict.get("lin-conv-slope") is not None:
                lin_conv_slope = common.check_float(conv_params_dict_dict.get("lin-conv-slope"))
        elif "lin_conv_slope" in conv_params_dict_dict:
            if conv_params_dict_dict.get("lin_conv_slope") is not None:
                lin_conv_slope = common.check_float(conv_params_dict_dict.get("lin_conv_slope"))
        if "non-lin-param1" in conv_params_dict_dict:
            if conv_params_dict_dict.get("non-lin-param1") is not None:
                non_lin_param1 = common.check_float(conv_params_dict_dict.get("non-lin-param1"))
        elif "non_lin_param1" in conv_params_dict_dict:
            if conv_params_dict_dict.get("non_lin_param1") is not None:
                non_lin_param1 = common.check_float(conv_params_dict_dict.get("non_lin_param1"))
        if "non-lin-param2" in conv_params_dict_dict:
            if conv_params_dict_dict.get("non-lin-param2") is not None:
                non_lin_param2 = common.check_float(conv_params_dict_dict.get("non-lin-param2"))
        elif "non_lin_param2" in conv_params_dict_dict:
            if conv_params_dict_dict.get("non_lin_param2") is not None:
                non_lin_param2 = common.check_float(conv_params_dict_dict.get("non_lin_param2"))
        return ConvParamsDict(lin_conv_offset = lin_conv_offset,
                              lin_conv_slope  = lin_conv_slope,
                              non_lin_param1  = non_lin_param1,
                              non_lin_param2  = non_lin_param2
                             )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        conv_params_dict_dict: dict = {}
        if self._lin_conv_offset is not None:
            conv_params_dict_dict["lin_conv_offset"] = self._lin_conv_offset
        if self._lin_conv_slope is not None:
            conv_params_dict_dict["lin_conv_slope"] = self._lin_conv_slope
        if self._non_lin_param1 is not None:
            conv_params_dict_dict["non_lin_param1"] = self._non_lin_param1
        if self._non_lin_param2 is not None:
            conv_params_dict_dict["non_lin_param2"] = self._non_lin_param2
        return conv_params_dict_dict
        
    #
    def to_dict_upload_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation.
                    
        :rtype:                     dict
        """
        
        conv_params_dict_dict: dict = {}
        if self._lin_conv_offset is not None:
            conv_params_dict_dict["lin-conv-offset"] = self._lin_conv_offset
        if self._lin_conv_slope is not None:
            conv_params_dict_dict["lin-conv-slope"] = self._lin_conv_slope
        if self._non_lin_param1 is not None:
            conv_params_dict_dict["non-lin-param1"] = self._non_lin_param1
        if self._non_lin_param2 is not None:
            conv_params_dict_dict["non-lin-param2"] = self._non_lin_param2
        return conv_params_dict_dict

    #
    def from_json(conv_params_dict_json: Any):

        """
        Create a ConvParamsDict object from json (dictonary or str).
        
        :param conv_params_dict_dict:        A json dictionary that contains the keys of a ConvParamsDict or a string representation of a json dictionary.
        :type conv_params_dict_dict:         Any             
        :rtype:                              ibmpairs.upload.ConvParamsDict
        :raises Exception:                   if not a dictionary or a string.
        """

        if isinstance(conv_params_dict_json, dict):
            conv_params_dict = ConvParamsDict.from_dict(conv_params_dict_json)
        elif isinstance(conv_params_dict_json, str):
            conv_params_dict_dict = json.loads(conv_params_dict_json)
            conv_params_dict = ConvParamsDict.from_dict(conv_params_dict_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(conv_params_dict_json), "conv_params_dict_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return conv_params_dict

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
        
    # 
    def to_json_upload_post(self):
        
        """
        Create a string representation of a json dictionary from the objects structure ready for a POSR operation.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict_upload_post())

#
class PdalPreprocessingJSON:
    #_type: str
    #_limits: str
    
    """
    A representation of an Upload PdalPreprocessingJSON.
    
    :param type:   Type.
    :type type:    str
    :param limits: Limits.
    :type limits:  str
    """

    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 type: str   = None, 
                 limits: str = None
                ):
        self._type   = type
        self._limits = limits
    
    #    
    def get_type(self):
        return self._type

    #
    def set_type(self, type):
        self._type = common.check_str(type)
    
    #    
    def del_type(self): 
        del self._type

    #    
    type = property(get_type, set_type, del_type)

    #    
    def get_limits(self):
        return self._limits

    #
    def set_limits(self, limits):
        self._limits = common.check_str(limits)
    
    #    
    def del_limits(self): 
        del self._limits

    #    
    limits = property(get_limits, set_limits, del_limits)

    #
    def from_dict(pdal_preprocessing_json_dict: Any):

        """
        Create a PDALPreprocessingJSON object from a dictionary.
        
        :param pdal_preprocessing_json_dict:    A dictionary that contains the keys of a PDALPreprocessingJSON.
        :type pdal_preprocessing_json_dict:     Any             
        :rtype:                                 ibmpairs.upload.PDALPreprocessingJSON
        :raises Exception:                      if not a dictionary.
        """
        
        type   = None
        limits = None
    
        common.check_dict(pdal_preprocessing_json_dict)
        if "type" in pdal_preprocessing_json_dict:
            if pdal_preprocessing_json_dict.get("type") is not None:
                type = common.check_str(pdal_preprocessing_json_dict.get("type"))
        if "limits" in pdal_preprocessing_json_dict:
            if pdal_preprocessing_json_dict.get("limits") is not None:
                limits = common.check_str(pdal_preprocessing_json_dict.get("limits"))
        return PdalPreprocessingJSON(type   = type,
                                     limits = limits
                                    )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        pdal_preprocessing_json_dict: dict = {}
        if self._type is not None:
            pdal_preprocessing_json_dict["type"] = self._type
        if self._limits is not None:
            pdal_preprocessing_json_dict["limits"] = self._limits
        return pdal_preprocessing_json_dict

    #
    def from_json(pdal_preprocessing_json_json: Any):

        """
        Create a PdalPreprocessingJSON object from json (dictonary or str).
        
        :param pdal_preprocessing_json_dict:        A json dictionary that contains the keys of a PdalPreprocessingJSON or a string representation of a json dictionary.
        :type pdal_preprocessing_json_dict:         Any             
        :rtype:                                     ibmpairs.upload.PdalPreprocessingJSON
        :raises Exception:                          if not a dictionary or a string.
        """

        if isinstance(pdal_preprocessing_json_json, dict):
            pdal_preprocessing_json = PdalPreprocessingJSON.from_dict(pdal_preprocessing_json_json)
        elif isinstance(pdal_preprocessing_json_json, str):
            pdal_preprocessing_json_dict = json.loads(pdal_preprocessing_json_json)
            pdal_preprocessing_json = PdalPreprocessingJSON.from_dict(pdal_preprocessing_json_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(pdal_preprocessing_json_json), "pdal_preprocessing_json_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return pdal_preprocessing_json

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())    
 

#
class Options:
    #_data_layers: List[str]
    #_n_pix_global_scale: int
    #_pdal_preprocessing_jsons: List[PdalPreprocessingJSON]
    #_raster_params: List[float]
    
    """
    A representation of an Upload Options.
    
    :param data_layers:              A list of Data Layer IDs yo upload to.
    :type data_layers:               List[str]
    :param n_pix_global_scale:       Number of Pixels Global Scale.
    :type n_pix_global_scale:        int
    :param pdal_preprocessing_jsons: A list of PDAL preprocessing steps.
    :type pdal_preprocessing_jsons:  List[ibmpairs.upload.PdalPreprocessingJSON]
    :param raster_params:            A list of raster preprocessing parameters.
    :type raster_params:             List[float]
    """

    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 data_layers: List[str]                                = None, 
                 n_pix_global_scale: int                               = None, 
                 pdal_preprocessing_jsons: List[PdalPreprocessingJSON] = None, 
                 raster_params: List[float]                            = None
                ):
        self._data_layers              = data_layers
        self._n_pix_global_scale       = n_pix_global_scale
        self._pdal_preprocessing_jsons = pdal_preprocessing_jsons
        self._raster_params            = raster_params

    #       
    def get_data_layers(self):
        return self._data_layers

    #
    def set_data_layers(self, data_layers):
        self._data_layers = common.check_class(data_layers, List[str])
        
    #    
    def del_data_layers(self): 
        del self._data_layers

    #    
    data_layers = property(get_data_layers, set_data_layers, del_data_layers)

    #    
    def get_n_pix_global_scale(self):
        return self._n_pix_global_scale

    #
    def set_n_pix_global_scale(self, n_pix_global_scale):
        self._n_pix_global_scale = common.check_int(n_pix_global_scale)
        
    #    
    def del_n_pix_global_scale(self): 
        del self._n_pix_global_scale

    #    
    n_pix_global_scale = property(get_n_pix_global_scale, set_n_pix_global_scale, del_n_pix_global_scale)
    
    # 
    def get_pdal_preprocessing_jsons(self):
        return self._pdal_preprocessing_jsons

    #
    def set_pdal_preprocessing_jsons(self, pdal_preprocessing_jsons):
        self._pdal_preprocessing_jsons = common.check_class(pdal_preprocessing_jsons, List[PdalPreprocessingJSON])

    #    
    def del_pdal_preprocessing_jsons(self): 
        del self._pdal_preprocessing_jsons

    #    
    pdal_preprocessing_jsons = property(get_pdal_preprocessing_jsons, set_pdal_preprocessing_jsons, del_pdal_preprocessing_jsons)
    
    #       
    def get_raster_params(self):
        return self._raster_params

    #
    def set_raster_params(self, raster_params):
        self._raster_params = common.check_class(raster_params, List[float])
        
    #    
    def del_raster_params(self): 
        del self._raster_params

    #    
    raster_params = property(get_raster_params, set_raster_params, del_raster_params)
    
    #
    def from_dict(options_dict: Any):

        """
        Create an Options object from a dictionary.
        
        :param options_dict:    A dictionary that contains the keys of an Options.
        :type options_dict:     Any             
        :rtype:                 ibmpairs.upload.Options
        :raises Exception:      if not a dictionary.
        """
        
        data_layers              = None
        n_pix_global_scale       = None
        pdal_preprocessing_jsons = None
        raster_params            = None
                
        common.check_dict(options_dict)
        if "data-layers" in options_dict:
            if options_dict.get("data-layers") is not None:
                data_layers = common.from_list(options_dict.get("data-layers"), common.check_str)
        elif "data_layers" in options_dict:
            if options_dict.get("data_layers") is not None:
                data_layers = common.from_list(options_dict.get("data_layers"), common.check_str)
        if "n-pix-global-scale" in options_dict:
            if options_dict.get("n-pix-global-scale") is not None:
                n_pix_global_scale = common.check_int(options_dict.get("n-pix-global-scale"))
        elif "n_pix_global_scale" in options_dict:
            if options_dict.get("n_pix_global_scale") is not None:
                n_pix_global_scale = common.check_int(options_dict.get("n_pix_global_scale"))
        if "pdal-preprocessing-jsons" in options_dict:
            if options_dict.get("pdal-preprocessing-jsons") is not None:
                pdal_preprocessing_jsons = common.from_list(options_dict.get("pdal-preprocessing-jsons"), PdalPreprocessingJSON.from_dict)
        elif "pdal_preprocessing_jsons" in options_dict:
            if options_dict.get("pdal_preprocessing_jsons") is not None:
                pdal_preprocessing_jsons = common.from_list(options_dict.get("pdal_preprocessing_jsons"), PdalPreprocessingJSON.from_dict)
        if "raster-params" in options_dict:
            if options_dict.get("raster-params") is not None:
                raster_params = common.from_list(options_dict.get("raster-params"), common.check_float)
        elif "raster_params" in options_dict:
            if options_dict.get("raster_params") is not None:
                raster_params = common.from_list(options_dict.get("raster_params"), common.check_float)
        return Options(data_layers              = data_layers,
                       n_pix_global_scale       = n_pix_global_scale,
                       pdal_preprocessing_jsons = pdal_preprocessing_jsons,
                       raster_params            = raster_params
                      )
    
    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        options_dict: dict = {}
        if self._data_layers is not None:
            options_dict["data_layers"] = self._data_layers
        if self._n_pix_global_scale is not None:
            options_dict["n_pix_global_scale"] = self._n_pix_global_scale
        if self._pdal_preprocessing_jsons is not None:
            options_dict["pdal_preprocessing_jsons"] = common.from_list(self._pdal_preprocessing_jsons, lambda item: common.class_to_dict(item, PdalPreprocessingJSON))
        if self._raster_params is not None:
            options_dict["raster_params"] = self._raster_params
        return options_dict
        
    #
    def to_dict_upload_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation.  
                  
        :rtype:                     dict
        """
        
        options_dict: dict = {}
        if self._data_layers is not None:
            options_dict["data-layers"] = self._data_layers
        if self._n_pix_global_scale is not None:
            options_dict["n-pix-global-scale"] = self._n_pix_global_scale
        if self._pdal_preprocessing_jsons is not None:
            options_dict["pdal-preprocessing-jsons"] = common.from_list(self._pdal_preprocessing_jsons, lambda item: common.class_to_dict(item, PdalPreprocessingJSON))
        if self._raster_params is not None:
            options_dict["raster-params"] = self._raster_params
        return options_dict

    #
    def from_json(options_json: Any):

        """
        Create an Options object from json (dictonary or str).
        
        :param options_dict:        A json dictionary that contains the keys of an Options or a string representation of a json dictionary.
        :type options_dict:         Any             
        :rtype:                     ibmpairs.upload.Options
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(options_json, dict):
            options = Options.from_dict(options_json)
        elif isinstance(options_json, str):
            options_dict = json.loads(options_json)
            options = Options.from_dict(options_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(options_json), "options_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return options

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict()) 
        
    #
    def to_json_upload_post(self):
        
        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict_upload_post()) 
    

#
class Preprocessing:
    #_type: str
    #_order: int
    #_options: Options
    
    """
    A representation of an Upload Preprocessing.
    
    :param type:    Type.
    :type type:     str
    :param order:   Order.
    :type order:    int
    :param options: Options.
    :type options:  ibmpairs.upload.Options
    """

    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 type: str        = None, 
                 order: int       = None, 
                 options: Options = None
                ):
        self._type    = type
        self._order   = order
        self._options = options
         
    #    
    def get_type(self):
        return self._type

    #
    def set_type(self, type):
        self._type = common.check_str(type)
        
    #    
    def del_type(self): 
        del self._type

    #    
    type = property(get_type, set_type, del_type)
    
    #    
    def get_order(self):
        return self._order

    #
    def set_order(self, order):
        self._order = common.check_int(order)
        
    #    
    def del_order(self): 
        del self._order

    #    
    order = property(get_order, set_order, del_order)
     
    #       
    def get_options(self):
        return self._options

    #
    def set_options(self, options):
        self._options = common.check_class(options, Options)
        
    #    
    def del_options(self): 
        del self._options

    #    
    options = property(get_options, set_options, del_options)
    
    #
    def from_dict(preprocessing_dict: Any):

        """
        Create an Preprocessing object from a dictionary.
        
        :param processing_dict:    A dictionary that contains the keys of an Preprocessing.
        :type processing_dict:     Any             
        :rtype:                    ibmpairs.upload.Preprocessing
        :raises Exception:         if not a dictionary.
        """
        
        type    = None
        order   = None
        options = None
                
        common.check_dict(preprocessing_dict)
        if "type" in preprocessing_dict:
            if preprocessing_dict.get("type") is not None:
                type = common.check_str(preprocessing_dict.get("type"))
        if "order" in preprocessing_dict:
            if preprocessing_dict.get("order") is not None:
                order = common.check_int(preprocessing_dict.get("order"))
        if "options" in preprocessing_dict:
            if preprocessing_dict.get("options") is not None:
                options = Options.from_dict(preprocessing_dict.get("options"))        
        return Preprocessing(type    = type,
                             order   = order,
                             options = options
                            )
    
    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        preprocessing_dict: dict = {}
        if self._type is not None:
            preprocessing_dict["type"] = self._type
        if self._order is not None:
            preprocessing_dict["order"] = self._order
        if self._options is not None:
            preprocessing_dict["options"] = common.class_to_dict(self._options, Options)
        return preprocessing_dict
      
    #
    def to_dict_upload_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation. 
                   
        :rtype:                     dict
        """
        
        preprocessing_dict: dict = {}
        if self._type is not None:
            preprocessing_dict["type"] = self._type
        if self._order is not None:
            preprocessing_dict["order"] = self._order
        if self._options is not None:
            preprocessing_dict["options"] = self._options.to_dict_upload_post()
        return preprocessing_dict

    #
    def from_json(preprocessing_json: Any):

        """
        Create a Preprocessing object from json (dictonary or str).
        
        :param preprocessing_dict:        A json dictionary that contains the keys of a Preprocessing or a string representation of a json dictionary.
        :type preprocessing_dict:         Any             
        :rtype:                           ibmpairs.upload.Preprocessing
        :raises Exception:                if not a dictionary or a string.
        """

        if isinstance(preprocessing_json, dict):
            preprocessing = Preprocessing.from_dict(preprocessing_json)
        elif isinstance(preprocessing_json, str):
            preprocessing_dict = json.loads(preprocessing_json)
            preprocessing = Preprocessing.from_dict(preprocessing_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(preprocessing_json), "preprocessing_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return preprocessing

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict()) 

    #
    def to_json_upload_post(self):
        
        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict_upload_post()) 

#
class Upload:
    # 
    #_client: cl.Client
    
    #_tracking_id: str
    
    #_delete_data: bool
    #_data_layer_id: List[int]
    #_hdf_type: List[str]
    #_conv: List[str]
    #_hdf_band_name: List[str]
    #_url: str
    #_timestamp: str
    #_file_type: str
    #_pairs_data_type: str
    #_pairs_dimension: List[str]
    #_band: List[int]
    #_input_no_data: str
    #_preprocessing: List[Preprocessing]
    #_ignore_tile: bool
    #_geospatial_projection: str
    #_conv_params_dict: List[ConvParamsDict]
    #_data_interpolation: str
    #_user_tag: str
    #_dimension_value: List[str]
    #_tile_y: int
    #_tile_x: int
    
    #_upload_status: UploadStatusResponse
    
    #_file_path: str
#    _storage
    #_storage_key: str
    #_delete: bool
    #_local: bool
    
    """
    A representation of a PAIRS Upload.
    
    :param client:                An instance of an ibmpairs.client.Client.
    :type client:                 ibmpairs.client.Client
    :param tracking_id:           A tracking ID number for an upload.
    :type tracking_id:            str
    :param delete_data:           Replace existing data from PAIRS.
    :type delete_data:            bool
    :param data_layer_id:         A list of Data Layer IDs to upload to.
    :type data_layer_id:          List[int]
    :param hdf_type:              A list of HDF type.
    :type hdf_type:               List[str]
    :param conv:                  A list of conv properties.
    :type conv:                   List[str]
    :param hdf_band_name:         A list of HDF band names.
    :type hdf_band_name:          List[str]
    :param url:                   URL.
    :type url:                    str
    :param timestamp:             A timestamp for the upload.
    :type timestamp:              str
    :param file_type:             Upload file type.
    :type file_type:              str
    :param pairs_data_type:       IBM PAIRs data type for the Upload.
    :type pairs_data_type:        str
    :param pairs_dimension:       A list of IBM PAIRS Data Layer Dimensions.
    :type pairs_dimension:        List[str]
    :param band:                  A list of bands.
    :type band:                   List[int]
    :param input_no_data:         The No Data value (or NAN) of the file to Upload.
    :type input_no_data:          str
    :param preprocessing:         A list of preprocessing steps to be applied to the Upload file.
    :type preprocessing:          List[ibmpairs.upload.Preprocessing]
    :param ignore_tile:           Ignore tile.
    :type ignore_tile:            bool
    :param geospatial_projection: The geospatial projection of the file to Upload.
    :type geospatial_projection:  str
    :param conv_params_dict:      A list of conversion parameter dictionaries.
    :type conv_params_dict:       List[ibmpairs.upload.ConvParamsDict]
    :param data_interpolation:    Data interpolation.
    :type data_interpolation:     str
    :param user_tag:              A user tag for the Upload.
    :type user_tag:               str
    :param dimension_value:       A list of dimension values.
    :type dimension_value:        List[str]
    :param tile_y:                The tile y value.
    :type tile_y:                 int
    :param tile_x:                The tile x value.
    :type tile_x:                 int
    :param upload_status:         A response to the status call.
    :type upload_status:          ibmpairs.upload.UploadStatusResponse
    :param file_path:             A path for the file to upload.
    :type file_path:              str
    :param storage:               A storage mechanism (currently only supports ibmpairs.external.ibm.IBMCOSBucket).
    :type storage:                ibmpairs.upload.UploadStatusResponse
    :param storage_key:           A storage key location for the file to upload (if None assume file_path).
    :type storage_key:            str
    :param delete:                Should the file be deleted from the storage mechanism afterwards?
    :type delete:                 bool
    :param local:                 Is the file local (i.e. does it need to be uploaded to the storage mechanism first).
    :type local:                  bool
    :raises Exception:            if an ibmpairs.client.Client is not provided or 
                                  found in the environment.
    """
    
    #_upload_status: UploadStatusResponse
    
    #_file_path: str
  #    _storage
    #_storage_key: str
    #_delete: bool
    #_local: bool

    #
    def __str__(self):
                
        """
        The method creates a string representation of the internal class structure.
        
        :returns:       A string representation of the internal class structure.
        :rtype:         str
        """
                                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
                
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:       A dict representation of the internal class structure.
        :rtype:         dict
        """
                
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self, 
                 client: cl.Client                      = None,
                 tracking_id: str                       = None,
                 delete_data: bool                      = None,
                 data_layer_id: List[int]               = None,
                 hdf_type: List[str]                    = None,
                 conv: List[str]                        = None,
                 hdf_band_name: List[str]               = None,
                 url: str                               = None,
                 timestamp: str                         = None,
                 file_type: str                         = None,
                 pairs_data_type: str                   = None,
                 pairs_dimension: List[str]             = None,
                 band: List[int]                        = None,
                 input_no_data: str                     = None,
                 preprocessing: List[Preprocessing]     = None, 
                 ignore_tile: bool                      = None, 
                 geospatial_projection: str             = None,
                 conv_params_dict: List[ConvParamsDict] = None,
                 data_interpolation: str                = None, 
                 user_tag: str                          = None,
                 dimension_value: List[int]             = None,
                 tile_y: int                            = None,
                 tile_x: int                            = None,
                 upload_status: UploadStatusResponse    = None,
                 file_path: str                         = None,
                 storage                                = None,
                 storage_key: str                       = None,
                 delete: bool                           = False,
                 local: bool                            = True
                ):
        self._client                = common.set_client(input_client  = client,
                                                        global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._tracking_id           = tracking_id
        self._delete_data           = delete_data
        self._data_layer_id         = data_layer_id
        self._hdf_type              = hdf_type
        self._conv                  = conv
        self._hdf_band_name         = hdf_band_name
        self._url                   = url
        self._timestamp             = timestamp
        self._file_type             = file_type
        self._pairs_data_type       = pairs_data_type
        self._pairs_dimension       = pairs_dimension
        self._band                  = band
        self._input_no_data         = input_no_data
        self._preprocessing         = preprocessing
        self._ignore_tile           = ignore_tile
        self._geospatial_projection = geospatial_projection
        self._conv_params_dict      = conv_params_dict
        self._data_interpolation    = data_interpolation
        self._user_tag              = user_tag
        self._dimension_value       = dimension_value
        self._tile_y                = tile_y
        self._tile_x                = tile_x
        
        if upload_status is None:
          self._upload_status       = UploadStatusResponse()
        else:
          self._upload_status       = upload_status
        
        self._file_path             = file_path
        self._storage               = storage
        self._storage_key           = storage_key
        self._delete                = delete
        self._local                 = local
    
    #
    def get_client(self):
        return self._client

    #
    def set_client(self, c):
        self._client = common.check_class(c, cl.Client)

    #    
    def del_client(self): 
        del self._client

    #    
    client = property(get_client, set_client, del_client)
    
    #
    def set_client_with_parameters(self,
                                   client: cl.Client = None,
                                   authentication    = None,
                                   host              = None
                                  ):
        if client is not None:
            self.set_client(client)
        
        if authentication is not None:
            self.client.set_authentication(authentication)
            
        if host is not None:
            self.client.set_host(host)
    
    #    
    def get_tracking_id(self):
        return self._tracking_id

    #
    def set_tracking_id(self, tracking_id):
        self._tracking_id = common.check_str(tracking_id)
        
    #    
    def del_tracking_id(self): 
        del self._tracking_id

    #    
    tracking_id = property(get_tracking_id, set_tracking_id, del_tracking_id)
    
    #    
    def get_delete_data(self):
        return self._delete_data

    #
    def set_delete_data(self, delete_data):
        self._delete_data = common.check_bool(delete_data)
        
    #    
    def del_delete_data(self): 
        del self._delete_data

    #    
    delete_data = property(get_delete_data, set_delete_data, del_delete_data)
    
    #       
    def get_data_layer_id(self):
        return self._data_layer_id

    #
    def set_data_layer_id(self, data_layer_id):
        self._data_layer_id = common.check_class(data_layer_id, List[int])
        
    #    
    def del_data_layer_id(self): 
        del self._data_layer_id

    #    
    data_layer_id = property(get_data_layer_id, set_data_layer_id, del_data_layer_id)
    
    #       
    def get_hdf_type(self):
        return self._hdf_type

    #
    def set_hdf_type(self, hdf_type):
        self._hdf_type = common.check_class(hdf_type, List[str])
        
    #    
    def del_hdf_type(self): 
        del self._hdf_type

    #    
    hdf_type = property(get_hdf_type, set_hdf_type, del_hdf_type)
    
    #       
    def get_conv(self):
        return self._conv

    #
    def set_conv(self, conv):
        self._conv = common.check_class(conv, List[str])
        
    #    
    def del_conv(self): 
        del self._conv

    #    
    conv = property(get_conv, set_conv, del_conv)
    
    #       
    def get_hdf_band_name(self):
        return self._hdf_band_name

    #
    def set_hdf_band_name(self, hdf_band_name):
        self._hdf_band_name = common.check_class(hdf_band_name, List[str])
        
    #    
    def del_hdf_band_name(self): 
        del self._hdf_band_name

    #    
    hdf_band_name = property(get_hdf_band_name, set_hdf_band_name, del_hdf_band_name)
    
    #    
    def get_url(self):
        return self._url

    #
    def set_url(self, url):
        self._url = common.check_str(url)
        
    #    
    def del_url(self): 
        del self._url

    #    
    url = property(get_url, set_url, del_url)
    
    #    
    def get_timestamp(self):
        return self._timestamp

    #
    def set_timestamp(self, timestamp):
        self._timestamp = common.check_str(timestamp)
        
    #    
    def del_timestamp(self): 
        del self._timestamp

    #    
    timestamp = property(get_timestamp, set_timestamp, del_timestamp)
    
    #    
    def get_file_type(self):
        return self._file_type

    #
    def set_file_type(self, file_type):
        self._file_type = common.check_str(file_type)
        
    #    
    def del_file_type(self): 
        del self._file_type

    #    
    file_type = property(get_file_type, set_file_type, del_file_type)
    
    #    
    def get_pairs_data_type(self):
        return self._pairs_data_type

    #
    def set_pairs_data_type(self, pairs_data_type):
        self._pairs_data_type = common.check_str(pairs_data_type)
        
    #    
    def del_pairs_data_type(self): 
        del self._pairs_data_type

    #    
    pairs_data_type = property(get_pairs_data_type, set_pairs_data_type, del_pairs_data_type)
    
    #       
    def get_pairs_dimension(self):
        return self._pairs_dimension

    #
    def set_pairs_dimension(self, pairs_dimension):
        self._pairs_dimension = common.check_class(pairs_dimension, List[str])
        
    #    
    def del_pairs_dimension(self): 
        del self._pairs_dimension

    #    
    pairs_dimension = property(get_pairs_dimension, set_pairs_dimension, del_pairs_dimension)
    
    #       
    def get_band(self):
        return self._band

    #
    def set_band(self, band):
        self._band = common.check_class(band, List[int])
        
    #    
    def del_band(self): 
        del self._band

    #    
    band = property(get_band, set_band, del_band)

    #    
    def get_input_no_data(self):
        return self._input_no_data

    #
    def set_input_no_data(self, input_no_data):
        self._input_no_data = common.check_str(input_no_data)
        
    #    
    def del_input_no_data(self): 
        del self._input_no_data

    #    
    input_no_data = property(get_input_no_data, set_input_no_data, del_input_no_data)
    
    # 
    def get_preprocessing(self):
        return self._preprocessing

    #
    def set_preprocessing(self, preprocessing):
        self._preprocessing = common.check_class(preprocessing, List[Preprocessing])

    #    
    def del_preprocessing(self): 
        del self._preprocessing

    #    
    preprocessing = property(get_preprocessing, set_preprocessing, del_preprocessing)
    
    #    
    def get_ignore_tile(self):
        return self._ignore_tile

    #
    def set_ignore_tile(self, ignore_tile):
        self._ignore_tile = common.check_bool(ignore_tile)
        
    #    
    def del_ignore_tile(self): 
        del self._ignore_tile

    #    
    ignore_tile = property(get_ignore_tile, set_ignore_tile, del_ignore_tile)
    
    #    
    def get_geospatial_projection(self):
        return self._geospatial_projection

    #
    def set_geospatial_projection(self, geospatial_projection):
        self._geospatial_projection = common.check_str(geospatial_projection)
        
    #    
    def del_geospatial_projection(self): 
        del self._geospatial_projection

    #    
    geospatial_projection = property(get_geospatial_projection, set_geospatial_projection, del_geospatial_projection)

    #       
    def get_conv_params_dict(self):
        return self._conv_params_dict

    #
    def set_conv_params_dict(self, conv_params_dict):
        self._conv_params_dict = common.check_class(conv_params_dict, List[ConvParamsDict])
        
    #    
    def del_conv_params_dict(self): 
        del self._conv_params_dict

    #    
    conv_params_dict = property(get_conv_params_dict, set_conv_params_dict, del_conv_params_dict)
    
    #    
    def get_data_interpolation(self):
        return self._data_interpolation

    #
    def set_data_interpolation(self, data_interpolation):
        self._data_interpolation = common.check_str(data_interpolation)
        
    #    
    def del_data_interpolation(self): 
        del self._data_interpolation

    #    
    data_interpolation = property(get_data_interpolation, set_data_interpolation, del_data_interpolation)
    
    #    
    def get_user_tag(self):
        return self._user_tag

    #
    def set_user_tag(self, user_tag):
        self._user_tag = common.check_str(user_tag)
        
    #    
    def del_user_tag(self): 
        del self._user_tag

    #    
    user_tag = property(get_user_tag, set_user_tag, del_user_tag)
    
    #       
    def get_dimension_value(self):
        return self._dimension_value

    #
    def set_dimension_value(self, dimension_value):
        self._dimension_value = common.check_class(dimension_value, List[str])
        
    #    
    def del_dimension_value(self): 
        del self._dimension_value

    #    
    dimension_value = property(get_dimension_value, set_dimension_value, del_dimension_value)

    #    
    def get_tile_y(self):
        return self._tile_y

    #
    def set_tile_y(self, tile_y):
        self._tile_y = common.check_int(tile_y)
        
    #    
    def del_tile_y(self): 
        del self._tile_y

    #    
    tile_y = property(get_tile_y, set_tile_y, del_tile_y)
    
    #    
    def get_tile_x(self):
        return self._tile_x

    #
    def set_tile_x(self, tile_x):
        self._tile_x = common.check_int(tile_x)
        
    #    
    def del_tile_x(self): 
        del self._tile_x

    #    
    tile_x = property(get_tile_x, set_tile_x, del_tile_x)
    
    #
    def get_upload_status(self):
        return self._upload_status

    #
    def set_upload_status(self, upload_status):
        self._upload_status = common.check_class(upload_status, UploadStatusResponse)

    #    
    def del_upload_status(self): 
        del self._upload_status

    #    
    upload_status = property(get_upload_status, set_upload_status, del_upload_status)
    
    #
    def get_file_path(self):
        return self._file_path

    #
    def set_file_path(self, file_path):
        self._file_path = common.check_str(file_path)

    #    
    def del_file_path(self): 
        del self._file_path

    #    
    file_path = property(get_file_path, set_file_path, del_file_path)

#TODO: Make storage addressable; check type within [].

    #
    def get_storage(self):
        return self._storage

    #
    def set_storage(self, storage):
        self._storage = storage

    #    
    def del_storage(self): 
        del self._storage

    #    
    storage = property(get_storage, set_storage, del_storage)
    
    #
    def get_storage_key(self):
        return self._storage_key

    #
    def set_storage_key(self, storage_key):
        self._storage_key = common.check_str(storage_key)

    #    
    def del_storage_key(self): 
        del self._storage_key

    #    
    storage_key = property(get_storage_key, set_storage_key, del_storage_key)
    
    #
    def get_delete(self):
        return self._delete

    #
    def set_delete(self, delete):
        self._delete = common.check_bool(delete)

    #    
    def del_delete(self): 
        del self._delete

    #    
    delete = property(get_delete, set_delete, del_delete)
    
    #
    def get_local(self):
        return self._local

    #
    def set_local(self, local):
        self._local = common.check_bool(local)

    #    
    def del_local(self): 
        del self._local

    #    
    local = property(get_local, set_local, del_local)
    
    #
    def from_dict(upload_dict: Any):

        """
        Create an Upload object from a dictionary.
        
        :param upload_dict:    A dictionary that contains the keys of an Upload.
        :type upload_dict:     Any
        :rtype:                ibmpairs.upload.Upload
        :raises Exception:     if not a dictionary.
        """
        
        tracking_id           = None
        delete_data           = None
        data_layer_id         = None
        hdf_type              = None
        conv                  = None
        hdf_band_name         = None
        url                   = None
        timestamp             = None
        file_type             = None
        pairs_data_type       = None
        pairs_dimension       = None
        band                  = None
        input_no_data         = None
        preprocessing         = None
        ignore_tile           = None
        geospatial_projection = None
        conv_params_dict      = None
        data_interpolation    = None
        user_tag              = None
        dimension_value       = None
        tile_y                = None
        tile_x                = None
        upload_status         = None
        file_path             = None
        storage               = None
        storage_key           = None
        delete                = None
        local                 = None
        
        common.check_dict(upload_dict)
        if "tracking_id" in upload_dict:
            if upload_dict.get("tracking_id") is not None:
                tracking_id = common.check_str(upload_dict.get("tracking_id")) 
        if "deletedata" in upload_dict:
            if upload_dict.get("deletedata") is not None:
                delete_data = common.check_bool(upload_dict.get("deletedata"))
        elif "delete_data" in upload_dict:
            if upload_dict.get("delete_data") is not None:
                delete_data = common.check_bool(upload_dict.get("delete_data"))
        if "datalayer_id" in upload_dict:
            if upload_dict.get("datalayer_id") is not None:
                data_layer_id = common.from_list(upload_dict.get("datalayer_id"), common.check_int)
        elif "data_layer_id" in upload_dict:
            if upload_dict.get("data_layer_id") is not None:
                data_layer_id = common.from_list(upload_dict.get("data_layer_id"), common.check_int)
        if "hdftype" in upload_dict:
            if upload_dict.get("hdftype") is not None:
                hdf_type = common.from_list(upload_dict.get("hdftype"), common.check_str)
        elif "hdf_type" in upload_dict:
            if upload_dict.get("hdf_type") is not None:
                hdf_type = common.from_list(upload_dict.get("hdf_type"), common.check_str)
        if "conv" in upload_dict:
            if upload_dict.get("conv") is not None:
                conv = common.from_list(upload_dict.get("conv"), common.check_str)
        if "hdfbandname" in upload_dict:
            if upload_dict.get("hdfbandname") is not None:
                hdf_band_name = common.from_list(upload_dict.get("hdfbandname"), common.check_str)
        elif "hdf_band_name" in upload_dict:
            if upload_dict.get("hdf_band_name") is not None:
                hdf_band_name = common.from_list(upload_dict.get("hdf_band_name"), common.check_str)
        if "url" in upload_dict:
            if upload_dict.get("url") is not None:
                url = common.check_str(upload_dict.get("url"))
        if "timestamp" in upload_dict:
            if upload_dict.get("timestamp") is not None:
                timestamp = common.check_str(upload_dict.get("timestamp"))
        if "filetype" in upload_dict:
            if upload_dict.get("filetype") is not None:
                file_type = common.check_str(upload_dict.get("filetype"))
        elif "file_type" in upload_dict:
            if upload_dict.get("file_type") is not None:
                file_type = common.check_str(upload_dict.get("file_type"))
        if "pairsdatatype" in upload_dict:
            if upload_dict.get("pairsdatatype") is not None:
                pairs_data_type = common.check_str(upload_dict.get("pairsdatatype"))
        elif "pairs_data_type" in upload_dict:
            if upload_dict.get("pairs_data_type") is not None:
                pairs_data_type = common.check_str(upload_dict.get("pairs_data_type"))
        if "pairsdimension" in upload_dict:
            if upload_dict.get("pairsdimension") is not None:
                pairs_dimension = common.from_list(upload_dict.get("pairsdimension"), common.check_str)
        elif "pairs_dimension" in upload_dict:
            if upload_dict.get("pairs_dimension") is not None:
                pairs_dimension = common.from_list(upload_dict.get("pairs_dimension"), common.check_str)
        if "band" in upload_dict:
            if upload_dict.get("band") is not None:
                band = common.from_list(upload_dict.get("band"), common.check_int)
        if "inputnodata" in upload_dict:
            if upload_dict.get("inputnodata") is not None:
                input_no_data = common.check_str(upload_dict.get("inputnodata"))
        elif "input_no_data" in upload_dict:
            if upload_dict.get("input_no_data") is not None:
                pairs_data_type = common.check_int(upload_dict.get("input_no_data"))
        if "preprocessing" in upload_dict:
            if upload_dict.get("preprocessing") is not None:
                preprocessing = common.from_list(upload_dict.get("preprocessing"), Preprocessing.from_dict)
        if "ignoretile" in upload_dict:
            if upload_dict.get("ignoretile") is not None:
                ignore_tile = common.check_bool(upload_dict.get("ignoretile"))
        elif "ignore_tile" in upload_dict:
            if upload_dict.get("ignore_tile") is not None:
                ignore_tile = common.check_bool(upload_dict.get("ignore_tile"))
        if "geospatialprojection" in upload_dict:
            if upload_dict.get("geospatialprojection") is not None:
                geospatial_projection = common.check_str(upload_dict.get("geospatialprojection"))
        elif "geospatial_projection" in upload_dict:
            if upload_dict.get("geospatial_projection") is not None:
                geospatial_projection = common.check_str(upload_dict.get("geospatial_projection"))
        if "conv_params_dict" in upload_dict:
            if upload_dict.get("conv_params_dict") is not None:
                conv_params_dict = common.from_list(upload_dict.get("conv_params_dict"), ConvParamsDict.from_dict)
        if "datainterpolation" in upload_dict:
            if upload_dict.get("datainterpolation") is not None:
                data_interpolation = common.check_str(upload_dict.get("datainterpolation"))
        elif "data_interpolation" in upload_dict:
            if upload_dict.get("data_interpolation") is not None:
                data_interpolation = common.check_str(upload_dict.get("data_interpolation"))
        if "user_tag" in upload_dict:
            if upload_dict.get("user_tag") is not None:
                user_tag = common.check_str(upload_dict.get("user_tag"))
        if "dimension_value" in upload_dict:
            if upload_dict.get("dimension_value") is not None:
                dimension_value = common.from_list(upload_dict.get("dimension_value"), common.check_str)
        if "tile_y" in upload_dict:
            if upload_dict.get("tile_y") is not None:
                tile_y = common.check_int(upload_dict.get("tile_y"))
        if "tile_x" in upload_dict:
            if upload_dict.get("tile_x") is not None:
                tile_x = common.check_int(upload_dict.get("tile_x"))
        if "upload_status" in upload_dict:
            if upload_dict.get("upload_status") is not None:
                upload_status = UploadStatusResponse.from_dict(upload_dict.get("upload_status"))
        if "file_path" in upload_dict:
            if upload_dict.get("file_path") is not None:
                file_path = common.check_str(upload_dict.get("file_path"))
        if "storage" in upload_dict:
            if upload_dict.get("storage") is not None:
                if isinstance(upload_dict.get("storage"), ibm_cos.IBMCOSBucket):
                    storage = ibm_cos.IBMCOSBucket.from_dict(upload_dict.get("storage"))
        if "storage_key" in upload_dict:
            if upload_dict.get("storage_key") is not None:
                storage_key = common.check_str(upload_dict.get("storage_key"))
        if "delete" in upload_dict:
            if upload_dict.get("delete") is not None:
                delete = common.check_bool(upload_dict.get("delete"))
        if "local" in upload_dict:
            if upload_dict.get("local") is not None:
                local = common.check_bool(upload_dict.get("local"))
        return Upload(tracking_id           = tracking_id,
                      delete_data           = delete_data,
                      data_layer_id         = data_layer_id,
                      hdf_type              = hdf_type,
                      conv                  = conv,
                      hdf_band_name         = hdf_band_name,
                      url                   = url,
                      timestamp             = timestamp,
                      file_type             = file_type,
                      pairs_data_type       = pairs_data_type,
                      pairs_dimension       = pairs_dimension,
                      band                  = band,
                      input_no_data         = input_no_data,
                      preprocessing         = preprocessing,
                      ignore_tile           = ignore_tile,
                      geospatial_projection = geospatial_projection,
                      conv_params_dict      = conv_params_dict,
                      data_interpolation    = data_interpolation,
                      user_tag              = user_tag,
                      dimension_value       = dimension_value,
                      tile_y                = tile_y,
                      tile_x                = tile_x,
                      upload_status         = upload_status,
                      file_path             = file_path,
                      storage               = storage,
                      storage_key           = storage_key,
                      delete                = delete,
                      local                 = local
                     )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        upload_dict: dict = {}
        
        if self._tracking_id is not None:
            upload_dict["tracking_id"] = self._tracking_id
        if self._delete_data is not None:
            upload_dict["delete_data"] = self._delete_data
        if self._data_layer_id is not None:
            #upload_dict["data_layer_id"] = self._data_layer_id
            upload_dict["data_layer_id"] = common.from_list(self._data_layer_id, lambda item: common.check_int(item))
        if self._hdf_type is not None:
            #upload_dict["hdf_type"] = self._hdf_type
            upload_dict["hdf_type"] = common.from_list(self._hdf_type, lambda item: common.check_str(item))
        if self._conv is not None:
            #upload_dict["conv"] = self._conv
            upload_dict["conv"] = common.from_list(self._conv, lambda item: common.check_str(item))
        if self._hdf_band_name is not None:
            #upload_dict["hdf_band_name"] = self._hdf_band_name
            upload_dict["hdf_band_name"] = common.from_list(self._hdf_band_name, lambda item: common.check_str(item))
        if self._url is not None:
            upload_dict["url"] = self._url
        if self._timestamp is not None:
            upload_dict["timestamp"] = self._timestamp
        if self._file_type is not None:
            upload_dict["file_type"] = self._file_type
        if self._pairs_data_type is not None:
            upload_dict["pairs_data_type"] = self._pairs_data_type
        if self._pairs_dimension is not None:
            #upload_dict["pairs_dimension"] = self._pairs_dimension
            upload_dict["pairs_dimension"] = common.from_list(self._pairs_dimension, lambda item: common.check_str(item))
        if self._band is not None:
            #upload_dict["band"] = self._band
            upload_dict["band"] = common.from_list(self._band, lambda item: common.check_int(item))
        if self._input_no_data is not None:
            upload_dict["input_no_data"] = self._input_no_data
        if self._preprocessing is not None:
            upload_dict["preprocessing"] = common.from_list(self._preprocessing, lambda item: common.class_to_dict(item, Preprocessing))
        if self._ignore_tile is not None:
            upload_dict["ignore_tile"] = self._ignore_tile
        if self._geospatial_projection is not None:
            upload_dict["geospatial_projection"] = self._geospatial_projection
        if self._conv_params_dict is not None:
            upload_dict["conv_params_dict"] = common.from_list(self._conv_params_dict, lambda item: common.class_to_dict(item, ConvParamsDict))
        if self._data_interpolation is not None:
            upload_dict["data_interpolation"] = self._data_interpolation
        if self._user_tag is not None:
            upload_dict["user_tag"] = self._user_tag
        if self._dimension_value is not None:
            #upload_dict["dimension_value"] = self._dimension_value
            upload_dict["dimension_value"] = common.from_list(self._dimension_value, lambda item: common.check_str(item))
        if self._tile_y is not None:
            upload_dict["tile_y"] = self._tile_y
        if self._tile_x is not None:
            upload_dict["tile_x"] = self._tile_x
        if self._upload_status is not None:
            upload_dict["upload_status"] = common.class_to_dict(self._upload_status, UploadStatusResponse)
        if self._file_path is not None:
            upload_dict["file_path"] = self._file_path
        if self._storage is not None:
            if isinstance(self._storage, ibm_cos.IBMCOSBucket):
                upload_dict["storage"] = common.class_to_dict(self._storage, ibm_cos.IBMCOSBucket)
        if self._storage_key is not None:
          upload_dict["storage_key"] = self._storage_key
        if self._delete is not None:
            upload_dict["delete"] = self._delete
        if self._local is not None:
            upload_dict["local"] = self._local
        return upload_dict
        
    #
    def to_dict_upload_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation. 
                   
        :rtype:                     dict
        """
        
        upload_dict: dict = {}
        if self._delete_data is not None:
            upload_dict["deletedata"] = self._delete_data
        if self._data_layer_id is not None:
            #upload_dict["datalayer_id"] = self._data_layer_id
            upload_dict["datalayer_id"] = common.from_list(self._data_layer_id, lambda item: common.check_int(item))
        if self._hdf_type is not None:
            #upload_dict["hdftype"] = self._hdf_type
            upload_dict["hdftype"] = common.from_list(self._hdf_type, lambda item: common.check_str(item))
        if self._conv is not None:
            #upload_dict["conv"] = self._conv
            upload_dict["conv"] = common.from_list(self._conv, lambda item: common.check_str(item))
        if self._hdf_band_name is not None:
            #upload_dict["hdfbandname"] = self._hdf_band_name
            upload_dict["hdfbandname"] = common.from_list(self._hdf_band_name, lambda item: common.check_str(item))
        if self._url is not None:
            upload_dict["url"] = self._url
        if self._timestamp is not None:
            upload_dict["timestamp"] = self._timestamp
        if self._file_type is not None:
            upload_dict["filetype"] = self._file_type
        if self._pairs_data_type is not None:
            upload_dict["pairsdatatype"] = self._pairs_data_type
        if self._pairs_dimension is not None:
            #upload_dict["pairsdimension"] = self._pairs_dimension
            upload_dict["pairsdimension"] = common.from_list(self._pairs_dimension, lambda item: common.check_str(item))
        if self._band is not None:
            #upload_dict["band"] = self._band
            upload_dict["band"] = common.from_list(self._band, lambda item: common.check_int(item))
        if self._input_no_data is not None:
            upload_dict["inputnodata"] = self._input_no_data
        if self._preprocessing is not None:
#            upload_dict["preprocessing"] = common.from_list(self._preprocessing, lambda item: common.class_to_dict(item, Preprocessing))
            upload_dict["preprocessing"] = common.from_list(self._preprocessing, lambda item: item.to_dict_upload_post())
        if self._ignore_tile is not None:
            upload_dict["ignoretile"] = self._ignore_tile
        if self._geospatial_projection is not None:
            upload_dict["geospatialprojection"] = self._geospatial_projection
        if self._conv_params_dict is not None:
#            upload_dict["conv_params_dict"] = common.from_list(self._conv_params_dict, lambda item: common.class_to_dict(item, ConvParamsDict))
            upload_dict["conv_params_dict"] = common.from_list(self._conv_params_dict, lambda item: item.to_dict_upload_post())
        if self._data_interpolation is not None:
            upload_dict["datainterpolation"] = self._data_interpolation
        if self._user_tag is not None:
            upload_dict["user_tag"] = self._user_tag
        if self._dimension_value is not None:
            #upload_dict["dimension_value"] = self._dimension_value
            upload_dict["dimension_value"] = common.from_list(self._dimension_value, lambda item: common.check_str(item))
        if self._tile_y is not None:
            upload_dict["tile_y"] = self._tile_y
        if self._tile_x is not None:
            upload_dict["tile_x"] = self._tile_x
        return upload_dict

    #
    def from_json(upload_json: Any):
        """
        Create an Upload object from json (dictonary or str).
        
        :param upload_dict:         A json dictionary that contains the keys of an Upload or a string representation of a json dictionary.
        :type upload_dict:          Any             
        :rtype:                     ibmpairs.upload.Upload
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(upload_json, dict):
            upload = Upload.from_dict(upload_json)
        elif isinstance(upload_json, str):
            upload_dict = json.loads(upload_json)
            upload = Upload.from_dict(upload_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(upload_json), "upload_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return upload

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
        
    #
    def to_json_upload_post(self):
        
        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation. 
                   
        :rtype:                     string
        """

        return json.dumps(self.to_dict_upload_post())
        
    def check_local_file(self,
                         file_path
                        ):
                          
        """
        A method to check if a local file exists. 
        
        :param file_path: A file path.
        :type file_path:  str
        :returns:         A flag to state whether local file is found.       
        :rtype:           bool
        """
        
        if os.path.isfile(file_path):
            return True
        return False
    
    #
    def get_metadata(self,
                     storage,
                     storage_key
                    ):
        
        """
        A method to get a metadata file from a storage backend. 
        
        :param storage:     A storage backend.
        :type storage:      Any
        :param storage_key: A storage key.
        :type storage_key:  str
        :returns:           A dictionary of metadata.       
        :rtype:             dict
        :raises Exception:  If the metadata could not be found.
        """
        
        metadata_storage_key = storage_key + constants.UPLOAD_METADATA_FILE_EXTENTION
        logger.debug("metadata_storage_key " + metadata_storage_key)
        metadata_object = storage.get(key = str(metadata_storage_key))
        try:
            metadata_json_string = metadata_object['Body'].read().decode("utf-8")
            return json.loads(metadata_json_string)
        except:
            provider          = ""
            storage_type      = ""
            storage_structure = ""
            storage_name      = ""

            if isinstance(storage, ibm_cos.IBMCOSBucket):
                provider          = "IBM"
                storage_type      = "Cloud Object Storage"
                storage_structure = "Bucket"
                storage_name      = storage.bucket
            
            msg = messages.ERROR_UPLOAD_STORAGE_METADATA_COULD_NOT_BE_LOADED.format(storage_key, provider, storage_type, storage_structure, storage_name)
            logger.error(msg)
            raise common.PAWException(msg)

    #
    def submit(self,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to submit an Upload.

        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              upload storage type not recognized, 
                              no upload storage defined, 
                              error making request to server, 
                              the status of the request is not 201.
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            msg = messages.DEBUG_FOUND_EVENT_LOOP
            logger.debug(msg)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("submit")
            logger.info(msg)
            
            common.run_async_in_thread(self.async_submit, upload = self, 
                                                          client = cli,
                                                          verify = verify)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("submit")
            logger.info(msg)
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_submit(upload = self, 
                                          client = cli,
                                          verify = verify
                                         )
                       )

    #
    def status(self,
               client: cl.Client    = None,
               tracking_id          = None,
               poll: bool           = True,
               status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
               verify: bool         = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to check the status of an Upload.
        
        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param tracking_id:     A tracking ID (if checking a previously run upload)
        :type tracking_id:      str
        :param poll:            Whether the status check should poll until completion.
        :type poll:             bool
        :param status_interval: The status interval for the run to perform a call back.
        :type status_interval:  bool
        :param verify:          SSL verification
        :type verify:           bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                error making request to server, 
                                the status of the request is not 200.
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        if tracking_id is not None:
            self.tracking_id = tracking_id
        
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            msg = messages.DEBUG_FOUND_EVENT_LOOP
            logger.debug(msg)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("status")
            logger.info(msg)
            
            common.run_async_in_thread(self.async_status, upload          = self,
                                                          client          = cli,
                                                          poll            = poll,
                                                          status_interval = status_interval,
                                                          verify          = verify)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("status")
            logger.info(msg)
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_status(upload          = self,
                                          client          = cli,
                                          poll            = poll,
                                          status_interval = status_interval,
                                          verify          = verify
                                          )
                       )
    
    #
    def submit_and_check_status(self,
                                client: cl.Client    = None,
                                poll: bool           = True,
                                status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
                                verify: bool         = constants.GLOBAL_SSL_VERIFY
                               ):
                                
        """
        A method to submit and check the status of an Upload.
        
        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param poll:            Whether the status check should poll until completion.
        :type poll:             bool
        :param status_interval: The status interval for the run to perform a call back.
        :type status_interval:  bool
        :param verify:          SSL verification
        :type verify:           bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                upload storage type not recognized, 
                                no upload storage defined, 
                                error making request to server, 
                                the status of the request is not 201 (submit), 
                                the status of the request is not 200 (status).
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            msg = messages.DEBUG_FOUND_EVENT_LOOP
            logger.debug(msg)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("submit_and_check_status")
            logger.info(msg)
            
            common.run_async_in_thread(self.async_submit_and_check_status, upload          = self,
                                                                           client          = cli,
                                                                           poll            = poll,
                                                                           status_interval = status_interval,
                                                                           verify          = verify)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("submit_and_check_status")
            logger.info(msg)
            
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_submit_and_check_status(upload          = self,
                                                           client          = cli,
                                                           poll            = poll,
                                                           status_interval = status_interval,
                                                           verify          = verify
                                                          )
                       )
            
    async def async_submit(self,
                           upload,
                           client: cl.Client = None,
                           verify: bool      = constants.GLOBAL_SSL_VERIFY
                          ):
                            
        """
        An asynchronous method to submit an Upload.
        
        :param upload:        The Upload to submit.
        :type upload:         ibmpairs.upload.Upload
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              upload storage type not recognized, 
                              no upload storage defined, 
                              error making request to server, 
                              the status of the request is not 201.
        """
                            
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        # The key for the file, unless provided, is the file name from the `file_path`
        if upload.storage_key is None:
            f_path = Path(upload.file_path)
            upload.storage_key = f_path.name
        
        if upload.storage is not None:
            if isinstance(upload.storage, ibm_cos.IBMCOSBucket):
                # Generate a presigned url and assign to url attribute.
                upload.url = upload.storage.get_presigned_url(key = upload.storage_key)
                # Get the metadata json (previously uploaded, either with local flag or
                # by user, from the IBM COS Bucket. 
                try:
                    msg = messages.DEBUG_UPLOAD_SUBMIT_SEARCH_METADATA.format(upload.storage_key + constants.UPLOAD_METADATA_FILE_EXTENTION)
                    logger.debug(msg)
                    upload_metadata = self.get_metadata(storage = upload.storage, 
                                                        storage_key = upload.storage_key
                                                       )
                    upload_metadata["url"] = upload.url
                
                    up = Upload.from_dict(upload_metadata)
                    upload_json = up.to_dict_upload_post()
                    msg = messages.DEBUG_UPLOAD_SUBMIT_FOUND_METADATA.format(upload.storage_key + constants.UPLOAD_METADATA_FILE_EXTENTION, upload_json)
                    logger.debug(msg)
                except:
                    upload_json = upload.to_dict_upload_post()
                    msg = messages.DEBUG_UPLOAD_SUBMIT_NO_METADATA_IN_STORAGE.format(upload.storage_key + constants.UPLOAD_METADATA_FILE_EXTENTION, upload.to_dict_upload_post())
                    logger.info(msg)
            else:
                msg = messages.ERROR_UPLOAD_STORAGE_NOT_RECOGNISED.format(upload.storage)
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            msg = messages.INFO_UPLOAD_STORAGE_NOT_PRESENT
            logger.info(msg)
            # If storage is none, assume object contains metadata (inc. a valid url).
            upload_json = upload.to_dict_upload_post()

        # If the file is local, upload first.
        if upload.local:
            upload.storage.upload(file_name = upload.file_path,
                                  key       = upload.storage_key
                                 )
            # If the meta.json file is not contained within the local directory, flush
            # the attributes of the object to a file on disk and upload.
            if self.check_local_file(upload.file_path + constants.UPLOAD_METADATA_FILE_EXTENTION) == False:
                with open(upload.file_path + constants.UPLOAD_METADATA_FILE_EXTENTION, "w") as f:
                    f.write(upload.to_json_upload_post())
            upload.storage.upload(file_name = upload.file_path + constants.UPLOAD_METADATA_FILE_EXTENTION,
                                  key       = upload.storage_key + constants.UPLOAD_METADATA_FILE_EXTENTION
                                 )
        
        try:
            response = await cli.async_post(url     = cli.get_host() + 
                                                         constants.UPLOAD_API,
                                            headers = constants.CLIENT_PUT_AND_POST_HEADER,
                                            body    = upload_json,
                                            verify  = verify
                                           )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('POST', 'request', cli.get_host() + constants.UPLOAD_API, e)
            logger.error(msg)
            response = cl.ClientResponse(status = -999, 
                                         body = r"""{"message":"Unspecified Server Error"}"""
                                        )

        logger.info(response.status)

        if response.status != 201:
            error_message = 'failed'
            
            if response.body is not None:
                try:
                    upload_response = upload_response_from_json(response.body)
                    error_message = upload_response.message
                except:
                    msg = messages.INFO_UPLOAD_RESPONSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_UPLOAD_RESPOSE_NOT_SUCCESSFUL.format('POST', 'request', constants.UPLOAD_API, response.status, error_message)
            logger.error(msg)
            upload.upload_status.status = 'FAILED'
            raise common.PAWException(msg)
        else:
            upload_response = upload_response_from_json(response.body)
            
            upload.tracking_id = upload_response.id

            msg = messages.INFO_UPLOAD_SUBMIT_SUCCESS.format(str(upload.tracking_id))
            logger.info(msg)

        if upload.delete:
            upload.storage.delete(key = upload.storage_key)
        

    async def async_status(self,
                           upload,
                           client: cl.Client    = None,
                           poll: bool           = True,
                           status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
                           verify: bool         = constants.GLOBAL_SSL_VERIFY
                          ):
                            
        """
        An asynchronous method to check the status of an Upload.
        
        :param upload:          The Upload to check the status of.
        :type upload:           ibmpairs.upload.Upload
        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param poll:            Whether the status check should poll until completion.
        :type poll:             bool
        :param status_interval: The status interval for the run to perform a call back.
        :type status_interval:  bool
        :param verify:          SSL verification
        :type verify:           bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                error making request to server, 
                                the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        incomplete = True

        while incomplete:
            
            try:
                response = await cli.async_get(url    = cli.get_host() +
                                                        constants.UPLOAD_STATUS_API +
                                                        upload.tracking_id,
                                               verify = verify
                                              )
            except Exception as e:
                msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.UPLOAD_STATUS_API + str(upload.tracking_id), e)
                logger.error(msg)
                response = cl.ClientResponse(status = -999, 
                                             body = r"""{"message":"Unspecified Server Error"}"""
                                            )
          
            if response.status == 200:
                
                upload.upload_status = upload_status_response_from_json(response.body)
                
                msg = messages.INFO_UPLOAD_STATUS.format(upload.tracking_id, upload.upload_status.status)
                logger.info(msg)
                
                if poll == False:
                    incomplete = False
                
                if upload.upload_status.status == 'SUCCEEDED':
                    msg = messages.INFO_UPLOAD_SUCCESS.format(upload.tracking_id)
                    logger.info(msg)
                    incomplete = False
                elif upload.upload_status.status == 'FAILED':
                    msg = messages.ERROR_UPLOAD_FAILED.format(upload.tracking_id, upload.upload_status.status)
                    logger.error(msg)
                    incomplete = False
                
                if upload.upload_status.summary:
                    for single_upload_status in upload.upload_status.summary:
                        if single_upload_status.status < 0:
                            upload.upload_status.status = 'FAILED'
                            msg = messages.ERROR_UPLOAD_FAILED.format(upload.tracking_id, upload.upload_status.status)
                            logger.error(msg)
                            incomplete = False

            elif response.status == 400:
                # Cannot identify upload with tracking ID
                msg = messages.ERROR_UPLOAD_STATUS_INCORRECT_TRACKING_ID
                logger.error(msg)
                upload.upload_status.status = 'FAILED'
                incomplete = False
            elif response.status == 401:
                msg = messages.ERROR_UPLOAD_STATUS_NOT_AUTHORIZED
                logger.error(msg)
                upload.upload_status.status = 'FAILED'
                incomplete = False
            else:
                msg = messages.ERROR_UPLOAD_STATUS_HTTP_RESPONSE_CODE.format(response.status)
                logger.error(msg)
                upload.upload_status.status = 'FAILED'
                incomplete = False

            if poll == True:
                await asyncio.sleep(status_interval)

    async def async_submit_and_check_status(self,
                                            upload,
                                            client: cl.Client,
                                            poll: bool           = True,
                                            status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
                                            verify: bool         = constants.GLOBAL_SSL_VERIFY
                                           ):
        
        """
        An asynchronous method to submit and check the status of an Upload.
        
        :param upload:          The Upload to check the status of.
        :type upload:           ibmpairs.upload.Upload
        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param poll:            Whether the status check should poll until completion.
        :type poll:             bool
        :param status_interval: The status interval for the run to perform a call back.
        :type status_interval:  bool
        :param verify:          SSL verification
        :type verify:           bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                upload storage type not recognized, 
                                no upload storage defined, 
                                error making request to server, 
                                the status of the request is not 201 (submit), 
                                the status of the request is not 200 (status).
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        await self.async_submit(upload = upload, 
                                client = cli,
                                verify = verify
                               )

        await self.async_status(upload          = upload, 
                                client          = cli,
                                poll            = poll,
                                status_interval = status_interval,
                                verify          = verify
                               )

#        
async def upload_worker(uploads: List[Upload],
                        client: cl.Client,
                        status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
                        workers: int         = UPLOAD_DEFAULT_WORKERS,
                        verify: bool         = constants.GLOBAL_SSL_VERIFY
                       ):
                        
    """
    An asynchronous method to operate and await a number of submit and status calls.
    
    :param uploads:         A list of uploads.
    :type uploads:          List[ibmpairs.upload.Upload]
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param status_interval: How often the async run operation should call back.
    :type status_interval:  int
    :param workers:         How many async operations should run contemporaneously.
    :type workers:          int
    :param verify:          SSL verification
    :type verify:           bool
    :returns:               A list of queries.
    :rtype:                 List[ibmpairs.upload.Upload]
    """
    
    cli = common.set_client(input_client  = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)

    cli.session()

    tasks = set()
    for upload in uploads:
        if len(tasks) >= workers:
            # Wait for some download to finish before adding a new one
            _done, tasks = await asyncio.wait(tasks, 
                                              return_when = asyncio.FIRST_COMPLETED
                                             )

        tasks.add(asyncio.create_task(upload.async_submit_and_check_status(upload = upload, 
                                                                           client = cli,
                                                                           status_interval = status_interval,
                                                                           verify = verify
                                                                          )))

    # Wait for the remaining uploads to finish
    await asyncio.wait(tasks)

    return(uploads)

#
def batch_upload(uploads: List[Upload],
                 client: cl.Client    = None,
                 status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
                 workers: int         = UPLOAD_DEFAULT_WORKERS,
                 verify: bool         = constants.GLOBAL_SSL_VERIFY
                ):
                  
    """
    A method to submit and track a number of batched uploads using the upload_worker method.
    
    :param uploads:         A list of uploads.
    :type uploads:          List[ibmpairs.upload.Upload]
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param status_interval: How often the async run operation should call back.
    :type status_interval:  int
    :param workers:         How many async operations should run contemporaneously.
    :type workers:          int
    :param verify:          SSL verification
    :type verify:           bool
    :returns:               A list of uploads.
    :rtype:                 List[ibmpairs.upload.Upload]
    """
                  
    cli = common.set_client(input_client  = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)

    if status_interval < constants.UPLOAD_MIN_STATUS_INTERVAL:
        msg = messages.ERROR_UPLOAD_STATUS_INTERVAL.format(status_interval, constants.UPLOAD_MIN_STATUS_INTERVAL)
        logger.error(msg)
        raise common.PAWException(msg)

    if workers > constants.UPLOAD_MAX_WORKERS:
        msg = messages.ERROR_UPLOAD_EXCEED_MAX_WORKERS.format(workers, constants.UPLOAD_MAX_WORKERS)
        logger.error(msg)
        raise common.PAWException(msg)

    #logger.debug('Commencing upload run.')
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        msg = messages.DEBUG_FOUND_EVENT_LOOP
        logger.debug(msg)
        
        msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("batch_upload")
        logger.info(msg)
        
        result = common.run_async_in_thread(upload_worker, uploads         = uploads, 
                                                           client          = cli,
                                                           status_interval = status_interval,
                                                           workers         = workers,
                                                           verify          = verify
                                           )
        
        msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("batch_upload")
        logger.info(msg)
    else:
        msg = messages.INFO_STARTING_EVENT_LOOP
        logger.info(msg)
        result = asyncio.run(upload_worker(uploads         = uploads, 
                                           client          = cli,
                                           status_interval = status_interval,
                                           workers         = workers,
                                           verify          = verify
                                          ),
                              debug = constants.UPLOAD_WORKER_DEBUG
                             )

    return(result)
    
def submit(upload: Any,
           client: cl.Client = None,
           file_path: str    = None,
           storage           = None,
           storage_key: str  = None,
           delete: bool      = None,
           local: bool       = None,
           verify: bool      = constants.GLOBAL_SSL_VERIFY
          ):
            
    """
    A helper method to submit an Upload.
    
    :param upload:        An upload to submit.
    :type upload:         ibmpairs.upload.Upload or dict or str
    :param client:        An IBM PAIRS Client.
    :type client:         ibmpairs.client.Client
    :param file_path:     A path for the file to upload.
    :type file_path:      str
    :param storage:       A storage mechanism (currently only supports ibmpairs.external.ibm.IBMCOSBucket).
    :type storage:        Any
    :param storage_key:   A storage key location for the file to upload (if None assume file_path).
    :type storage_key:    str
    :param delete:        Should the file be deleted from the storage mechanism afterwards?
    :type delete:         bool
    :param local:         Is the file local (i.e. does it need to be uploaded to the storage mechanism first).
    :type local:          bool
    :param verify:        SSL verification
    :type verify:         bool
    :returns:             An upload object.
    :rtype:               ibmpairs.upload.Upload
    :raises Exception:    A ibmpairs.client.Client is not found, 
                          error making request to server, 
                          the status of the request is not 200, 
                          the type or format of Upload is incorrect.
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(upload, Upload):
        pass
    elif isinstance(upload, dict):
        upload = upload_from_dict(upload)
    elif isinstance(upload, str):
        upload = upload_from_json(upload)
    else:
        msg = messages.ERROR_UPLOAD_TYPE_NOT_RECOGNIZED.format(type(upload))
        logger.error(msg)
        raise common.PAWException(msg)
        
    if file_path is not None:
        upload.file_path = file_path
    if storage is not None:
        upload.storage = storage
    if storage_key is not None:
        upload.storage_key = storage_key
    if delete is not None:
        upload.delete = delete
    if local is not None:
        upload.local = local
        
    upload.submit(client = cli,
                  verify = verify
                 )
    
    return upload

def status(upload: Any          = None,
           client: cl.Client    = None,
           tracking_id          = None,
           poll: bool           = True,
           status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
           verify: bool         = constants.GLOBAL_SSL_VERIFY
          ):
    
    """
    A helper method to check the status of an Upload.
    
    :param upload:          An upload to submit.
    :type upload:           ibmpairs.upload.Upload or dict or str
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param tracking_id:     A tracking ID (if checking a previously run upload)
    :type tracking_id:      str
    :param poll:            Whether the status check should poll until completion.
    :type poll:             bool
    :param status_interval: The status interval for the run to perform a call back.
    :type status_interval:  bool
    :param verify:          SSL verification
    :type verify:           bool
    :returns:               An upload object.
    :rtype:                 ibmpairs.upload.Upload
    :raises Exception:      A ibmpairs.client.Client is not found, 
                            error making request to server, 
                            the status of the request is not 200.
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(upload, Upload):
        pass
    elif isinstance(upload, dict):
        upload = upload_from_dict(upload)
    elif isinstance(upload, str):
        upload = upload_from_json(upload)
    else:
        upload = Upload()
        
    upload.status(client          = cli,
                  tracking_id     = tracking_id,
                  poll            = poll,
                  status_interval = status_interval,
                  verify          = verify
                 )
    
    return upload
    
def submit_and_check_status(upload: Any          = None,
                            client: cl.Client    = None,
                            file_path: str       = None,
                            storage              = None,
                            storage_key: str     = None,
                            delete: bool         = None,
                            local: bool          = None,
                            poll: bool           = True,
                            status_interval: int = UPLOAD_STATUS_CHECK_INTERVAL,
                            verify: bool         = constants.GLOBAL_SSL_VERIFY
                           ):
    
    """
    A helper method to submit and check the status of an Upload.
      
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param file_path:       A path for the file to upload.
    :type file_path:        str
    :param storage:         A storage mechanism (currently only supports ibmpairs.external.ibm.IBMCOSBucket).
    :type storage:          Any
    :param storage_key:     A storage key location for the file to upload (if None assume file_path).
    :type storage_key:      str
    :param delete:          Should the file be deleted from the storage mechanism afterwards?
    :type delete:           bool
    :param local:           Is the file local (i.e. does it need to be uploaded to the storage mechanism first).
    :type local:            bool
    :param poll:            Whether the status check should poll until completion.
    :type poll:             bool
    :param status_interval: The status interval for the run to perform a call back.
    :type status_interval:  bool
    :param verify:          SSL verification
    :type verify:           bool
    :returns:               An upload object.
    :rtype:                 ibmpairs.upload.Upload
    :raises Exception:      A ibmpairs.client.Client is not found, 
                            upload storage type not recognized, 
                            no upload storage defined, 
                            error making request to server, 
                            the status of the request is not 201 (submit), 
                            the status of the request is not 200 (status).
    """
    
    cli = common.set_client(input_client = client,
                global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(upload, Upload):
        pass
    elif isinstance(upload, dict):
        upload = upload_from_dict(upload)
    elif isinstance(upload, str):
        upload = upload_from_json(upload)
    else:
        msg = messages.ERROR_UPLOAD_TYPE_NOT_RECOGNIZED.format(type(upload))
        logger.error(msg)
        raise common.PAWException(msg)
      
    if file_path is not None:
        upload.file_path = file_path
    if storage is not None:
        upload.storage = storage
    if storage_key is not None:
        upload.storage_key = storage_key
    if delete is not None:
        upload.delete = delete
    if local is not None:
        upload.local = local
        
    upload.submit_and_check_status(client          = cli,
                                   poll            = poll,
                                   status_interval = status_interval,
                                   verify          = verify
                                  )
    
    return upload

#
def service_parameters_from_dict(service_parameters_dictionary: dict):
    """
    The function converts a dictionary of ServiceParameters to a ServiceParameters object.
    
    :param service_parameters_dict:    A dictionary that contains the keys of a ServiceParameters.
    :type service_parameters_dict:     dict             
    :rtype:                            ibmpairs.upload.ServiceParameters
    :raises Exception:                 if not a dict.
    """
    return ServiceParameters.from_dict(service_parameters_dictionary)

#
def service_parameters_to_dict(service_parameters: ServiceParameters):
    """
    The function converts an object of ServiceParameters to a dict.
    
    :param service_parameters:    A ServiceParameters object.
    :type service_parameters:     ibmpairs.upload.ServiceParameters             
    :rtype:                       dict
    """
    return ServiceParameters.to_dict(service_parameters)

#
def service_parameters_from_json(service_parameters_json: Any):
    """
    The function converts a dictionary or json string of ServiceParameters to a ServiceParameters object.
    
    :param service_parameters_json:    A dictionary or json string that contains the keys of a ServiceParameters.
    :type service_parameters_json:     Any             
    :rtype:                            ibmpairs.upload.ServiceParameters
    :raises Exception:                 if not a dict or a str.
    """
    return ServiceParameters.from_json(service_parameters_json)

#
def service_parameters_to_json(service_parameters: ServiceParameters):
    """
    The function converts an object of ServiceParameters to a json string.
    
    :param service_parameters:    A ServiceParameters object.
    :type service_parameters:     ibmpairs.upload.ServiceParameters             
    :rtype:                       str
    """
    return ServiceParameters.to_json(service_parameters)

#
def upload_info_from_dict(upload_info_dictionary: dict):
    """
    The function converts a dictionary of UploadInfo to a UploadInfo object.
    
    :param upload_info_dict:    A dictionary that contains the keys of a UploadInfo.
    :type upload_info_dict:     dict             
    :rtype:                     ibmpairs.upload.UploadInfo
    :raises Exception:          if not a dict.
    """
    return UploadInfo.from_dict(upload_info_dictionary)

#
def upload_info_to_dict(upload_info: UploadInfo):
    """
    The function converts an object of UploadInfo to a dict.
    
    :param upload_info:    A UploadInfo object.
    :type upload_info:     ibmpairs.upload.UploadInfo             
    :rtype:                dict
    """
    return UploadInfo.to_dict(upload_info)

#
def upload_info_from_json(upload_info_json: Any):
    """
    The function converts a dictionary or json string of UploadInfo to a UploadInfo object.
    
    :param upload_info_json:    A dictionary or json string that contains the keys of a UploadInfo.
    :type upload_info_json:     Any             
    :rtype:                     ibmpairs.upload.UploadInfo
    :raises Exception:          if not a dict or a str.
    """
    return UploadInfo.from_json(upload_info_json)

#
def upload_info_to_json(upload_info: UploadInfo):
    """
    The function converts an object of UploadInfo to a json string.
    
    :param upload_info:    A UploadInfo object.
    :type upload_info:     ibmpairs.upload.UploadInfo             
    :rtype:                str
    """
    return UploadInfo.to_json(upload_info)

#
def summary_from_dict(summary_dictionary: dict):
    """
    The function converts a dictionary of Summary to a Summary object.
    
    :param summary_dict:        A dictionary that contains the keys of a Summary.
    :type summary_dict:         dict             
    :rtype:                     ibmpairs.upload.Summary
    :raises Exception:          if not a dict.
    """
    return Summary.from_dict(summary_dictionary)

#
def summary_to_dict(summary: Summary):
    """
    The function converts an object of Summary to a dict.
    
    :param summary:    A Summary object.
    :type summary:     ibmpairs.upload.Summary             
    :rtype:            dict
    """
    return Summary.to_dict(summary)

#
def summary_from_json(summary_json: Any):
    """
    The function converts a dictionary or json string of Summary to a Summary object.
    
    :param summary_json:        A dictionary or json string that contains the keys of a Summary.
    :type summary_json:         Any             
    :rtype:                     ibmpairs.upload.Summary
    :raises Exception:          if not a dict or a str.
    """
    return Summary.from_json(summary_json)

#
def summary_to_json(summary: Summary):
    """
    The function converts an object of Summary to a json string.
    
    :param summary:    A Summary object.
    :type summary:     ibmpairs.upload.Summary             
    :rtype:            str
    """
    return Summary.to_json(summary)

#
def upload_response_from_dict(upload_response_dictionary: dict):
    """
    The function converts a dictionary of UploadResponse to a UploadResponse object.
    
    :param upload_response_dict:    A dictionary that contains the keys of a UploadResponse.
    :type upload_response_dict:     dict             
    :rtype:                         ibmpairs.upload.UploadResponse
    :raises Exception:              if not a dict.
    """
    return UploadResponse.from_dict(upload_response_dictionary)

#
def upload_response_to_dict(upload_response: UploadResponse):
    """
    The function converts an object of UploadResponse to a dict.
    
    :param upload_response:    A UploadResponse object.
    :type upload_response:     ibmpairs.upload.UploadResponse             
    :rtype:                    dict
    """
    return UploadResponse.to_dict(upload_response)

#
def upload_response_from_json(upload_response_json: Any):
    """
    The function converts a dictionary or json string of UploadResponse to a UploadResponse object.
    
    :param upload_response_json:    A dictionary or json string that contains the keys of a UploadResponse.
    :type upload_response_json:     Any             
    :rtype:                         ibmpairs.upload.UploadResponse
    :raises Exception:              if not a dict or a str.
    """
    return UploadResponse.from_json(upload_response_json)

#
def upload_response_to_json(upload_response: UploadResponse):
    """
    The function converts an object of UploadResponse to a json string.
    
    :param upload_response:    A UploadResponse object.
    :type upload_response:     ibmpairs.upload.UploadResponse             
    :rtype:                    str
    """
    return UploadResponse.to_json(upload_response)

#
def upload_status_response_from_dict(upload_status_response_dictionary: dict):
    """
    The function converts a dictionary of UploadStatusResponse to a UploadStatusResponse object.
    
    :param upload_status_response_dict:    A dictionary that contains the keys of a UploadStatusResponse.
    :type upload_status_response_dict:     dict             
    :rtype:                                ibmpairs.upload.UploadStatusResponse
    :raises Exception:                     if not a dict.
    """
    return UploadStatusResponse.from_dict(upload_status_response_dictionary)

#
def upload_status_response_to_dict(upload_status_response: UploadStatusResponse):
    """
    The function converts an object of UploadStatusResponse to a dict.
    
    :param upload_status_response:    A UploadStatusResponse object.
    :type upload_status_response:     ibmpairs.upload.UploadStatusResponse             
    :rtype:                           dict
    """
    return UploadStatusResponse.to_dict(upload_status_response)

#
def upload_status_response_from_json(upload_status_response_json: Any):
    """
    The function converts a dictionary or json string of UploadStatusResponse to a UploadStatusResponse object.
    
    :param upload_status_response_json:    A dictionary or json string that contains the keys of a UploadStatusResponse.
    :type upload_status_response_json:     Any             
    :rtype:                                ibmpairs.upload.UploadStatusResponse
    :raises Exception:                     if not a dict or a str.
    """
    return UploadStatusResponse.from_json(upload_status_response_json)

#
def upload_status_response_to_json(upload_status_response: UploadStatusResponse):
    """
    The function converts an object of UploadStatusResponse to a json string.
    
    :param upload_status_response:    A UploadStatusResponse object.
    :type upload_status_response:     ibmpairs.upload.UploadStatusResponse             
    :rtype:                           str
    """
    return UploadStatusResponse.to_json(upload_status_response)

#
def conv_params_dict_from_dict(conv_params_dict_dictionary: dict):
    """
    The function converts a dictionary of ConvParamsDict to a ConvParamsDict object.
    
    :param conv_params_dict_dict:    A dictionary that contains the keys of a ConvParamsDict.
    :type conv_params_dict_dict:     dict             
    :rtype:                          ibmpairs.upload.ConvParamsDict
    :raises Exception:               if not a dict.
    """
    return ConvParamsDict.from_dict(conv_params_dict_dictionary)

#
def conv_params_dict_to_dict(conv_params_dict: ConvParamsDict):
    """
    The function converts an object of ConvParamsDict to a dict.
    
    :param conv_params_dict:    A ConvParamsDict object.
    :type conv_params_dict:     ibmpairs.upload.ConvParamsDict             
    :rtype:                     dict
    """
    return ConvParamsDict.to_dict(conv_params_dict)
    
#
def conv_params_dict_to_dict_post(conv_params_dict: ConvParamsDict):
    """
    The function converts an object of ConvParamsDict to a dict, ready for upload post.
    
    :param conv_params_dict:    A ConvParamsDict object.
    :type conv_params_dict:     ibmpairs.upload.ConvParamsDict             
    :rtype:                     dict
    """
    return ConvParamsDict.to_dict_upload_post(conv_params_dict)

#
def conv_params_dict_from_json(conv_params_dict_json: Any):
    """
    The function converts a dictionary or json string of ConvParamsDict to a ConvParamsDict object.
    
    :param conv_params_dict_json:    A dictionary or json string that contains the keys of a ConvParamsDict.
    :type conv_params_dict_json:     Any             
    :rtype:                          ibmpairs.upload.ConvParamsDict
    :raises Exception:               if not a dict or a str.
    """
    return ConvParamsDict.from_json(conv_params_dict_json)

#
def conv_params_dict_to_json(conv_params_dict: ConvParamsDict):
    """
    The function converts an object of ConvParamsDict to a json string.
    
    :param conv_params_dict:    A ConvParamsDict object.
    :type conv_params_dict:     ibmpairs.upload.ConvParamsDict             
    :rtype:                     str
    """
    return ConvParamsDict.to_json(conv_params_dict)
    
#
def conv_params_dict_to_json_post(conv_params_dict: ConvParamsDict):
    """
    The function converts an object of ConvParamsDict to a json string, ready for upload post.
    
    :param conv_params_dict:    A ConvParamsDict object.
    :type conv_params_dict:     ibmpairs.upload.ConvParamsDict             
    :rtype:                     str
    """
    return ConvParamsDict.to_json_upload_post(conv_params_dict)

#
def pdal_preprocessing_json_from_dict(pdal_preprocessing_json_dictionary: dict):
    """
    The function converts a dictionary of PdalPreprocessingJSON to a PdalPreprocessingJSON object.
    
    :param pdal_preprocessing_json_dict:    A dictionary that contains the keys of a PdalPreprocessingJSON.
    :type pdal_preprocessing_json_dict:     dict             
    :rtype:                                 ibmpairs.upload.PdalPreprocessingJSON
    :raises Exception:                      if not a dict.
    """
    return PdalPreprocessingJSON.from_dict(pdal_preprocessing_json_dictionary)

#
def pdal_preprocessing_json_to_dict(pdal_preprocessing_json: PdalPreprocessingJSON):
    """
    The function converts an object of PdalPreprocessingJSON to a dict.
    
    :param pdal_preprocessing_json:    A PdalPreprocessingJSON object.
    :type pdal_preprocessing_json:     ibmpairs.upload.PdalPreprocessingJSON             
    :rtype:                            dict
    """
    return PdalPreprocessingJSON.to_dict(pdal_preprocessing_json)

#
def pdal_preprocessing_json_from_json(pdal_preprocessing_json_json: Any):
    """
    The function converts a dictionary or json string of PdalPreprocessingJSON to a PdalPreprocessingJSON object.
    
    :param pdal_preprocessing_json_json:    A dictionary or json string that contains the keys of a PdalPreprocessingJSON.
    :type pdal_preprocessing_json_json:     Any             
    :rtype:                                 ibmpairs.upload.PdalPreprocessingJSON
    :raises Exception:                      if not a dict or a str.
    """
    return PdalPreprocessingJSON.from_json(pdal_preprocessing_json_json)

#
def pdal_preprocessing_json_to_json(pdal_preprocessing_json: PdalPreprocessingJSON):
    """
    The function converts an object of PdalPreprocessingJSON to a json string.
    
    :param pdal_preprocessing_json:    A PdalPreprocessingJSON object.
    :type pdal_preprocessing_json:     ibmpairs.upload.PdalPreprocessingJSON             
    :rtype:                            str
    """
    return PdalPreprocessingJSON.to_json(pdal_preprocessing_json)

#
def options_from_dict(options_dictionary: dict):
    """
    The function converts a dictionary of Options to a Options object.
    
    :param options_dict:    A dictionary that contains the keys of a Options.
    :type options_dict:     dict             
    :rtype:                 ibmpairs.upload.Options
    :raises Exception:      if not a dict.
    """
    return Options.from_dict(options_dictionary)

#
def options_to_dict(options: Options):
    """
    The function converts an object of Options to a dict.
    
    :param options:    A Options object.
    :type options:     ibmpairs.upload.Options             
    :rtype:            dict
    """
    return Options.to_dict(options)
    
#
def options_to_dict_post(options: Options):
    """
    The function converts an object of Options to a dict, ready for upload post.
    
    :param options:    A Options object.
    :type options:     ibmpairs.upload.Options             
    :rtype:            dict
    """
    return Options.to_dict_upload_post(options)

#
def options_from_json(options_json: Any):
    """
    The function converts a dictionary or json string of Options to a Options object.
    
    :param options_json:        A dictionary or json string that contains the keys of a Options.
    :type options_json:         Any             
    :rtype:                     ibmpairs.upload.Options
    :raises Exception:          if not a dict or a str.
    """
    return Options.from_json(options_json)

#
def options_to_json(options: Options):
    """
    The function converts an object of Options to a json string.
    
    :param options:    A Options object.
    :type options:     ibmpairs.upload.Options             
    :rtype:            str
    """
    return Options.to_json(options)

#
def options_to_json_post(options: Options):
    """
    The function converts an object of Options to a json string, ready for upload post.
    
    :param options:    A Options object.
    :type options:     ibmpairs.upload.Options             
    :rtype:            str
    """
    return Options.to_json_upload_post(options)

#
def preprocessing_from_dict(preprocessing_dictionary: dict):
    """
    The function converts a dictionary of Preprocessing to a Preprocessing object.
    
    :param preprocessing_dict:    A dictionary that contains the keys of a Preprocessing.
    :type preprocessing_dict:     dict             
    :rtype:                       ibmpairs.upload.Preprocessing
    :raises Exception:            if not a dict.
    """
    return Preprocessing.from_dict(preprocessing_dictionary)

#
def preprocessing_to_dict(preprocessing: Preprocessing):
    """
    The function converts an object of Preprocessing to a dict.
    
    :param preprocessing:    A Preprocessing object.
    :type preprocessing:     ibmpairs.upload.Preprocessing             
    :rtype:                  dict
    """
    return Preprocessing.to_dict(preprocessing)
    
#
def preprocessing_to_dict_post(preprocessing: Preprocessing):
    """
    The function converts an object of Preprocessing to a dict, ready for upload post.
    
    :param preprocessing:    A Preprocessing object.
    :type preprocessing:     ibmpairs.upload.Preprocessing             
    :rtype:                  dict
    """
    return Preprocessing.to_dict_upload_post(preprocessing)

#
def preprocessing_from_json(preprocessing_json: Any):
    """
    The function converts a dictionary or json string of Preprocessing to a Preprocessing object.
    
    :param preprocessing_json:    A dictionary or json string that contains the keys of a Preprocessing.
    :type preprocessing_json:     Any             
    :rtype:                       ibmpairs.upload.Preprocessing
    :raises Exception:            if not a dict or a str.
    """
    return Preprocessing.from_json(preprocessing_json)

#
def preprocessing_to_json(preprocessing: Preprocessing):
    """
    The function converts an object of Preprocessing to a json string.
    
    :param preprocessing:    A Preprocessing object.
    :type preprocessing:     ibmpairs.upload.Preprocessing             
    :rtype:                  str
    """
    return Preprocessing.to_json(preprocessing)
    
#
def preprocessing_to_json_post(preprocessing: Preprocessing):
    """
    The function converts an object of Preprocessing to a json string, ready for upload post.
    
    :param preprocessing:    A Preprocessing object.
    :type preprocessing:     ibmpairs.upload.Preprocessing             
    :rtype:                  str
    """
    return Preprocessing.to_json_upload_post(preprocessing)

def upload_from_dict(upload_dictionary: dict,
                     client: cl.Client = None):
    """
    The function converts a dictionary of Upload to a Upload object.
    
    :param upload_dict:    A dictionary that contains the keys of a Upload.
    :type upload_dict:     dict
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client              
    :rtype:                ibmpairs.upload.Upload
    :raises Exception:     if not a dict.
    """
    upload = Upload.from_dict(upload_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    upload.client = cli
    return upload

#
def upload_to_dict(upload: Upload):
    """
    The function converts an object of Upload to a dict.
    
    :param upload:    A Upload object.
    :type upload:     ibmpairs.upload.Upload             
    :rtype:           dict
    """
    return Upload.to_dict(upload)

#
def upload_to_dict_post(upload: Upload):
    """
    The function converts an object of Upload to a dict, ready for upload post.
    
    :param upload:    A Upload object.
    :type upload:     ibmpairs.upload.Upload             
    :rtype:           dict
    """
    return Upload.to_dict_upload_post(upload)

#
def upload_from_json(upload_json: Any,
                     client: cl.Client = None):
    """
    The function converts a dictionary or json string of Upload to a Upload object.
    
    :param upload_json:    A dictionary or json string that contains the keys of a Upload.
    :type upload_json:     Any
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client           
    :rtype:                ibmpairs.upload.Upload
    :raises Exception:     if not a dict or a str.
    """
    upload = Upload.from_json(upload_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    upload.client = cli
    return upload

#
def upload_to_json(upload: Upload):
    """
    The function converts an object of Upload to a json string.
    
    :param upload:    A Upload object.
    :type upload:     ibmpairs.upload.Upload             
    :rtype:           str
    """
    return Upload.to_json(upload)
    
#
def upload_to_json_post(upload: Upload):
    """
    The function converts an object of Upload to a json string, ready for upload post.
    
    :param upload:    A Upload object.
    :type upload:     ibmpairs.upload.Upload             
    :rtype:           str
    """
    return Upload.to_json_upload_post(upload)
