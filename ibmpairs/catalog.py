"""
IBM PAIRS Catalog: A Python module to assist with the retrival, creation, 
update and deletion of metadata in the IBM PAIRS catalog.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
import json
import os
from typing import List, Any
import re
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
import ibmpairs.client as cl
import ibmpairs.common as common
import ibmpairs.constants as constants
from ibmpairs.logger import logger
import ibmpairs.messages as messages
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import pandas as pd
try:
    import rasterio
    HAS_RASTERIO=True
except:
    HAS_RASTERIO=False
from tableschema import Table
#}}}

#
class Category:
    #_id: int
    #_name: str
    
    """
    An object to represent a catalog category.

    :param id:             category id
    :type id:              int
    :param name:           category name
    :type name:            str
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
    
    #
    def __init__(self,
                 id: int   = None,
                 name: str = None
                ):
        self._id   = id
        self._name = name
    
    #    
    def get_id(self):
        return self._id

    #
    def set_id(self, id):
        self._id = common.check_int(id)
        
    #    
    def del_id(self): 
        del self._id

    #    
    id = property(get_id, set_id, del_id)
    
    #    
    def get_name(self):
        return self._name

    #
    def set_name(self, name):
        self._name = common.check_str(name)
        
    #    
    def del_name(self): 
        del self._name

    #    
    name = property(get_name, set_name, del_name)
        
    #    
    def from_dict(category_dict: Any):

        """
        Create a Category object from a dictionary.
        
        :param category_dict: A dictionary that contains the keys of a Category.
        :type category_dict:  Any             
        :rtype:               ibmpairs.catalog.Category
        :raises Exception:    if not a dictionary.
        """
        
        id   = None
        name = None
        
        common.check_dict(category_dict)
        if "id" in category_dict:
            if category_dict.get("id") is not None:
                id = common.check_int(category_dict.get("id"))
        if "name" in category_dict:
            if category_dict.get("name") is not None:
                name = common.check_str(category_dict.get("name"))
        return Category(id   = id,
                        name = name
                       )

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure.  
                  
        :rtype: dict
        """
      
        category_dict: dict = {}
        if self._id is not None:
            category_dict["id"] = self._id
        if self._name is not None:
            category_dict["name"] = self._name
        return category_dict

    #
    def from_json(category_json: Any):

        """
        Create a Category object from json (dictonary or str).
        
        :param category_dict: A json dictionary that contains the keys of a Category or a string representation of a json dictionary.
        :type category_dict:  Any             
        :rtype:               ibmpairs.catalog.Category
        :raises Exception:    if not a dictionary or a string.
        """
        
        if isinstance(category_json, dict):
            category = Category.from_dict(category_json)
        elif isinstance(category_json, str):
            category_dict = json.loads(category_json)
            category = Category.from_dict(category_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(category), "category")
            logger.error(msg)
            raise common.PAWException(msg)
        return category

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                  
        :rtype: string
        """

        return json.dumps(self.to_dict())


#
class Properties:
    #_sector: List[str]
    #_application: List[str]
    #_domain: List[str]
    #_type: List[str]
    #_source: List[str]
    
    """
    An object to represent a list of catalog properties.

    :param sector:      A list of sectors
    :type sector:       List[str]
    :param application: A list of applications
    :type application:  List[str]
    :param domain:      A list of domains
    :type domain:       List[str]
    :param type:        A list of types
    :type type:         List[str]
    :param source:      A list of sources
    :type source:       List[str]
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
    
    #
    def __init__(self,
                 sector: List[str]      = None,
                 application: List[str] = None,
                 domain: List[str]      = None,
                 type: List[str]        = None,
                 source: List[str]      = None
                ):
        self._sector      = sector
        self._application = application
        self._domain      = domain
        self._type        = type
        self._source      = source
    
    #       
    def get_sector(self):
        return self._sector

    #
    def set_sector(self, sector):
        self._sector = common.check_class(sector, List[str])
        
    #    
    def del_sector(self): 
        del self._sector

    #    
    sector = property(get_sector, set_sector, del_sector)
    
    #       
    def get_application(self):
        return self._application

    #
    def set_application(self, application):
        self._application = common.check_class(application, List[str])
        
    #    
    def del_application(self): 
        del self._application

    #    
    application = property(get_application, set_application, del_application)
    
    #       
    def get_domain(self):
        return self._domain

    #
    def set_domain(self, domain):
        self._domain = common.check_class(domain, List[str])
        
    #    
    def del_domain(self): 
        del self._domain

    #    
    domain = property(get_domain, set_domain, del_domain)
    
    #       
    def get_type(self):
        return self._type

    #
    def set_type(self, type):
        self._type = common.check_class(type, List[str])
        
    #    
    def del_type(self): 
        del self._type

    #    
    type = property(get_type, set_type, del_type)
    
    #       
    def get_source(self):
        return self._source

    #
    def set_source(self, source):
        self._source = common.check_class(source, List[str])
        
    #    
    def del_source(self): 
        del self._source

    #    
    source = property(get_source, set_source, del_source)
        
    #
    def from_dict(properties_dict: Any):

        """
        Create a Properties object from a dictionary.
        
        :param properties_dict: A dictionary that contains the keys of a Properties.
        :type properties_dict:  Any             
        :rtype:                 ibmpairs.catalog.Properties
        :raises Exception:      if not a dictionary.
        """
        
        sector      = None
        application = None
        domain      = None
        type        = None
        source      = None
                
        common.check_dict(properties_dict)
        if "Sector" in properties_dict:
            if properties_dict.get("Sector") is not None:
                sector = common.from_list(properties_dict.get("Sector"), common.check_str)
        elif "sector" in properties_dict:
            if properties_dict.get("sector") is not None:
                sector = common.from_list(properties_dict.get("sector"), common.check_str)
        if "Application" in properties_dict:
            if properties_dict.get("Application") is not None:
                application = common.from_list(properties_dict.get("Application"), common.check_str)
        elif "application" in properties_dict:
            if properties_dict.get("application") is not None:
                application = common.from_list(properties_dict.get("application"), common.check_str)
        if "Domain" in properties_dict:
            if properties_dict.get("Domain") is not None:
                domain = common.from_list(properties_dict.get("Domain"), common.check_str)
        elif "domain" in properties_dict:
            if properties_dict.get("domain") is not None:
                domain = common.from_list(properties_dict.get("domain"), common.check_str)
        if "Type" in properties_dict:
            if properties_dict.get("Type") is not None:
                type = common.from_list(properties_dict.get("Type"), common.check_str)
        elif "type" in properties_dict:
            if properties_dict.get("type") is not None:
                type = common.from_list(properties_dict.get("type"), common.check_str)
        if "Source" in properties_dict:
            if properties_dict.get("Source") is not None:
                source = common.from_list(properties_dict.get("Source"), common.check_str)
        elif "source" in properties_dict:
            if properties_dict.get("source") is not None:
                source = common.from_list(properties_dict.get("source"), common.check_str)
        return Properties(sector      = sector,
                          application = application,
                          domain      = domain,
                          type        = type,
                          source      = source
                         )
    
    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        properties_dict: dict = {}
        if self._sector is not None:
            properties_dict["sector"] = common.from_list(self._sector, common.check_str)
        if self._application is not None:
            properties_dict["application"] = common.from_list(self._application, common.check_str)
        if self._domain is not None:
            properties_dict["domain"] = common.from_list(self._domain, common.check_str)
        if self._type is not None:
            properties_dict["type"] = common.from_list(self._type, common.check_str)
        if self._source is not None:
            properties_dict["source"] = common.from_list(self._source, common.check_str)
        return properties_dict

    #
    def from_json(properties_json: Any):

        """
        Create a Properties object from json (dictonary or str).
        
        :param properties_dict: A json dictionary that contains the keys of a Properties or a string representation of a json dictionary.
        :type properties_dict:  Any             
        :rtype:                 ibmpairs.catalog.Properties
        :raises Exception:      if not a dictionary or a string.
        """
        
        if isinstance(properties_json, dict):
            properties = Properties.from_dict(properties_json)
        elif isinstance(properties_json, str):
            properties_dict = json.loads(properties_json)
            properties = Properties.from_dict(properties_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(properties), "properties")
            logger.error(msg)
            raise common.PAWException(msg)
        return properties

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())


class SpatialCoverage:
    #_country: List[str]
    
    """
    An object to represent a catalog spatial coverage.

    :param country: A list of countries
    :type country:  List[str]
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
                 country: List[str] = None
                ):
        self._country = country
    
    #       
    def get_country(self):
        return self._country

    #
    def set_country(self, country):
        self._country = common.check_class(country, List[str])
        
    #    
    def del_country(self): 
        del self._country

    #    
    country = property(get_country, set_country, del_country)

    #
    def from_dict(spatial_coverage_dict: Any):

        """
        Create a SpatialCoverage object from a dictionary.
        
        :param spatial_coverage_dict: A dictionary that contains the keys of a SpatialCoverage.
        :type spatial_coverage_dict:  Any             
        :rtype:                       ibmpairs.catalog.SpatialCoverage
        :raises Exception:            if not a dictionary.
        """
        
        country = None
        
        common.check_dict(spatial_coverage_dict)
        if "Country" in spatial_coverage_dict:
            if spatial_coverage_dict.get("Country") is not None:
                country = common.from_list(spatial_coverage_dict.get("Country"), common.check_str)
        elif "country" in spatial_coverage_dict:
            if spatial_coverage_dict.get("country") is not None:
                country = common.from_list(spatial_coverage_dict.get("country"), common.check_str)
        return SpatialCoverage(country)
    
    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        spatial_coverage_dict: dict = {}
        if self._country is not None:
            spatial_coverage_dict["country"] = common.from_list(self._country, common.check_str)
        return spatial_coverage_dict

    #
    def from_json(spatial_coverage_json: Any):

        """
        Create a SpatialCoverage object from json (dictonary or str).
        
        :param spatial_coverage_dict: A json dictionary that contains the keys of a SpatialCoverage or a string representation of a json dictionary.
        :type spatial_coverage_dict:  Any             
        :rtype:                       ibmpairs.catalog.SpatialCoverage
        :raises Exception:            if not a dictionary or a string.
        """
        
        if isinstance(spatial_coverage_json, dict):
            spatial_coverage = SpatialCoverage.from_dict(spatial_coverage_json)
        elif isinstance(spatial_coverage_json, str):
            spatial_coverage_dict = json.loads(spatial_coverage_json)
            spatial_coverage = SpatialCoverage.from_dict(spatial_coverage_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(spatial_coverage), "spatial_coverage")
            logger.error(msg)
            raise common.PAWException(msg)
        return spatial_coverage

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype: string
        """

        return json.dumps(self.to_dict()) 
        
#
class DataSetReturn:
    #_data_set_id: str
    #_status: int
    #_message: str
    
    """
    An object to represent the response from a DataSet object call.

    :param data_set_id: A data set id.
    :type data_set_id:  str
    :param status:      A status code.
    :type status:       int
    :param message:     A status message from the call.
    :type message:      str
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
    
    #
    def __init__(self,
                 data_set_id: str = None,
                 status: int      = None,
                 message: str     = None
                ):
        self._data_set_id = data_set_id
        self._status      = status
        self._message     = message
    
    #    
    def get_data_set_id(self):
        return self._data_set_id

    #
    def set_data_set_id(self, data_set_id):
        self._data_set_id = common.check_str(data_set_id)
        
    #    
    def del_data_set_id(self): 
        del self._data_set_id

    #    
    data_set_id = property(get_data_set_id, set_data_set_id, del_data_set_id)
    
    #    
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_int(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)
    
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
    def from_dict(data_set_return_dict: Any):

        """
        Create a DataSetReturn object from a dictionary.
        
        :param data_set_return_dict: A dictionary that contains the keys of a DataSetReturn.
        :type data_set_return_dict:  Any             
        :rtype:                      ibmpairs.catalog.DataSetReturn
        :raises Exception:           if not a dictionary.
        """
        
        data_set_id = None
        status      = None
        message     = None
        
        common.check_dict(data_set_return_dict)
        if "datasetId" in data_set_return_dict:
            if data_set_return_dict.get("datasetId") is not None:
                data_set_id = common.check_str(data_set_return_dict.get("datasetId"))
        elif "data_set_id" in data_set_return_dict:
            if data_set_return_dict.get("data_set_id") is not None:
                data_set_id = common.check_str(data_set_return_dict.get("data_set_id"))
        if "status" in data_set_return_dict:
            if data_set_return_dict.get("status") is not None:
                status = common.check_int(data_set_return_dict.get("status"))
        if "message" in data_set_return_dict:
            if data_set_return_dict.get("message") is not None:
                message = common.check_str(data_set_return_dict.get("message"))
        return DataSetReturn(data_set_id = data_set_id,
                             status      = status,
                             message     = message
                            )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
        
        :rtype: dict
        """
        
        data_set_return_dict: dict = {}
        if self.data_set_id is not None:
            data_set_return_dict["data_set_id"] = self._data_set_id
        if self._status is not None:
            data_set_return_dict["status"] = self._status
        if self._message is not None:
            data_set_return_dict["message"] = self._message
        return data_set_return_dict

    #
    def from_json(data_set_return_json: Any):

        """
        Create a DataSetReturn object from json (dictonary or str).
        
        :param data_set_return_dict: A json dictionary that contains the keys of a DataSetReturn or a string representation of a json dictionary.
        :type data_set_return_dict:  Any             
        :rtype:                      ibmpairs.catalog.DataSetReturn
        :raises Exception:           if not a dictionary or a string.
        """
        
        if isinstance(data_set_return_json, dict):
            data_set_return = DataSetReturn.from_dict(data_set_return_json)
        elif isinstance(data_set_return_json, str):
            data_set_return_dict = json.loads(data_set_return_json)
            data_set_return = DataSetReturn.from_dict(data_set_return_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_set_return_json), "data_set_return_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_set_return

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
#
class DataSet:
    # 
    #_client: cl.Client    

    # Common
    #_name: str
    #_category: Category
    #_max_layers: int
    #_name_alternate: str
    #_rating: float
    #_description_short: str
    #_description_long: str
    #_description_links: List[str]
    #_data_source_name: str
    #_data_source_attribution: str
    #_data_source_description: str
    #_data_source_links: List[str]
    #_update_interval_max: str
    #_update_interval_description: str
    #_lag_horizon: str
    #_lag_horizon_description: str
    #_temporal_resolution: str
    #_temporal_resolution_description: str
    #_spatial_resolution_of_raw_data: str
    #_interpolation: str
    #_dimensions_description: str
    #_permanence: bool
    #_permanence_description: str
    #_known_issues: str
    #_responsible_organization: str
    #_properties: Properties
    #_spatial_coverage: SpatialCoverage
    #_latitude_min: float
    #_longitude_min: float
    #_latitude_max: float
    #_longitude_max: float
    #_temporal_min: str # datetime?
    #_temporal_max: str # datetime?
    
    # Get Exclusive 
    # (GET /v2/datasets/{dataset_id})
    #_id: str
    #_key: str
    #_dsource_h_link: str
    #_dsource_desc: str
    #_status: str
    #_data_origin: str
    #_created_at: str 
    #_updated_at: str
    
    # Create Exclusive
    # (POST /v2/datasets/{dataset_id})
    # N/A
    
    # Update Exclusive 
    # (PUT /v2/datasets/{dataset_id})
    # N/A

    # Create & Get Common
    # (POST /v2/datasets/{dataset_id})
    # (GET /v2/datasets/{dataset_id})
    #_level: int
    #_crs: str
    #_offering_status: str

    # Create & Update Common
    # (POST /v2/datasets/{dataset_id})
    # (PUT /v2/datasets/{dataset_id})
    #_contact_person: str
    #_description_internal: str
    #_description_internal_links: List[str]
    #_data_storage_mid_term: str
    #_data_storage_long_term: str
    #_elt_scripts_links: List[str]
    #_license_information: str
    
    # Get & Update Common
    # (GET /v2/datasets/{dataset_id}) 
    # (PUT /v2/datasets/{dataset_id}) 
    # N/A  
    
    # Internal
    # data_set_response: DataSetReturn
    
    """
    An object to represent an IBM PAIRS Data Set.
    
    :param client:                          An IBM PAIRS Client.
    :type client:                           ibmpairs.client.Client
    :param name:                            Data Set name.
    :type name:                             str
    :param category:                        A category entry.
    :type category:                         ibmpairs.catalog.Category
    :param max_layers:                      The maximum number of Data Layers the Data Set can contain.
    :type max_layers:                       int
    :param name_alternate:                  Alternative Data Set name.
    :type name_alternate:                   str
    :param rating:                          Rating.
    :type rating:                           float
    :param description_short:               Short description of the Data Set.
    :type description_short:                str
    :param description_long:                Long description of the Data Set.
    :type description_long:                 str
    :param description_links:               A list of URLs with supporting documentation.
    :type description_links:                List[str]
    :param data_source_name:                A name for the origin data source.
    :type data_source_name:                 str
    :param data_source_attribution:         An attribution for the origin data source.
    :type data_source_attribution:          str
    :param data_source_description:         A description of the origin data source.
    :type data_source_description:          str
    :param data_source_links:               A list of URLs with supporting documentation of the origin data source.
    :type data_source_links:                List[str]
    :param update_interval_max:             The maximum interval of an update to the Data Set.
    :type update_interval_max:              str
    :param update_interval_description:     A description of the maximum update interval.
    :type update_interval_description:      str
    :param lag_horizon:                     Lag horizon of the Data Set.
    :type lag_horizon:                      str
    :param lag_horizon_description:         Lag horizon description.
    :type lag_horizon_description:          str
    :param temporal_resolution:             The temporal resolution of the Data Set.
    :type temporal_resolution:              str
    :param temporal_resolution_description: A description of the temporal resolution.
    :type temporal_resolution_description:  str
    :param spatial_resolution_of_raw_data:  Spatial resolution of the raw data.
    :type spatial_resolution_of_raw_data:   str
    :param interpolation:                   Interpolation.
    :type interpolation:                    str
    :param dimensions_description:          A description of the dimensions.
    :type dimensions_description:           str
    :param permanence:                      Permanence.
    :type permanence:                       bool
    :param permanence_description:          A description of the permanence value.
    :type permanence_description:           str
    :param known_issues:                    Known issues with the data.
    :type known_issues:                     str
    :param responsible_organization:        An organization responsible for the data.
    :type responsible_organization:         str
    :param properties:                      A properties entry.
    :type properties:                       ibmpairs.catalog.Properties
    :param spatial_coverage:                A spatial coverage entry.
    :type spatial_coverage:                 ibmpairs.catalog.SpatialCoverage 
    :param latitude_min:                    The minimum latitude of the Data Set.
    :type latitude_min:                     float 
    :param longitude_min:                   The minimum longitude of the Data Set.
    :type longitude_min:                    float
    :param latitude_max:                    The maximum latitude of the Data Set.
    :type latitude_max:                     float
    :param longitude_max:                   The maximum longitude of the Data Set.
    :type longitude_max:                    float 
    :param temporal_min:                    The minimum temporal value of the Data Set.
    :type temporal_min:                     str
    :param temporal_max:                    The maximum temporal value of the Data Set.
    :type temporal_max:                     str
    :param id:                              The Data Set ID.
    :type id:                               str
    :param key:                             The Data Set key.
    :type key:                              str
    :param dsource_h_link:                  Data source hyperlink.
    :type dsource_h_link:                   str
    :param dsource_desc:                    Data source description.
    :type dsource_desc:                     str
    :param status:                          Data Set status.
    :type status:                           str
    :param data_origin:                     The origin of the data contained within the Data Set.
    :type data_origin:                      str
    :param created_at:                      The date of creation.
    :type created_at:                       str
    :param updated_at:                      The last updated date.
    :type updated_at:                       str
    :param level:                           The default IBM PAIRS level for the Data Set.
    :type level:                            int
    :param crs:                             CRS.
    :type crs:                              str
    :param offering_status:                 The legal status of the offering.
    :type offering_status:                  str
    :param contact_person:                  A contact person for the Data Set.
    :type contact_person:                   str
    :param description_internal:            An internal description of the Data Set.
    :type description_internal:             str
    :param description_internal_links:      A list of links that give context to the description_internal.
    :type description_internal_links:       List[str]
    :param data_storage_mid_term:           The mid term data storage for the Data Set.
    :type data_storage_mid_term:            str
    :param data_storage_long_term:          The lon term data storage for the Data Set.
    :type data_storage_long_term:           str
    :param elt_scripts_links:               Extract Load Transform script links for the Data Set.
    :type elt_scripts_links:                List[str]
    :param license_information:             License information for data in the Data Set.
    :type license_information:              str
    :param data_set_response:               A server response to a executed Data Set method call.
    :type data_set_response:                ibmpairs.catalog.DataSetReturn
    :raises Exception:                      An ibmpairs.client.Client is not found.
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
    
    #
    def __init__(self,
                 client: cl.Client                     = None,
                 name: str                             = None,
                 category: Category                    = None,
                 max_layers: int                       = None,
                 name_alternate: str                   = None,
                 rating: float                         = None,
                 description_short: str                = None,
                 description_long: str                 = None,
                 description_links: List[str]          = None,
                 data_source_name: str                 = None,
                 data_source_attribution: str          = None,
                 data_source_description: str          = None,
                 data_source_links: List[str]          = None,
                 update_interval_max: str              = None,
                 update_interval_description: str      = None,
                 lag_horizon: str                      = None,
                 lag_horizon_description: str          = None,
                 temporal_resolution: str              = None,
                 temporal_resolution_description: str  = None,
                 spatial_resolution_of_raw_data: str   = None,
                 interpolation: str                    = None,
                 dimensions_description: str           = None,
                 permanence: bool                      = None,
                 permanence_description: str           = None,
                 known_issues: str                     = None,
                 responsible_organization: str         = None,
                 properties: Properties                = None,
                 spatial_coverage: SpatialCoverage     = None,
                 latitude_min: float                   = None,
                 longitude_min: float                  = None,
                 latitude_max: float                   = None,
                 longitude_max: float                  = None,
                 temporal_min: str                     = None,
                 temporal_max: str                     = None,
                 id: str                               = None,
                 key: str                              = None,
                 dsource_h_link: str                   = None,
                 dsource_desc: str                     = None,
                 status: str                           = None,
                 data_origin: str                      = None,
                 created_at: str                       = None,
                 updated_at: str                       = None,
                 level: int                            = None,
                 crs: str                              = None,
                 offering_status: str                  = None,
                 contact_person: str                   = None,
                 description_internal: str             = None,
                 description_internal_links: List[str] = None,
                 data_storage_mid_term: str            = None,
                 data_storage_long_term: str           = None,
                 elt_scripts_links: List[str]          = None,
                 license_information: str              = None,
                 data_set_response: DataSetReturn      = None
                ):
        self._client                          = common.set_client(input_client  = client,
                                                                  global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._name                            = name
        self._category                        = category
        self._max_layers                      = max_layers
        self._name_alternate                  = name_alternate
        self._rating                          = rating
        self._description_short               = description_short
        self._description_long                = description_long
        self._description_links               = description_links
        self._data_source_name                = data_source_name
        self._data_source_attribution         = data_source_attribution
        self._data_source_description         = data_source_description
        self._data_source_links               = data_source_links
        self._update_interval_max             = update_interval_max
        self._update_interval_description     = update_interval_description
        self._lag_horizon                     = lag_horizon
        self._lag_horizon_description         = lag_horizon_description
        self._temporal_resolution             = temporal_resolution
        self._temporal_resolution_description = temporal_resolution_description
        self._spatial_resolution_of_raw_data  = spatial_resolution_of_raw_data
        self._interpolation                   = interpolation
        self._dimensions_description          = dimensions_description
        self._permanence                      = permanence
        self._permanence_description          = permanence_description
        self._known_issues                    = known_issues
        self._responsible_organization        = responsible_organization
        self._properties                      = properties
        self._spatial_coverage                = spatial_coverage
        self._latitude_min                    = latitude_min
        self._longitude_min                   = longitude_min
        self._latitude_max                    = latitude_max
        self._longitude_max                   = longitude_max
        self._temporal_min                    = temporal_min
        self._temporal_max                    = temporal_max
        self._id                              = id
        self._key                             = key
        self._dsource_h_link                  = dsource_h_link
        self._dsource_desc                    = dsource_desc
        self._status                          = status
        self._data_origin                     = data_origin
        self._created_at                      = created_at
        self._updated_at                      = updated_at
        self._level                           = level
        self._crs                             = crs
        self._offering_status                 = offering_status
        self._contact_person                  = contact_person
        self._description_internal            = description_internal
        self._description_internal_links      = description_internal_links
        self._data_storage_mid_term           = data_storage_mid_term
        self._data_storage_long_term          = data_storage_long_term
        self._elt_scripts_links               = elt_scripts_links
        self._license_information             = license_information
        if data_set_response is None:
            self._data_set_response           = DataSetReturn()
        else:
            self._data_set_response           = data_set_response
    
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
    def get_name(self):
        return self._name

    #
    def set_name(self, name):
        self._name = common.check_str(name)
        
    #    
    def del_name(self): 
        del self._name

    #    
    name = property(get_name, set_name, del_name)

    #    
    def get_category(self):
        return self._category

    #
    def set_category(self, category):
        self._category = common.check_class(category, Category)
        
    #    
    def del_category(self): 
        del self._category

    #    
    category = property(get_category, set_category, del_category)

    #    
    def get_max_layers(self):
        return self._max_layers

    #
    def set_max_layers(self, max_layers):
        self._max_layers = common.check_int(max_layers)
        
    #    
    def del_max_layers(self): 
        del self._max_layers

    #    
    max_layers = property(get_max_layers, set_max_layers, del_max_layers)

    #    
    def get_name_alternate(self):
        return self._name_alternate

    #
    def set_name_alternate(self, name_alternate):
        self._name_alternate = common.check_str(name_alternate)
        
    #    
    def del_name_alternate(self): 
        del self._name_alternate

    #    
    name_alternate = property(get_name_alternate, set_name_alternate, del_name_alternate)

    #    
    def get_rating(self):
        return self._rating

    #
    def set_rating(self, rating):
        self._rating = common.check_float(rating)
        
    #    
    def del_rating(self): 
        del self._rating

    #    
    rating = property(get_rating, set_rating, del_rating)

    #    
    def get_description_short(self):
        return self._description_short

    #
    def set_description_short(self, description_short):
        self._description_short = common.check_str(description_short)
        
    #    
    def del_description_short(self): 
        del self._description_short

    #    
    description_short = property(get_description_short, set_description_short, del_description_short)

    #    
    def get_description_long(self):
        return self._description_long

    #
    def set_description_long(self, description_long):
        self._description_long = common.check_str(description_long)
        
    #    
    def del_description_long(self): 
        del self._description_long

    #    
    description_long = property(get_description_long, set_description_long, del_description_long)

    #    
    def get_description_links(self):
        return self._description_links

    #
    def set_description_links(self, description_links):
        self._description_links = common.check_class(description_links, List[str])
        
    #    
    def del_description_links(self): 
        del self._description_links

    #    
    description_links = property(get_description_links, set_description_links, del_description_links)

    #    
    def get_data_source_name(self):
        return self._data_source_name

    #
    def set_data_source_name(self, data_source_name):
        self._data_source_name = common.check_str(data_source_name)
        
    #    
    def del_data_source_name(self): 
        del self._data_source_name

    #    
    data_source_name = property(get_data_source_name, set_data_source_name, del_data_source_name)

    #    
    def get_data_source_attribution(self):
        return self._data_source_attribution

    #
    def set_data_source_attribution(self, data_source_attribution):
        self._data_source_attribution = common.check_str(data_source_attribution)
        
    #    
    def del_data_source_attribution(self): 
        del self._data_source_attribution

    #    
    data_source_attribution = property(get_data_source_attribution, set_data_source_attribution, del_data_source_attribution)

    #    
    def get_data_source_description(self):
        return self._data_source_description

    #
    def set_data_source_description(self, data_source_description):
        self._data_source_description = common.check_str(data_source_description)
        
    #    
    def del_data_source_description(self): 
        del self._data_source_description

    #    
    data_source_description = property(get_data_source_description, set_data_source_description, del_data_source_description)

    #    
    def get_data_source_links(self):
        return self._data_source_links

    #
    def set_data_source_links(self, data_source_links):
        self._data_source_links = common.check_class(data_source_links, List[str])
        
    #    
    def del_data_source_links(self): 
        del self._data_source_links

    #    
    data_source_links = property(get_data_source_links, set_data_source_links, del_data_source_links)

    #    
    def get_update_interval_max(self):
        return self._update_interval_max

    #
    def set_update_interval_max(self, update_interval_max):
        self._update_interval_max = common.check_str(update_interval_max)
        
    #    
    def del_update_interval_max(self): 
        del self._update_interval_max

    #    
    update_interval_max = property(get_update_interval_max, set_update_interval_max, del_update_interval_max)

    #    
    def get_update_interval_description(self):
        return self._update_interval_description

    #
    def set_update_interval_description(self, update_interval_description):
        self._update_interval_description = common.check_str(update_interval_description)
        
    #    
    def del_update_interval_description(self): 
        del self._update_interval_description

    #    
    update_interval_description = property(get_update_interval_description, set_update_interval_description, del_update_interval_description)

    #    
    def get_lag_horizon(self):
        return self._lag_horizon

    #
    def set_lag_horizon(self, lag_horizon):
        self._lag_horizon = common.check_str(lag_horizon)
        
    #    
    def del_lag_horizon(self): 
        del self._lag_horizon

    #    
    lag_horizon = property(get_lag_horizon, set_lag_horizon, del_lag_horizon)

    #    
    def get_lag_horizon_description(self):
        return self._lag_horizon_description

    #
    def set_lag_horizon_description(self, lag_horizon_description):
        self._lag_horizon_description = common.check_str(lag_horizon_description)
        
    #    
    def del_lag_horizon_description(self): 
        del self._lag_horizon_description

    #    
    lag_horizon_description = property(get_lag_horizon_description, set_lag_horizon_description, del_lag_horizon_description)

    #    
    def get_temporal_resolution(self):
        return self._temporal_resolution

    #
    def set_temporal_resolution(self, temporal_resolution):
        self._temporal_resolution = common.check_str(temporal_resolution)
        
    #    
    def del_temporal_resolution(self): 
        del self._temporal_resolution

    #    
    temporal_resolution = property(get_temporal_resolution, set_temporal_resolution, del_temporal_resolution)

    #    
    def get_temporal_resolution_description(self):
        return self._temporal_resolution_description

    #
    def set_temporal_resolution_description(self, temporal_resolution_description):
        self._temporal_resolution_description = common.check_str(temporal_resolution_description)
        
    #    
    def del_temporal_resolution_description(self): 
        del self._temporal_resolution_description

    #    
    temporal_resolution_description = property(get_temporal_resolution_description, set_temporal_resolution_description, del_temporal_resolution_description)

    #    
    def get_spatial_resolution_of_raw_data(self):
        return self._spatial_resolution_of_raw_data

    #
    def set_spatial_resolution_of_raw_data(self, spatial_resolution_of_raw_data):
        self._spatial_resolution_of_raw_data = common.check_str(spatial_resolution_of_raw_data)
        
    #    
    def del_spatial_resolution_of_raw_data(self): 
        del self._spatial_resolution_of_raw_data

    #    
    spatial_resolution_of_raw_data = property(get_spatial_resolution_of_raw_data, set_spatial_resolution_of_raw_data, del_spatial_resolution_of_raw_data)

    #    
    def get_interpolation(self):
        return self._interpolation

    #
    def set_interpolation(self, interpolation):
        self._interpolation = common.check_str(interpolation)
        
    #    
    def del_interpolation(self): 
        del self._interpolation

    #    
    interpolation = property(get_interpolation, set_interpolation, del_interpolation)

    #    
    def get_dimensions_description(self):
        return self._dimensions_description

    #
    def set_dimensions_description(self, dimensions_description):
        self._dimensions_description = common.check_str(dimensions_description)
        
    #    
    def del_dimensions_description(self): 
        del self._dimensions_description

    #    
    dimensions_description = property(get_dimensions_description, set_dimensions_description, del_dimensions_description)

    #    
    def get_permanence(self):
        return self._permanence

    #
    def set_permanence(self, permanence):
        self._permanence = common.check_bool(permanence)
        
    #    
    def del_permanence(self): 
        del self._permanence

    #    
    permanence = property(get_permanence, set_permanence, del_permanence)

    #    
    def get_permanence_description(self):
        return self._permanence_description

    #
    def set_permanence_description(self, permanence_description):
        self._permanence_description = common.check_str(permanence_description)
        
    #    
    def del_permanence_description(self): 
        del self._permanence_description

    #    
    permanence_description = property(get_permanence_description, set_permanence_description, del_permanence_description)

    #    
    def get_known_issues(self):
        return self._known_issues

    #
    def set_known_issues(self, known_issues):
        self._known_issues = common.check_str(known_issues)
        
    #    
    def del_known_issues(self): 
        del self._known_issues

    #    
    known_issues = property(get_known_issues, set_known_issues, del_known_issues)

    #    
    def get_responsible_organization(self):
        return self._responsible_organization

    #
    def set_responsible_organization(self, responsible_organization):
        self._responsible_organization = common.check_str(responsible_organization)
        
    #    
    def del_responsible_organization(self): 
        del self._responsible_organization

    #    
    responsible_organization = property(get_responsible_organization, set_responsible_organization, del_responsible_organization)

    #    
    def get_properties(self):
        return self._properties

    #
    def set_properties(self, properties):
        self._properties = common.check_class(properties, Properties)
        
    #    
    def del_properties(self): 
        del self._properties

    #    
    properties = property(get_properties, set_properties, del_properties)

    #    
    def get_spatial_coverage(self):
        return self._spatial_coverage

    #
    def set_spatial_coverage(self, spatial_coverage):
        self._spatial_coverage = common.check_class(spatial_coverage, SpatialCoverage)
        
    #    
    def del_spatial_coverage(self): 
        del self._spatial_coverage

    #    
    spatial_coverage = property(get_spatial_coverage, set_spatial_coverage, del_spatial_coverage)

    #    
    def get_latitude_min(self):
        return self._latitude_min

    #
    def set_latitude_min(self, latitude_min):
        self._latitude_min = common.check_float(latitude_min)
        
    #    
    def del_latitude_min(self): 
        del self._latitude_min

    #    
    latitude_min = property(get_latitude_min, set_latitude_min, del_latitude_min)

    #    
    def get_longitude_min(self):
        return self._longitude_min

    #
    def set_longitude_min(self, longitude_min):
        self._longitude_min = common.check_float(longitude_min)
        
    #    
    def del_longitude_min(self): 
        del self._longitude_min

    #    
    longitude_min = property(get_longitude_min, set_longitude_min, del_longitude_min)

    #    
    def get_latitude_max(self):
        return self._latitude_max

    #
    def set_latitude_max(self, latitude_max):
        self._latitude_max = common.check_float(latitude_max)
        
    #    
    def del_latitude_max(self): 
        del self._latitude_max

    #    
    latitude_max = property(get_latitude_max, set_latitude_max, del_latitude_max)

    #    
    def get_longitude_max(self):
        return self._longitude_max

    #
    def set_longitude_max(self, longitude_max):
        self._longitude_max = common.check_float(longitude_max)
        
    #    
    def del_longitude_max(self): 
        del self._longitude_max

    #    
    longitude_max = property(get_longitude_max, set_longitude_max, del_longitude_max)

    #    
    def get_temporal_min(self):
        return self._temporal_min

    #
    def set_temporal_min(self, temporal_min):
        self._temporal_min = common.check_str(temporal_min)
        
    #    
    def del_temporal_min(self): 
        del self._temporal_min

    #    
    temporal_min = property(get_temporal_min, set_temporal_min, del_temporal_min)

    #    
    def get_temporal_max(self):
        return self._temporal_max

    #
    def set_temporal_max(self, temporal_max):
        self._temporal_max = common.check_str(temporal_max)
        
    #    
    def del_temporal_max(self): 
        del self._temporal_max

    #    
    temporal_max = property(get_temporal_max, set_temporal_max, del_temporal_max)

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
    def get_key(self):
        return self._key

    #
    def set_key(self, key):
        self._key = common.check_str(key)
        
    #    
    def del_key(self): 
        del self._key

    #    
    key = property(get_key, set_key, del_key)

    #    
    def get_dsource_h_link(self):
        return self._dsource_h_link

    #
    def set_dsource_h_link(self, dsource_h_link):
        self._dsource_h_link = common.check_str(dsource_h_link)
        
    #    
    def del_dsource_h_link(self): 
        del self._dsource_h_link

    #    
    dsource_h_link = property(get_dsource_h_link, set_dsource_h_link, del_dsource_h_link)

    #    
    def get_dsource_desc(self):
        return self._dsource_desc

    #
    def set_dsource_desc(self, dsource_desc):
        self._dsource_desc = common.check_str(dsource_desc)
        
    #    
    def del_dsource_desc(self): 
        del self._dsource_desc

    #    
    dsource_desc = property(get_dsource_desc, set_dsource_desc, del_dsource_desc)

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
    def get_data_origin(self):
        return self._data_origin

    #
    def set_data_origin(self, data_origin):
        self._data_origin = common.check_str(data_origin)
        
    #    
    def del_data_origin(self): 
        del self._data_origin

    #    
    data_origin = property(get_data_origin, set_data_origin, del_data_origin)
    
    #    
    def get_created_at(self):
        return self._created_at

    #
    def set_created_at(self, created_at):
        self._created_at = common.check_str(created_at)
        
    #    
    def del_created_at(self): 
        del self._created_at

    #    
    created_at = property(get_created_at, set_created_at, del_created_at)
    
    #    
    def get_updated_at(self):
        return self._updated_at

    #
    def set_updated_at(self, updated_at):
        self._updated_at = common.check_str(updated_at)
        
    #    
    def del_updated_at(self): 
        del self._updated_at

    #    
    updated_at = property(get_updated_at, set_updated_at, del_updated_at)

    #    
    def get_level(self):
        return self._level

    #
    def set_level(self, level):
        self._level = common.check_int(level)
        
    #    
    def del_level(self): 
        del self._level

    #    
    level = property(get_level, set_level, del_level)

    #    
    def get_crs(self):
        return self._crs

    #
    def set_crs(self, crs):
        self._crs = common.check_str(crs)
        
    #    
    def del_crs(self): 
        del self._crs

    #    
    crs = property(get_crs, set_crs, del_crs)

    #    
    def get_offering_status(self):
        return self._offering_status

    #
    def set_offering_status(self, offering_status):
        self._offering_status = common.check_str(offering_status)
        
    #    
    def del_offering_status(self): 
        del self._offering_status

    #    
    offering_status = property(get_offering_status, set_offering_status, del_offering_status)

    #    
    def get_contact_person(self):
        return self._contact_person

    #
    def set_contact_person(self, contact_person):
        self._contact_person = common.check_str(contact_person)
        
    #    
    def del_contact_person(self): 
        del self._contact_person

    #    
    contact_person = property(get_contact_person, set_contact_person, del_contact_person)

    #    
    def get_description_internal(self):
        return self._description_internal

    #
    def set_description_internal(self, description_internal):
        self._description_internal = common.check_str(description_internal)
        
    #    
    def del_description_internal(self): 
        del self._description_internal

    #    
    description_internal = property(get_description_internal, set_description_internal, del_description_internal)

    #    
    def get_description_internal_links(self):
        return self._description_internal_links

    #
    def set_description_internal_links(self, description_internal_links):
        self._description_internal_links = common.check_class(description_internal_links, List[str])
        
    #    
    def del_description_internal_links(self): 
        del self._description_internal_links

    #    
    description_internal_links = property(get_description_internal_links, set_description_internal_links, del_description_internal_links)

    #    
    def get_data_storage_mid_term(self):
        return self._data_storage_mid_term

    #
    def set_data_storage_mid_term(self, data_storage_mid_term):
        self._data_storage_mid_term = common.check_str(data_storage_mid_term)
        
    #    
    def del_data_storage_mid_term(self): 
        del self._data_storage_mid_term

    #    
    data_storage_mid_term = property(get_data_storage_mid_term, set_data_storage_mid_term, del_data_storage_mid_term)

    #    
    def get_data_storage_long_term(self):
        return self._data_storage_long_term

    #
    def set_data_storage_long_term(self, data_storage_long_term):
        self._data_storage_long_term = common.check_str(data_storage_long_term)
        
    #    
    def del_data_storage_long_term(self): 
        del self._data_storage_long_term

    #    
    data_storage_long_term = property(get_data_storage_long_term, set_data_storage_long_term, del_data_storage_long_term)

    #    
    def get_elt_scripts_links(self):
        return self._elt_scripts_links

    #
    def set_elt_scripts_links(self, elt_scripts_links):
        self._elt_scripts_links = common.check_class(elt_scripts_links, List[str])
        
    #    
    def del_elt_scripts_links(self): 
        del self._elt_scripts_links

    #    
    elt_scripts_links = property(get_elt_scripts_links, set_elt_scripts_links, del_elt_scripts_links)

    #    
    def get_license_information(self):
        return self._license_information

    #
    def set_license_information(self, license_information):
        self._license_information = common.check_str(license_information)
        
    #    
    def del_license_information(self): 
        del self._license_information

    #    
    license_information = property(get_license_information, set_license_information, del_license_information)
    
    #
    def get_data_set_response(self):
      return self._data_set_response

    #
    def set_data_set_response(self, data_set_response):
      self._data_set_response = common.check_class(data_set_response, DataSetReturn)

    #    
    def del_data_set_response(self): 
      del self._data_set_response

    #    
    data_set_response = property(get_data_set_response, set_data_set_response, del_data_set_response)
    
    #
    def from_dict(data_set_dict: Any):
        
        """
        Create a DataSet object from a dictionary.
        
        :param data_set_dict: A dictionary that contains the keys of a DataSet.
        :type data_set_dict:  Any             
        :rtype:               ibmpairs.catalog.DataSet
        :raises Exception:    if not a dictionary.
        """
        
        name                            = None
        category                        = None
        max_layers                      = None
        name_alternate                  = None
        rating                          = None
        description_short               = None
        description_long                = None
        description_links               = None
        data_source_name                = None
        data_source_attribution         = None
        data_source_description         = None
        data_source_links               = None
        update_interval_max             = None
        update_interval_description     = None
        lag_horizon                     = None
        lag_horizon_description         = None
        temporal_resolution             = None
        temporal_resolution_description = None
        spatial_resolution_of_raw_data  = None
        interpolation                   = None
        dimensions_description          = None
        permanence                      = None
        permanence_description          = None
        known_issues                    = None
        responsible_organization        = None
        properties                      = None
        spatial_coverage                = None
        latitude_min                    = None
        longitude_min                   = None
        latitude_max                    = None
        longitude_max                   = None
        temporal_min                    = None
        temporal_max                    = None
        id                              = None
        key                             = None
        dsource_h_link                  = None
        dsource_desc                    = None
        status                          = None
        data_origin                     = None
        created_at                      = None 
        updated_at                      = None
        level                           = None
        crs                             = None
        offering_status                 = None
        contact_person                  = None
        description_internal            = None
        description_internal_links      = None
        data_storage_mid_term           = None
        data_storage_long_term          = None
        elt_scripts_links               = None
        license_information             = None
        data_set_response               = None
                
        common.check_dict(data_set_dict)
    
        if "name" in data_set_dict:
            if data_set_dict.get("name") is not None:
                name = common.check_str(data_set_dict.get("name"))
        if "category" in data_set_dict:
            if data_set_dict.get("category") is not None:
                category = Category.from_dict(data_set_dict.get("category"))
        if "maxLayers" in data_set_dict:
            if data_set_dict.get("maxLayers") is not None:
                max_layers = common.check_int(data_set_dict.get("maxLayers"))
        elif "max_layers" in data_set_dict:
            if data_set_dict.get("max_layers") is not None:
                max_layers = common.check_int(data_set_dict.get("max_layers"))
        if "name_alternate" in data_set_dict:
            if data_set_dict.get("name_alternate") is not None:
                name_alternate = common.check_str(data_set_dict.get("name_alternate"))
        if "rating" in data_set_dict:
            if data_set_dict.get("rating") is not None:
                rating = common.check_float(data_set_dict.get("rating"))
        if "description_short" in data_set_dict:
            if data_set_dict.get("description_short") is not None:
                description_short = common.check_str(data_set_dict.get("description_short"))
        if "description_long" in data_set_dict:
            if data_set_dict.get("description_long") is not None:
                description_long = common.check_str(data_set_dict.get("description_long"))
        if "description_links" in data_set_dict:
            if data_set_dict.get("description_links") is not None:
                description_links = common.from_list(data_set_dict.get("description_links"), common.check_str)
        if "data_source_name" in data_set_dict:
            if data_set_dict.get("data_source_name") is not None:
                data_source_name = common.check_str(data_set_dict.get("data_source_name"))
        if "data_source_attribution" in data_set_dict:
            if data_set_dict.get("data_source_attribution") is not None:
                data_source_attribution = common.check_str(data_set_dict.get("data_source_attribution"))
        if "data_source_description" in data_set_dict:
            if data_set_dict.get("data_source_description") is not None:
                data_source_description = common.check_str(data_set_dict.get("data_source_description"))
        if "data_source_links" in data_set_dict:
            if data_set_dict.get("data_source_links") is not None:
                data_source_links = common.from_list(data_set_dict.get("data_source_links"), common.check_str)
        if "update_interval_max" in data_set_dict:
            if data_set_dict.get("update_interval_max") is not None:
                update_interval_max = common.check_str(data_set_dict.get("update_interval_max"))
        if "update_interval_description" in data_set_dict:
            if data_set_dict.get("update_interval_description") is not None:
                update_interval_description = common.check_str(data_set_dict.get("update_interval_description"))
        if "lag_horizon" in data_set_dict:
            if data_set_dict.get("lag_horizon") is not None:
                lag_horizon = common.check_str(data_set_dict.get("lag_horizon"))
        if "lag_horizon_description" in data_set_dict:
            if data_set_dict.get("lag_horizon_description") is not None:
                lag_horizon_description = common.check_str(data_set_dict.get("lag_horizon_description"))
        if "temporal_resolution" in data_set_dict:
            if data_set_dict.get("temporal_resolution") is not None:
                temporal_resolution = common.check_str(data_set_dict.get("temporal_resolution"))
        if "temporal_resolution_description" in data_set_dict:
            if data_set_dict.get("temporal_resolution_description") is not None:
                temporal_resolution_description = common.check_str(data_set_dict.get("temporal_resolution_description"))
        if "spatial_resolution_of_raw_data" in data_set_dict:
            if data_set_dict.get("spatial_resolution_of_raw_data") is not None:
                spatial_resolution_of_raw_data = common.check_str(data_set_dict.get("spatial_resolution_of_raw_data"))
        if "interpolation" in data_set_dict:
            if data_set_dict.get("interpolation") is not None:
                interpolation = common.check_str(data_set_dict.get("interpolation"))
        if "dimensions_description" in data_set_dict:
            if data_set_dict.get("dimensions_description") is not None:
                dimensions_description = common.check_str(data_set_dict.get("dimensions_description"))
        if "permanence" in data_set_dict:
            if data_set_dict.get("permanence") is not None:
                permanence = common.check_bool(data_set_dict.get("permanence"))
        if "permanence_description" in data_set_dict:
            if data_set_dict.get("permanence_description") is not None:
                permanence_description = common.check_str(data_set_dict.get("permanence_description"))
        if "known_issues" in data_set_dict:
            if data_set_dict.get("known_issues") is not None:
                known_issues = common.check_str(data_set_dict.get("known_issues"))
        if "responsible_organization" in data_set_dict:
            if data_set_dict.get("responsible_organization") is not None:
                responsible_organization = common.check_str(data_set_dict.get("responsible_organization"))
        if "properties" in data_set_dict:
            if data_set_dict.get("properties") is not None:
                properties = Properties.from_dict(data_set_dict.get("properties"))
        if "spatial_coverage" in data_set_dict:
            if data_set_dict.get("spatial_coverage") is not None:
                spatial_coverage = SpatialCoverage.from_dict(data_set_dict.get("spatial_coverage"))
        if "latitude_min" in data_set_dict:
            if data_set_dict.get("latitude_min") is not None:
                latitude_min = common.check_float(data_set_dict.get("latitude_min")) 
        if "longitude_min" in data_set_dict:
            if data_set_dict.get("longitude_min") is not None:
                longitude_min = common.check_float(data_set_dict.get("longitude_min")) 
        if "latitude_max" in data_set_dict:
            if data_set_dict.get("latitude_max") is not None:
                latitude_max = common.check_float(data_set_dict.get("latitude_max")) 
        if "longitude_max" in data_set_dict:
            if data_set_dict.get("longitude_max") is not None:
                longitude_max = common.check_float(data_set_dict.get("longitude_max")) 
        if "temporal_min" in data_set_dict:
            if data_set_dict.get("temporal_min") is not None:
                temporal_min = common.check_str(data_set_dict.get("temporal_min")) 
        if "temporal_max" in data_set_dict:
            if data_set_dict.get("temporal_max") is not None:
                temporal_max = common.check_str(data_set_dict.get("temporal_max"))       
        if "id" in data_set_dict:
            if data_set_dict.get("id") is not None:
                id = common.check_str(data_set_dict.get("id"))
        if "key" in data_set_dict:
            if data_set_dict.get("key") is not None:
                key = common.check_str(data_set_dict.get("key"))
        if "dsourceHLink" in data_set_dict:
            if data_set_dict.get("dsourceHLink") is not None:
                dsource_h_link = common.check_str(data_set_dict.get("dsourceHLink"))
        elif "dsource_h_link" in data_set_dict:
            if data_set_dict.get("dsource_h_link") is not None:
                dsource_h_link = common.check_str(data_set_dict.get("dsource_h_link"))
        if "dsourceDesc" in data_set_dict:
            if data_set_dict.get("dsourceDesc") is not None:
                dsource_desc = common.check_str(data_set_dict.get("dsourceDesc"))
        elif "dsource_desc" in data_set_dict:
            if data_set_dict.get("dsource_desc") is not None:
                dsource_desc = common.check_str(data_set_dict.get("dsource_desc"))
        if "status" in data_set_dict:
            if data_set_dict.get("status") is not None:
                status = common.check_str(data_set_dict.get("status"))
        if "dataOrigin" in data_set_dict:
            if data_set_dict.get("dataOrigin") is not None:
                data_origin = common.check_str(data_set_dict.get("dataOrigin"))
        elif "data_origin" in data_set_dict:
            if data_set_dict.get("data_origin") is not None:
                data_origin = common.check_str(data_set_dict.get("data_origin")) 
        if "created_at" in data_set_dict:
            if data_set_dict.get("created_at") is not None:
                created_at = common.check_str(data_set_dict.get("created_at"))
        if "updated_at" in data_set_dict:
            if data_set_dict.get("updated_at") is not None:
                updated_at = common.check_str(data_set_dict.get("updated_at"))
        if "level" in data_set_dict:
            if data_set_dict.get("level") is not None:
                level = common.check_int(data_set_dict.get("level"))
        if "crs" in data_set_dict:
            if data_set_dict.get("crs") is not None:
                crs = common.check_str(data_set_dict.get("crs"))
        if "offering_status" in data_set_dict:
            if data_set_dict.get("offering_status") is not None:
                offering_status = common.check_str(data_set_dict.get("offering_status"))
        if "contact_person" in data_set_dict:
            if data_set_dict.get("contact_person") is not None:
                contact_person = common.check_str(data_set_dict.get("contact_person"))
        if "description_internal" in data_set_dict:
            if data_set_dict.get("description_internal") is not None:
                description_internal = common.check_str(data_set_dict.get("description_internal"))
        if "description_internal_links" in data_set_dict:
            if data_set_dict.get("description_internal_links") is not None:
                description_internal_links = common.from_list(data_set_dict.get("description_internal_links"), common.check_str)
        if "data_storage_mid_term" in data_set_dict:
            if data_set_dict.get("data_storage_mid_term") is not None:
                data_storage_mid_term = common.check_str(data_set_dict.get("data_storage_mid_term"))
        if "data_storage_long_term" in data_set_dict:
            if data_set_dict.get("data_storage_long_term") is not None:
                data_storage_long_term = common.check_str(data_set_dict.get("data_storage_long_term"))
        if "elt_scripts_links" in data_set_dict:
            if data_set_dict.get("elt_scripts_links") is not None:
                elt_scripts_links = common.from_list(data_set_dict.get("elt_scripts_links"), common.check_str)
        if "license_information" in data_set_dict:
            if data_set_dict.get("license_information") is not None:
                license_information = common.check_str(data_set_dict.get("license_information")) 
        if "data_set_response" in data_set_dict:
            if data_set_dict.get("data_set_response") is not None:
                data_set_response = DataSetReturn.from_dict(data_set_dict.get("data_set_response"))
        return DataSet(name                            = name,
                       category                        = category,
                       max_layers                      = max_layers,
                       name_alternate                  = name_alternate,
                       rating                          = rating,
                       description_short               = description_short,
                       description_long                = description_long,
                       description_links               = description_links,
                       data_source_name                = data_source_name,
                       data_source_attribution         = data_source_attribution,
                       data_source_description         = data_source_description,
                       data_source_links               = data_source_links,
                       update_interval_max             = update_interval_max,
                       update_interval_description     = update_interval_description,
                       lag_horizon                     = lag_horizon,
                       lag_horizon_description         = lag_horizon_description,
                       temporal_resolution             = temporal_resolution,
                       temporal_resolution_description = temporal_resolution_description,
                       spatial_resolution_of_raw_data  = spatial_resolution_of_raw_data,
                       interpolation                   = interpolation,
                       dimensions_description          = dimensions_description,
                       permanence                      = permanence,
                       permanence_description          = permanence_description,
                       known_issues                    = known_issues,
                       responsible_organization        = responsible_organization,
                       properties                      = properties,
                       spatial_coverage                = spatial_coverage,
                       latitude_min                    = latitude_min,
                       longitude_min                   = longitude_min,
                       latitude_max                    = latitude_max,
                       longitude_max                   = longitude_max,
                       temporal_min                    = temporal_min,
                       temporal_max                    = temporal_max,
                       id                              = id,
                       key                             = key,
                       dsource_h_link                  = dsource_h_link,
                       dsource_desc                    = dsource_desc,
                       status                          = status,
                       data_origin                     = data_origin,
                       created_at                      = created_at, 
                       updated_at                      = updated_at,
                       level                           = level,
                       crs                             = crs,
                       offering_status                 = offering_status,
                       contact_person                  = contact_person,
                       description_internal            = description_internal,
                       description_internal_links      = description_internal_links,
                       data_storage_mid_term           = data_storage_mid_term,
                       data_storage_long_term          = data_storage_long_term,
                       elt_scripts_links               = elt_scripts_links,
                       license_information             = license_information,
                       data_set_response               = data_set_response
                      )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.   
                 
        :rtype: dict
        """
        
        data_set_dict: dict = {}
        if self._name is not None:
            data_set_dict["name"] = self._name
        if self._category is not None:
            data_set_dict["category"] = common.class_to_dict(self._category, Category) 
        if self._max_layers is not None:
            data_set_dict["max_layers"] = self._max_layers
        if self._name_alternate is not None:
            data_set_dict["name_alternate"] = self._name_alternate
        if self._rating is not None:
            data_set_dict["rating"] = self._rating
        if self._description_short is not None:
            data_set_dict["description_short"] = self._description_short
        if self._description_long is not None:
            data_set_dict["description_long"] = self._description_long
        if self._description_links is not None:
            data_set_dict["description_links"] = common.from_list(self._description_links, common.check_str)
        if self._data_source_name is not None:
            data_set_dict["data_source_name"] = self._data_source_name
        if self._data_source_attribution is not None:
            data_set_dict["data_source_attribution"] = self._data_source_attribution
        if self._data_source_description is not None:
            data_set_dict["data_source_description"] = self._data_source_description
        if self._data_source_links is not None:
            data_set_dict["data_source_links"] = common.from_list(self._data_source_links, common.check_str)
        if self._update_interval_max is not None:
            data_set_dict["update_interval_max"] = self._update_interval_max
        if self._update_interval_description is not None:
            data_set_dict["update_interval_description"] = self._update_interval_description
        if self._lag_horizon is not None:
            data_set_dict["lag_horizon"] = self._lag_horizon
        if self._lag_horizon_description is not None:
            data_set_dict["lag_horizon_description"] = self._lag_horizon_description
        if self._temporal_resolution is not None:
            data_set_dict["temporal_resolution"] = self._temporal_resolution
        if self._temporal_resolution_description is not None:
            data_set_dict["temporal_resolution_description"] = self._temporal_resolution_description
        if self._spatial_resolution_of_raw_data is not None:
            data_set_dict["spatial_resolution_of_raw_data"] = self._spatial_resolution_of_raw_data
        if self._interpolation is not None:
            data_set_dict["interpolation"] = self._interpolation
        if self._dimensions_description is not None:
            data_set_dict["dimensions_description"] = self._dimensions_description
        if self._permanence is not None:
            data_set_dict["permanence"] = self._permanence
        if self._permanence_description is not None:
            data_set_dict["permanence_description"] = self._permanence_description
        if self._known_issues is not None:
            data_set_dict["known_issues"] = self._known_issues
        if self._responsible_organization is not None:
            data_set_dict["responsible_organization"] = self._responsible_organization
        if self._properties is not None:
            data_set_dict["properties"] = common.class_to_dict(self._properties, Properties)
        if self._spatial_coverage is not None:
            data_set_dict["spatial_coverage"] = common.class_to_dict(self._spatial_coverage, SpatialCoverage)
        if self._latitude_min is not None:
            data_set_dict["latitude_min"] = self._latitude_min
        if self._longitude_min is not None:
            data_set_dict["longitude_min"] = self._longitude_min
        if self._latitude_max is not None:
            data_set_dict["latitude_max"] = self._latitude_max
        if self._longitude_max is not None:
            data_set_dict["longitude_max"] = self._longitude_max
        if self._temporal_min is not None:
            data_set_dict["temporal_min"] = self._temporal_min
        if self._temporal_max is not None:
            data_set_dict["temporal_max"] = self._temporal_max
        if self._id is not None:
            data_set_dict["id"] = self._id
        if self._key is not None:
            data_set_dict["key"] = self._key
        if self._dsource_h_link is not None:
            data_set_dict["dsource_h_link"] = self._dsource_h_link
        if self._dsource_desc is not None:
            data_set_dict["dsource_desc"] = self._dsource_desc
        if self._status is not None:
            data_set_dict["status"] = self._status
        if self._data_origin is not None:
            data_set_dict["data_origin"] = self._data_origin
        if self._created_at is not None:
            data_set_dict["created_at"] = self._created_at 
        if self._updated_at is not None:
            data_set_dict["updated_at"] = self._updated_at
        if self._level is not None:
            data_set_dict["level"] = self._level
        if self._crs is not None:
            data_set_dict["crs"] = self._crs
        if self._offering_status is not None:
            data_set_dict["offering_status"] = self._offering_status
        if self._contact_person is not None:
            data_set_dict["contact_person"] = self._contact_person
        if self._description_internal is not None:
            data_set_dict["description_internal"] = self._description_internal
        if self._description_internal_links is not None:
            data_set_dict["description_internal_links"] = common.from_list(self._description_internal_links, common.check_str)
        if self._data_storage_mid_term is not None:
            data_set_dict["data_storage_mid_term"] = self._data_storage_mid_term
        if self._data_storage_long_term is not None:
            data_set_dict["data_storage_long_term"] = self._data_storage_long_term
        if self._elt_scripts_links is not None:
            data_set_dict["elt_scripts_links"] = common.from_list(self._elt_scripts_links, common.check_str)
        if self._license_information is not None:
            data_set_dict["license_information"] = self._license_information
        if self._data_set_response is not None:
            data_set_dict["data_set_response"] = common.class_to_dict(self._data_set_response, DataSetReturn)
        return data_set_dict
    
    #    
    def to_dict_data_set_post(self):

        """
        Create a dictionary from the objects structure ready for a POST operation. 
                   
        :rtype: dict
        """
        
        data_set_dict: dict = {}
        # Common
        if self._name is not None:
            data_set_dict["name"] = self._name
        if self._category is not None:
            data_set_dict["category"] = common.class_to_dict(self._category, Category) 
        if self._max_layers is not None:
            data_set_dict["maxLayers"] = self._max_layers
        if self._name_alternate is not None:
            data_set_dict["name_alternate"] = self._name_alternate
        if self._rating is not None:
            data_set_dict["rating"] = self._rating
        if self._description_short is not None:
            data_set_dict["description_short"] = self._description_short
        if self._description_long is not None:
            data_set_dict["description_long"] = self._description_long
        if self._description_links is not None:
            data_set_dict["description_links"] = common.from_list(self._description_links, common.check_str)
        if self._data_source_name is not None:
            data_set_dict["data_source_name"] = self._data_source_name
        if self._data_source_attribution is not None:
            data_set_dict["data_source_attribution"] = self._data_source_attribution
        if self._data_source_description is not None:
            data_set_dict["data_source_description"] = self._data_source_description
        if self._data_source_links is not None:
            data_set_dict["data_source_links"] = common.from_list(self._data_source_links, common.check_str)
        if self._update_interval_max is not None:
            data_set_dict["update_interval_max"] = self._update_interval_max
        if self._update_interval_description is not None:
            data_set_dict["update_interval_description"] = self._update_interval_description
        if self._lag_horizon is not None:
            data_set_dict["lag_horizon"] = self._lag_horizon
        if self._lag_horizon_description is not None:
            data_set_dict["lag_horizon_description"] = self._lag_horizon_description
        if self._temporal_resolution is not None:
            data_set_dict["temporal_resolution"] = self._temporal_resolution
        if self._temporal_resolution_description is not None:
            data_set_dict["temporal_resolution_description"] = self._temporal_resolution_description
        if self._spatial_resolution_of_raw_data is not None:
            data_set_dict["spatial_resolution_of_raw_data"] = self._spatial_resolution_of_raw_data
        if self._interpolation is not None:
            data_set_dict["interpolation"] = self._interpolation
        if self._dimensions_description is not None:
            data_set_dict["dimensions_description"] = self._dimensions_description
        if self._permanence is not None:
            data_set_dict["permanence"] = self._permanence
        if self._permanence_description is not None:
            data_set_dict["permanence_description"] = self._permanence_description
        if self._known_issues is not None:
            data_set_dict["known_issues"] = self._known_issues
        if self._responsible_organization is not None:
            data_set_dict["responsible_organization"] = self._responsible_organization
        if self._properties is not None:
            data_set_dict["properties"] = common.class_to_dict(self._properties, Properties)
        if self._spatial_coverage is not None:
            data_set_dict["spatial_coverage"] = common.class_to_dict(self._spatial_coverage, SpatialCoverage)
        if self._latitude_min is not None:
            data_set_dict["latitude_min"] = self._latitude_min
        if self._longitude_min is not None:
            data_set_dict["longitude_min"] = self._longitude_min
        if self._latitude_max is not None:
            data_set_dict["latitude_max"] = self._latitude_max
        if self._longitude_max is not None:
            data_set_dict["longitude_max"] = self._longitude_max
        if self._temporal_min is not None:
            data_set_dict["temporal_min"] = self._temporal_min
        if self._temporal_max is not None:
            data_set_dict["temporal_max"] = self._temporal_max
        # CREATE (POST)
        if self._level is not None:
            data_set_dict["level"] = self._level
        if self._crs is not None:
            data_set_dict["crs"] = self._crs
        if self._offering_status is not None:
            data_set_dict["offering_status"] = self._offering_status
            
        return data_set_dict
        
    #
    def to_dict_data_set_put(self):
  
        """
        Create a dictionary from the objects structure ready for a PUT operation.
                    
        :rtype: dict
        """
        
        data_set_dict: dict = {}
        # Common
        if self._name is not None:
            data_set_dict["name"] = self._name
        if self._category is not None:
            data_set_dict["category"] = common.class_to_dict(self._category, Category) 
        if self._max_layers is not None:
            data_set_dict["maxLayers"] = self._max_layers
        if self._name_alternate is not None:
            data_set_dict["name_alternate"] = self._name_alternate
        if self._rating is not None:
            data_set_dict["rating"] = self._rating
        if self._description_short is not None:
            data_set_dict["description_short"] = self._description_short
        if self._description_long is not None:
            data_set_dict["description_long"] = self._description_long
        if self._description_links is not None:
            data_set_dict["description_links"] = common.from_list(self._description_links, common.check_str)
        if self._data_source_name is not None:
            data_set_dict["data_source_name"] = self._data_source_name
        if self._data_source_attribution is not None:
            data_set_dict["data_source_attribution"] = self._data_source_attribution
        if self._data_source_description is not None:
            data_set_dict["data_source_description"] = self._data_source_description
        if self._data_source_links is not None:
            data_set_dict["data_source_links"] = common.from_list(self._data_source_links, common.check_str)
        if self._update_interval_max is not None:
            data_set_dict["update_interval_max"] = self._update_interval_max
        if self._update_interval_description is not None:
            data_set_dict["update_interval_description"] = self._update_interval_description
        if self._lag_horizon is not None:
            data_set_dict["lag_horizon"] = self._lag_horizon
        if self._lag_horizon_description is not None:
            data_set_dict["lag_horizon_description"] = self._lag_horizon_description
        if self._temporal_resolution is not None:
            data_set_dict["temporal_resolution"] = self._temporal_resolution
        if self._temporal_resolution_description is not None:
            data_set_dict["temporal_resolution_description"] = self._temporal_resolution_description
        if self._spatial_resolution_of_raw_data is not None:
            data_set_dict["spatial_resolution_of_raw_data"] = self._spatial_resolution_of_raw_data
        if self._interpolation is not None:
            data_set_dict["interpolation"] = self._interpolation
        if self._dimensions_description is not None:
            data_set_dict["dimensions_description"] = self._dimensions_description
        if self._permanence is not None:
            data_set_dict["permanence"] = self._permanence
        if self._permanence_description is not None:
            data_set_dict["permanence_description"] = self._permanence_description
        if self._known_issues is not None:
            data_set_dict["known_issues"] = self._known_issues
        if self._responsible_organization is not None:
            data_set_dict["responsible_organization"] = self._responsible_organization
        if self._properties is not None:
            data_set_dict["properties"] = common.class_to_dict(self._properties, Properties)
        if self._spatial_coverage is not None:
            data_set_dict["spatial_coverage"] = common.class_to_dict(self._spatial_coverage, SpatialCoverage)
        if self._latitude_min is not None:
            data_set_dict["latitude_min"] = self._latitude_min
        if self._longitude_min is not None:
            data_set_dict["longitude_min"] = self._longitude_min
        if self._latitude_max is not None:
            data_set_dict["latitude_max"] = self._latitude_max
        if self._longitude_max is not None:
            data_set_dict["longitude_max"] = self._longitude_max
        if self._temporal_min is not None:
            data_set_dict["temporal_min"] = self._temporal_min
        if self._temporal_max is not None:
            data_set_dict["temporal_max"] = self._temporal_max
        # UPDATE (PUT)
        if self._contact_person is not None:
            data_set_dict["contact_person"] = self._contact_person
        if self._description_internal is not None:
            data_set_dict["description_internal"] = self._description_internal
        if self._description_internal_links is not None:
            data_set_dict["description_internal_links"] = common.from_list(self._description_internal_links, common.check_str)
        if self._data_storage_mid_term is not None:
            data_set_dict["data_storage_mid_term"] = self._data_storage_mid_term
        if self._data_storage_long_term is not None:
            data_set_dict["data_storage_long_term"] = self._data_storage_long_term
        if self._elt_scripts_links is not None:
            data_set_dict["elt_scripts_links"] = common.from_list(self._elt_scripts_links, common.check_str)
        if self._license_information is not None:
            data_set_dict["license_information"] = self._license_information

        return data_set_dict

    #
    def from_json(data_set_json: Any):

        """
        Create a DataSet object from json (dictonary or str).
        
        :param data_set_dict: A json dictionary that contains the keys of a DataSet or a string representation of a json dictionary.
        :type data_set_dict:  Any             
        :rtype:               ibmpairs.catalog.DataSet
        :raises Exception:    if not a dictionary or a string.
        """
        
        if isinstance(data_set_json, dict):
            data_set = DataSet.from_dict(data_set_json)
        elif isinstance(data_set_json, str):
            data_set_dict = json.loads(data_set_json)
            data_set = DataSet.from_dict(data_set_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_set_json), "data_set_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_set

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
    #
    def to_json_data_set_post(self):

        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict_data_set_post())
    
    #
    def to_json_data_set_put(self):

        """
        Create a string representation of a json dictionary from the objects structure ready for a PUT operation.            
        
        :rtype: string
        """

        return json.dumps(self.to_dict_data_set_put())

    #
    def display(self,
                columns: List[str] = ['id', 'name', 'description_short', 'description_long']
               ):
                
        """
        A method to return a pandas.DataFrame object of a get result.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['id', 'name', 'description_short', 'description_long']
        :type columns:  List[str]
        :returns:       A pandas.DataFrame of attributes from the object.
        :rtype:         pandas.DataFrame
        """

        display_dict = self.to_dict()
        
        display_df = pd.DataFrame([display_dict], columns=columns)  

        return display_df
        
    #
    def get(self,
            id                = None,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a Data Set.
        
        :param id:         The Data Set ID of the Data Set to be gathered.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A populated DataSet object.
        :rtype:            ibmpairs.catalog.DataSet
        :raises Exception: A ibmpairs.client.Client is not found, 
                           an ID is not provided or already held in the object, 
                           a server error occurred,
                           the status of the request is not 200.
        """
        
        if id is not None:
            self._id = common.check_str(id)
        
        if self._id is None:
            msg = messages.ERROR_CATALOG_DATA_SET_ID
            logger.error(msg)
            raise common.PAWException(msg)
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        try:
            response = cli.get(url    = cli.get_host() +
                                        constants.CATALOG_DATA_SETS_API + 
                                        common.check_str(self._id),
                               verify = verify
                              )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(self._id), e)
            logger.error(msg)
            raise common.PAWException(msg)
        
        if response.status_code != 200:
            error_message = 'failed'

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(self._id), response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            data_set_get = DataSet.from_dict(response.json())
            return data_set_get

    #
    def create(self,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to create a Data Set.

        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :raises Exception: A ibmpairs.client.Client is not found,
                           a server error occurred,
                           the status of the request is not 200.
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)  
        
        dataset_json = self.to_json_data_set_post()
        
        try:
            response = cli.post(url     = cli.get_host() + 
                                          constants.CATALOG_DATA_SETS_API,
                                headers = constants.CLIENT_PUT_AND_POST_HEADER,
                                body    = dataset_json,
                                verify  = verify
                               )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('POST', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API, e)
            logger.error(msg)
            raise common.PAWException(msg)
                              
        if response.status_code != 200:
            error_message = 'failed'
                
            if response.json is not None:
                try:
                    self._data_set_response = data_set_return_from_dict(response.json())
                    error_message = self._data_set_response.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('POST', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            self._data_set_response = data_set_return_from_dict(response.json())
            self._id = self._data_set_response.data_set_id

            msg = messages.INFO_CATALOG_DATA_SET_CREATE_SUCCESS.format(str(self._data_set_response.data_set_id))
            logger.info(msg)

    #
    def update(self,
               id                = None,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to update a Data Set.
        
        :param id:         The Data Set ID of the Data Set to be updated.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :raises Exception: A ibmpairs.client.Client is not found,
                           an ID is not provided or already held in the object,
                           a server error occurred,
                           the status of the request is not 200.
        """
                
        if id is not None:
            self._id = common.check_str(id)
        
        if self._id is None:
            msg = messages.ERROR_CATALOG_DATA_SET_ID
            logger.error(msg)
            raise common.PAWException(msg)
                
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
            
        dataset_json = self.to_json_data_set_put()
        
        try:
            response = cli.put(url      = cli.get_host() + 
                                          constants.CATALOG_DATA_SETS_API + 
                                          common.check_str(self._id),
                                headers = constants.CLIENT_PUT_AND_POST_HEADER,
                                body    = dataset_json,
                                verify  = verify
                               )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('PUT', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(self._id), e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status_code != 200:
            error_message = 'failed'
            
            if response.json is not None:                
                try:
                    self._data_set_response = data_set_return_from_dict(response.json())
                    error_message = self._data_set_response.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('PUT', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(self._id), response.status_code, error_message)

            logger.error(msg)
            raise common.PAWException(msg)
        else:
            self._data_set_response = data_set_return_from_dict(response.json())

            msg = messages.INFO_CATALOG_DATA_SET_UPDATE_SUCCESS.format(str(self._data_set_response.data_set_id))
            logger.info(msg)

    # To ensure a user wishes to delete, the data set id must be specified- this will not be pulled from the object.
    def delete(self,
               id,
               hard_delete: bool = False,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to delete a Data Set.
        
        :param id:          The Data Set ID of the Data Set to be deleted.
        :type id:           str
        :param hard_delete: Whether the Data Set should be 'hard deleted', NOTE: this also deletes all data held by associated Data Layers. This step is necessary where the intention is to delete and recreate a Data Set with the same name.
        :type hard_delete:  bool
        :param client:      An IBM PAIRS Client.
        :type client:       ibmpairs.client.Client
        :param verify:      SSL verification
        :type verify:       bool
        :raises Exception:  A ibmpairs.client.Client is not found,
                            an ID is not provided or already held in the object,
                            a server error occurred,
                            the status of the request is not 200.
        """
    
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
          
        if hard_delete is True:
            url = cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(id) + "?hard_delete=true&force=true"
        else:
            url = cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(id)

        try:
            response = response = cli.delete(url    = url,
                                             verify = verify)
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('DELETE', 'request', url, e)
            logger.error(msg)
            raise common.PAWException(msg)
        
        if response.status_code != 200:
            error_message = 'failed'
          
            if response.json() is not None:
                try:
                    self._data_set_response = data_set_return_from_dict(response.json())
                    error_message = self._data_set_response.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('DELETE', 'request', url, response.status_code, error_message)
          
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            self._data_set_response = data_set_return_from_dict(response.json())

            msg = messages.INFO_CATALOG_DATA_SET_DELETE_SUCCESS.format(str(self._data_set_response.data_set_id))
            logger.info(msg)

#
class DataSets:
    # 
    #_client: cl.Client 
    
    # Common
    #_data_sets: List[DataSet]
    
    """
    An object to represent a list of IBM PAIRS Data Sets.
    
    :param client:     An IBM PAIRS Client.
    :type client:      ibmpairs.client.Client
    :param data_sets:  A list of Data Sets.
    :type data_sets:   List[ibmpairs.catalog.DataSet]
    :raises Exception: An ibmpairs.client.Client is not found.
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
        
    #
    def __getitem__(self, data_set_name):
      
        """
        A method to overload the default behaviour of the slice on this object to be an
        element from the data_sets attribute.
        
        :param data_set_name: The name of a Data Set to search for, if this is numeric,
                              the method simply returns the default (list order).
        :type data_set_name:  str
        :raises Exception:    If less than one value is found,
                              if more than one value is found.
        """    
      
        if isinstance(data_set_name, int):
            return self._data_sets[data_set_name]
        elif isinstance(data_set_name, str):
            index_list = []
            index      = 0
            foundCount = 0

            for data_set in self._data_sets:
                if data_set.name is not None:
                    if (data_set.name == data_set_name):
                        foundCount = foundCount + 1
                        index_list.append(index)
                else:
                    msg = messages.WARN_CATALOG_DATA_SETS_DATA_SET_OBJECT_NO_NAME.format(data_set_name)
                    logger.warning(msg)
                  
                index = index + 1

            if foundCount == 0:
                msg = messages.ERROR_CATALOG_DATA_SETS_NO_DATA_SET.format(data_set_name)
                logger.error(msg)
                raise common.PAWException(msg)
            elif foundCount == 1:
                return self._data_sets[index_list[0]]
            else:
                msg = messages.ERROR_CATALOG_DATA_SETS_MULTIPLE_IDENTICAL_NAMES.format(data_set_name)
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            msg = messages.ERROR_CATALOG_DATA_SETS_TYPE_UNKNOWN.format(type(data_set_name))
            logger.error(msg)
            raise common.PAWException(msg)
      
        
    #
    def __init__(self,
                 client: cl.Client        = None,
                 data_sets: List[DataSet] = None
                ):
        self._client    = common.set_client(input_client  = client,
                                            global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._data_sets = data_sets
    
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
    def get_data_sets(self):
        return self._data_sets

    #
    def set_data_sets(self, data_sets):
        self._data_sets = common.check_class(data_sets, List[DataSet])

    #    
    def del_data_sets(self): 
        del self._data_sets

    #    
    data_sets = property(get_data_sets, set_data_sets, del_data_sets)
    
    #
    def from_dict(data_sets_input: Any):

        """
        Create a DataSets object from a dictionary.
        
        :param data_sets_dict: A dictionary that contains the keys of a DataSets.
        :type data_sets_dict:  Any             
        :rtype:                ibmpairs.catalog.DataSets
        :raises Exception:     If not a dictionary.
        """
        
        data_sets = None
        
        if isinstance(data_sets_input, dict):
            common.check_dict(data_sets_input)
            if "data_sets" in data_sets_input:
                if data_sets_input.get("data_sets") is not None:
                    data_sets = common.from_list(data_sets_input.get("data_sets"), DataSet.from_dict)
        elif isinstance(data_sets_input, list):
            data_sets = common.from_list(data_sets_input, DataSet.from_dict)
        else:
            msg = messages.ERROR_CATALOG_DATA_SETS_UNKNOWN.format(type(data_sets_input))
            logger.error(msg)
            raise common.PAWException(msg)

        return DataSets(data_sets = data_sets)

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_sets_dict: dict = {}
        if self._data_sets is not None:
            data_sets_dict["data_sets"] = common.from_list(self._data_sets, lambda item: common.class_to_dict(item, DataSet)) 
        return data_sets_dict
    
    #
    def from_json(data_sets_json: Any):

        """
        Create a DataSets object from json (dictonary or str).
        
        :param data_sets_dict: A json dictionary that contains the keys of a DataSets or a string representation of a json dictionary.
        :type data_sets_dict:  Any             
        :rtype:                ibmpairs.catalog.DataSets
        :raises Exception:     if not a dictionary or a string.
        """
        
        if isinstance(data_sets_json, dict):
            data_sets = DataSets.from_dict(data_sets_json)
        elif isinstance(data_sets_json, str):
            data_sets_dict = json.loads(data_sets_json)
            data_sets = DataSets.from_dict(data_sets_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_sets_json), "data_sets_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_sets

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
    #
    def display(self,
                columns: List[str] = ['id', 'name', 'description_short', 'description_long'],
                sort_by: str       = 'id'
               ):
        
        """
        A method to return a pandas.DataFrame object of get results.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['id', 'name', 'description_short', 'description_long']
        :type columns:  List[str]
        :returns:       A pandas.DataFrame of attributes from the data_sets attribute.
        :rtype:         pandas.DataFrame
        """
                
        display_df = None
        
        for data_set in self._data_sets:
            next_display = data_set.display(columns)
            if display_df is None:
                display_df = next_display
            else:
                display_df = pd.concat([display_df, next_display])
                
        display_df.reset_index(inplace=True, drop=True)
        display_df.sort_values(by=[sort_by])

        return display_df
    
    #
    def get(self,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get all of Data Sets a user has access to.
        
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A populated DataSets object.
        :rtype:            ibmpairs.catalog.DataSets
        :raises Exception: A ibmpairs.client.Client is not found,
                           a server error occurred,
                           the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        try:
            response = cli.get(url    = cli.get_host() +
                                        constants.CATALOG_DATA_SETS_API_FULL,
                               verify = verify
                              )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API_FULL, e)
            logger.error(msg)
            raise common.PAWException(msg)
        
        if response.status_code != 200:
            error_message = 'failed'

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API_FULL, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            data_sets_get = DataSets.from_dict(response.json())
            self._data_sets = data_sets_get.data_sets
            return data_sets_get

#
class ColorTable:
    #_id: str
    #_name: str
    #_colors: str 
    
    """
    An object to represent a catalog color table.

    :param id:     An ID of a color table.
    :type id:      str
    :param name:   A name for the color table.
    :type name:    str
    :param colors: A string list of colors.
    :type colors:  str
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
    
    #
    def __init__(self,
                 id: str     = None,
                 name: str   = None,
                 colors: str = None
                ):
        self._id     = id
        self._name   = name
        self._colors = colors
    
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
    def get_name(self):
        return self._name

    #
    def set_name(self, name):
        self._name = common.check_str(name)
        
    #    
    def del_name(self): 
        del self._name

    #    
    name = property(get_name, set_name, del_name)
    
    #    
    def get_colors(self):
        return self._colors

    #
    def set_colors(self, colors):
        self._colors = common.check_str(colors)
        
    #    
    def del_colors(self): 
        del self._colors

    #    
    colors = property(get_colors, set_colors, del_colors)
        
    #    
    def from_dict(color_table_dict: Any):

        """
        Create a ColorTable object from a dictionary.
        
        :param color_table_dict: A dictionary that contains the keys of a ColorTable.
        :type color_table_dict:  Any             
        :rtype:                  ibmpairs.catalog.ColorTable
        :raises Exception:       If not a dictionary.
        """
        
        id     = None
        name   = None
        colors = None
        
        common.check_dict(color_table_dict)
        if "id" in color_table_dict:
            if color_table_dict.get("id") is not None:
                id = common.check_str(color_table_dict.get("id"))
        if "name" in color_table_dict:
            if color_table_dict.get("name") is not None:
                name = common.check_str(color_table_dict.get("name"))
        if "colors" in color_table_dict:
            if color_table_dict.get("colors") is not None:
                colors = common.check_str(color_table_dict.get("colors"))
        return ColorTable(id     = id,
                          name   = name,
                          colors = colors
                         )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 

        :rtype: dict
        """
        
        color_table_dict: dict = {}
        if self._id is not None:
            color_table_dict["id"] = self._id
        if self._name is not None:
            color_table_dict["name"] = self._name
        if self._colors is not None:
            color_table_dict["colors"] = self._colors
        return color_table_dict

    #
    def from_json(color_table_json: Any):

        """
        Create a ColorTable object from json (dictonary or str).
        
        :param color_table_dict: A json dictionary that contains the keys of a ColorTable or a string representation of a json dictionary.
        :type color_table_dict:  Any             
        :rtype:                  ibmpairs.catalog.ColorTable
        :raises Exception:       If not a dictionary or a string.
        """
        
        if isinstance(color_table_json, dict):
            color_table = ColorTable.from_dict(color_table_json)
        elif isinstance(color_table_json, str):
            color_table_dict = json.loads(color_table_json)
            color_table = ColorTable.from_dict(color_table_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(color_table_json), "color_table_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return color_table

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())


#
class DataLayerReturn:
    #_data_layer_ids: List[str]
    #_status: int
    #_message: str
    #_id: str
    
    """
    An object to represent the response from a DataLayer object call.
    
    :param data_layer_ids: A list of Data Layer IDs.
    :type data_layer_ids:  List[str]
    :param status:         A status code.
    :type status:          int
    :param message:        A status message from the call.
    :type message:         str
    :param id:             A Data Layer ID.
    :type id:              str
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
    
    #
    def __init__(self,
                 data_layer_ids: List[str] = None,
                 status: int               = None,
                 message: str              = None,
                 id: str                   = None
                ):
        self._data_layer_ids = data_layer_ids
        self._status         = status
        self._message        = message
        self._id             = id
    
    #    
    def get_data_layer_ids(self):
        return self._data_layer_ids

    #
    def set_data_layer_ids(self, data_layer_ids):
        if common.check_str(data_layer_ids):
            self._data_layer_ids = data_layer_ids
        elif common.check_class(data_layer_ids, List[str]):
            self._data_layer_ids = data_layer_ids
        else:
            msg = messages.ERROR_CATALOG_SET_DATA_LAYER_ID
            logger.error(msg)
            raise common.PAWException(msg)
    #    
    def del_data_layer_ids(self): 
        del self._data_layer_ids

    #    
    data_layer_ids = property(get_data_layer_ids, set_data_layer_ids, del_data_layer_ids)
    
    #    
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_int(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)
    
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
    def from_dict(data_layer_return_dict: Any):

        """
        Create a DataLayerReturn object from a dictionary.
        
        :param data_layer_return_dict: A dictionary that contains the keys of a DataLayerReturn.
        :type data_layer_return_dict:  Any             
        :rtype:                        ibmpairs.catalog.DataLayerReturn
        :raises Exception:             If not a dictionary.
        """
        
        data_layer_ids = None
        status         = None
        message        = None
        id             = None
        
        common.check_dict(data_layer_return_dict)
        if "datalayerIds" in data_layer_return_dict:
            if data_layer_return_dict.get("datalayerIds") is not None:
                if isinstance(data_layer_return_dict.get("datalayerIds"), list):
                    data_layer_ids = common.from_list(data_layer_return_dict.get("datalayerIds"), common.check_str)
                elif isinstance(data_layer_return_dict.get("datalayerIds"), int):
                    data_layer_ids = common.check_str(data_layer_return_dict.get("datalayerIds"))
        elif "data_layer_ids" in data_layer_return_dict:
            if data_layer_return_dict.get("data_layer_ids") is not None:
                if isinstance(data_layer_return_dict.get("data_layer_ids"), list):
                    data_layer_ids = common.from_list(data_layer_return_dict.get("data_layer_ids"), common.check_str)
                elif isinstance(data_layer_return_dict.get("data_layer_ids"), int):
                    data_layer_ids = common.check_str(data_layer_return_dict.get("data_layer_ids"))
        if "status" in data_layer_return_dict:
            if data_layer_return_dict.get("status") is not None:
                status = common.check_int(data_layer_return_dict.get("status"))
        if "message" in data_layer_return_dict:
            if data_layer_return_dict.get("message") is not None:
                message = common.check_str(data_layer_return_dict.get("message"))
        if "id" in data_layer_return_dict:
            if data_layer_return_dict.get("id") is not None:
                id = common.check_str(data_layer_return_dict.get("id"))
        return DataLayerReturn(data_layer_ids = data_layer_ids,
                               status         = status,
                               message        = message,
                               id             = id
                              )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.   
                 
        :rtype: dict
        """
        
        data_layer_return_dict: dict = {}
        if self._data_layer_ids is not None:
            data_layer_return_dict["data_layer_ids"] = self._data_layer_ids
        if self._status is not None:
            data_layer_return_dict["status"] = self._status
        if self._message is not None:
            data_layer_return_dict["message"] = self._message
        if self._id is not None:
            data_layer_return_dict["id"] = self._id
        return data_layer_return_dict

    #
    def from_json(data_layer_return_json: Any):

        """
        Create a DataLayerReturn object from json (dictonary or str).
        
        :param data_layer_return_dict: A json dictionary that contains the keys of a DataLayerReturn or a string representation of a json dictionary.
        :type data_layer_return_dict:  Any             
        :rtype:                        ibmpairs.catalog.DataLayerReturn
        :raises Exception:             If not a dictionary or a string.
        """
        
        if isinstance(data_layer_return_json, dict):
            data_layer_return = DataLayerReturn.from_dict(data_layer_return_json)
        elif isinstance(data_layer_return_json, str):
            data_layer_return_dict = json.loads(data_layer_return_json)
            data_layer_return = DataLayerReturn.from_dict(data_layer_return_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_return_json), "data_layer_return_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layer_return

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict())


#
class DataLayerDimensionReturn:
    #_data_layer_dimension_id: str
    #_status: int
    #_message: str
    
    """
    An object to represent the response from a DataLayerDimension object call.
    
    :param data_layer_dimension_id: A Data Layer Dimension ID.
    :type data_layer_dimension_id:  str
    :param status:                  A status code.
    :type status:                   int
    :param message:                 A status message from the call.
    :type message:                  str
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
                 data_layer_dimension_id: str = None,
                 status: int                  = None,
                 message: str                 = None
                ):
        self._data_layer_dimension_id = data_layer_dimension_id
        self._status                  = status
        self._message                 = message
        
    #    
    def get_data_layer_dimension_id(self):
        return self._data_layer_dimension_id

    #
    def set_data_layer_dimension_id(self, data_layer_dimension_id):
        self._data_layer_dimension_id = common.check_str(data_layer_dimension_id)
        
    #    
    def del_data_layer_dimension_id(self): 
        del self._data_layer_dimension_id

    #    
    data_layer_dimension_id = property(get_data_layer_dimension_id, set_data_layer_dimension_id, del_data_layer_dimension_id)

    #    
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_int(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)

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
    def from_dict(data_layer_dimension_return_dict: Any):

        """
        Create a DataLayerDimensionReturn object from a dictionary.
        
        :param data_layer_dimensions_return_dict: A dictionary that contains the keys of a DataLayerDimensionReturn.
        :type data_layer_dimensions_return_dict:  Any             
        :rtype:                                   ibmpairs.catalog.DataLayerDimensionReturn
        :raises Exception:                        If not a dictionary.
        """
        
        data_layer_property_id = None
        status                 = None
        message                = None
        
        common.check_dict(data_layer_dimension_return_dict)
        if "datalayerDimensionId" in data_layer_dimension_return_dict:
            if data_layer_dimension_return_dict.get("datalayerDimensionId") is not None:
                data_layer_dimension_id = common.check_str(data_layer_dimension_return_dict.get("datalayerDimensionId"))
        elif "data_layer_dimension_id" in data_layer_dimension_return_dict:
            if data_layer_dimension_return_dict.get("data_layer_dimension_id") is not None:
                data_layer_dimension_id = common.check_str(data_layer_dimension_return_dict.get("data_layer_dimension_id"))
        if "status" in data_layer_dimension_return_dict:
            if data_layer_dimension_return_dict.get("status") is not None:
                status = common.check_int(data_layer_dimension_return_dict.get("status"))
        if "message" in data_layer_dimension_return_dict:
            if data_layer_dimension_return_dict.get("message") is not None:
                message = common.check_str(data_layer_dimension_return_dict.get("message"))
        return DataLayerDimensionReturn(data_layer_dimension_id = data_layer_dimension_id,
                                        status                  = status,
                                        message                 = message
                                       )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype: dict
        """
        
        data_layer_dimension_return_dict: dict = {}
        if self._data_layer_dimension_id is not None:
            data_layer_dimension_return_dict["data_layer_dimension_id"] = self._data_layer_dimension_id
        if self._status is not None:
            data_layer_dimension_return_dict["status"] = self._status
        if self._message is not None:
            data_layer_dimension_return_dict["message"] = self._message
        return data_layer_dimension_return_dict

    #
    def from_json(data_layer_dimension_return_json: Any):

        """
        Create a DataLayerDimensionReturn object from json (dictonary or str).
        
        :param data_layer_dimensions_return_dict: A json dictionary that contains the keys of a DataLayerDimensionReturn or a string representation of a json dictionary.
        :type data_layer_dimensions_return_dict:  Any             
        :rtype:                                   ibmpairs.catalog.DataLayerDimensionReturn
        :raises Exception:                        If not a dictionary or a string.
        """
        
        if isinstance(data_layer_dimension_return_json, dict):
            data_layer_dimension_return = DataLayerDimensionReturn.from_dict(data_layer_dimension_return_json)
        elif isinstance(data_layer_dimension_return_json, str):
            data_layer_dimension_return_dict = json.loads(data_layer_dimension_return_json)
            data_layer_dimension_return = DataLayerDimensionReturn.from_dict(data_layer_dimension_return_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_dimension_return_json), "data_layer_dimension_return_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layer_dimension_return

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict())


#
class DataLayerDimension:
    #_client: cl.Client
    #_data_layer_id: str
    
    # Common
    #_full_name: str
    #_short_name: str
    #_type: str
    #_unit: str
    
    # GET Exclusive 
    # (GET /v2/datalayers/{datalayer_id}/datalayer_dimensions)
    #_id: str
    #_order: int
    #_identifier: str
    
    # Internal
    #_data_layer_dimension_response: DataLayerDimensionReturn
    
    """
    An object to represent an IBM PAIRS Data Layer Dimension.
    
    :param client:                        An IBM PAIRS Client.
    :type client:                         ibmpairs.client.Client
    :param data_layer_id:                 A Data Layer ID.
    :type data_layer_id:                  str
    :param id:                            The ID number of the Data Layer Dimension.
    :type id:                             str
    :param order:                         The order number.
    :type order:                          int
    :param full_name:                     Full name of the Data Layer Dimension.
    :type full_name:                      str
    :param short_name:                    Short name of the Data Layer Dimension.
    :type short_name:                     str
    :param type:                          Type of the Data Layer Dimension.
    :type type:                           str
    :param identifier:                    The identifier.
    :type identifier:                     str
    :param unit:                          Unit of the Data Layer Dimension.
    :type unit:                           str
    :param data_layer_dimension_response: A response object from a DataLayerDimension method call.
    :type data_layer_dimension_response:  ibmpairs.catalog.DataLayerDimensionReturn
    :raises Exception:                    An ibmpairs.client.Client is not found.
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
                 client: cl.Client                                       = None, 
                 data_layer_id: str                                      = None,
                 id: str                                                 = None,
                 order: int                                              = None,
                 full_name: str                                          = None,
                 short_name: str                                         = None,
                 type: str                                               = None,
                 identifier: str                                         = None,
                 unit: str                                               = None,
                 data_layer_dimension_response: DataLayerDimensionReturn = None
                ):
        self._client        = common.set_client(input_client  = client,
                                                global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._data_layer_id = data_layer_id
        self._id            = id
        self._order         = order
        self._full_name     = full_name
        self._short_name    = short_name
        self._type          = type
        self._identifier    = identifier
        self._unit          = unit
        
        if data_layer_dimension_response is None:
            self._data_layer_dimension_response = DataLayerDimensionReturn()
        else:
            self._data_layer_dimension_response = data_layer_dimension_response
        
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
    def get_data_layer_id(self):
        return self._data_layer_id

    #
    def set_data_layer_id(self, data_layer_id):
        self._data_layer_id = common.check_str(data_layer_id)
        
    #    
    def del_data_layer_id(self): 
        del self._data_layer_id

    #    
    data_layer_id = property(get_data_layer_id, set_data_layer_id, del_data_layer_id)
    
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
    def get_full_name(self):
        return self._full_name

    #
    def set_full_name(self, full_name):
        self._full_name = common.check_str(full_name)
        
    #    
    def del_full_name(self): 
        del self._full_name

    #    
    full_name = property(get_full_name, set_full_name, del_full_name)

    #    
    def get_short_name(self):
        return self._short_name

    #
    def set_short_name(self, short_name):
        self._short_name = common.check_str(short_name)
        
    #    
    def del_short_name(self): 
        del self._short_name

    #    
    short_name = property(get_short_name, set_short_name, del_short_name)

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
    def get_identifier(self):
        return self._identifier

    #
    def set_identifier(self, identifier):
        self._identifier = common.check_str(identifier)
        
    #    
    def del_identifier(self): 
        del self._identifier

    #    
    identifier = property(get_identifier, set_identifier, del_identifier)

    #    
    def get_unit(self):
        return self._unit

    #
    def set_unit(self, unit):
        self._unit = common.check_str(unit)
        
    #    
    def del_unit(self): 
        del self._unit

    #    
    unit = property(get_unit, set_unit, del_unit)

    #
    def get_data_layer_dimension_response(self):
      return self._data_layer_dimension_response

    #
    def set_data_layer_dimension_response(self, data_layer_dimension_response):
      self._data_layer_dimension_response = common.check_class(data_layer_dimension_response, DataLayerDimensionReturn)

    #    
    def del_data_layer_dimension_response(self): 
      del self._data_layer_dimension_response

    #    
    data_layer_dimension_response = property(get_data_layer_dimension_response, set_data_layer_dimension_response, del_data_layer_dimension_response)
    
    #    
    def from_dict(data_layer_dimension_dict: Any):

        """
        Create a DataLayerDimension object from a dictionary.
        
        :param data_layer_dimension_dict: A dictionary that contains the keys of a DataLayerDimension.
        :type data_layer_dimension_dict:  Any             
        :rtype:                           ibmpairs.catalog.DataLayerDimension
        :raises Exception:                if not a dictionary.
        """
        
        data_layer_id                 = None 
        id                            = None
        order                         = None
        full_name                     = None
        short_name                    = None
        type                          = None
        identifier                    = None
        unit                          = None
        data_layer_dimension_response = None
        
        common.check_dict(data_layer_dimension_dict)
        if "data_layer_id" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("data_layer_id") is not None:
                data_layer_id = common.check_str(data_layer_dimension_dict.get("data_layer_id"))
        if "id" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("id") is not None:
                id = common.check_str(data_layer_dimension_dict.get("id"))
        if "order" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("order") is not None:
                order = common.check_int(data_layer_dimension_dict.get("order"))
        if "fullName" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("fullName") is not None:
                full_name = common.check_str(data_layer_dimension_dict.get("fullName"))
        elif "full_name" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("full_name") is not None:
                full_name = common.check_str(data_layer_dimension_dict.get("full_name"))
        if "shortName" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("shortName") is not None:
                short_name = common.check_str(data_layer_dimension_dict.get("shortName"))
        elif "short_name" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("short_name") is not None:
                short_name = common.check_str(data_layer_dimension_dict.get("short_name"))
        if "type" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("type") is not None:
                type = common.check_str(data_layer_dimension_dict.get("type"))
        if "identifier" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("identifier") is not None:
                identifier = common.check_str(data_layer_dimension_dict.get("identifier"))
        if "unit" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("unit") is not None:
                unit = common.check_str(data_layer_dimension_dict.get("unit"))
        if "data_layer_dimension_response" in data_layer_dimension_dict:
            if data_layer_dimension_dict.get("data_layer_dimension_response") is not None:
                data_layer_dimension_response = DataLayerDimensionReturn.from_dict(data_layer_dimension_dict.get("data_layer_dimension_response"))
        return DataLayerDimension(data_layer_id                 = data_layer_id,
                                  id                            = id,
                                  order                         = order,
                                  full_name                     = full_name,
                                  short_name                    = short_name,
                                  type                          = type,
                                  identifier                    = identifier,
                                  unit                          = unit,
                                  data_layer_dimension_response = data_layer_dimension_response                                                                
                                 )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_layer_dimension_dict: dict = {}
        if self._data_layer_id is not None:
          data_layer_dimension_dict["data_layer_id"] = self._data_layer_id
        if self._id is not None:
            data_layer_dimension_dict["id"] = self._id
        if self._order is not None:
            data_layer_dimension_dict["order"] = self._order
        if self._full_name is not None:
            data_layer_dimension_dict["full_name"] = self._full_name
        if self._short_name is not None:
            data_layer_dimension_dict["short_name"] = self._short_name
        if self._type is not None:
            data_layer_dimension_dict["type"] = self._type
        if self._identifier is not None:
            data_layer_dimension_dict["identifier"] = self._identifier
        if self._unit is not None:
            data_layer_dimension_dict["unit"] = self._unit
        if self._data_layer_dimension_response is not None:
            data_layer_dimension_dict["data_layer_dimension_response"] = common.class_to_dict(self._data_layer_dimension_response, DataLayerDimensionReturn)
        return data_layer_dimension_dict
    
    #    
    def to_dict_data_layer_dimension_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation. 
                   
        :rtype: dict
        """
        
        data_layer_dimension_dict: dict = {}
        if self._full_name is not None:
            data_layer_dimension_dict["fullName"] = self._full_name
        if self._short_name is not None:
            data_layer_dimension_dict["shortName"] = self._short_name
        if self._type is not None:
            data_layer_dimension_dict["type"] = self._type
        if self._unit is not None:
            data_layer_dimension_dict["unit"] = self._unit
        return data_layer_dimension_dict

    #
    def from_json(data_layer_dimension_json: Any):

        """
        Create a DataLayerDimension object from json (dictonary or str).
        
        :param data_layer_dimension_dict: A json dictionary that contains the keys of a DataLayerDimension or a string representation of a json dictionary.
        :type data_layer_dimension_dict:  Any             
        :rtype:                           ibmpairs.catalog.DataLayerDimension
        :raises Exception:                if not a dictionary or a string.
        """
        
        if isinstance(data_layer_dimension_json, dict):
            data_layer_dimension = DataLayerDimension.from_dict(data_layer_dimension_json)
        elif isinstance(data_layer_dimension_json, str):
            data_layer_dimension_dict = json.loads(data_layer_dimension_json)
            data_layer_dimension = DataLayerDimension.from_dict(data_layer_dimension_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_dimension_json), "data_layer_dimension_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layer_dimension

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict())
        
    #
    def to_json_data_layer_dimension_post(self):

        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict_data_layer_dimension_post())
    
    #
    def display(self,
                columns: List[str] = ['id', 'short_name', 'identifier', 'order', 'full_name', 'type', 'unit']
               ):
                
        """
        A method to return a pandas.DataFrame object of a get result.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['id', 'short_name', 'identifier', 'order', 'full_name', 'type', 'unit']
        :type columns:  List[str]
        :returns:       A pandas.DataFrame of attributes from the object.
        :rtype:         pandas.DataFrame
        """

        display_dict = self.to_dict()
      
        display_df = pd.DataFrame([display_dict], columns=columns)  

        return display_df
        
    #
    def get(self,
            id                = None,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a Data Layer Dimension.
        
        :param id:         The Data Layer Dimension ID of the Data Layer Dimension to be gathered.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A populated Data Layer Dimension object.
        :rtype:            ibmpairs.catalog.DataLayerDimension
        :raises Exception: A ibmpairs.client.Client is not found,
                           an ID is not provided or already held in the object,
                           a server error occurred,
                           the status of the request is not 200.
        """
            
        if id is not None:
            self._id = common.check_str(id)
            
        if self._id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_DIMENSION_ID
            logger.error(msg)
            raise common.PAWException(msg)
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        try:
            response = cli.get(url    = cli.get_host() +
                                        constants.CATALOG_DATA_LAYER_DIMENSIONS_API +
                                        common.check_str(self._id),
                               verify = verify
                              )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYER_DIMENSIONS_API + common.check_str(self._id), e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status_code != 200:
            error_message = 'failed'

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYER_DIMENSIONS_API + common.check_str(self._id), response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            data_layer_dimension_get = DataLayerDimension.from_dict(response.json())
            return data_layer_dimension_get

    #
    def create(self,
               data_layer_id      = None,
               client: cl.Client  = None,
               verify: bool       = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to create a Data Layer Dimension.
        
        :param data_layer_id: The ID of the Data Layer the Data Layer Dimension should be created for.
        :type data_layer_id:  str
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :raises Exception:    A ibmpairs.client.Client is not found,
                              a Data Layer ID is not provided or already held in the object,
                              a server error occurred,
                              the status of the request is not 200.
        """
                
        if data_layer_id is not None:
            self._data_layer_id = common.check_str(data_layer_id)
          
        if self._data_layer_id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_DIMENSION_DATA_LAYER_ID
            logger.error(msg)
            raise common.PAWException(msg)

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client) 
        
        data_layer_dimension = self.to_json_data_layer_dimension_post()
        
        try:
             response = cli.post(url   = cli.get_host() + 
                                         constants.CATALOG_DATA_LAYERS_API +
                                         self._data_layer_id + 
                                         constants.CATALOG_DATA_LAYERS_API_DIMENSIONS,
                               headers = constants.CLIENT_PUT_AND_POST_HEADER,
                               body    = data_layer_dimension,
                               verify  = verify
                              )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('POST', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._data_layer_id) + constants.CATALOG_DATA_LAYERS_API_DIMENSIONS, e)
            logger.error(msg)
            raise common.PAWException(msg)
                              
        if response.status_code != 200:
            error_message = 'failed'
                
            if response.json() is not None:
                try:
                    data_layer_dimension_return = data_layer_dimension_return_from_dict(response.json())
                    error_message = data_layer_dimension_return.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('POST', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._data_layer_id) + constants.CATALOG_DATA_LAYERS_API_DIMENSIONS, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            self._data_layer_dimension_response = data_layer_dimension_return_from_dict(response.json())
            self._id = common.check_str(self._data_layer_dimension_response._data_layer_dimension_id)
            msg = messages.INFO_CATALOG_DATA_LAYER_DIMENSIONS_CREATE_SUCCESS.format(str(self._data_layer_dimension_response._data_layer_dimension_id))
            logger.info(msg)

#
class DataLayerDimensions:
    # 
    #_client: cl.Client 
    
    # Common
    #_data_layer_dimensions: List[DataLayerDimension]
    #_data_layer_id: str
    
    """
    An object to represent a list of IBM PAIRS Data Layer Dimensions.
    
    :param client:                An IBM PAIRS Client.
    :type client:                 ibmpairs.client.Client
    :param data_layer_dimensions: An list of Data Layer Dimensions.
    :type data_layer_dimensions:  List[ibmpairs.catalog.DataLayerDimension]
    :param data_layer_id:         The Data Layer ID of the Data Layer Dimensions.
    :type data_layer_id:          str
    :raises Exception:            An ibmpairs.client.Client is not found.
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
    
    #
    def __getitem__(self, data_layer_dimension_full_name):
      
        """
        A method to overload the default behaviour of the slice on this object to be an
        element from the data_layer_dimensions attribute.
        
        :param data_layer_dimension_full_name: The name of a Data Layer Dimension to search for, if this is 
                                               numeric, the method simply returns the default (list order).
        :type data_layer_dimension_full_name:  str
        :raises Exception:                     If less than one value is found,
                                               if more than one value is found.
        """ 
      
        if isinstance(data_layer_dimension_full_name, int):
            return self._data_layer_dimensions[data_layer_dimension_full_name]
        elif isinstance(data_layer_dimension_full_name, str):
            index_list = []
            index      = 0
            foundCount = 0

            for data_layer_dimension in self._data_layer_dimensions:
                if (data_layer_dimension.full_name == data_layer_dimension_full_name):
                    if (data_layer_dimension.full_name == data_layer_dimension_full_name):
                        foundCount = foundCount + 1
                        index_list.append(index)
                else:
                    msg = messages.WARN_CATALOG_DATA_LAYER_DIMENSIONS_OBJECT_NO_NAME.format(data_layer_dimension_full_name)
                    logger.warning(msg)
                  
                index = index + 1

            if foundCount == 0:
                msg = messages.ERROR_CATALOG_DATA_LAYER_DIMENSIONS_NO_DATA_SET.format(data_layer_dimension_full_name)
                logger.error(msg)
                raise common.PAWException(msg)
            elif foundCount == 1:
                return self._data_layer_dimensions[index_list[0]]
            else:
                msg = messages.ERROR_CATALOG_DATA_LAYER_DIMENSIONS_MULTIPLE_IDENTICAL_NAMES.format(data_layer_dimension_full_name)
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            msg = messages.ERROR_CATALOG_DATA_LAYER_DIMENSIONS_TYPE_UNKNOWN.format(type(data_layer_dimension_full_name))
            logger.error(msg)
            raise common.PAWException(msg)
        
    #
    def __init__(self,
                 client: cl.Client                               = None,
                 data_layer_dimensions: List[DataLayerDimension] = None,
                 data_layer_id: str                              = None
                ):
        self._client                = common.set_client(input_client  = client,
                                                        global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._data_layer_dimensions = data_layer_dimensions
        self._data_layer_id         = data_layer_id
    
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
    def get_data_layer_dimensions(self):
        return self._data_layer_dimensions

    #
    def set_data_layer_dimensions(self, data_layer_dimensions):
        self._data_layer_dimensions = common.check_class(data_layer_dimensions, List[DataLayerDimension])

    #    
    def del_data_layer_dimensions(self): 
        del self._data_layer_dimensions

    #    
    data_layer_dimensions = property(get_data_layer_dimensions, set_data_layer_dimensions, del_data_layer_dimensions)
    
    # 
    def get_data_layer_id(self):
      return self._data_layer_id

    #
    def set_data_layer_id(self, data_layer_id):
      self._data_layer_id = common.check_str(data_layer_id)

    #    
    def del_data_layer_id(self): 
      del self._data_layer_id

    #    
    data_layer_id = property(get_data_layer_id, set_data_layer_id, del_data_layer_id)
    
    #
    def from_dict(data_layer_dimensions_input: Any):

        """
        Create a DataLayerDimensions object from a dictionary.
        
        :param data_layer_dimensions_dict: A dictionary that contains the keys of a DataLayerDimensions.
        :type data_layer_dimensions_dict:  Any             
        :rtype:                            ibmpairs.catalog.DataLayerDimensions
        :raises Exception:                 If not a dictionary.
        """
        
        data_layer_dimensions = None
        
        if isinstance(data_layer_dimensions_input, dict):
            common.check_dict(data_layer_dimensions_input)
            if "data_layer_dimensions" in data_layer_dimensions_input:
                if data_layer_dimensions_input.get("data_layer_dimensions") is not None:
                    data_layer_dimensions = common.from_list(data_layer_dimensions_input.get("data_layer_dimensions"), DataLayerDimension.from_dict)
            if "data_layer_id" in data_layer_dimensions_input:
                if data_layer_dimensions_input.get("data_layer_id") is not None:
                    data_layer_id = common.check_str(data_layer_dimensions_input.get("data_layer_id"))
        elif isinstance(data_layer_dimensions_input, list):
            data_layer_dimensions = common.from_list(data_layer_dimensions_input, DataLayerDimension.from_dict)
        else:
            msg = messages.ERROR_CATALOG_DATA_LAYER_DIMENSIONS_UNKNOWN.format(type(data_layer_dimensions_input))
            logger.error(msg)
            raise common.PAWException(msg)

        return DataLayerDimensions(data_layer_dimensions = data_layer_dimensions)

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_layer_dimensions_dict: dict = {}
        if self._data_layer_dimensions is not None:
            data_layer_dimensions_dict["data_layer_dimensions"] = common.from_list(self._data_layer_dimensions, lambda item: common.class_to_dict(item, DataLayerDimension)) 
        if self._data_layer_id is not None:
            data_layer_dimensions_dict["data_layer_id"] = self._data_layer_id
        return data_layer_dimensions_dict
    
    #
    def from_json(data_layer_dimensions_json: Any):
        
        """
        Create a DataLayerDimensions object from json (dictonary or str).
        
        :param data_layer_dimensions_dict: A json dictionary that contains the keys of a DataLayerDimensions or a string representation of a json dictionary.
        :type data_layer_dimensions_dict:  Any             
        :rtype:                            ibmpairs.catalog.DataLayerDimensions
        :raises Exception:                 If not a dictionary or a string.
        """
        
        if isinstance(data_layer_dimensions_json, dict):
            data_layer_dimensions = DataLayerDimensions.from_dict(data_layer_dimensions_json)
        elif isinstance(data_layer_dimensions_json, str):
            data_layer_dimensions_dict = json.loads(data_layer_dimensions_json)
            data_layer_dimensions = DataLayerDimensions.from_dict(data_layer_dimensions_dict)
        else:
             msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_dimensions_json), "data_layer_dimensions_json")
             logger.error(msg)
             raise common.PAWException(msg)
        return data_layer_dimensions

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
    #
    def display(self,
                columns: List[str] = ['id', 'short_name', 'identifier', 'order', 'full_name', 'type', 'unit'],
                sort_by: str       = 'id'
               ):
        
        """
        A method to return a pandas.DataFrame object of get results.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['id', 'short_name', 'identifier', 'order', 'full_name', 'type', 'unit']
        :type columns:  List[str]
        :returns:       A pandas.DataFrame of attributes from the data_layer_dimensions attribute.
        :rtype:         pandas.DataFrame
        """
                
        display_df = None
      
        for data_layer_dimension in self._data_layer_dimensions:
            next_display = data_layer_dimension.display(columns)
            if display_df is None:
                display_df = next_display
            else:
                display_df = pd.concat([display_df, next_display])
        
        display_df.reset_index(inplace=True, drop=True)
            
        return display_df.sort_values(by=[sort_by])
    
    #
    def get(self,
            data_layer_id     = None,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a list of Data Layer Dimensions by Data Layer ID.
        
        :param data_layer_id: The Data Layer ID of the Data Layer Dimensions to be gathered.
        :type data_layer_id:  str
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :returns:             A populated Data Layer Dimensions object.
        :rtype:               ibmpairs.catalog.DataLayerDimensions
        :raises Exception:    A ibmpairs.client.Client is not found,
                              a Data Layer ID is not provided or already held in the object,
                              a server error occurred,
                              the status of the request is not 200.
        """
        
        if data_layer_id is not None:
            self._data_layer_id = common.check_str(data_layer_id)
          
        if self._data_layer_id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_DIMENSIONS_DATA_LAYER_ID
            logger.error(msg)
            raise common.PAWException(msg)
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        try:
           response = cli.get(url    = cli.get_host() +
                                       constants.CATALOG_DATA_LAYERS_API +
                                       common.check_str(self._data_layer_id) +
                                       constants.CATALOG_DATA_LAYERS_API_DIMENSIONS,
                              verify = verify
                             )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._data_layer_id) + constants.CATALOG_DATA_LAYERS_API_DIMENSIONS, e)
            logger.error(msg)
            raise common.PAWException(msg)
        
        if response.status_code != 200:
            error_message = 'failed'

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._data_layer_id) + constants.CATALOG_DATA_LAYERS_API_DIMENSIONS, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            data_layer_dimensions_get   = DataLayerDimensions.from_dict(response.json())
            self._data_layer_dimensions = data_layer_dimensions_get.data_layer_dimensions

            return data_layer_dimensions_get 


#
class DataLayerPropertyReturn:
    #_data_layer_property_id: str
    #_status: int
    #_message: str
    
    """
    An object to represent the response from a DataLayerProperty object call.
    
    :param data_layer_property_id: A Data Layer Property ID.
    :type data_layer_property_id:  str
    :param status:                 A status code.
    :type status:                  int
    :param message:                A status message from the call.
    :type message:                 str
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
    
    #
    def __init__(self, 
                 data_layer_property_id: str = None,
                 status: int                 = None,
                 message: str                = None
                ):
        self._data_layer_property_id = data_layer_property_id
        self._status                 = status
        self._message                = message
        
    #    
    def get_data_layer_property_id(self):
        return self._data_layer_property_id

    #
    def set_data_layer_property_id(self, data_layer_property_id):
        self._data_layer_property_id = common.check_str(data_layer_property_id)
        
    #    
    def del_data_layer_property_id(self): 
        del self._data_layer_property_id

    #    
    data_layer_property_id = property(get_data_layer_property_id, set_data_layer_property_id, del_data_layer_property_id)

    #    
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_int(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)

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
    def from_dict(data_layer_property_return_dict: Any):

        """
        Create a DataLayerPropertyReturn object from a dictionary.
        
        :param data_layer_property_return_dict: A dictionary that contains the keys of a DataLayerPropertyReturn.
        :type data_layer_property_return_dict:  Any             
        :rtype:                                 ibmpairs.catalog.DataLayerPropertyReturn
        :raises Exception:                      if not a dictionary.
        """
        
        data_layer_property_id = None
        status                 = None
        message                = None
        
        common.check_dict(data_layer_property_return_dict)
        if "datalayerPropertyId" in data_layer_property_return_dict:
            if data_layer_property_return_dict.get("datalayerPropertyId") is not None:
                data_layer_property_id = common.check_str(data_layer_property_return_dict.get("datalayerPropertyId"))
        elif "data_layer_property_id" in data_layer_property_return_dict:
            if data_layer_property_return_dict.get("data_layer_property_id") is not None:
                data_layer_property_id = common.check_str(data_layer_property_return_dict.get("data_layer_property_id"))
        if "status" in data_layer_property_return_dict:
            if data_layer_property_return_dict.get("status") is not None:
                status = common.check_int(data_layer_property_return_dict.get("status"))
        if "message" in data_layer_property_return_dict:
            if data_layer_property_return_dict.get("message") is not None:
                message = common.check_str(data_layer_property_return_dict.get("message"))
        return DataLayerPropertyReturn(data_layer_property_id = data_layer_property_id,
                                       status                 = status,
                                       message                = message
                                      )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_layer_property_return_dict: dict = {}
        if self._data_layer_property_id is not None:
            data_layer_property_return_dict["data_layer_property_id"] = self._data_layer_property_id
        if self._status is not None:
            data_layer_property_return_dict["status"] = self._status
        if self._message is not None:
            data_layer_property_return_dict["message"] = self._message
        return data_layer_property_return_dict

    #
    def from_json(data_layer_property_return_json: Any):

        """
        Create a DataLayerPropertyReturn object from json (dictonary or str).
        
        :param data_layer_property_return_dict: A json dictionary that contains the keys of a DataLayerPropertyReturn or a string representation of a json dictionary.
        :type data_layer_property_return_dict:  Any             
        :rtype:                                 ibmpairs.catalog.DataLayerPropertyReturn
        :raises Exception:                      If not a dictionary or a string.
        """
        
        if isinstance(data_layer_property_return_json, dict):
            data_layer_property_return = DataLayerPropertyReturn.from_dict(data_layer_property_return_json)
        elif isinstance(data_layer_property_return_json, str):
            data_layer_property_return_dict = json.loads(data_layer_property_return_json)
            data_layer_property_return = DataLayerPropertyReturn.from_dict(data_layer_property_return_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_property_return_json), "data_layer_property_return_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layer_property_return

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())

#
class DataLayerProperty:
    # 
    #_client: cl.Client
    
    # Common
    #_full_name: str
    #_short_name: str
    #_type: str
    #_unit: str
    
    # GET Exclusive 
    # (GET /v2/datalayers/{datalayer_id}/datalayer_dimensions)
    #_id: int
    #_order: int
    #_identifier: str
    
    #_data_layer_id: str
    
    # Internal
    #_data_layer_property_response
    
    """
    An object to represent an IBM PAIRS Data Layer Property.
    
    :param client:                       An IBM PAIRS Client.
    :type client:                        ibmpairs.client.Client
    :param data_layer_id:                A Data Layer ID.
    :type data_layer_id:                 str
    :param id:                           The ID number of the Data Layer Property.
    :type id:                            str
    :param order:                        The order number.
    :type order:                         int
    :param full_name:                    Full name of the Data Layer Property.
    :type full_name:                     str
    :param short_name:                   Short name of the Data Layer Property.
    :type short_name:                    str
    :param type:                         Type of the Data Layer Property.
    :type type:                          str
    :param identifier:                   The identifier.
    :type identifier:                    str
    :param unit:                         Unit of the Data Layer Property.
    :type unit:                          str
    :param data_layer_property_response: A response object from a DataLayerProperty method call.
    :type data_layer_property_response:  ibmpairs.catalog.DataLayerPropertyReturn
    :raises Exception:                   An ibmpairs.client.Client is not found.
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
    
    #
    def __init__(self, 
                 client: cl.Client                                     = None,
                 data_layer_id: str                                    = None,
                 id: str                                               = None,
                 order: int                                            = None,
                 full_name: str                                        = None,
                 short_name: str                                       = None,
                 type: str                                             = None,
                 identifier: str                                       = None,
                 unit: str                                             = None,
                 data_layer_property_response: DataLayerPropertyReturn = None
                ):
        self._client        = common.set_client(input_client  = client,
                                                global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._data_layer_id = data_layer_id
        self._id            = id
        self._order         = order
        self._full_name     = full_name
        self._short_name    = short_name
        self._type          = type
        self._identifier    = identifier
        self._unit          = unit
        
        if data_layer_property_response is None:
            self._data_layer_property_response = DataLayerPropertyReturn()
        else:
            self._data_layer_property_response = data_layer_property_response
        
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
    def get_data_layer_id(self):
      return self._data_layer_id

    #
    def set_data_layer_id(self, data_layer_id):
      self._data_layer_id = common.check_str(data_layer_id)
      
    #    
    def del_data_layer_id(self): 
      del self._data_layer_id

    #    
    data_layer_id = property(get_data_layer_id, set_data_layer_id, del_data_layer_id)
    
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
    def get_full_name(self):
        return self._full_name

    #
    def set_full_name(self, full_name):
        self._full_name = common.check_str(full_name)
        
    #    
    def del_full_name(self): 
        del self._full_name

    #    
    full_name = property(get_full_name, set_full_name, del_full_name)

    #    
    def get_short_name(self):
        return self._short_name

    #
    def set_short_name(self, short_name):
        self._short_name = common.check_str(short_name)
        
    #    
    def del_short_name(self): 
        del self._short_name

    #    
    short_name = property(get_short_name, set_short_name, del_short_name)

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
    def get_unit(self):
      return self._unit

    #
    def set_unit(self, unit):
      self._unit = common.check_str(unit)
      
    #    
    def del_unit(self): 
      del self._unit

    #    
    unit = property(get_unit, set_unit, del_unit)

    #    
    def get_identifier(self):
        return self._identifier

    #
    def set_identifier(self, identifier):
        self._identifier = common.check_str(identifier)
        
    #    
    def del_identifier(self): 
        del self._identifier

    #    
    identifier = property(get_identifier, set_identifier, del_identifier)
    
    #
    def get_data_layer_property_response(self):
        return self._data_layer_property_response

    #
    def set_data_layer_property_response(self, data_layer_property_response):
        self._data_layer_property_response = common.check_class(data_layer_property_response, DataLayerPropertyReturn)

    #    
    def del_data_layer_property_response(self): 
        del self._data_layer_property_response

    #    
    data_layer_property_response = property(get_data_layer_property_response, set_data_layer_property_response, del_data_layer_property_response)
    
    #    
    def from_dict(data_layer_property_dict: Any):

        """
        Create a DataLayerProperty object from a dictionary.
        
        :param data_layer_property_dict: A dictionary that contains the keys of a DataLayerProperty.
        :type data_layer_property_dict:  Any             
        :rtype:                          ibmpairs.catalog.DataLayerProperty
        :raises Exception:               if not a dictionary.
        """
        
        data_layer_id                = None
        id                           = None
        order                        = None
        full_name                    = None
        short_name                   = None
        type                         = None
        identifier                   = None
        unit                         = None
        data_layer_property_response = None
        
        common.check_dict(data_layer_property_dict)
        if "data_layer_id" in data_layer_property_dict:
          if data_layer_property_dict.get("data_layer_id") is not None:
            data_layer_id = common.check_int(data_layer_property_dict.get("data_layer_id"))
        if "id" in data_layer_property_dict:
            if data_layer_property_dict.get("id") is not None:
                id = common.check_str(data_layer_property_dict.get("id"))
        if "order" in data_layer_property_dict:
            if data_layer_property_dict.get("order") is not None:
                order = common.check_int(data_layer_property_dict.get("order"))
        if "fullName" in data_layer_property_dict:
            if data_layer_property_dict.get("fullName") is not None:
                full_name = common.check_str(data_layer_property_dict.get("fullName"))
        elif "full_name" in data_layer_property_dict:
            if data_layer_property_dict.get("full_name") is not None:
                full_name = common.check_str(data_layer_property_dict.get("full_name"))
        if "shortName" in data_layer_property_dict:
            if data_layer_property_dict.get("shortName") is not None:
                short_name = common.check_str(data_layer_property_dict.get("shortName"))
        elif "short_name" in data_layer_property_dict:
            if data_layer_property_dict.get("short_name") is not None:
                short_name = common.check_str(data_layer_property_dict.get("short_name"))
        if "type" in data_layer_property_dict:
            if data_layer_property_dict.get("type") is not None:
                type = common.check_str(data_layer_property_dict.get("type"))
        if "identifier" in data_layer_property_dict:
            if data_layer_property_dict.get("identifier") is not None:
                identifier = common.check_str(data_layer_property_dict.get("identifier"))
        if "unit" in data_layer_property_dict:
            if data_layer_property_dict.get("unit") is not None:
                unit = common.check_str(data_layer_property_dict.get("unit"))
        if "data_layer_property_response" in data_layer_property_dict:
            if data_layer_property_dict.get("data_layer_property_response") is not None:
                data_layer_property_response = DataLayerPropertyReturn.from_dict(data_layer_property_dict.get("data_layer_property_response"))
        return DataLayerProperty(data_layer_id                = data_layer_id,
                                 id                           = id,
                                 order                        = order,
                                 full_name                    = full_name,
                                 short_name                   = short_name,
                                 type                         = type,
                                 identifier                   = identifier,
                                 unit                         = unit,
                                 data_layer_property_response = data_layer_property_response                                                               
                                )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_layer_property_dict: dict = {}
        if self._data_layer_id is not None:
            data_layer_property_dict["data_layer_id"] = self._data_layer_id
        if self._id is not None:
            data_layer_property_dict["id"] = self._id
        if self._order is not None:
            data_layer_property_dict["order"] = self._order
        if self._full_name is not None:
            data_layer_property_dict["full_name"] = self._full_name
        if self._short_name is not None:
            data_layer_property_dict["short_name"] = self._short_name
        if self._type is not None:
            data_layer_property_dict["type"] = self._type
        if self._identifier is not None:
            data_layer_property_dict["identifier"] = self._identifier
        if self._unit is not None:
            data_layer_property_dict["unit"] = self._unit
        if self._data_layer_property_response is not None:
            data_layer_property_dict["data_layer_property_response"] = common.class_to_dict(self._data_layer_property_response, DataLayerPropertyReturn)
        return data_layer_property_dict
        
    # 
    def to_dict_data_layer_property_post(self):

        """
        Create a dictionary from the objects structure ready for a POST operation. 
                   
        :rtype: dict
        """
        
        data_layer_property_dict: dict = {}
        if self._full_name is not None:
            data_layer_property_dict["fullName"] = self._full_name
        if self._short_name is not None:
            data_layer_property_dict["shortName"] = self._short_name
        if self._type is not None:
            data_layer_property_dict["type"] = self._type
        if self._unit is not None:
            data_layer_property_dict["unit"] = self._unit
        return data_layer_property_dict

    #
    def from_json(data_layer_property_json: Any):

        """
        Create a DataLayerProperty object from json (dictonary or str).
        
        :param data_layer_property_dict: A json dictionary that contains the keys of a DataLayerProperty or a string representation of a json dictionary.
        :type data_layer_property_dict:  Any             
        :rtype:                          ibmpairs.catalog.DataLayerProperty
        :raises Exception:               If not a dictionary or a string.
        """
        
        if isinstance(data_layer_property_json, dict):
            data_layer_property = DataLayerProperty.from_dict(data_layer_property_json)
        elif isinstance(data_layer_property_json, str):
            data_layer_property_dict = json.loads(data_layer_property_json)
            data_layer_property = DataLayerProperty.from_dict(data_layer_property_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_property_json), "data_layer_property_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layer_property

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())
        
    #
    def to_json_data_layer_property_post(self):

        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation.

        :rtype: string
        """

        return json.dumps(self.to_dict_data_layer_property_post())
        
    #
    def display(self,
                columns: List[str] = ['id', 'short_name', 'identifier', 'order', 'full_name', 'type', 'unit']
               ):
                
        """
        A method to return a pandas.DataFrame object of a get result.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['id', 'short_name', 'identifier', 'order', 'full_name', 'type', 'unit']
        :type columns:  List[str]
        :returns:       A pandas.DataFrame of attributes from the object.
        :rtype:         pandas.DataFrame
        """

        display_dict = self.to_dict()
      
        display_df = pd.DataFrame([display_dict], columns=columns)  

        return display_df
        
    #
    def get(self,
            id                = None,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a Data Layer Property.
        
        :param id:         The Data Layer Property ID of the Data Layer Property to be gathered.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A populated Data Layer Property object.
        :rtype:            ibmpairs.catalog.DataLayerProperty
        :raises Exception: A ibmpairs.client.Client is not found,
                           an ID is not provided or already held in the object,
                           a server error occurred,
                           the status of the request is not 200.
        """
            
        if id is not None:
            self._id = common.check_str(id)
          
        if self._id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_PROPERTY_ID
            logger.error(msg)
            raise common.PAWException(msg)

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        try:
            response = cli.get(url    = cli.get_host() +
                                        constants.CATALOG_DATA_LAYER_PROPERTIES_API +
                                        common.check_str(self._id),
                               verify = verify
                              )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYER_PROPERTIES_API + common.check_str(self._id), e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status_code != 200:
            error_message = 'failed'

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYER_PROPERTIES_API + common.check_str(self._id), response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else: 
            data_layer_property_get = DataLayerProperty.from_dict(response.json())
            return data_layer_property_get
        
    #
    def create(self,
               data_layer_id     = None,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to create a Data Layer Property.
        
        :param data_layer_id: The ID of the Data Layer the Data Layer Property should be created for.
        :type data_layer_id:  str
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :raises Exception:    A ibmpairs.client.Client is not found,
                              a Data Layer ID is not provided or already held in the object,
                              a server error occurred,
                              the status of the request is not 200.
        """
                
        if data_layer_id is not None:
            self._data_layer_id = common.check_str(data_layer_id)
          
        if self._data_layer_id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_PROPERTY_DATA_LAYER_ID
            logger.error(msg)
            raise common.PAWException(msg)

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        data_layer_property = self.to_json_data_layer_property_post()
        
        try:
            response = cli.post(url     = cli.get_host() + 
                                          constants.CATALOG_DATA_LAYERS_API +
                                          common.check_str(self._data_layer_id) + 
                                          constants.CATALOG_DATA_LAYERS_API_PROPERTIES,
                                headers = constants.CLIENT_PUT_AND_POST_HEADER,
                                body    = data_layer_property,
                                verify  = verify
                               )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('POST', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._data_layer_id) + constants.CATALOG_DATA_LAYERS_API_PROPERTIES, e)
            logger.error(msg)
            raise common.PAWException(msg)
                              
        if response.status_code != 200:
            error_message = 'failed'
                
            if response.json() is not None:
                try:
                    self._data_layer_property_return = data_layer_property_return_from_dict(response.json())
                    error_message = self._data_layer_property_return.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('POST', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._data_layer_id) + constants.CATALOG_DATA_LAYERS_API_PROPERTIES, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            self._data_layer_property_response = data_layer_property_return_from_dict(response.json())
            self._id = common.check_str(self._data_layer_property_response._data_layer_property_id)
            msg = messages.INFO_CATALOG_DATA_LAYER_PROPERTY_CREATE_SUCCESS.format(common.check_str(self._data_layer_property_response._data_layer_property_id))
            logger.info(msg) 

#
class DataLayerProperties:
    # 
    #_client: cl.Client 
    
    # Common
    #_data_layer_properties: List[DataLayerProperty]
    #_data_layer_id: str
    
    """
    An object to represent a list of IBM PAIRS Data Layer Properties.
    
    :param client:                An IBM PAIRS Client.
    :type client:                 ibmpairs.client.Client
    :param data_layer_properties: An list of Data Layer Properties.
    :type data_layer_properties:  List[ibmpairs.catalog.DataLayerProperty]
    :param data_layer_id:         The Data Layer ID of the Data Layer Properties.
    :type data_layer_id:          str
    :raises Exception:            An ibmpairs.client.Client is not found.
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
    def __getitem__(self, data_layer_property_full_name):
      
        """
        A method to overload the default behaviour of the slice on this object to be an
        element from the data_layer_properties attribute.
        
        :param data_layer_property_full_name: The name of a Data Layer Property to search for, if this is 
                                               numeric, the method simply returns the default (list order).
        :type data_layer_property_full_name:  str
        :raises Exception:                    If less than one value is found, 
                                              if more than one value is found.
        """
        
        if isinstance(data_layer_property_full_name, int):
            return self._data_layer_properties[data_layer_property_full_name]
        elif isinstance(data_layer_property_full_name, str):
            index_list = []
            index      = 0
            foundCount = 0

            for data_layer_property in self._data_layer_properties:
                if (data_layer_property.full_name == data_layer_property_full_name):
                    if (data_layer_property.full_name == data_layer_property_full_name):
                        foundCount = foundCount + 1
                        index_list.append(index)
                else:
                    msg = messages.WARN_CATALOG_DATA_LAYER_PROPERTIES_OBJECT_NO_NAME.format(data_layer_property_full_name)
                    logger.warning(msg)
                  
                index = index + 1

            if foundCount == 0:
                msg = messages.ERROR_CATALOG_DATA_LAYER_PROPERTIES_NO_DATA_SET.format(data_layer_property_full_name)
                logger.error(msg)
                raise common.PAWException(msg)
            elif foundCount == 1:
                return self._data_layer_properties[index_list[0]]
            else:
                msg = messages.ERROR_CATALOG_DATA_LAYER_PROPERTIES_MULTIPLE_IDENTICAL_NAMES.format(data_layer_property_full_name)
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            msg = messages.ERROR_CATALOG_DATA_LAYER_PROPERTIES_TYPE_UNKNOWN.format(type(data_layer_property_full_name))
            logger.error(msg)
            raise common.PAWException(msg)
        
    #
    def __init__(self,
                 client: cl.Client                              = None,
                 data_layer_properties: List[DataLayerProperty] = None,
                 data_layer_id: str                             = None
                ):
        self._client                = common.set_client(input_client  = client,
                                                        global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._data_layer_properties = data_layer_properties
        self._data_layer_id         = data_layer_id
    
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
    def get_data_layer_properties(self):
        return self._data_layer_properties

    #
    def set_data_layer_properties(self, data_layer_properties):
        self._data_layer_properties = common.check_class(data_layer_properties, List[DataLayerProperty])

    #    
    def del_data_layer_properties(self): 
        del self._data_layer_properties

    #    
    data_layer_properties = property(get_data_layer_properties, set_data_layer_properties, del_data_layer_properties)
    
    # 
    def get_data_layer_id(self):
      return self._data_layer_id

    #
    def set_data_layer_id(self, data_layer_id):
      self._data_layer_id = common.check_str(data_layer_id)

    #    
    def del_data_layer_id(self): 
      del self._data_layer_id

    #    
    data_layer_id = property(get_data_layer_id, set_data_layer_id, del_data_layer_id)
    
    #
    def from_dict(data_layer_properties_input: Any):

        """
        Create a DataLayerProperties object from a dictionary.
        
        :param data_layer_properties_dict: A dictionary that contains the keys of a DataLayerProperties.
        :type data_layer_properties_dict:  Any             
        :rtype:                            ibmpairs.catalog.DataLayerProperties
        :raises Exception:                 If not a dictionary.
        """
        
        data_layer_properties = None
        
        if isinstance(data_layer_properties_input, dict):
            common.check_dict(data_layer_properties_input)
            if "data_layer_properties" in data_layer_properties_input:
                if data_layer_properties_input.get("data_layer_properties") is not None:
                    data_layer_properties = common.from_list(data_layer_properties_input.get("data_layer_properties"), DataLayerProperty.from_dict)
            if "data_layer_id" in data_layer_properties_input:
                if data_layer_properties_input.get("data_layer_id") is not None:
                    data_layer_id = common.check_str(data_layer_properties_input.get("data_layer_id"))
        elif isinstance(data_layer_properties_input, list):
            data_layer_properties = common.from_list(data_layer_properties_input, DataLayerProperty.from_dict)
        else:
            msg = messages.ERROR_CATALOG_DATA_LAYER_PROPERTIES_UNKNOWN.format(type(data_layer_properties_input))
            logger.error(msg)
            raise common.PAWException(msg)

        return DataLayerProperties(data_layer_properties = data_layer_properties)

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_layer_properties_dict: dict = {}
        if self._data_layer_properties is not None:
            data_layer_properties_dict["data_layer_properties"] = common.from_list(self._data_layer_properties, lambda item: common.class_to_dict(item, DataLayerProperty)) 
        if self._data_layer_id is not None:
            data_layer_properties_dict["data_layer_id"] = self._data_layer_id
        return data_layer_properties_dict
    
    #
    def from_json(data_layer_properties_json: Any):

        """
        Create a DataLayerProperties object from json (dictonary or str).

        :param data_layer_properties_dict: A json dictionary that contains the keys of a DataLayerProperties or a string representation of a json dictionary.
        :type data_layer_properties_dict:  Any             
        :rtype:                            ibmpairs.catalog.DataLayerProperties
        :raises Exception:                 If not a dictionary or a string.
        """
        
        if isinstance(data_layer_properties_json, dict):
            data_layer_properties = DataLayerProperties.from_dict(data_layer_properties_json)
        elif isinstance(data_layer_properties_json, str):
            data_layer_properties_dict = json.loads(data_layer_properties_json)
            data_layer_properties = DataLayerProperties.from_dict(data_layer_properties_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_properties_json), "data_layer_properties_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layer_properties

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
    #
    def display(self,
                columns: List[str] = ['id', 'short_name', 'identifier', 'order', 'full_name', 'type', 'unit'],
                sort_by: str       = 'id'
               ):
                
        """
        A method to return a pandas.DataFrame object of get results.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['id', 'name', 'description_short', 'description_long']
        :type columns:  List[str]
        :returns:       A pandas.DataFrame of attributes from the data_layer_properties attribute.
        :rtype:         pandas.DataFrame
        """
        
        display_df = None
      
        for data_layer_property in self._data_layer_properties:
            next_display = data_layer_property.display(columns)
            if display_df is None:
                display_df = next_display
            else:
                display_df = pd.concat([display_df, next_display])
                
        display_df.reset_index(inplace=True, drop=True)
            
        return display_df.sort_values(by=[sort_by]) 
    
    #
    def get(self,
            data_layer_id     = None,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a list of Data Layer Properties by Data Layer ID.
        
        :param data_layer_id: The Data Layer ID of the Data Layer Properties to be gathered.
        :type data_layer_id:  str
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :returns:             A populated Data Layer Properties object.
        :rtype:               ibmpairs.catalog.DataLayerProperties
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              a Data Layer ID is not provided or already held in the object, 
                              a server error occurred, 
                              the status of the request is not 200.
        """
        
        if data_layer_id is not None:
            self._data_layer_id = common.check_str(data_layer_id)
          
        if self._data_layer_id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_PROPERTIES_ID
            logger.error(msg)
            raise common.PAWException(msg)
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        try:
            response = cli.get(url = cli.get_host() +
                                     constants.CATALOG_DATA_LAYERS_API +
                                     common.check_str(data_layer_id) +
                                     constants.CATALOG_DATA_LAYERS_API_PROPERTIES,
                               verify = verify
                              )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(data_layer_id) + constants.CATALOG_DATA_LAYERS_API_PROPERTIES, e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status_code != 200:
            error_message = 'failed'

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(data_layer_id) + constants.CATALOG_DATA_LAYERS_API_PROPERTIES, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            data_layer_properties_get   = DataLayerProperties.from_dict(response.json())
            self._data_layer_properties = data_layer_properties_get.data_layer_properties

            return data_layer_properties_get

#
class DataLayer:
    # 
    #_client: cl.Client
    
    # Common
    #_name: str
    #_description: str
    #_name_alternate: str
    #_rating: float
    #_description_short: str
    #_description_long: str
    #_description_links: List[str]
    #_data_source_name: str
    #_data_source_attribution: str
    #_data_source_description: str
    #_data_source_links: List[str]
    #_update_interval_max: str
    #_update_interval_description: str
    #_lag_horizon: str
    #_lag_horizon_description: str
    #_temporal_resolution: str
    #_temporal_resolution_description: str
    #_spatial_resolution_of_raw_data: str
    #_interpolation: str
    #_interpolation_upload: str
    #_dimensions_description: str
    #_permanence: bool
    #_permanence_description: str
    #_known_issues: str
    #_properties: Properties
    #_spatial_coverage: SpatialCoverage
    #_latitude_min: float
    #_longitude_min: float
    #_latitude_max: float
    #_longitude_max: float
    #_temporal_min: str
    #_temporal_max: str
    #_measurement_interval: str
    #_measurement_interval_description: str
    #_meaning_of_timestamp: str
    #_meaning_of_spatial_descriptor: str
    #_data_layer_return: DataLayerReturn
    
    # Get Exclusive
    # (GET /v2/datalayers/{datalayer_id})
    #_id: str
    #_dataset: DataSet
    #_created_at: str
    #_updated_at: str 
    #_type: str 
    #_unit: str
    #_dataset_id: str 

    # Create Exclusive
    # (POST /v2/datasets/{dataset_id}/datalayers)
    # N/A
    
    # Update Exclusive
    # (PUT /v2/datalayers/{datalayer_id})
    # N/A
    
    # Get & Update 
    # (GET /v2/datalayers/{datalayer_id})
    # (GET /v2/datalayers/full)
    #_min_value: float
    #_max_value: float

    # Create & Get Common
    # (POST /v2/datasets/{dataset_id}/datalayers)
    # (GET /v2/datalayers/{datalayer_id})
    #_units: str
    #_datatype: str
    #_level: int
    #_crs: str
    #_color_table: ColorTable
    
    # Create & Update Common
    # (POST /v2/datasets/{dataset_id}/datalayers)
    # (PUT /v2/datalayers/{datalayer_id})
    #_description_internal: str
    #_description_internal_links: List[str]
    #_formula: str
    
    # Internal
    #_data_layer_response: DataLayerReturn
    
    """
    An object to represent an IBM PAIRS Data Set.
    
    :param client:                           An IBM PAIRS Client.
    :type client:                            ibmpairs.client.Client
    :param name:                             Data Layer name.
    :type name:                              str
    :param description:                      Data Layer description.
    :type description:                       str
    :param name_alternate:                   Alternative Data Layer name.
    :type name_alternate:                    str
    :param rating:                           Rating.
    :type rating:                            float
    :param description_short:                Short description of the Layer Set.
    :type description_short:                 str
    :param description_long:                 Long description of the Layer Set.
    :type description_long:                  str
    :param description_links:                A list of URLs with supporting documentation.
    :type description_links:                 List[str]
    :param data_source_name:                 A name for the origin data source.
    :type data_source_name:                  str
    :param data_source_attribution:          An attribution for the origin data source.
    :type data_source_attribution:           str
    :param data_source_description:          A description of the origin data source.
    :type data_source_description:           str
    :param data_source_links:                A list of URLs with supporting documentation of the origin data source.
    :type data_source_links:                 List[str]
    :param update_interval_max:              The maximum interval of an update to the Data Layer.
    :type update_interval_max:               str
    :param update_interval_description:      A description of the maximum update interval.
    :type update_interval_description:       str
    :param lag_horizon:                      Lag horizon of the Data Layer.
    :type lag_horizon:                       str
    :param lag_horizon_description:          Lag horizon description.
    :type lag_horizon_description:           str
    :param temporal_resolution:              The temporal resolution of the Data Layer.
    :type temporal_resolution:               str
    :param temporal_resolution_description:  A description of the temporal resolution.
    :type temporal_resolution_description:   str
    :param spatial_resolution_of_raw_data:   Spatial resolution of the raw data.
    :type spatial_resolution_of_raw_data:    str
    :param interpolation:                    Interpolation.
    :type interpolation:                     str
    :param interpolation_upload:             Interpolation on upload.
    :type interpolation_upload:              str
    :param dimensions_description:           A description of the dimensions.
    :type dimensions_description:            str
    :param permanence:                       Permanence.
    :type permanence:                        bool
    :param permanence_description:           A description of the permanence value.
    :type permanence_description:            str
    :param known_issues:                     Known issues with the data.
    :type known_issues:                      str
    :param properties:                       A properties entry.
    :type properties:                        ibmpairs.catalog.Properties
    :param spatial_coverage:                 A spatial coverage entry.
    :type spatial_coverage:                  ibmpairs.catalog.SpatialCoverage 
    :param latitude_min:                     The minimum latitude of the Data Set.
    :type latitude_min:                      float 
    :param longitude_min:                    The minimum longitude of the Data Set.
    :type longitude_min:                     float
    :param latitude_max:                     The maximum latitude of the Data Set.
    :type latitude_max:                      float
    :param longitude_max:                    The maximum longitude of the Data Set.
    :type longitude_max:                     float 
    :param temporal_min:                     The minimum temporal value of the Data Set.
    :type temporal_min:                      str
    :param temporal_max:                     The maximum temporal value of the Data Set.
    :type temporal_max:                      str
    :param measurement_interval:             The measurement interval of the data.
    :type measurement_interval:              str
    :param measurement_interval_description: A description of the measurement interval.
    :type measurement_interval_description:  str
    :param meaning_of_timestamp:             A description of the meaning of the timestamp value.
    :type meaning_of_timestamp:              str
    :param meaning_of_spatial_descriptor:    A description of the meaning of the spatial descriptor.
    :type meaning_of_spatial_descriptor:     str
    :param id:                               The Data Layer ID.
    :type id:                                str
    :param dataset:                          The Data Set a Data Layer belongs to.
    :type dataset:                           ibmpairs.catalog.DataSet
    :param created_at:                       The date of creation.
    :type created_at:                        str
    :param updated_at:                       The last updated date.
    :type updated_at:                        str
    :param type:                             Type.
    :type type:                              str
    :param unit:                             Unit.
    :type unit:                              str
    :param dataset_id:                       The Data Set ID.
    :type dataset_id:                        str
    :param min_value:                        The maximum value of the data in the Data Layer.
    :type min_value:                         float
    :param max_value:                        The minimum value of the data in the Data Layer.
    :type max_value:                         float
    :param units:                            Units.
    :type units:                             str
    :param datatype:                         The data type of the Data Layer.
    :type datatype:                          str
    :param level:                            The default IBM PAIRS level for the Data Layer.
    :type level:                             int
    :param crs:                              CRS.
    :type crs:                               str
    :param color_table:                      A color table to apply to the Data Layer.
    :type color_table:                       ibmpairs.catalog.ColorTable
    :param description_internal:             An internal description of the Data Layer.
    :type description_internal:              str
    :param description_internal_links:       A list of links that give context to the description internal.
    :type description_internal_links:        List[str]
    :param formula:                          Formula.
    :type formula:                           str
    :param data_layer_response:              A server response to a executed Data Layer method call.
    :type data_layer_response:               ibmpairs.catalog.DataLayerReturn
    :raises Exception:                       An ibmpairs.client.Client is not found.
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
                 client: cl.Client                     = None, 
                 name: str                             = None, 
                 description: str                      = None, 
                 name_alternate: str                   = None, 
                 rating: float                         = None, 
                 description_short: str                = None, 
                 description_long: str                 = None, 
                 description_links: List[str]          = None, 
                 data_source_name: str                 = None, 
                 data_source_attribution: str          = None, 
                 data_source_description: str          = None, 
                 data_source_links: List[str]          = None, 
                 update_interval_max: str              = None, 
                 update_interval_description: str      = None, 
                 lag_horizon: str                      = None, 
                 lag_horizon_description: str          = None, 
                 temporal_resolution: str              = None, 
                 temporal_resolution_description: str  = None, 
                 spatial_resolution_of_raw_data: str   = None, 
                 interpolation: str                    = None, 
                 interpolation_upload: str             = None, 
                 dimensions_description: str           = None, 
                 permanence: bool                      = None, 
                 permanence_description: str           = None, 
                 known_issues: str                     = None, 
                 properties: Properties                = None, 
                 spatial_coverage: SpatialCoverage     = None, 
                 latitude_min: float                   = None, 
                 longitude_min: float                  = None, 
                 latitude_max: float                   = None, 
                 longitude_max: float                  = None, 
                 temporal_min: str                     = None, 
                 temporal_max: str                     = None, 
                 measurement_interval: str             = None, 
                 measurement_interval_description: str = None, 
                 meaning_of_timestamp: str             = None, 
                 meaning_of_spatial_descriptor: str    = None,
                 id: str                               = None,
                 dataset: DataSet                      = None,
                 created_at: str                       = None,
                 updated_at: str                       = None,
                 type: str                             = None,
                 unit: str                             = None,
                 dataset_id: str                       = None,
                 min_value: float                      = None,
                 max_value: float                      = None,
                 units: str                            = None,
                 datatype: str                         = None,
                 level: int                            = None,
                 crs: str                              = None,
                 color_table: ColorTable               = None,
                 description_internal: str             = None,
                 description_internal_links: List[str] = None,
                 formula: str                          = None,
                 data_layer_response: DataLayerReturn  = None
                ):
        self._client                           = common.set_client(input_client  = client,
                                                                   global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._name                             = name
        self._description                      = description
        self._name_alternate                   = name_alternate
        self._rating                           = rating
        self._description_short                = description_short
        self._description_long                 = description_long
        self._description_links                = description_links
        self._data_source_name                 = data_source_name
        self._data_source_attribution          = data_source_attribution
        self._data_source_description          = data_source_description
        self._data_source_links                = data_source_links
        self._update_interval_max              = update_interval_max
        self._update_interval_description      = update_interval_description
        self._lag_horizon                      = lag_horizon
        self._lag_horizon_description          = lag_horizon_description
        self._temporal_resolution              = temporal_resolution
        self._temporal_resolution_description  = temporal_resolution_description
        self._spatial_resolution_of_raw_data   = spatial_resolution_of_raw_data
        self._interpolation                    = interpolation
        self._interpolation_upload             = interpolation_upload
        self._dimensions_description           = dimensions_description
        self._permanence                       = permanence
        self._permanence_description           = permanence_description
        self._known_issues                     = known_issues
        self._properties                       = properties
        self._spatial_coverage                 = spatial_coverage
        self._latitude_min                     = latitude_min
        self._longitude_min                    = longitude_min
        self._latitude_max                     = latitude_max
        self._longitude_max                    = longitude_max
        self._temporal_min                     = temporal_min
        self._temporal_max                     = temporal_max
        self._measurement_interval             = measurement_interval
        self._measurement_interval_description = measurement_interval_description
        self._meaning_of_timestamp             = meaning_of_timestamp
        self._meaning_of_spatial_descriptor    = meaning_of_spatial_descriptor
        self._id                               = id
        self._dataset                          = dataset
        self._created_at                       = created_at
        self._updated_at                       = updated_at
        self._type                             = type
        self._unit                             = unit
        self._dataset_id                       = dataset_id
        self._min_value                        = min_value
        self._max_value                        = max_value
        self._units                            = units
        self._datatype                         = datatype
        self._level                            = level
        self._crs                              = crs
        self._color_table                      = color_table
        self._description_internal             = description_internal
        self._description_internal_links       = description_internal_links
        self._formula                          = formula
        
        if data_layer_response is None:
            self._data_layer_response          = DataLayerReturn()
        else:
            self._data_layer_response          = data_layer_response

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
    def get_name(self):
        return self._name

    #
    def set_name(self, name):
        self._name = common.check_str(name)
        
    #    
    def del_name(self): 
        del self._name

    #    
    name = property(get_name, set_name, del_name)

    #    
    def get_description(self):
        return self._description

    #
    def set_description(self, description):
        self._description = common.check_str(description)
        
    #    
    def del_description(self): 
        del self._description

    #    
    description = property(get_description, set_description, del_description)

    #    
    def get_name_alternate(self):
        return self._name_alternate

    #
    def set_name_alternate(self, name_alternate):
        self._name_alternate = common.check_str(name_alternate)
        
    #    
    def del_name_alternate(self): 
        del self._name_alternate

    #    
    name_alternate = property(get_name_alternate, set_name_alternate, del_name_alternate)

    #    
    def get_rating(self):
        return self._rating

    #
    def set_rating(self, rating):
        self._rating = common.check_float(rating)
        
    #    
    def del_rating(self): 
        del self._rating

    #    
    rating = property(get_rating, set_rating, del_rating)

    #    
    def get_description_short(self):
        return self._description_short

    #
    def set_description_short(self, description_short):
        self._description_short = common.check_str(description_short)
        
    #    
    def del_description_short(self): 
        del self._description_short

    #    
    description_short = property(get_description_short, set_description_short, del_description_short)

    #    
    def get_description_long(self):
        return self._description_long

    #
    def set_description_long(self, description_long):
        self._description_long = common.check_str(description_long)
        
    #    
    def del_description_long(self): 
        del self._description_long

    #    
    description_long = property(get_description_long, set_description_long, del_description_long)

    #    
    def get_description_links(self):
        return self._description_links

    #
    def set_description_links(self, description_links):
        self._description_links = common.check_class(description_links, List[str])
        
    #    
    def del_description_links(self): 
        del self._description_links

    #    
    description_links = property(get_description_links, set_description_links, del_description_links)

    #    
    def get_data_source_name(self):
        return self._data_source_name

    #
    def set_data_source_name(self, data_source_name):
        self._data_source_name = common.check_str(data_source_name)
        
    #    
    def del_data_source_name(self): 
        del self._data_source_name

    #    
    data_source_name = property(get_data_source_name, set_data_source_name, del_data_source_name)

    #    
    def get_data_source_attribution(self):
        return self._data_source_attribution

    #
    def set_data_source_attribution(self, data_source_attribution):
        self._data_source_attribution = common.check_str(data_source_attribution)
        
    #    
    def del_data_source_attribution(self): 
        del self._data_source_attribution

    #    
    data_source_attribution = property(get_data_source_attribution, set_data_source_attribution, del_data_source_attribution)

    #    
    def get_data_source_description(self):
        return self._data_source_description

    #
    def set_data_source_description(self, data_source_description):
        self._data_source_description = common.check_str(data_source_description)
        
    #    
    def del_data_source_description(self): 
        del self._data_source_description

    #    
    data_source_description = property(get_data_source_description, set_data_source_description, del_data_source_description)

    #    
    def get_data_source_links(self):
        return self._data_source_links

    #
    def set_data_source_links(self, data_source_links):
        self._data_source_links = common.check_class(data_source_links, List[str])
        
    #    
    def del_data_source_links(self): 
        del self._data_source_links

    #    
    data_source_links = property(get_data_source_links, set_data_source_links, del_data_source_links)

    #    
    def get_update_interval_max(self):
        return self._update_interval_max

    #
    def set_update_interval_max(self, update_interval_max):
        self._update_interval_max = common.check_str(update_interval_max)
        
    #    
    def del_update_interval_max(self): 
        del self._update_interval_max

    #    
    update_interval_max = property(get_update_interval_max, set_update_interval_max, del_update_interval_max)

    #    
    def get_update_interval_description(self):
        return self._update_interval_description

    #
    def set_update_interval_description(self, update_interval_description):
        self._update_interval_description = common.check_str(update_interval_description)
        
    #    
    def del_update_interval_description(self): 
        del self._update_interval_description

    #    
    update_interval_description = property(get_update_interval_description, set_update_interval_description, del_update_interval_description)

    #    
    def get_lag_horizon(self):
        return self._lag_horizon

    #
    def set_lag_horizon(self, lag_horizon):
        self._lag_horizon = common.check_str(lag_horizon)
        
    #    
    def del_lag_horizon(self): 
        del self._lag_horizon

    #    
    lag_horizon = property(get_lag_horizon, set_lag_horizon, del_lag_horizon)

    #    
    def get_lag_horizon_description(self):
        return self._lag_horizon_description

    #
    def set_lag_horizon_description(self, lag_horizon_description):
        self._lag_horizon_description = common.check_str(lag_horizon_description)
        
    #    
    def del_lag_horizon_description(self): 
        del self._lag_horizon_description

    #    
    lag_horizon_description = property(get_lag_horizon_description, set_lag_horizon_description, del_lag_horizon_description)

    #    
    def get_temporal_resolution(self):
        return self._temporal_resolution

    #
    def set_temporal_resolution(self, temporal_resolution):
        self._temporal_resolution = common.check_str(temporal_resolution)
        
    #    
    def del_temporal_resolution(self): 
        del self._temporal_resolution

    #    
    temporal_resolution = property(get_temporal_resolution, set_temporal_resolution, del_temporal_resolution)

    #    
    def get_temporal_resolution_description(self):
        return self._temporal_resolution_description

    #
    def set_temporal_resolution_description(self, temporal_resolution_description):
        self._temporal_resolution_description = common.check_str(temporal_resolution_description)
        
    #    
    def del_temporal_resolution_description(self): 
        del self._temporal_resolution_description

    #    
    temporal_resolution_description = property(get_temporal_resolution_description, set_temporal_resolution_description, del_temporal_resolution_description)

    #    
    def get_spatial_resolution_of_raw_data(self):
        return self._spatial_resolution_of_raw_data

    #
    def set_spatial_resolution_of_raw_data(self, spatial_resolution_of_raw_data):
        self._spatial_resolution_of_raw_data = common.check_str(spatial_resolution_of_raw_data)
        
    #    
    def del_spatial_resolution_of_raw_data(self): 
        del self._spatial_resolution_of_raw_data

    #    
    spatial_resolution_of_raw_data = property(get_spatial_resolution_of_raw_data, set_spatial_resolution_of_raw_data, del_spatial_resolution_of_raw_data)

    #    
    def get_interpolation(self):
        return self._interpolation

    #
    def set_interpolation(self, interpolation):
        self._interpolation = common.check_str(interpolation)
        
    #    
    def del_interpolation(self): 
        del self._interpolation

    #    
    interpolation = property(get_interpolation, set_interpolation, del_interpolation)

    #    
    def get_interpolation_upload(self):
        return self._interpolation_upload

    #
    def set_interpolation_upload(self, interpolation_upload):
        self._interpolation_upload = common.check_str(interpolation_upload)
        
    #    
    def del_interpolation_upload(self): 
        del self._interpolation_upload

    #    
    interpolation_upload = property(get_interpolation_upload, set_interpolation_upload, del_interpolation_upload)

    #    
    def get_dimensions_description(self):
        return self._dimensions_description

    #
    def set_dimensions_description(self, dimensions_description):
        self._dimensions_description = common.check_str(dimensions_description)
        
    #    
    def del_dimensions_description(self): 
        del self._dimensions_description

    #    
    dimensions_description = property(get_dimensions_description, set_dimensions_description, del_dimensions_description)

    #    
    def get_permanence(self):
        return self._permanence

    #
    def set_permanence(self, permanence):
        self._permanence = common.check_bool(permanence)
        
    #    
    def del_permanence(self): 
        del self._permanence

    #    
    permanence = property(get_permanence, set_permanence, del_permanence)

    #    
    def get_permanence_description(self):
        return self._permanence_description

    #
    def set_permanence_description(self, permanence_description):
        self._permanence_description = common.check_str(permanence_description)
        
    #    
    def del_permanence_description(self): 
        del self._permanence_description

    #    
    permanence_description = property(get_permanence_description, set_permanence_description, del_permanence_description)

    #    
    def get_known_issues(self):
        return self._known_issues

    #
    def set_known_issues(self, known_issues):
        self._known_issues = common.check_str(known_issues)
        
    #    
    def del_known_issues(self): 
        del self._known_issues

    #    
    known_issues = property(get_known_issues, set_known_issues, del_known_issues)

    #    
    def get_properties(self):
        return self._properties

    #
    def set_properties(self, properties):
        self._properties = common.check_class(properties, Properties)
        
    #    
    def del_properties(self): 
        del self._properties

    #    
    properties = property(get_properties, set_properties, del_properties)

    #    
    def get_spatial_coverage(self):
        return self._spatial_coverage

    #
    def set_spatial_coverage(self, spatial_coverage):
        self._spatial_coverage = common.check_class(spatial_coverage, SpatialCoverage)
        
    #    
    def del_spatial_coverage(self): 
        del self._spatial_coverage

    #    
    spatial_coverage = property(get_spatial_coverage, set_spatial_coverage, del_spatial_coverage)

    #    
    def get_latitude_min(self):
        return self._latitude_min

    #
    def set_latitude_min(self, latitude_min):
        self._latitude_min = common.check_float(latitude_min)
        
    #    
    def del_latitude_min(self): 
        del self._latitude_min

    #    
    latitude_min = property(get_latitude_min, set_latitude_min, del_latitude_min)

    #    
    def get_longitude_min(self):
        return self._longitude_min

    #
    def set_longitude_min(self, longitude_min):
        self._longitude_min = common.check_float(longitude_min)
        
    #    
    def del_longitude_min(self): 
        del self._longitude_min

    #    
    longitude_min = property(get_longitude_min, set_longitude_min, del_longitude_min)

    #    
    def get_latitude_max(self):
        return self._latitude_max

    #
    def set_latitude_max(self, latitude_max):
        self._latitude_max = common.check_float(latitude_max)
        
    #    
    def del_latitude_max(self): 
        del self._latitude_max

    #    
    latitude_max = property(get_latitude_max, set_latitude_max, del_latitude_max)

    #    
    def get_longitude_max(self):
        return self._longitude_max

    #
    def set_longitude_max(self, longitude_max):
        self._longitude_max = common.check_float(longitude_max)
        
    #    
    def del_longitude_max(self): 
        del self._longitude_max

    #    
    longitude_max = property(get_longitude_max, set_longitude_max, del_longitude_max)

    #    
    def get_temporal_min(self):
        return self._temporal_min

    #
    def set_temporal_min(self, temporal_min):
        self._temporal_min = common.check_str(temporal_min)
        
    #    
    def del_temporal_min(self): 
        del self._temporal_min

    #    
    temporal_min = property(get_temporal_min, set_temporal_min, del_temporal_min)

    #    
    def get_temporal_max(self):
        return self._temporal_max

    #
    def set_temporal_max(self, temporal_max):
        self._temporal_max = common.check_str(temporal_max)
        
    #    
    def del_temporal_max(self): 
        del self._temporal_max

    #    
    temporal_max = property(get_temporal_max, set_temporal_max, del_temporal_max)

    #    
    def get_measurement_interval(self):
        return self._measurement_interval

    #
    def set_measurement_interval(self, measurement_interval):
        self._measurement_interval = common.check_str(measurement_interval)
        
    #    
    def del_measurement_interval(self): 
        del self._measurement_interval

    #    
    measurement_interval = property(get_measurement_interval, set_measurement_interval, del_measurement_interval)

    #    
    def get_measurement_interval_description(self):
        return self._measurement_interval_description

    #
    def set_measurement_interval_description(self, measurement_interval_description):
        self._measurement_interval_description = common.check_str(measurement_interval_description)
        
    #    
    def del_measurement_interval_description(self): 
        del self._measurement_interval_description

    #    
    measurement_interval_description = property(get_measurement_interval_description, set_measurement_interval_description, del_measurement_interval_description)

    #    
    def get_meaning_of_timestamp(self):
        return self._meaning_of_timestamp

    #
    def set_meaning_of_timestamp(self, meaning_of_timestamp):
        self._meaning_of_timestamp = common.check_str(meaning_of_timestamp)
        
    #    
    def del_meaning_of_timestamp(self): 
        del self._meaning_of_timestamp

    #    
    meaning_of_timestamp = property(get_meaning_of_timestamp, set_meaning_of_timestamp, del_meaning_of_timestamp)

    #    
    def get_meaning_of_spatial_descriptor(self):
        return self._meaning_of_spatial_descriptor

    #
    def set_meaning_of_spatial_descriptor(self, meaning_of_spatial_descriptor):
        self._meaning_of_spatial_descriptor = common.check_str(meaning_of_spatial_descriptor)
        
    #    
    def del_meaning_of_spatial_descriptor(self): 
        del self._meaning_of_spatial_descriptor

    #    
    meaning_of_spatial_descriptor = property(get_meaning_of_spatial_descriptor, set_meaning_of_spatial_descriptor, del_meaning_of_spatial_descriptor)

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
    def get_dataset(self):
        return self._dataset

    #
    def set_dataset(self, dataset):
        self._dataset = common.check_class(dataset, DataSet)
        
    #    
    def del_dataset(self): 
        del self._dataset
        
    dataset = property(get_dataset, set_dataset, del_dataset)

    #    
    def get_created_at(self):
        return self._created_at

    #
    def set_created_at(self, created_at):
        self._created_at = common.check_str(created_at)
        
    #    
    def del_created_at(self): 
        del self._created_at

    #    
    created_at = property(get_created_at, set_created_at, del_created_at)
    
    #    
    def get_updated_at(self):
        return self._updated_at

    #
    def set_updated_at(self, updated_at):
        self._updated_at = common.check_str(updated_at)
        
    #    
    def del_updated_at(self): 
        del self._updated_at

    #    
    updated_at = property(get_updated_at, set_updated_at, del_updated_at)
    
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
    def get_unit(self):
        return self._unit

    #
    def set_unit(self, unit):
        self._unit = common.check_str(unit)
        
    #    
    def del_unit(self): 
        del self._unit

    #    
    unit = property(get_unit, set_unit, del_unit)
    
    #    
    def get_dataset_id(self):
        return self._dataset_id

    #
    def set_dataset_id(self, dataset_id):
        self._dataset_id = common.check_str(dataset_id)
        
    #    
    def del_dataset_id(self): 
        del self._dataset_id

    #    
    dataset_id = property(get_dataset_id, set_dataset_id, del_dataset_id)
    
    #    
    def get_min_value(self):
        return self._min_value

    #
    def set_min_value(self, min_value):
        self._min_value = common.check_float(min_value)
        
    #    
    def del_min_value(self): 
        del self._min_value

    #    
    min_value = property(get_min_value, set_min_value, del_min_value)

    #    
    def get_max_value(self):
        return self._max_value

    #
    def set_max_value(self, max_value):
        self._max_value = common.check_float(max_value)
        
    #    
    def del_max_value(self): 
        del self._max_value

    #    
    max_value = property(get_max_value, set_max_value, del_max_value)

    #    
    def get_units(self):
        return self._units

    #
    def set_units(self, units):
        self._units = common.check_str(units)
        
    #    
    def del_units(self): 
        del self._units

    #    
    units = property(get_units, set_units, del_units)

    #    
    def get_datatype(self):
        return self._datatype

    #
    def set_datatype(self, datatype):
        self._datatype = common.check_str(datatype)
        
    #    
    def del_datatype(self): 
        del self._datatype

    #    
    datatype = property(get_datatype, set_datatype, del_datatype)

    #    
    def get_level(self):
        return self._level

    #
    def set_level(self, level):
        self._level = common.check_int(level)
        
    #    
    def del_level(self): 
        del self._level

    #    
    level = property(get_level, set_level, del_level)

    #    
    def get_crs(self):
        return self._crs

    #
    def set_crs(self, crs):
        self._crs = common.check_str(crs)
        
    #    
    def del_crs(self): 
        del self._crs

    #    
    crs = property(get_crs, set_crs, del_crs)

    #    
    def get_color_table(self):
        return self._color_table

    #
    def set_color_table(self, color_table):
        self._color_table = common.check_class(color_table, ColorTable)
        
    #    
    def del_color_table(self): 
        del self._color_table

    #    
    color_table = property(get_color_table, set_color_table, del_color_table)

    #    
    def get_description_internal(self):
        return self._description_internal

    #
    def set_description_internal(self, description_internal):
        self._description_internal = common.check_str(description_internal)
        
    #    
    def del_description_internal(self): 
        del self._description_internal

    #    
    description_internal = property(get_description_internal, set_description_internal, del_description_internal)

    #    
    def get_description_internal_links(self):
        return self._description_internal_links

    #
    def set_description_internal_links(self, description_internal_links):
        self._description_internal_links = common.check_class(description_internal_links, List[str])
        
    #    
    def del_description_internal_links(self): 
        del self._description_internal_links

    #    
    description_internal_links = property(get_description_internal_links, set_description_internal_links, del_description_internal_links)

    #    
    def get_formula(self):
        return self._formula

    #
    def set_formula(self, formula):
        self._formula = common.check_str(formula)
        
    #    
    def del_formula(self): 
        del self._formula

    #    
    formula = property(get_formula, set_formula, del_formula)
    
    #
    def get_data_layer_response(self):
        return self._data_layer_response

    #
    def set_data_layer_response(self, data_layer_response):
        self._data_layer_response = common.check_class(data_layer_response, DataLayerReturn)

    #    
    def del_data_layer_response(self): 
        del self._data_layer_response

    #    
    data_layer_response = property(get_data_layer_response, set_data_layer_response, del_data_layer_response)
    
    #
    def from_dict(data_layer_dict: Any):

        """
        Create a DataLayer object from a dictionary.
        
        :param data_layer_dict: A dictionary that contains the keys of a DataLayer.
        :type data_layer_dict:  Any             
        :rtype:                 ibmpairs.catalog.DataLayer
        :raises Exception:      if not a dictionary.
        """
        
        name                             = None
        description                      = None
        name_alternate                   = None
        rating                           = None
        description_short                = None
        description_long                 = None
        description_links                = None
        data_source_name                 = None
        data_source_attribution          = None
        data_source_description          = None
        data_source_links                = None
        update_interval_max              = None
        update_interval_description      = None
        lag_horizon                      = None
        lag_horizon_description          = None
        temporal_resolution              = None
        temporal_resolution_description  = None
        spatial_resolution_of_raw_data   = None
        interpolation                    = None
        interpolation_upload             = None
        dimensions_description           = None
        permanence                       = None
        permanence_description           = None
        known_issues                     = None
        properties                       = None
        spatial_coverage                 = None
        latitude_min                     = None
        longitude_min                    = None
        latitude_max                     = None
        longitude_max                    = None
        temporal_min                     = None
        temporal_max                     = None
        measurement_interval             = None
        measurement_interval_description = None
        meaning_of_timestamp             = None
        meaning_of_spatial_descriptor    = None
        id                               = None
        dataset                          = None
        created_at                       = None
        updated_at                       = None
        type                             = None
        unit                             = None
        dataset_id                       = None
        min_value                        = None
        max_value                        = None
        units                            = None
        datatype                         = None
        level                            = None
        crs                              = None
        color_table                      = None
        description_internal             = None
        description_internal_links       = None
        formula                          = None
        data_layer_response              = None
                
        common.check_dict(data_layer_dict)
    
        if "name" in data_layer_dict:
            if data_layer_dict.get("name") is not None:
                name = common.check_str(data_layer_dict.get("name"))
        if "description" in data_layer_dict:
            if data_layer_dict.get("description") is not None:
                description = common.check_str(data_layer_dict.get("description"))        
        if "name_alternate" in data_layer_dict:
            if data_layer_dict.get("name_alternate") is not None:
                name_alternate = common.check_str(data_layer_dict.get("name_alternate")) 
        if "rating" in data_layer_dict:
            if data_layer_dict.get("rating") is not None:
                rating = common.check_float(data_layer_dict.get("rating")) 
        if "description_short" in data_layer_dict:
            if data_layer_dict.get("description_short") is not None:
                description_short = common.check_str(data_layer_dict.get("description_short")) 
        if "description_long" in data_layer_dict:
            if data_layer_dict.get("description_long") is not None:
                description_long = common.check_str(data_layer_dict.get("description_long"))
        if "description_links" in data_layer_dict:
            if data_layer_dict.get("description_links") is not None:
                description_links = common.from_list(data_layer_dict.get("description_links"), common.check_str)
        if "data_source_name" in data_layer_dict:
            if data_layer_dict.get("data_source_name") is not None:
                data_source_name = common.check_str(data_layer_dict.get("data_source_name")) 
        if "data_source_attribution" in data_layer_dict:
            if data_layer_dict.get("data_source_attribution") is not None:
                data_source_attribution = common.check_str(data_layer_dict.get("data_source_attribution")) 
        if "data_source_description" in data_layer_dict:
            if data_layer_dict.get("data_source_description") is not None:
                data_source_description = common.check_str(data_layer_dict.get("data_source_description"))
        if "data_source_links" in data_layer_dict:
            if data_layer_dict.get("data_source_links") is not None:
                data_source_links = common.from_list(data_layer_dict.get("data_source_links"), common.check_str)
        if "update_interval_max" in data_layer_dict:
            if data_layer_dict.get("update_interval_max") is not None:
                update_interval_max = common.check_str(data_layer_dict.get("update_interval_max"))
        if "update_interval_description" in data_layer_dict:
            if data_layer_dict.get("update_interval_description") is not None:
                update_interval_description = common.check_str(data_layer_dict.get("update_interval_description"))
        if "lag_horizon" in data_layer_dict:
            if data_layer_dict.get("lag_horizon") is not None:
                lag_horizon = common.check_str(data_layer_dict.get("lag_horizon"))
        if "lag_horizon_description" in data_layer_dict:
            if data_layer_dict.get("lag_horizon_description") is not None:
                lag_horizon_description = common.check_str(data_layer_dict.get("lag_horizon_description"))
        if "temporal_resolution" in data_layer_dict:
            if data_layer_dict.get("temporal_resolution") is not None:
                temporal_resolution = common.check_str(data_layer_dict.get("temporal_resolution"))
        if "temporal_resolution_description" in data_layer_dict:
            if data_layer_dict.get("temporal_resolution_description") is not None:
                temporal_resolution_description = common.check_str(data_layer_dict.get("temporal_resolution_description"))
        if "spatial_resolution_of_raw_data" in data_layer_dict:
            if data_layer_dict.get("spatial_resolution_of_raw_data") is not None:
                spatial_resolution_of_raw_data = common.check_str(data_layer_dict.get("spatial_resolution_of_raw_data"))
        if "interpolation" in data_layer_dict:
            if data_layer_dict.get("interpolation") is not None:
                interpolation = common.check_str(data_layer_dict.get("interpolation"))
        if "interpolation_upload" in data_layer_dict:
            if data_layer_dict.get("interpolation_upload") is not None:
                interpolation_upload = common.check_str(data_layer_dict.get("interpolation_upload"))
        if "dimensions_description" in data_layer_dict:
            if data_layer_dict.get("dimensions_description") is not None:
                dimensions_description = common.check_str(data_layer_dict.get("dimensions_description"))
        if "permanence" in data_layer_dict:
            if data_layer_dict.get("permanence") is not None:
                permanence = common.check_bool(data_layer_dict.get("permanence"))
        if "permanence_description" in data_layer_dict:
            if data_layer_dict.get("permanence_description") is not None:
                permanence_description = common.check_str(data_layer_dict.get("permanence_description"))
        if "known_issues" in data_layer_dict:
            if data_layer_dict.get("known_issues") is not None:
                known_issues = common.check_str(data_layer_dict.get("known_issues"))
        if "properties" in data_layer_dict:
            if data_layer_dict.get("properties") is not None:
                properties = Properties.from_dict(data_layer_dict.get("properties"))
        if "spatial_coverage" in data_layer_dict:
            if data_layer_dict.get("spatial_coverage") is not None:
                spatial_coverage = SpatialCoverage.from_dict(data_layer_dict.get("spatial_coverage"))
        if "latitude_min" in data_layer_dict:
            if data_layer_dict.get("latitude_min") is not None:
                latitude_min = common.check_float(data_layer_dict.get("latitude_min")) 
        if "longitude_min" in data_layer_dict:
            if data_layer_dict.get("longitude_min") is not None:
                longitude_min = common.check_float(data_layer_dict.get("longitude_min")) 
        if "latitude_max" in data_layer_dict:
            if data_layer_dict.get("latitude_max") is not None:
                latitude_max = common.check_float(data_layer_dict.get("latitude_max")) 
        if "longitude_max" in data_layer_dict:
            if data_layer_dict.get("longitude_max") is not None:
                longitude_max = common.check_float(data_layer_dict.get("longitude_max")) 
        if "temporal_min" in data_layer_dict:
            if data_layer_dict.get("temporal_min") is not None:
                temporal_min = common.check_str(data_layer_dict.get("temporal_min")) 
        if "temporal_max" in data_layer_dict:
            if data_layer_dict.get("temporal_max") is not None:
                temporal_max = common.check_str(data_layer_dict.get("temporal_max"))
        if "measurement_interval" in data_layer_dict:
            if data_layer_dict.get("measurement_interval") is not None:
                measurement_interval = common.check_str(data_layer_dict.get("measurement_interval"))
        if "measurement_interval_description" in data_layer_dict:
            if data_layer_dict.get("measurement_interval_description") is not None:
                measurement_interval_description = common.check_str(data_layer_dict.get("measurement_interval_description"))
        if "meaning_of_timestamp" in data_layer_dict:
            if data_layer_dict.get("meaning_of_timestamp") is not None:
                meaning_of_timestamp = common.check_str(data_layer_dict.get("meaning_of_timestamp"))
        if "meaning_of_spatial_descriptor" in data_layer_dict:
            if data_layer_dict.get("meaning_of_spatial_descriptor") is not None:
                meaning_of_spatial_descriptor = common.check_str(data_layer_dict.get("meaning_of_spatial_descriptor"))
        if "id" in data_layer_dict:
            if data_layer_dict.get("id") is not None:
                id = common.check_str(data_layer_dict.get("id"))
        if "dataset" in data_layer_dict:
            if data_layer_dict.get("dataset") is not None:
                dataset = DataSet.from_dict(data_layer_dict.get("dataset"))
        if "created_at" in data_layer_dict:
            if data_layer_dict.get("created_at") is not None:
                created_at = common.check_str(data_layer_dict.get("created_at"))
        if "updated_at" in data_layer_dict:
            if data_layer_dict.get("updated_at") is not None:
                updated_at = common.check_str(data_layer_dict.get("updated_at"))
        if "type" in data_layer_dict:
            if data_layer_dict.get("type") is not None:
                type = common.check_str(data_layer_dict.get("type"))
        if "unit" in data_layer_dict:
            if data_layer_dict.get("unit") is not None:
                unit = common.check_str(data_layer_dict.get("unit"))
        if "dataset_id" in data_layer_dict:
            if data_layer_dict.get("dataset_id") is not None:
                dataset_id = common.check_str(data_layer_dict.get("dataset_id"))
        if "min_value" in data_layer_dict:
            if data_layer_dict.get("min_value") is not None:
                min_value = common.check_float(data_layer_dict.get("min_value"))
        if "max_value" in data_layer_dict:
            if data_layer_dict.get("max_value") is not None:
                max_value = common.check_float(data_layer_dict.get("max_value"))
        if "units" in data_layer_dict:
            if data_layer_dict.get("units") is not None:
                units = common.check_str(data_layer_dict.get("units"))
        if "datatype" in data_layer_dict:
            if data_layer_dict.get("datatype") is not None:
                datatype = common.check_str(data_layer_dict.get("datatype"))
        if "level" in data_layer_dict:
            if data_layer_dict.get("level") is not None:
                level = common.check_int(data_layer_dict.get("level"))
        if "crs" in data_layer_dict:
            if (data_layer_dict.get("crs") is not None):
                crs = common.check_str(data_layer_dict.get("crs"))
        if "colorTable" in data_layer_dict:
            if data_layer_dict.get("colorTable") is not None:
                color_table = ColorTable.from_dict(data_layer_dict.get("colorTable"))
        elif "color_table" in data_layer_dict:
            if data_layer_dict.get("color_table") is not None:
                color_table = ColorTable.from_dict(data_layer_dict.get("color_table"))
        if "description_internal" in data_layer_dict:
            if data_layer_dict.get("description_internal") is not None:
                description_internal = common.check_str(data_layer_dict.get("description_internal"))
        if "description_internal_links" in data_layer_dict:
            if data_layer_dict.get("description_internal_links") is not None:
                description_internal_links = common.from_list(data_layer_dict.get("description_internal_links"), common.check_str)
        if "formula" in data_layer_dict:
            if data_layer_dict.get("formula") is not None:
                formula = common.check_str(data_layer_dict.get("formula"))
        if "data_layer_response" in data_layer_dict:
            if data_layer_dict.get("data_layer_response") is not None:
                data_layer_response = DataLayerReturn.from_dict(data_layer_dict.get("data_layer_response"))
        return DataLayer(name                             = name,
                         description                      = description,
                         name_alternate                   = name_alternate,
                         rating                           = rating,
                         description_short                = description_short,
                         description_long                 = description_long,
                         description_links                = description_links,
                         data_source_name                 = data_source_name,
                         data_source_attribution          = data_source_attribution,
                         data_source_description          = data_source_description,
                         data_source_links                = data_source_links,
                         update_interval_max              = update_interval_max,
                         update_interval_description      = update_interval_description,
                         lag_horizon                      = lag_horizon,
                         lag_horizon_description          = lag_horizon_description,
                         temporal_resolution              = temporal_resolution,
                         temporal_resolution_description  = temporal_resolution_description,
                         spatial_resolution_of_raw_data   = spatial_resolution_of_raw_data,
                         interpolation                    = interpolation,
                         interpolation_upload             = interpolation_upload,
                         dimensions_description           = dimensions_description,
                         permanence                       = permanence,
                         permanence_description           = permanence_description,
                         known_issues                     = known_issues,
                         properties                       = properties,
                         spatial_coverage                 = spatial_coverage,
                         latitude_min                     = latitude_min,
                         longitude_min                    = longitude_min,
                         latitude_max                     = latitude_max,
                         longitude_max                    = longitude_max,
                         temporal_min                     = temporal_min,
                         temporal_max                     = temporal_max,
                         measurement_interval             = measurement_interval,
                         measurement_interval_description = measurement_interval_description,
                         meaning_of_timestamp             = meaning_of_timestamp,
                         meaning_of_spatial_descriptor    = meaning_of_spatial_descriptor,
                         id                               = id,
                         dataset                          = dataset,
                         created_at                       = created_at,
                         updated_at                       = updated_at, 
                         type                             = type,
                         unit                             = unit,
                         dataset_id                       = dataset_id, 
                         min_value                        = min_value,
                         max_value                        = max_value,
                         units                            = units,
                         datatype                         = datatype,
                         level                            = level,
                         crs                              = crs,
                         color_table                      = color_table,
                         description_internal             = description_internal,
                         description_internal_links       = description_internal_links,
                         formula                          = formula,
                         data_layer_response              = data_layer_response
                        )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_layer_dict: dict = {}
        if self._name is not None:
            data_layer_dict["name"] = self._name
        if self._description is not None:
            data_layer_dict["description"] = self._description
        if self._name_alternate is not None:
            data_layer_dict["name_alternate"] = self._name_alternate
        if self._rating is not None:
            data_layer_dict["rating"] = self._rating
        if self._description_short is not None:
            data_layer_dict["description_short"] = self._description_short
        if self._description_long is not None:
            data_layer_dict["description_long"] = self._description_long
        if self._description_links is not None:
            data_layer_dict["description_links"] = common.from_list(self._description_links, common.check_str)
        if self._data_source_name is not None:
            data_layer_dict["data_source_name"] = self._data_source_name
        if self._data_source_attribution is not None:
            data_layer_dict["data_source_attribution"] = self._data_source_attribution
        if self._data_source_description is not None:
            data_layer_dict["data_source_description"] = self._data_source_description
        if self._data_source_links is not None:
            data_layer_dict["data_source_links"] = common.from_list(self._data_source_links, common.check_str)
        if self._update_interval_max is not None:
            data_layer_dict["update_interval_max"] = self._update_interval_max
        if self._update_interval_description is not None:
            data_layer_dict["update_interval_description"] = self._update_interval_description
        if self._lag_horizon is not None:
            data_layer_dict["lag_horizon"] = self._lag_horizon
        if self._lag_horizon_description is not None:
            data_layer_dict["lag_horizon_description"] = self._lag_horizon_description
        if self._temporal_resolution is not None:
            data_layer_dict["temporal_resolution"] = self._temporal_resolution
        if self._temporal_resolution_description is not None:
            data_layer_dict["temporal_resolution_description"] = self._temporal_resolution_description
        if self._spatial_resolution_of_raw_data is not None:
            data_layer_dict["spatial_resolution_of_raw_data"] = self._spatial_resolution_of_raw_data
        if self._interpolation is not None:
            data_layer_dict["interpolation"] = self._interpolation
        if self._interpolation_upload is not None:
            data_layer_dict["interpolation_upload"] = self._interpolation_upload    
        if self._dimensions_description is not None:
            data_layer_dict["dimensions_description"] = self._dimensions_description
        if self._permanence is not None:
            data_layer_dict["permanence"] = self._permanence
        if self._permanence_description is not None:
            data_layer_dict["permanence_description"] = self._permanence_description
        if self._known_issues is not None:
            data_layer_dict["known_issues"] = self._known_issues
        if self._properties is not None:
            data_layer_dict["properties"] = common.class_to_dict(self._properties, Properties)
        if self._spatial_coverage is not None:
            data_layer_dict["spatial_coverage"] = common.class_to_dict(self._spatial_coverage, SpatialCoverage)
        if self._latitude_min is not None:
            data_layer_dict["latitude_min"] = self._latitude_min
        if self._longitude_min is not None:
            data_layer_dict["longitude_min"] = self._longitude_min
        if self._latitude_max is not None:
            data_layer_dict["latitude_max"] = self._latitude_max
        if self._longitude_max is not None:
            data_layer_dict["longitude_max"] = self._longitude_max
        if self._temporal_min is not None:
            data_layer_dict["temporal_min"] = self._temporal_min
        if self._temporal_max is not None:
            data_layer_dict["temporal_max"] = self._temporal_max
        if self._measurement_interval is not None:
            data_layer_dict["measurement_interval"] = self._measurement_interval
        if self._measurement_interval_description is not None:
            data_layer_dict["measurement_interval_description"] = self._measurement_interval_description
        if self._meaning_of_timestamp is not None:
            data_layer_dict["meaning_of_timestamp"] = self._meaning_of_timestamp
        if self._meaning_of_spatial_descriptor is not None:
            data_layer_dict["meaning_of_spatial_descriptor"] = self._meaning_of_spatial_descriptor
        if self._id is not None:
            data_layer_dict["id"] = self._id
        if self._dataset is not None:
            data_layer_dict["dataset"] = common.class_to_dict(self._dataset, DataSet) 
        if self._created_at is not None:
            data_layer_dict["created_at"] = self._created_at
        if self._updated_at is not None:
            data_layer_dict["updated_at"] = self._updated_at
        if self._type is not None:
            data_layer_dict["type"] = self._type
        if self._unit is not None:
            data_layer_dict["unit"] = self._unit
        if self._dataset_id is not None:
            data_layer_dict["dataset_id"] = self._dataset_id               
        if self._min_value is not None:
            data_layer_dict["min_value"] = self._min_value
        if self._max_value is not None:
            data_layer_dict["max_value"] = self._max_value
        if self._units is not None:
            data_layer_dict["units"] = self._units
        if self._datatype is not None:
            data_layer_dict["datatype"] = self._datatype
        if self._level is not None:
            data_layer_dict["level"] = self._level
        if self._crs is not None:
            data_layer_dict["crs"] = self._crs
        if self._color_table is not None:
            data_layer_dict["color_table"] = common.class_to_dict(self._color_table, ColorTable) 
        if self._description_internal is not None:
            data_layer_dict["description_internal"] = self._description_internal
        if self._description_internal_links is not None:
            data_layer_dict["description_internal_links"] = common.from_list(self._description_internal_links, common.check_str)
        if self._formula is not None:
            data_layer_dict["formula"] = self._formula   
        if self._data_layer_response is not None:
            data_layer_dict["data_layer_response"] = common.class_to_dict(self._data_layer_response, DataLayerReturn)

        return data_layer_dict
              
    #
    def to_dict_data_layer_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation.
                    
        :rtype: dict
        """
        
        data_layer_dict: dict = {}
        if self._name is not None:
          data_layer_dict["name"] = self._name
        if self._description is not None:
          data_layer_dict["description"] = self._description
        if self._name_alternate is not None:
          data_layer_dict["name_alternate"] = self._name_alternate
        if self._rating is not None:
          data_layer_dict["rating"] = self._rating
        if self._description_short is not None:
          data_layer_dict["description_short"] = self._description_short
        if self._description_long is not None:
          data_layer_dict["description_long"] = self._description_long
        if self._description_links is not None:
          data_layer_dict["description_links"] = common.from_list(self._description_links, common.check_str)
        if self._data_source_name is not None:
          data_layer_dict["data_source_name"] = self._data_source_name
        if self._data_source_attribution is not None:
          data_layer_dict["data_source_attribution"] = self._data_source_attribution
        if self._data_source_description is not None:
          data_layer_dict["data_source_description"] = self._data_source_description
        if self._data_source_links is not None:
          data_layer_dict["data_source_links"] = common.from_list(self._data_source_links, common.check_str)
        if self._update_interval_max is not None:
          data_layer_dict["update_interval_max"] = self._update_interval_max
        if self._update_interval_description is not None:
          data_layer_dict["update_interval_description"] = self._update_interval_description
        if self._lag_horizon is not None:
          data_layer_dict["lag_horizon"] = self._lag_horizon
        if self._lag_horizon_description is not None:
          data_layer_dict["lag_horizon_description"] = self._lag_horizon_description
        if self._temporal_resolution is not None:
          data_layer_dict["temporal_resolution"] = self._temporal_resolution
        if self._temporal_resolution_description is not None:
          data_layer_dict["temporal_resolution_description"] = self._temporal_resolution_description
        if self._spatial_resolution_of_raw_data is not None:
          data_layer_dict["spatial_resolution_of_raw_data"] = self._spatial_resolution_of_raw_data
        if self._interpolation is not None:
          data_layer_dict["interpolation"] = self._interpolation
        if self._interpolation_upload is not None:
          data_layer_dict["interpolation_upload"] = self._interpolation_upload    
        if self._dimensions_description is not None:
          data_layer_dict["dimensions_description"] = self._dimensions_description
        if self._permanence is not None:
          data_layer_dict["permanence"] = self._permanence
        if self._permanence_description is not None:
          data_layer_dict["permanence_description"] = self._permanence_description
        if self._known_issues is not None:
          data_layer_dict["known_issues"] = self._known_issues
        if self._properties is not None:
          data_layer_dict["properties"] = common.class_to_dict(self._properties, Properties)
        if self._spatial_coverage is not None:
          data_layer_dict["spatial_coverage"] = common.class_to_dict(self._spatial_coverage, SpatialCoverage)
        if self._latitude_min is not None:
          data_layer_dict["latitude_min"] = self._latitude_min
        if self._longitude_min is not None:
          data_layer_dict["longitude_min"] = self._longitude_min
        if self._latitude_max is not None:
          data_layer_dict["latitude_max"] = self._latitude_max
        if self._longitude_max is not None:
          data_layer_dict["longitude_max"] = self._longitude_max
        if self._temporal_min is not None:
          data_layer_dict["temporal_min"] = self._temporal_min
        if self._temporal_max is not None:
          data_layer_dict["temporal_max"] = self._temporal_max
        if self._measurement_interval is not None:
          data_layer_dict["measurement_interval"] = self._measurement_interval
        if self._measurement_interval_description is not None:
          data_layer_dict["measurement_interval_description"] = self._measurement_interval_description
        if self._meaning_of_timestamp is not None:
          data_layer_dict["meaning_of_timestamp"] = self._meaning_of_timestamp
        if self._meaning_of_spatial_descriptor is not None:
          data_layer_dict["meaning_of_spatial_descriptor"] = self._meaning_of_spatial_descriptor   
        if self._units is not None:
          data_layer_dict["units"] = self._units
        if self._datatype is not None:
          data_layer_dict["datatype"] = self._datatype
        if self._level is not None:
          data_layer_dict["level"] = self._level
        if self._crs is not None:
          data_layer_dict["crs"] = self._crs
        if self._color_table is not None:
          data_layer_dict["colorTable"] = common.class_to_dict(self._color_table, ColorTable) 
        if self._description_internal is not None:
          data_layer_dict["description_internal"] = self._description_internal
        if self._description_internal_links is not None:
          data_layer_dict["description_internal_links"] = common.from_list(self._description_internal_links, common.check_str)
        if self._formula is not None:
          data_layer_dict["formula"] = self._formula   

        return data_layer_dict
        
    #
    def to_dict_data_layer_put(self):

        """
        Create a dictionary from the objects structure ready for a PUT operation. 
                   
        :rtype: dict
        """
        
        data_layer_dict: dict = {}
        if self._name is not None:
          data_layer_dict["name"] = self._name
        if self._description is not None:
          data_layer_dict["description"] = self._description
        if self._name_alternate is not None:
          data_layer_dict["name_alternate"] = self._name_alternate
        if self._rating is not None:
          data_layer_dict["rating"] = self._rating
        if self._description_short is not None:
          data_layer_dict["description_short"] = self._description_short
        if self._description_long is not None:
          data_layer_dict["description_long"] = self._description_long
        if self._description_links is not None:
          data_layer_dict["description_links"] = common.from_list(self._description_links, common.check_str)
        if self._data_source_name is not None:
          data_layer_dict["data_source_name"] = self._data_source_name
        if self._data_source_attribution is not None:
          data_layer_dict["data_source_attribution"] = self._data_source_attribution
        if self._data_source_description is not None:
          data_layer_dict["data_source_description"] = self._data_source_description
        if self._data_source_links is not None:
          data_layer_dict["data_source_links"] = common.from_list(self._data_source_links, common.check_str)
        if self._update_interval_max is not None:
          data_layer_dict["update_interval_max"] = self._update_interval_max
        if self._update_interval_description is not None:
          data_layer_dict["update_interval_description"] = self._update_interval_description
        if self._lag_horizon is not None:
          data_layer_dict["lag_horizon"] = self._lag_horizon
        if self._lag_horizon_description is not None:
          data_layer_dict["lag_horizon_description"] = self._lag_horizon_description
        if self._temporal_resolution is not None:
          data_layer_dict["temporal_resolution"] = self._temporal_resolution
        if self._temporal_resolution_description is not None:
          data_layer_dict["temporal_resolution_description"] = self._temporal_resolution_description
        if self._spatial_resolution_of_raw_data is not None:
          data_layer_dict["spatial_resolution_of_raw_data"] = self._spatial_resolution_of_raw_data
        if self._interpolation is not None:
          data_layer_dict["interpolation"] = self._interpolation
        if self._interpolation_upload is not None:
          data_layer_dict["interpolation_upload"] = self._interpolation_upload    
        if self._dimensions_description is not None:
          data_layer_dict["dimensions_description"] = self._dimensions_description
        if self._permanence is not None:
          data_layer_dict["permanence"] = self._permanence
        if self._permanence_description is not None:
          data_layer_dict["permanence_description"] = self._permanence_description
        if self._known_issues is not None:
          data_layer_dict["known_issues"] = self._known_issues
        if self._properties is not None:
          data_layer_dict["properties"] = common.class_to_dict(self._properties, Properties)
        if self._spatial_coverage is not None:
          data_layer_dict["spatial_coverage"] = common.class_to_dict(self._spatial_coverage, SpatialCoverage)
        if self._latitude_min is not None:
          data_layer_dict["latitude_min"] = self._latitude_min
        if self._longitude_min is not None:
          data_layer_dict["longitude_min"] = self._longitude_min
        if self._latitude_max is not None:
          data_layer_dict["latitude_max"] = self._latitude_max
        if self._longitude_max is not None:
          data_layer_dict["longitude_max"] = self._longitude_max
        if self._temporal_min is not None:
          data_layer_dict["temporal_min"] = self._temporal_min
        if self._temporal_max is not None:
          data_layer_dict["temporal_max"] = self._temporal_max
        if self._measurement_interval is not None:
          data_layer_dict["measurement_interval"] = self._measurement_interval
        if self._measurement_interval_description is not None:
          data_layer_dict["measurement_interval_description"] = self._measurement_interval_description
        if self._meaning_of_timestamp is not None:
          data_layer_dict["meaning_of_timestamp"] = self._meaning_of_timestamp
        if self._meaning_of_spatial_descriptor is not None:
          data_layer_dict["meaning_of_spatial_descriptor"] = self._meaning_of_spatial_descriptor   
        if self._min_value is not None:
          data_layer_dict["min_value"] = self._min_value
        if self._max_value is not None:
          data_layer_dict["max_value"] = self._max_value
        if self._description_internal is not None:
          data_layer_dict["description_internal"] = self._description_internal
        if self._description_internal_links is not None:
          data_layer_dict["description_internal_links"] = common.from_list(self._description_internal_links, common.check_str)
        if self._formula is not None:
          data_layer_dict["formula"] = self._formula   

        return data_layer_dict

    #
    def from_json(data_layer_json: Any):

        """
        Create a DataLayer object from json (dictonary or str).
        
        :param data_layer_dict: A json dictionary that contains the keys of a DataLayer or a string representation of a json dictionary.
        :type data_layer_dict:  Any             
        :rtype:                 ibmpairs.catalog.DataLayer
        :raises Exception:      If not a dictionary or a string.
        """
        
        if isinstance(data_layer_json, dict):
            data_layer = DataLayer.from_dict(data_layer_json)
        elif isinstance(data_layer_json, str):
            data_layer_dict = json.loads(data_layer_json)
            data_layer = DataLayer.from_dict(data_layer_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layer_json), "data_layer_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layer

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
    #
    def to_json_data_layer_post(self):

        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation.   
                 
        :rtype: string
        """

        return json.dumps(self.to_dict_data_layer_post())

    #
    def to_json_data_layer_put(self):

        """
        Create a string representation of a json dictionary from the objects structure ready for a PUT operation.    
                
        :rtype: string
        """

        return json.dumps(self.to_dict_data_layer_put())
        
    #
    def display(self,
                columns: List[str] = ['dataset_id', 'id', 'name', 'description_short', 'description_long', 'level', 'type', 'unit']
               ):
                
        """
        A method to return a pandas.DataFrame object of a get result.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['dataset_id', 'id', 'name', 'description_short', 'description_long', 'level', 'type', 'unit']
        :type columns:  List[str]
        :returns:       A pandas.DataFrame of attributes from the object.
        :rtype:         pandas.DataFrame
        """

        display_dict = self.to_dict()
      
        display_df = pd.DataFrame([display_dict], columns=columns)
        if 'type' in columns:
            display_df["type"] = display_df["type"].map(lambda x: "Raster" if "R" in str(x) else "Vector" if "V" in str(x) else str(x))
      
        return display_df
        
    #
    def get(self,
            id                = None,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a Data Layer.
        
        :param id:         The Data Layer ID of the Data Layer to be gathered.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A populated DataLayer object.
        :rtype:            ibmpairs.catalog.DataLayer
        :raises Exception: A ibmpairs.client.Client is not found,
                           an ID is not provided or already held in the object,
                           a server error occurred,
                           the status of the request is not 200.
        """
        
        if id is not None:
            self._id = common.check_str(id)
        
        if self._id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_ID
            logger.error(msg)
            raise common.PAWException(msg)
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        try:
           response = cli.get(url = cli.get_host() +
                                    constants.CATALOG_DATA_LAYERS_API + 
                                    common.check_str(self._id),
                              verify = verify
                             )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._id), e)
            logger.error(msg)
            raise common.PAWException(msg)
        
        if response.status_code != 200:
            error_message = 'failed'

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._id), response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)    
        else:
            data_layer_get = DataLayer.from_dict(response.json())

            return data_layer_get
      
    #
    def create(self,
               data_set_id: str,
               data_layer_type: str,
               data_layer_group: str  = None,
               client: cl.Client      = None,
               verify: bool           = constants.GLOBAL_SSL_VERIFY
              ):
        
        """
        A method to create a Data Layer.
        
        :param data_set_id:      The Data Set ID of the Data Layer should be created for.
        :type data_set_id:       str
        :param data_layer_type:  The Data Layer type to be created, (e.g. 2draster).
        :type data_layer_type:   str
        :param data_layer_group: In the case of vector data, the P group number the Data Layer
                                 should be created within.
        :type data_layer_group:  str
        :param client:           An IBM PAIRS Client.
        :type client:            ibmpairs.client.Client
        :param verify:           SSL verification
        :type verify:            bool
        :raises Exception:       A ibmpairs.client.Client is not found,
                                 a Data Set ID is not provided, 
                                 a Data Layer type is not provided, 
                                 a Data Layer group is not provided and the type is a Vector, 
                                 a server error occurred, 
                                 the status of the request is not 200.
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
    
        dls = DataLayers(data_set_id = common.check_str(data_set_id), 
                         group = data_layer_group,
                         layer_type = common.check_str(data_layer_type),
                         data_layers = [self],
                         client = cli
                        )
        dls.create()
        
        return dls

    #
    def update(self,
               id                = None,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):
        
        """
        A method to update a Data Layer.
        
        :param id:         The Data Layer ID of the Data Layer to be updated.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :raises Exception: A ibmpairs.client.Client is not found, 
                           an ID is not provided or already held in the object, 
                           a server error occurred, 
                           the status of the request is not 200.
        """

        if id is not None:
            self._id = common.check_str(id)

        if self._id is None:
            msg = messages.ERROR_CATALOG_DATA_LAYER_ID
            logger.error(msg)
            raise common.PAWException(msg)

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
            
        data_layer_update_json = self.to_json_data_layer_put()

        try:
            response = cli.put(url     = cli.get_host() + 
                                         constants.CATALOG_DATA_LAYERS_API + 
                                         common.check_str(self._id),
                               headers = constants.CLIENT_PUT_AND_POST_HEADER,
                               body    = data_layer_update_json,
                               verify  = verify
                              )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('PUT', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._id), e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status_code != 200:
            error_message = 'failed'
            
            if response.json() is not None:
                try:
                    self._data_layer_response = data_layer_return_from_dict(response.json())
                    error_message = self._data_layer_response.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('PUT', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(self._id), response.status_code, error_message)
            
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            self._data_layer_response = data_layer_return_from_dict(response.json())
          
            msg = messages.INFO_CATALOG_DATA_LAYER_UPDATE_SUCCESS.format(self._data_layer_response.data_layer_ids)
            logger.info(msg)

    # To ensure a user wishes to delete, the data layer id must be specified- this will not be pulled from the object.
    def delete(self,
               id                = None,
               hard_delete       = False,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to delete a Data Layer.
        
        :param id:          The Data Layer ID of the Data Layer to be deleted.
        :type id:           str
        :param hard_delete: Whether the Data Layer should be 'hard deleted', NOTE: this also deletes all data held by associated Data Layer. This step is necessary where the intention is to delete and recreate a Data Layer with the same name.
        :type hard_delete:  bool
        :param client:      An IBM PAIRS Client.
        :type client:       ibmpairs.client.Client
        :param verify:      SSL verification
        :type verify:       bool
        :raises Exception:  A ibmpairs.client.Client is not found, 
                            an ID is not provided or already held in the object, 
                            a server error occurred, 
                            t he status of the request is not 200.
        """
         
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
            
        if hard_delete is True:
            url = cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(id) + "?hard_delete=true&force=true"
        else:
            url = cli.get_host() + constants.CATALOG_DATA_LAYERS_API + common.check_str(id)
        
        try:
            response = cli.delete(url    = url,
                                  verify = verify)
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('DELETE', 'request', url, e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status_code != 200:
            error_message = 'failed'
          
            if response.json is not None:
                try:
                    self._data_layer_response = data_layer_return_from_dict(response.json())
                    error_message = self._data_layer_response.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('DELETE', 'request', url, response.status_code, error_message)
          
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            self._data_layer_response = data_layer_return_from_dict(response.json())

            msg = messages.INFO_CATALOG_DATA_LAYER_DELETE_SUCCESS.format(self._data_layer_response.id)
            logger.info(msg)
    
    #
    def vector_layer_definition_from_file(self,
                                          csv_file,
                                          data_layer_type         = None,
                                          data_layer_group        = None,
                                          number_of_layer_columns = None
                                         ):
        
        if os.path.isfile(os.path.join(os.getcwd(), csv_file)):
            csv_file = os.path.join(os.getcwd(), csv_file)
        elif os.path.isfile(csv_file):
            csv_file = csv_file
        else:
            msg = messages.ERROR_CATALOG_VECTOR_DATA_LAYER_FROM_FILE_NOT_FOUND.format(csv_file)
            logger.error(msg)
            raise common.PAWException(msg)
        
        layer_type = data_layer_type
        
        type_map = {
            'integer' : 'in',
            'number': 'fl',
            'string' : 'st'
        }
        res = []
        m = pd.read_csv(csv_file)
        res.append(m.columns.tolist())
        for i in m.values.tolist():
            res.append(i)

        table = Table(res)
        table.infer()
        schema = table.schema
        if layer_type.lower() not in ['vectorpoint', 'vectorpolygon']:
            msg = messages.ERROR_CATALOG_VECTOR_DATA_LAYER_FROM_FILE_LAYER_TYPE.format(layer_type.lower())
            logger.error(msg)
            raise common.PAWException(msg)
        if (schema.descriptor['fields'][0]['type']!='integer'):
            msg = messages.ERROR_CATALOG_VECTOR_DATA_LAYER_FROM_FILE_INCORRECT_TYPE.format('first','integer','contain the timestamp epoch')
            logger.error(msg)
            raise common.PAWException(msg)
        if (layer_type.lower() in ['vectorpolygon'] and schema.descriptor.fields[1].type != 'integer'):
            msg = messages.ERROR_CATALOG_VECTOR_DATA_LAYER_FROM_FILE_INCORRECT_TYPE.format('second','integer','contain the ID of a polygon')
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            if (schema.descriptor['fields'][1]['type']!='number' and schema.descriptor['fields'][2]['type']!='number'):
                msg = messages.ERROR_CATALOG_VECTOR_DATA_LAYER_FROM_FILE_INCORRECT_TYPE.format('second and third','number','contain the latitude and longitude values')
                logger.error(msg)
                raise common.PAWException(msg)

        layer_list = []
        for field in schema.descriptor['fields'][3:(3+number_of_layer_columns)]:
            layer_list.append({"name": field['name'],"datatype":type_map[field['type']], "units":"N/A"}),
        
        payload = {"layerType": layer_type,
                   "group": data_layer_group,
                   "layers": layer_list
                  }
        
        layers = data_layers_from_dict(payload)
        
        return layers

    def raster_layer_definition_from_file(self, 
                                          data_layer_name,
                                          filename
                                         ):
        if HAS_RASTERIO:
            with rasterio.open(filename) as src:
                level = -1
                datatype = 'xx'
                epsg_number = common.check_str(src.crs.to_epsg())
                # print (src.crs.to_epsg())
                # print (src.dtypes[0])
                if (src.dtypes[0] == 'uint8'):
                    datatype = 'bt'
                if (src.dtypes[0] == 'uint16'):
                    #            arr = src.read(1)
                    #            print("min:", arr.min())
                    #            print("max:", arr.max())
                    #            if (arr.max() - arr.min() < 256 )
                    print(
                        "Depending on the range of data in your dataset, you might be able to convert the tif to a byte datatype to save space and increase query speed?")
                    datatype = 'in'
                if (src.dtypes[0]== 'float16' or src.dtypes[0] == 'float32') :
                    datatype = 'fl'
                resolution = src.res[0]
                # print (resolution)
                x = re.findall("(?<=UNIT\[\").*?\"", src.crs.wkt)
                if "metre\"" in x:
                    for idx, d in enumerate(constants.RASTER_METRE_STEPS):
                        if d < resolution:
                            break
                else:
                    for idx, d in enumerate(constants.RASTER_DEGREE_STEPS):
                        if d < resolution:
                            break
                level = common.check_str(idx + 1)
        
            definition = {
                "layerType": "Raster",
                "layers": [
                    {
                        "name": data_layer_name,
                        "colorTable": {
                            "id": "58"
                        },
                        "crs": "EPSG:" + epsg_number,
                        "level": level,
                        "datatype": datatype
                    }
                ]
            }
        
            layers = data_layers_from_dict(definition)

            return layers
        else:
            msg = messages.ERROR_NO_RASTERIO
            logger.error(msg)
            raise common.PAWException(msg)

#
class DataLayers:
    # 
    #_client: cl.Client
    
    # Common
    #_data_set_id: str
    #_group: str
    #_group_id: str
    #_layer_type: str
    #_data_layers: List[DataLayer]
    
    # 
    #_data_layer_response: DataLayerReturn
    
    """
    An object to represent a list of IBM PAIRS Data Layers.
    
    :param client:              An IBM PAIRS Client.
    :type client:               ibmpairs.client.Client
    :param data_set_id:         The Data Set ID for the Data Layers.
    :type data_set_id:          str
    :param group:               The group name of the Data Layers.
    :type group:                str
    :param group_id:            The group ID of the Data Layers.
    :type group_id:             str
    :param layer_type:          The layer type (e.g. 2draster).
    :type layer_type:           str
    :param data_layers:         A list of Data Layers.
    :type data_layers:          List[DataLayer]
    :param data_layer_response: A server response to a executed Data Layer method call.
    :type data_layer_response:  ibmpairs.catalog.DataLayerReturn
    :raises Exception:          An ibmpairs.client.Client is not found.
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
    def __getitem__(self, data_layer_name):
      
        """
        A method to overload the default behaviour of the slice on this object to be an
        element from the data_layers attribute.
        
        :param data_layer_name: The name of a Data Layer to search for, if this is numeric, the method simply returns the default (list order).
        :type data_layer_name:  str
        :raises Exception:      If less than one value is found, 
                                if more than one value is found.
        """
      
        if isinstance(data_layer_name, int):
            return self._data_layers[data_layer_name]
        elif isinstance(data_layer_name, str):
            index_list = []
            index      = 0
            foundCount = 0

            for data_layer in self._data_layers:
                if data_layer.name is not None:
                    if (data_layer.name == data_layer_name):
                        foundCount = foundCount + 1
                        index_list.append(index)
                else:
                    msg = messages.WARN_CATALOG_DATA_LAYERS_DATA_SET_OBJECT_NO_NAME.format(data_layer_name)
                    logger.warning(msg)
                  
                index = index + 1

            if foundCount == 0:
                msg = messages.ERROR_CATALOG_DATA_LAYERS_NO_DATA_SET.format(data_layer_name)
                logger.error(msg)
                raise common.PAWException(msg)
            elif foundCount == 1:
                return self._data_layers[index_list[0]]
            else:
                msg = messages.ERROR_CATALOG_DATA_LAYERS_MULTIPLE_IDENTICAL_NAMES.format(data_layer_name)
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            msg = messages.ERROR_CATALOG_DATA_SETS_TYPE_UNKNOWN.format(type(data_layer_name))
            logger.error(msg)
            raise common.PAWException(msg)

    #
    def __init__(self,
                 client: cl.Client                    = None,
                 data_set_id: str                     = None,
                 group: str                           = None,
                 group_id: str                        = None,
                 layer_type: str                      = None,
                 data_layers: List[DataLayer]         = None,
                 data_layer_response: DataLayerReturn = None,
                ):
        self._client            = common.set_client(input_client  = client,
                                                    global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._data_set_id       = data_set_id
        self._group             = group
        self._group_id          = group_id
        self._layer_type        = layer_type
        self._data_layers       = data_layers
        
        if data_layer_response is None:
            self._data_layer_response = DataLayerReturn()
        else:
            self._data_layer_response = data_layer_response

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
    def get_data_set_id(self):
        return self._data_set_id

    #
    def set_data_set_id(self, data_set_id):
        self._data_set_id = common.check_str(data_set_id)
        
    #    
    def del_data_set_id(self): 
        del self._data_set_id

    #    
    data_set_id = property(get_data_set_id, set_data_set_id, del_data_set_id)
    
    #    
    def get_group(self):
        return self._group

    #
    def set_group(self, group):
        self._group = common.check_str(group)
        
    #    
    def del_group(self): 
        del self._group

    #    
    group = property(get_group, set_group, del_group)
    
    #    
    def get_group_id(self):
      return self._group_id

    #
    def set_group_id(self, group_id):
      self._group_id = common.check_str(group_id)
      
    #    
    def del_group_id(self): 
      del self._group_id

    #    
    group_id = property(get_group_id, set_group_id, del_group_id)
    
    #    
    def get_layer_type(self):
        return self._layer_type

    #
    def set_layer_type(self, layer_type):
        self._layer_type = common.check_str(layer_type)
        
    #    
    def del_layer_type(self): 
        del self._layer_type

    #    
    layer_type = property(get_layer_type, set_layer_type, del_layer_type)
        
    # 
    def get_data_layers(self):
        return self._data_layers

    #
    def set_data_layers(self, data_layers):
        self._data_layers = common.check_class(data_layers, List[DataLayer])

    #    
    def del_data_layers(self): 
        del self._data_layers

    #    
    data_layers = property(get_data_layers, set_data_layers, del_data_layers)
    
    #
    def get_data_layer_response(self):
        return self._data_layer_response

    #
    def set_data_layer_response(self, data_layer_response):
        self._data_layer_response = common.check_class(data_layer_response, DataLayerReturn)

    #    
    def del_data_layer_response(self): 
        del self._data_layer_response

    #    
    data_layer_response = property(get_data_layer_response, set_data_layer_response, del_data_layer_response)
    
    #
    def from_dict(data_layers_input: Any):

        """
        Create a DataLayers object from a dictionary.
        
        :param data_layers_dict: A dictionary that contains the keys of a DataLayers.
        :type data_layers_dict:  Any             
        :rtype:                  ibmpairs.catalog.DataLayers
        :raises Exception:       If not a dictionary.
        """
        
        data_set_id         = None
        group               = None
        group_id            = None
        layer_type          = None
        data_layers         = None
        data_layer_response = None
        
        if isinstance(data_layers_input, dict):
            common.check_dict(data_layers_input)

            if "data_set_id" in data_layers_input:
                if data_layers_input.get("data_set_id") is not None:
                    data_set_id = common.check_str(data_layers_input.get("data_set_id"))
            if "group" in data_layers_input:
                if data_layers_input.get("group") is not None:
                    group = common.check_str(data_layers_input.get("group"))
            if "group_id" in data_layers_input:
                if data_layers_input.get("group_id") is not None:
                    group_id = common.check_str(data_layers_input.get("group_id"))
            if "layerType" in data_layers_input:
                if data_layers_input.get("layerType") is not None:
                    layer_type = common.check_str(data_layers_input.get("layerType"))
            elif "layer_type" in data_layers_input:
                if data_layers_input.get("layer_type") is not None:
                    layer_type = common.check_str(data_layers_input.get("layer_type")) 
            if "data_layers" in data_layers_input:
                if data_layers_input.get("data_layers") is not None:
                    data_layers = common.from_list(data_layers_input.get("data_layers"), DataLayer.from_dict)
            elif "layers" in data_layers_input:
                if data_layers_input.get("layers") is not None:
                    data_layers = common.from_list(data_layers_input.get("layers"), DataLayer.from_dict)
            if "data_layer_response" in data_layers_input:
                if data_layers_input.get("data_layer_response") is not None:
                    data_layer_response = DataLayerReturn.from_dict(data_layers_input.get("data_layer_response"))

        elif isinstance(data_layers_input, list):
            data_layers = common.from_list(data_layers_input, DataLayer.from_dict)
        else:
            msg = messages.ERROR_CATALOG_DATA_LAYERS_UNKNOWN.format(type(data_layers_input))
            logger.error(msg)
            raise common.PAWException(msg)
 
        return DataLayers(data_set_id         = data_set_id,
                          group               = group,
                          group_id            = group_id,
                          layer_type          = layer_type,
                          data_layers         = data_layers,
                          data_layer_response = data_layer_response
                         )
    
    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype: dict
        """
        
        data_layers_dict: dict = {}
        if self._data_set_id is not None:
            data_layers_dict["data_set_id"] = self._data_set_id
        if self._group is not None:
            data_layers_dict["group"] = self._group
        if self._group_id is not None:
            data_layers_dict["group_id"] = self._group_id 
        if self._layer_type is not None:
            data_layers_dict["layer_type"] = self._layer_type
        if self._data_layers is not None:
            data_layers_dict["data_layers"] = common.from_list(self._data_layers, lambda item: common.class_to_dict(item, DataLayer))
        if self._data_layer_response is not None:
            data_layers_dict["data_layer_response"] = common.class_to_dict(self._data_layer_response, DataLayerReturn)
        return data_layers_dict
    
    #
    def to_dict_data_layers_post(self):
 
        """
        Create a dictionary from the objects structure ready for a POST operation.
                    
        :rtype: dict
        """
        
        data_layers_dict: dict = {}
        if self._group is not None:
            data_layers_dict["group"] = self._group
        if self._layer_type is not None:
            data_layers_dict["layerType"] = self._layer_type
        if self._data_layers is not None:
            data_layers_dict["layers"] = common.from_list(self._data_layers, lambda item: item.to_dict_data_layer_post())
        return data_layers_dict
    
    #
    def from_json(data_layers_json: Any):

        """
        Create a DataLayers object from json (dictonary or str).
        
        :param data_layers_dict: A json dictionary that contains the keys of a DataLayers or a string representation of a json dictionary.
        :type data_layers_dict:  Any             
        :rtype:                  ibmpairs.catalog.DataLayers
        :raises Exception:       If not a dictionary or a string.
        """
        
        if isinstance(data_layers_json, dict):
            data_layers = DataLayers.from_dict(data_layers_json)
        elif isinstance(data_layers_json, str):
            data_layers_dict = json.loads(data_layers_json)
            data_layers = DataLayers.from_dict(data_layers_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(data_layers_json), "data_layers_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return data_layers

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
    #
    def to_json_data_layers_post(self):

        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation.        
            
        :rtype: string
        """

        return json.dumps(self.to_dict_data_layers_post())
            
    #
    def filter_data_layers_by_attribute(self,
                                        attribute,
                                        value,
                                        regex = None
                                       ):
        
        """
        A method to filter a list of Data Layers by an attribute.
        
        :param attribute:  An attribute of a Data Layer.
        :type attribute:   str
        :param value:      A value to search for.
        :type value:       str
        :param regex:      A regex string to apply.
        :type regex:       str
        :returns:          A list of DataLayers that fit the criteria.
        :rtype:            List[ibmpairs.catalog.DataLayer]
        :raises Exception: The value is not found in any Data Layer.
        """
        
        filtered_data_layers: List[DataLayer] = []

        for data_layer in self._data_layers:

            value_from_object = getattr(data_layer, attribute) 
            if regex is None:
                value_to_compare = value_from_object       
            else: 
                value_regex = re.search(regex, value_from_object)
                    
                if value_regex:
                    value_to_compare = value_regex.group(0)
                
                    if value_to_compare is not None:
                        if value_to_compare == value:
                            filtered_data_layers.append(data_layer)
        
        if len(filtered_data_layers) <= 0:
            msg = messages.ERROR_CATALOG_DATA_LAYERS_FILTER_DATA_LAYER_BY_ATTRIBUTE.format(attribute, value, common.check_str(regex))
            logger.error(msg)
            raise common.PAWException(msg)
        
        return filtered_data_layers

    def display(self,
                columns: List[str] = ['dataset_id', 'id', 'name', 'description_short', 'description_long', 'level', 'type', 'unit'],
                sort_by: str       = 'id'
               ):
        
        """
        A method to return a pandas.DataFrame object of get results.
        
        :param columns: The columns to be returned in the pandas.DataFrame object, defaults to ['dataset_id', 'id', 'name', 'description_short', 'description_long', 'level', 'type', 'unit']
        :type columns:  List[str]
        :param sort_by: A sort_by column
        :type sort_by:  str
        :returns:       A pandas.DataFrame of attributes from the data_layers object.
        :rtype:         pandas.DataFrame
        """
                
        display_df = None
      
        for data_layer in self._data_layers:
            next_display = data_layer.display(columns)
            if display_df is None:
                display_df = next_display
            else:
                display_df = pd.concat([display_df, next_display])
                
        display_df.reset_index(inplace=True, drop=True)
        display_df.sort_values(by=[sort_by])
            
        return display_df
        
    #
    def get(self,
            data_set_id               = None,
            data_layer_group_id: str  = None,
            data_layer_group: str     = None,
            client: cl.Client         = None,
            verify: bool              = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a list of Data Layers, either all, or with specification of a 
        Data Set ID, those for a Data Set.
        
        :param data_set_id:         The Data Set ID to gather Data Layers for, if unspecified, the method gathers all Data Layers a user has access to.
        :type data_set_id:          int or str
        :param data_layer_group_id: The Data Layer Group ID to filter the results on.
        :type data_layer_group_id:  str
        :param data_layer_group:    The Data Layer Group name to filter the results on.
        :type data_layer_group:     str
        :param client:              An IBM PAIRS Client.
        :type client:               ibmpairs.client.Client
        :param verify:              SSL verification
        :type verify:               bool
        :returns:                   A populated DataLayers object.
        :rtype:                     ibmpairs.catalog.DataLayers
        :raises Exception:          A ibmpairs.client.Client is not found, 
                                    if a Data Set ID is specified but could not be found, 
                                    a server error occurred, 
                                    the status of the request is not 200.
        """
            
        if data_set_id is not None:
            self._data_set_id = common.check_str(data_set_id)
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        if self._data_set_id is not None:
            try:
                response = cli.get(url = cli.get_host() +
                                         constants.CATALOG_DATA_SETS_API + 
                                         common.check_str(self._data_set_id) + 
                                         constants.CATALOG_DATA_SETS_LAYERS_API,
                                   verify = verify
                                  )
            except Exception as e:
                msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(self._data_set_id) + constants.CATALOG_DATA_SETS_LAYERS_API, e)
                logger.error(msg)
                raise common.PAWException(msg)

        else:
            try:
                response = cli.get(url = cli.get_host() +
                                         constants.CATALOG_DATA_LAYERS_API_FULL,
                                   verify = verify
                                  )
            except Exception as e:
                msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API_FULL, e)
                logger.error(msg)
                raise common.PAWException(msg)

        if response.status_code != 200:
            error_message = 'failed'
            
            if self._data_set_id is not None:
                msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(self._data_set_id) + constants.CATALOG_DATA_SETS_LAYERS_API, response.status_code, error_message) 
            else:
                msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + constants.CATALOG_DATA_LAYERS_API_FULL, response.status_code, error_message)
            
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            data_layers_get   = DataLayers.from_dict(response.json())
            self._data_layers = data_layers_get.data_layers

            if data_layer_group_id is not None:
                self._data_layers = data_layers_get.filter_data_layers_by_attribute(attribute = 'id',
                                                                                    value = data_layer_group_id,
                                                                                    regex = "(?<=P)(.*?)(?=C)"
                                                                                   )
            elif (data_layer_group_id is None) and (data_layer_group is not None):
                self._data_layers = data_layers_get.filter_data_layers_by_attribute(attribute = 'name',
                                                                                    value = data_layer_group,
                                                                                    regex = ".+?(?=\.)"
                                                                                   )
            else:
                self._data_layers = data_layers_get.data_layers
        
            return self

    #
    def create(self,
               data_set_id: str       = None,
               data_layer_group: str  = None,
               data_layer_type: str   = None,
               client: cl.Client      = None,
               verify: bool           = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to create a number of Data Layers.
        
        :param data_set_id:      The Data Set ID of the Data Layer should be created for.
        :type data_set_id:       str
        :param data_layer_type:  The Data Layer type to be created, (e.g. 2draster).
        :type data_layer_type:   str
        :param data_layer_group: In the case of vector data, the P group number the Data Layer
                                 should be created within.
        :type data_layer_group:  str
        :param client:           An IBM PAIRS Client.
        :type client:            ibmpairs.client.Client
        :param verify:           SSL verification
        :type verify:            bool
        :raises Exception:       A ibmpairs.client.Client is not found, 
                                 a Data Set ID is not provided or set in the object, 
                                 a Data Layer type is not providedor set in the object, 
                                 a Data Layer group is not provided (or set in the object) and the type is a Vector, 
                                 a server error occurred, 
                                 the status of the request is not 200.
        """
                
        if data_set_id is not None:
            self._data_set_id = common.check_str(data_set_id)
        else:
            if self._data_set_id is None:
                msg = messages.ERROR_CATALOG_DATA_LAYERS_SET_ID
                logger.error(msg)
                raise common.PAWException(msg)
            
        if data_layer_type is not None:
            self._layer_type = data_layer_type
        else:
            if self._layer_type is None:
                msg = messages.ERROR_CATALOG_DATA_LAYERS_SET_LAYER_TYPE
                logger.error(msg)
                raise common.PAWException(msg)
            
        if self._layer_type.lower() in ['vectorpoint', 'vectorpolygon']:
            if data_layer_group is not None:
                self._group = data_layer_group
                
            if self._group is None:
                msg = messages.ERROR_CATALOG_DATA_LAYERS_NO_GROUP
                logger.error(msg)
                raise common.PAWException(msg)
        elif self._layer_type.lower() in ['raster']:
            self._group = None
        else:
            msg = messages.ERROR_CATALOG_DATA_LAYERS_TYPE_UNKNOWN.format(data_layer_type)
            logger.error(msg)
            raise common.PAWException(msg)

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        data_layer_create_json = self.to_json_data_layers_post()
        
        try:
            response = cli.post(url     = cli.get_host() + 
                                          constants.CATALOG_DATA_SETS_API + 
                                          common.check_str(self._data_set_id) +
                                          constants.CATALOG_DATA_SETS_LAYERS_API,
                                headers = constants.CLIENT_PUT_AND_POST_HEADER,
                                body    = data_layer_create_json,
                                verify  = verify
                               )
        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('POST', 'request', cli.get_host() + constants.CATALOG_DATA_SETS_API + common.check_str(self._data_set_id) + constants.CATALOG_DATA_SETS_LAYERS_API, e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status_code != 200:
            
            error_message = 'failed'

            if response.json() is not None:
                try:
                    self._data_layer_response = data_layer_return_from_dict(response.json())
                    error_message = self._data_layer_response.message
                except:
                    msg = messages.INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)

            msg = messages.ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL.format('POST', 'request', constants.CATALOG_DATA_SETS_API + common.check_str(self._data_set_id) + constants.CATALOG_DATA_SETS_LAYERS_API, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
          
            self._data_layer_response = data_layer_return_from_dict(response.json())
            
            msg = messages.INFO_CATALOG_DATA_LAYERS_CREATE_SUCCESS.format(str(self._data_layer_response.data_layer_ids))
            logger.info(msg)
            
            self.get(data_set_id = self._data_set_id)
            
            group_id_regex = re.search("(?<=P)(.*?)(?=C)", self._data_layer_response.data_layer_ids[0])
            
            if group_id_regex is not None:
                self.set_group_id(common.check_str(group_id_regex.group(0)))

# 
class Search:
    #_data_sets: DataSets
    #_data_layers: DataLayers
    
    """
    An object to search Data Sets and Data Layers for search terms.
    
    :param client:      An IBM PAIRS Client.
    :type client:       ibmpairs.client.Client
    :param data_sets:   A list of Data Sets.
    :type data_sets:    List[DataSet]
    :param data_layers: A list of Data Layers.
    :type data_layers:  List[DataLayer]
    :raises Exception:  An ibmpairs.client.Client is not found.
    """
    
    #
    def __init__(self,
                 client: cl.Client       = None,
                 data_sets: DataSets     = None,
                 data_layers: DataLayers = None
                ):
                  
        self._client      = common.set_client(input_client  = client,
                                              global_client = cl.GLOBAL_PAIRS_CLIENT)
                  
        self._data_sets   = data_sets
        self._data_layers = data_layers
    
    # 
    def get_data_sets(self):
      return self._data_sets

    #
    def set_data_sets(self, data_sets):
      self._data_sets = common.check_class(data_sets, DataSets)

    #    
    def del_data_sets(self): 
      del self._data_sets

    #    
    data_sets = property(get_data_sets, set_data_sets, del_data_sets)
    
    # 
    def get_data_layers(self):
      return self._data_layers

    #
    def set_data_layers(self, data_layers):
      self._data_layers = common.check_class(data_layers, DataLayers)

    #    
    def del_data_layers(self): 
      del self._data_layers

    #    
    data_layers = property(get_data_layers, set_data_layers, del_data_layers)
    
                                  
    def get_catalog(self,
                    client: cl.Client = None,
                    verify: bool      = constants.GLOBAL_SSL_VERIFY
                   ):
                    
        """
        A method to get Data Sets and Data Layers to search.
        
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A pandas.DataFrame of merged Data Set and Data Layer information.
        :rtype:            pandas.DataFrame
        :raises Exception: An ibmpairs.client.Client is not found.
        """
                    
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)            
        
        data_set_columns = ['id', 'name', 'description_short', 'description_long']
        
        if self._data_sets is not None:
            dso = self._data_sets
        else:
            dso = DataSets()
            dso.get(client = cli,
                    verify = verify)
            self._data_sets = dso
            
        ds = dso.display(columns = data_set_columns)
        
        ds.columns = ['data_set_' + x for x in ds.columns]
        #ds.index.names = ['dataset_id']
        
        data_layer_columns   = ['dataset_id', 'id', 'name', 'description_short', 'description_long', 'level', 'type', 'unit']
        
        if self._data_layers is not None:
            dlo = self._data_layers
        else:
            dlo = DataLayers()
            dlo.get(client = cli,
                    verify = verify)
            self._data_layers = dlo
        
        dl = dlo.display(columns = data_layer_columns)
        
        dl.columns = ['data_layer_' + x if x != 'dataset_id' else x for x in dl.columns]
        #dl.index.names = ['datalayer_id']
        
        catalog_merge = pd.merge(dl, ds, left_on = 'dataset_id', right_on = 'data_set_id', how = 'left')
        
        catalog_merge.reset_index(inplace=True, drop=True)
        
        return catalog_merge
        
    def all(self,
            search_term: str,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to search Data Sets and Data Layers.
        
        :param search_term: A search term to be used.
        :type search_term:  str
        :param client:      An IBM PAIRS Client.
        :type client:       ibmpairs.client.Client
        :param verify:      SSL verification
        :type verify:       bool
        :returns:           A pandas.DataFrame of matching searched Data Sets and Data Layers.
        :rtype:             pandas.DataFrame
        :raises Exception:  An ibmpairs.client.Client is not found.
        """
            
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        ds = self.data_sets(search_term = search_term, 
                            client      = cli,
                            verify      = verify
                           )
        dl = self.data_layers(search_term = search_term, 
                              client      = cli,
                              verify      = verify
                             )
        
        frames = [ds, dl]
        union = pd.concat(frames)
        union.drop_duplicates(subset=None, keep='first', inplace=False)
        
        return union
        
    def data_sets(self,
                  search_term: str,
                  client: cl.Client = None,
                  verify: bool      = constants.GLOBAL_SSL_VERIFY
                 ):
                  
        """
        A method to search Data Sets.
        
        :param search_term: A search term to be used.
        :type search_term:  str
        :param client:      An IBM PAIRS Client.
        :type client:       ibmpairs.client.Client
        :param verify:      SSL verification
        :type verify:       bool
        :returns:           A pandas.DataFrame of matching searched Data Sets.
        :rtype:             pandas.DataFrame
        :raises Exception:  An ibmpairs.client.Client is not found.
        """
                  
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
                
        ds = self.get_catalog(client = cli,
                              verify = verify
                             )
                            
        ds = ds.fillna("")

        try:
            float(search_term) #check if searchterm is a number, if not search df for string
            search = ds.query('data_set_id ==' + search_term, engine='python')
        except:
            search = ds.query('data_set_name.str.contains("'+search_term+'")' or
                                  'dataset_description_short.str.contains("'+ search_term +'")' or
                                  'data_set_description_long.str.contains("'+ search_term +'")', 
                              engine='python'
                             )
                            
        search.reset_index(inplace=True, drop=True)
                            
        return search
        
    def data_layers(self,
                    search_term: str,
                    client: cl.Client = None,
                    verify: bool      = constants.GLOBAL_SSL_VERIFY
                   ):
                    
        """
        A method to search Data Layers.
        
        :param search_term: A search term to be used.
        :type search_term:  str
        :param client:      An IBM PAIRS Client.
        :type client:       ibmpairs.client.Client
        :param verify:      SSL verification
        :type verify:       bool
        :returns:           A pandas.DataFrame of matching searched Data Layers.
        :rtype:             pandas.DataFrame
        :raises Exception:  An ibmpairs.client.Client is not found.
        """
                    
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        dl = self.get_catalog(client = cli,
                              verify = verify
                             )
                            
        dl = dl.fillna("")
        
        try:
            float(search_term)
            search = dl.query('data_layer_id.str.contains("'+search_term+'")', engine='python')
        except:
            search = dl.query('data_layer_id.str.contains("'+search_term+'")' or
                              'data_layer_name.str.contains("'+search_term+'")' or
                                  'data_layer_description_short.str.contains("'+ search_term +'")' or
                                  'data_layer_description_long.str.contains("'+ search_term +'")', 
                              engine='python'
                             )

        search.reset_index(inplace=True, drop=True)
                            
        return search

#
def category_from_dict(category_dictionary: dict):
    """
    The method converts a dictionary of Category to a Category object.
    
    :param category_dict: A dictionary that contains the keys of a Category.
    :type category_dict:  dict             
    :rtype:               ibmpairs.catalog.Category
    :raises Exception:    If not a dict.
    """
    category = Category.from_dict(category_dictionary)
    return category

#
def category_to_dict(category: Category):
    """
    The method converts an object of Category to a dict.
    
    :param category: A Category object.
    :type category:  ibmpairs.catalog.Category             
    :rtype:          dict
    """
    return Category.to_dict(category)

#
def category_from_json(category_json: Any):
    """
    The method converts a dictionary or json string of Category to a Category object.
    
    :param category_json: A dictionary or json string that contains the keys of a Category.
    :type category_json:  Any             
    :rtype:               ibmpairs.catalog.Category
    :raises Exception:    If not a dict or a str.
    """
    category = Category.from_json(category_json)
    return category

#
def category_to_json(category: Category):
    """
    The method converts an object of Category to a json string.
    
    :param category: A Category object.
    :type category:  ibmpairs.catalog.Category             
    :rtype:          str
    """
    return Category.to_json(category)
    
#
def properties_from_dict(properties_dictionary: dict):
    """
    The method converts a dictionary of Properties to a Properties object.
    
    :param properties_dict: A dictionary that contains the keys of a Properties.
    :type properties_dict:  dict             
    :rtype:                 ibmpairs.catalog.Properties
    :raises Exception:      If not a dict.
    """
    properties = Properties.from_dict(properties_dictionary)
        
    return properties

#
def properties_to_dict(properties: Properties):
    """
    The method converts an object of Properties to a dict.
    
    :param properties:  A Properties object.
    :type properties:   ibmpairs.catalog.Properties             
    :rtype:             dict
    """
    return Properties.to_dict(properties)

#
def properties_from_json(properties_json: Any):
    """
    The method converts a dictionary or json string of Properties to a Properties object.
    
    :param properties_json: A dictionary or json string that contains the keys of a Properties.
    :type properties_json:  Any             
    :rtype:                 ibmpairs.catalog.Properties
    :raises Exception:      If not a dict or a str.
    """
    properties = Properties.from_json(properties_json)
    return properties

#
def properties_to_json(properties: Properties):
    """
    The method converts an object of Properties to a json string.
    
    :param properties: A Properties object.
    :type properties:  ibmpairs.catalog.Properties             
    :rtype:            str
    """
    return Properties.to_json(properties)

#
def spatial_coverage_from_dict(spatial_coverage_dictionary: dict):
    """
    The method converts a dictionary of SpatialCoverage to a SpatialCoverage object.
    
    :param spatial_coverage_dict: A dictionary that contains the keys of a SpatialCoverage.
    :type spatial_coverage_dict:  dict             
    :rtype:                       ibmpairs.catalog.SpatialCoverage
    :raises Exception:            If not a dict.
    """
    spatial_coverage = SpatialCoverage.from_dict(spatial_coverage_dictionary)
        
    return spatial_coverage

#
def spatial_coverage_to_dict(spatial_coverage: SpatialCoverage):
    """
    The method converts an object of SpatialCoverage to a dict.
    
    :param spatial_coverage: A SpatialCoverage object.
    :type spatial_coverage:  ibmpairs.catalog.SpatialCoverage             
    :rtype:                  dict
    """
    return SpatialCoverage.to_dict(spatial_coverage)

#
def spatial_coverage_from_json(spatial_coverage_json: Any):
    """
    The method converts a dictionary or json string of SpatialCoverage to a SpatialCoverage object.
    
    :param spatial_coverage_json: A dictionary or json string that contains the keys of a SpatialCoverage.
    :type spatial_coverage_json:  Any             
    :rtype:                       ibmpairs.catalog.SpatialCoverage
    :raises Exception:            If not a dict or a str.
    """
    spatial_coverage = SpatialCoverage.from_json(spatial_coverage_json)
    return spatial_coverage

#
def spatial_coverage_to_json(spatial_coverage: SpatialCoverage):
    """
    The method converts an object of SpatialCoverage to a json string.
    
    :param spatial_coverage: A SpatialCoverage object.
    :type spatial_coverage:  ibmpairs.catalog.SpatialCoverage             
    :rtype:                  str
    """
    return SpatialCoverage.to_json(spatial_coverage)

#
def data_set_from_dict(data_set_dictionary: dict,
                       client: cl.Client = None):
    """
    The method converts a dictionary of DataSet to a DataSet object.
    
    :param data_set_dict: A dictionary that contains the keys of a DataSet.
    :type data_set_dict:  dict  
    :param client:        An IBM PAIRS client.
    :type client:         ibmpairs.client.Client            
    :rtype:               ibmpairs.catalog.DataSet
    :raises Exception:    If not a dict.
    """
    data_set = DataSet.from_dict(data_set_dictionary)
    cli = common.set_client(input_client  = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_set.client = cli
    return data_set

#
def data_set_to_dict(data_set: DataSet):
    """
    The method converts an object of DataSet to a dict.
    
    :param data_set: A DataSet object.
    :type data_set:  ibmpairs.catalog.DataSet             
    :rtype:          dict
    """
    return DataSet.to_dict(data_set)

#
def data_set_to_dict_post(data_set: DataSet):
    """
    The method converts an object of DataSet to a dict ready for a POST call.
    
    :param data_set: A DataSet object.
    :type data_set:  ibmpairs.catalog.DataSet             
    :rtype:          dict
    """
    return DataSet.to_dict_data_set_post(data_set)

#
def data_set_to_dict_put(data_set: DataSet):
    """
    The method converts an object of DataSet to a dict ready for a PUT call.
    
    :param data_set: A DataSet object.
    :type data_set:  ibmpairs.catalog.DataSet             
    :rtype:          dict
    """
    return DataSet.to_dict_data_set_put(data_set)

#
def data_set_from_json(data_set_json: Any,
                       client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataSet to a DataSet object.
    
    :param data_set_json: A dictionary or json string that contains the keys of a DataSet.
    :type data_set_json:  Any   
    :param client:        An IBM PAIRS client.
    :type client:         ibmpairs.client.Client           
    :rtype:               ibmpairs.catalog.DataSet
    :raises Exception:    If not a dict or a str.
    """
    data_set = DataSet.from_json(data_set_json)
    
    cli = common.set_client(input_client  = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_set.client = cli
    return data_set

#
def data_set_to_json(data_set: DataSet):
    """
    The method converts an object of DataSet to a json string.
    
    :param data_set: A DataSet object.
    :type data_set:  ibmpairs.catalog.DataSet             
    :rtype:          str
    """
    return DataSet.to_json(data_set)
    
#
def data_set_to_json_post(data_set: DataSet):
    """
    The method converts an object of DataSet to a json string ready for a POST call.
    
    :param data_set: A DataSet object.
    :type data_set:  ibmpairs.catalog.DataSet             
    :rtype:          str
    """
    return DataSet.to_json_data_set_post(data_set)

#
def data_set_to_json_put(data_set: DataSet):
    """
    The method converts an object of DataSet to a json string ready for a PUT call.
    
    :param data_set: A DataSet object.
    :type data_set:  ibmpairs.catalog.DataSet             
    :rtype:          str
    """
    return DataSet.to_json_data_set_put(data_set)

#
def data_sets_from_dict(data_sets_dictionary: dict,
                        client: cl.Client = None):
    """
    The method converts a dictionary of DataSets to a DataSets object.
    
    :param data_sets_dict: A dictionary that contains the keys of a DataSets.
    :type data_sets_dict:  dict   
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client           
    :rtype:                ibmpairs.catalog.DataSets
    :raises Exception:     If not a dict.
    """
    data_sets = DataSets.from_dict(data_sets_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_sets.client = cli
    return data_sets

#
def data_sets_to_dict(data_sets: DataSets):
    """
    The method converts an object of DataSets to a dict.
    
    :param data_sets: A DataSets object.
    :type data_sets:  ibmpairs.catalog.DataSets             
    :rtype:           dict
    """
    return DataSets.to_dict(data_sets)

#
def data_sets_from_json(data_sets_json: Any,
                        client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataSets to a DataSets object.
    
    :param data_sets_json: A dictionary or json string that contains the keys of a DataSets.
    :type data_sets_json:  Any 
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client             
    :rtype:                ibmpairs.catalog.DataSets
    :raises Exception:     If not a dict or a str.
    """
    data_sets = DataSets.from_json(data_sets_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_sets.client = cli
    return data_sets

#
def data_sets_to_json(data_sets: DataSets):
    """
    The method converts an object of DataSets to a json string.
    
    :param data_sets: A DataSets object.
    :type data_sets:  ibmpairs.catalog.DataSets             
    :rtype:           str
    """
    return DataSets.to_json(data_sets)

#
def data_set_return_from_dict(data_set_return_dictionary: dict):
    """
    The method converts a dictionary of DataSetReturn to a DataSetReturn object.
    
    :param data_set_return_dict: A dictionary that contains the keys of a DataSetReturn.
    :type data_set_return_dict:  dict             
    :rtype:                      ibmpairs.catalog.DataSetReturn
    :raises Exception:           If not a dict.
    """
    data_set_return = DataSetReturn.from_dict(data_set_return_dictionary)
        
    return data_set_return

#
def data_set_return_to_dict(data_set_return: DataSetReturn):
    """
    The method converts an object of DataSetReturn to a dict.
    
    :param data_set_return: A DataSetReturn object.
    :type data_set_return:  ibmpairs.catalog.DataSetReturn             
    :rtype:                 dict
    """
    return DataSetReturn.to_dict(data_set_return)

#
def data_set_return_from_json(data_set_return_json: Any):
    """
    The method converts a dictionary or json string of DataSetReturn to a DataSetReturn object.
    
    :param data_set_return_json: A dictionary or json string that contains the keys of a DataSetReturn.
    :type data_set_return_json:  Any             
    :rtype:                      ibmpairs.catalog.DataSetReturn
    :raises Exception:           If not a dict or a str.
    """
    data_set_return = DataSetReturn.from_json(data_set_return_json)
    return data_set_return

#
def data_set_return_to_json(data_set_return: DataSetReturn):
    """
    The method converts an object of DataSetReturn to a json string.
    
    :param data_set_return: A DataSetReturn object.
    :type data_set_return:  ibmpairs.catalog.DataSetReturn             
    :rtype:                 str
    """
    return DataSetReturn.to_json(data_set_return)

#
def color_table_from_dict(color_table_dictionary: dict):
    """
    The method converts a dictionary of ColorTable to a ColorTable object.
    
    :param color_table_dict: A dictionary that contains the keys of a ColorTable.
    :type color_table_dict:  dict             
    :rtype:                  ibmpairs.catalog.ColorTable
    :raises Exception:       If not a dict.
    """
    color_table = ColorTable.from_dict(color_table_dictionary)
        
    return color_table

#
def color_table_to_dict(color_table: ColorTable):
    """
    The method converts an object of ColorTable to a dict.
    
    :param color_table:         A ColorTable object.
    :type color_table:          ibmpairs.catalog.ColorTable             
    :rtype:                     dict
    """
    return ColorTable.to_dict(color_table)

#
def color_table_from_json(color_table_json: Any):
    """
    The method converts a dictionary or json string of ColorTable to a ColorTable object.
    
    :param color_table_json:    A dictionary or json string that contains the keys of a ColorTable.
    :type color_table_json:     Any             
    :rtype:                     ibmpairs.catalog.ColorTable
    :raises Exception:          if not a dict or a str.
    """
    color_table = ColorTable.from_json(color_table_json)
    return color_table

#
def color_table_to_json(color_table: ColorTable):
    """
    The method converts an object of ColorTable to a json string.
    
    :param color_table:         A ColorTable object.
    :type color_table:          ibmpairs.catalog.ColorTable             
    :rtype:                     str
    """
    return ColorTable.to_json(color_table)

#
def data_layer_return_from_dict(data_layer_return_dictionary: dict):
    """
    The method converts a dictionary of DataLayerReturn to a DataLayerReturn object.
    
    :param data_layer_return_dict:    A dictionary that contains the keys of a DataLayerReturn.
    :type data_layer_return_dict:     dict             
    :rtype:                           ibmpairs.catalog.DataLayerReturn
    :raises Exception:                If not a dict.
    """
    data_layer_return = DataLayerReturn.from_dict(data_layer_return_dictionary)
        
    return data_layer_return

#
def data_layer_return_to_dict(data_layer_return: DataLayerReturn):
    """
    The method converts an object of DataLayerReturn to a dict.
    
    :param data_layer_return:         A DataLayerReturn object.
    :type data_layer_return:          ibmpairs.catalog.DataLayerReturn             
    :rtype:                           dict
    """
    return DataLayerReturn.to_dict(data_layer_return)

#
def data_layer_return_from_json(data_layer_return_json: Any):
    """
    The method converts a dictionary or json string of DataLayerReturn to a DataLayerReturn object.
    
    :param data_layer_return_json:    A dictionary or json string that contains the keys of a DataLayerReturn.
    :type data_layer_return_json:     Any             
    :rtype:                           ibmpairs.catalog.DataLayerReturn
    :raises Exception:                If not a dict or a str.
    """
    data_layer_return = DataLayerReturn.from_json(data_layer_return_json)
    return data_layer_return

#
def data_layer_return_to_json(data_layer_return: DataLayerReturn):
    """
    The method converts an object of DataLayerReturn to a json string.
    
    :param data_layer_return:         A DataLayerReturn object.
    :type data_layer_return:          ibmpairs.catalog.DataLayerReturn             
    :rtype:                           str
    """
    return DataLayerReturn.to_json(data_layer_return)

#
def data_layer_dimension_return_from_dict(data_layer_dimension_return_dictionary: dict):
    """
    The method converts a dictionary of DataLayerDimensionReturn to a DataLayerDimensionReturn object.
    
    :param data_layer_dimension_return_dict:    A dictionary that contains the keys of a DataLayerDimensionReturn.
    :type data_layer_dimension_return_dict:     dict             
    :rtype:                                     ibmpairs.catalog.DataLayerDimensionReturn
    :raises Exception:                          If not a dict.
    """
    data_layer_dimension_return = DataLayerDimensionReturn.from_dict(data_layer_dimension_return_dictionary)
        
    return data_layer_dimension_return

#
def data_layer_dimension_return_to_dict(data_layer_dimension_return: DataLayerDimensionReturn):
    """
    The method converts an object of DataLayerDimensionReturn to a dict.
    
    :param data_layer_dimension_return:         A DataLayerDimensionReturn object.
    :type data_layer_dimension_return:          ibmpairs.catalog.DataLayerDimensionReturn             
    :rtype:                                     dict
    """
    return DataLayerDimensionReturn.to_dict(data_layer_dimension_return)

#
def data_layer_dimension_return_from_json(data_layer_dimension_return_json: Any):
    """
    The method converts a dictionary or json string of DataLayerDimensionReturn to a DataLayerDimensionReturn object.
    
    :param data_layer_dimension_return_json:    A dictionary or json string that contains the keys of a DataLayerDimensionReturn.
    :type data_layer_dimension_return_json:     Any             
    :rtype:                                     ibmpairs.catalog.DataLayerDimensionReturn
    :raises Exception:                          If not a dict or a str.
    """
    data_layer_dimension_return = DataLayerDimensionReturn.from_json(data_layer_dimension_return_json)
    return data_layer_dimension_return

#
def data_layer_dimension_return_to_json(data_layer_dimension_return: DataLayerDimensionReturn):
    """
    The method converts an object of DataLayerDimensionReturn to a json string.
    
    :param data_layer_dimension_return:         A DataLayerDimensionReturn object.
    :type data_layer_dimension_return:          ibmpairs.catalog.DataLayerDimensionReturn             
    :rtype:                                     str
    """
    return DataLayerDimensionReturn.to_json(data_layer_dimension_return)

#
def data_layer_dimension_from_dict(data_layer_dimension_dictionary: dict,
                                   client: cl.Client = None):
    """
    The method converts a dictionary of DataLayerDimension to a DataLayerDimension object.

    :param data_layer_dimension_dict:    A dictionary that contains the keys of a DataLayerDimension.
    :type data_layer_dimension_dict:     dict  
    :param client:                       An IBM PAIRS client.
    :type client:                        ibmpairs.client.Client            
    :rtype:                              ibmpairs.catalog.DataLayerDimension
    :raises Exception:                   If not a dict.
    """
    data_layer_dimension = DataLayerDimension.from_dict(data_layer_dimension_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_dimension.client = cli
    return data_layer_dimension

#
def data_layer_dimension_to_dict(data_layer_dimension: DataLayerDimension):
    """
    The method converts an object of DataLayerDimension to a dict.
    
    :param data_layer_dimension:         A DataLayerDimension object.
    :type data_layer_dimension:          ibmpairs.catalog.DataLayerDimension             
    :rtype:                              dict
    """
    return DataLayerDimension.to_dict(data_layer_dimension)

#
def data_layer_dimension_to_dict_post(data_layer_dimension: DataLayerDimension):
    """
    The method converts an object of DataLayerDimension to a dict ready for a POST call.
    
    :param data_layer_dimension:         A DataLayerDimension object.
    :type data_layer_dimension:          ibmpairs.catalog.DataLayerDimension             
    :rtype:                              dict
    """
    return DataLayerDimension.to_dict_data_layer_dimension_post(data_layer_dimension)

#
def data_layer_dimension_from_json(data_layer_dimension_json: Any,
                                   client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataLayerDimension to a DataLayerDimension object.
    
    :param data_layer_dimension_json:    A dictionary or json string that contains the keys of a DataLayerDimension.
    :type data_layer_dimension_json:     Any        
    :param client:                       An IBM PAIRS client.
    :type client:                        ibmpairs.client.Client      
    :rtype:                              ibmpairs.catalog.DataLayerDimension
    :raises Exception:                   If not a dict or a str.
    """
    data_layer_dimension = DataLayerDimension.from_json(data_layer_dimension_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_dimension.client = cli
    return data_layer_dimension

#
def data_layer_dimension_to_json(data_layer_dimension: DataLayerDimension):
    """
    The method converts an object of DataLayerDimension to a json string.
    
    :param data_layer_dimension:         A DataLayerDimension object.
    :type data_layer_dimension:          ibmpairs.catalog.DataLayerDimension             
    :rtype:                              str
    """
    return DataLayerDimension.to_json(data_layer_dimension)

#
def data_layer_dimension_to_json_post(data_layer_dimension: DataLayerDimension):
    """
    The method converts an object of DataLayerDimension to a json string ready for a POST call.
    
    :param data_layer_dimension:         A DataLayerDimension object.
    :type data_layer_dimension:          ibmpairs.catalog.DataLayerDimension             
    :rtype:                              str
    """
    return DataLayerDimension.to_json_data_layer_dimension_post(data_layer_dimension)

#
def data_layer_dimensions_from_dict(data_layer_dimensions_dictionary: dict,
                                    client: cl.Client = None):
    """
    The method converts a dictionary of DataLayerDimensions to a DataLayerDimensions object.
    
    :param data_layer_dimensions_dict:    A dictionary that contains the keys of a DataLayerDimensions.
    :type data_layer_dimensions_dict:     dict 
    :param client:                        An IBM PAIRS client.
    :type client:                         ibmpairs.client.Client             
    :rtype:                               ibmpairs.catalog.DataLayerDimensions
    :raises Exception:                    If not a dict.
    """
    data_layer_dimensions = DataLayerDimensions.from_dict(data_layer_dimensions_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_dimensions.client = cli
    return data_layer_dimensions

#
def data_layer_dimensions_to_dict(data_layer_dimensions: DataLayerDimensions):
    """
    The method converts an object of DataLayerDimensions to a dict.
    
    :param data_layer_dimensions:         A DataLayerDimensions object.
    :type data_layer_dimensions:          ibmpairs.catalog.DataLayerDimensions             
    :rtype:                              dict
    """
    return DataLayerDimensions.to_dict(data_layer_dimensions)
    
#
def data_layer_dimensions_from_json(data_layer_dimensions_json: Any,
                                    client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataLayerDimensions to a DataLayerDimensions object.
    
    :param data_layer_dimensions_json:    A dictionary or json string that contains the keys of a DataLayerDimensions.
    :type data_layer_dimensions_json:     Any 
    :param client:                        An IBM PAIRS client.
    :type client:                         ibmpairs.client.Client             
    :rtype:                               ibmpairs.catalog.DataLayerDimensions
    :raises Exception:                    If not a dict or a str.
    """
    data_layer_dimensions = DataLayerDimensions.from_json(data_layer_dimensions_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_dimensions.client = cli
    return data_layer_dimensions

#
def data_layer_dimensions_to_json(data_layer_dimensions: DataLayerDimensions):
    """
    The method converts an object of DataLayerDimensions to a json string.
    
    :param data_layer_dimensions:         A DataLayerDimensions object.
    :type data_layer_dimensions:          ibmpairs.catalog.DataLayerDimensions             
    :rtype:                              str
    """
    return DataLayerDimensions.to_json(data_layer_dimensions)

#
def data_layer_property_return_from_dict(data_layer_property_return_dictionary: dict):
    """
    The method converts a dictionary of DataLayerPropertyReturn to a DataLayerPropertyReturn object.
    
    :param data_layer_property_return_dict:    A dictionary that contains the keys of a DataLayerPropertyReturn.
    :type data_layer_property_return_dict:     dict             
    :rtype:                                    ibmpairs.catalog.DataLayerPropertyReturn
    :raises Exception:                         If not a dict.
    """
    data_layer_property_return = DataLayerPropertyReturn.from_dict(data_layer_property_return_dictionary)
        
    return data_layer_property_return

#
def data_layer_property_return_to_dict(data_layer_property_return: DataLayerPropertyReturn):
    """
    The method converts an object of DataLayerPropertyReturn to a dict.
    
    :param data_layer_property_return:         A DataLayerPropertyReturn object.
    :type data_layer_property_return:          ibmpairs.catalog.DataLayerPropertyReturn             
    :rtype:                                    dict
    """
    return DataLayerPropertyReturn.to_dict(data_layer_property_return)

#
def data_layer_property_return_from_json(data_layer_property_return_json: Any):
    """
    The method converts a dictionary or json string of DataLayerPropertyReturn to a DataLayerPropertyReturn object.
    
    :param data_layer_property_return_json:    A dictionary or json string that contains the keys of a DataLayerPropertyReturn.
    :type data_layer_property_return_json:     Any             
    :rtype:                                    ibmpairs.catalog.DataLayerPropertyReturn
    :raises Exception:                         If not a dict or a str.
    """
    data_layer_property_return = DataLayerPropertyReturn.from_json(data_layer_property_return_json)
    return data_layer_property_return

#
def data_layer_property_return_to_json(data_layer_property_return: DataLayerPropertyReturn):
    """
    The method converts an object of DataLayerPropertyReturn to a json string.
    
    :param data_layer_property_return:         A DataLayerPropertyReturn object.
    :type data_layer_property_return:          ibmpairs.catalog.DataLayerPropertyReturn             
    :rtype:                                    str
    """
    return json.dumps(DataLayerPropertyReturn.to_dict(data_layer_property_return))

#
def data_layer_property_from_dict(data_layer_property_dictionary: dict,
                                  client: cl.Client = None):
    """
    The method converts a dictionary of DataLayerProperty to a DataLayerProperty object.
    
    :param data_layer_property_dict:    A dictionary that contains the keys of a DataLayerProperty.
    :type data_layer_property_dict:     dict   
    :param client:                      An IBM PAIRS client.
    :type client:                       ibmpairs.client.Client           
    :rtype:                             ibmpairs.catalog.DataLayerProperty
    :raises Exception:                  If not a dict.
    """
    data_layer_property = DataLayerProperty.from_dict(data_layer_property_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_property.client = cli
    return data_layer_property

#
def data_layer_property_to_dict(data_layer_property: DataLayerProperty):
    """
    The method converts an object of DataLayerProperty to a dict.
    
    :param data_layer_property:         A DataLayerProperty object.
    :type data_layer_property:          ibmpairs.catalog.DataLayerProperty             
    :rtype:                             dict
    """
    return DataLayerProperty.to_dict(data_layer_property)
    
#
def data_layer_property_to_dict_post(data_layer_property: DataLayerProperty):
    """
    The method converts an object of DataLayerProperty to a dict ready for a POST call.
    
    :param data_layer_property:         A DataLayerProperty object.
    :type data_layer_property:          ibmpairs.catalog.DataLayerProperty             
    :rtype:                             dict
    """
    return DataLayerProperty.to_dict_data_layer_property_post(data_layer_property)

#
def data_layer_property_from_json(data_layer_property_json: Any,
                                  client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataLayerProperty to a DataLayerProperty object.
    
    :param data_layer_property_json:    A dictionary or json string that contains the keys of a DataLayerProperty.
    :type data_layer_property_json:     Any    
    :param client:                      An IBM PAIRS client.
    :type client:                       ibmpairs.client.Client          
    :rtype:                             ibmpairs.catalog.DataLayerProperty
    :raises Exception:                  If not a dict or a str.
    """
    data_layer_property = DataLayerProperty.from_json(data_layer_property_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_property.client = cli
    return data_layer_property

#
def data_layer_property_to_json(data_layer_property: DataLayerProperty):
    """
    The method converts an object of DataLayerProperty to a json string.
    
    :param data_layer_property:         A DataLayerProperty object.
    :type data_layer_property:          ibmpairs.catalog.DataLayerProperty             
    :rtype:                             str
    """
    return DataLayerProperty.to_json(data_layer_property)
    
#
def data_layer_property_to_json_post(data_layer_property: DataLayerProperty):
    """
    The method converts an object of DataLayerProperty to a json string ready for a POST call.
    
    :param data_layer_property:         A DataLayerProperty object.
    :type data_layer_property:          ibmpairs.catalog.DataLayerProperty             
    :rtype:                             str
    """
    return DataLayerProperty.to_json_data_layer_property_post(data_layer_property)

#
def data_layer_properties_from_dict(data_layer_properties_dictionary: dict,
                                    client: cl.Client = None):
    """
    The method converts a dictionary of DataLayerProperties to a DataLayerProperties object.
    
    :param data_layer_properties_dict:    A dictionary that contains the keys of a DataLayerProperties.
    :type data_layer_properties_dict:     dict  
    :param client:                        An IBM PAIRS client.
    :type client:                         ibmpairs.client.Client            
    :rtype:                               ibmpairs.catalog.DataLayerProperties
    :raises Exception:                    if not a dict.
    """
    data_layer_properties = DataLayerProperties.from_dict(data_layer_properties_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_properties.client = cli
    return data_layer_properties

#
def data_layer_properties_to_dict(data_layer_properties: DataLayerProperties):
    """
    The method converts an object of DataLayerProperties to a dict.
    
    :param data_layer_properties:         A DataLayerProperties object.
    :type data_layer_properties:          ibmpairs.catalog.DataLayerProperties             
    :rtype:                               dict
    """
    return DataLayerProperties.to_dict(data_layer_properties)

#
def data_layer_properties_from_json(data_layer_properties_json: Any,
                                    client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataLayerProperties to a DataLayerProperties object.
    
    :param data_layer_properties_json:    A dictionary or json string that contains the keys of a DataLayerProperties.
    :type data_layer_properties_json:     Any  
    :param client:                        An IBM PAIRS client.
    :type client:                         ibmpairs.client.Client            
    :rtype:                               ibmpairs.catalog.DataLayerProperties
    :raises Exception:                    If not a dict or a str.
    """
    data_layer_properties = DataLayerProperties.from_json(data_layer_properties_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer_properties.client = cli
    return data_layer_properties

#
def data_layer_properties_to_json(data_layer_properties: DataLayerProperties):
    """
    The method converts an object of DataLayerProperties to a json string.
    
    :param data_layer_properties:         A DataLayerProperties object.
    :type data_layer_properties:          ibmpairs.catalog.DataLayerProperties             
    :rtype:                               str
    """
    return DataLayerProperties.to_json(data_layer_properties)

#
def data_layer_from_dict(data_layer_dictionary: dict,
                         client: cl.Client = None):
    """
    The method converts a dictionary of DataLayer to a DataLayer object.
    
    :param data_layer_dict:     A dictionary that contains the keys of a DataLayer.
    :type data_layer_dict:      dict   
    :param client:              An IBM PAIRS client.
    :type client:               ibmpairs.client.Client           
    :rtype:                     ibmpairs.catalog.DataLayer
    :raises Exception:          If not a dict.
    """
    data_layer = DataLayer.from_dict(data_layer_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer.client = cli
    return data_layer

#
def data_layer_to_dict(data_layer: DataLayer):
    """
    The method converts an object of DataLayer to a dict.
    
    :param data_layer:          A DataLayer object.
    :type data_layer:           ibmpairs.catalog.DataLayer             
    :rtype:                     dict
    """
    return DataLayer.to_dict(data_layer)
    
#
def data_layer_to_dict_post(data_layer: DataLayer):
    """
    The method converts an object of DataLayer to a dict ready for a POST call.
    
    :param data_layer:          A DataLayer object.
    :type data_layer:           ibmpairs.catalog.DataLayer             
    :rtype:                     dict
    """
    return DataLayer.to_dict_data_layer_post(data_layer)
    
#
def data_layer_to_dict_put(data_layer: DataLayer):
    """
    The method converts an object of DataLayer to a dict ready for a PUT call.
    
    :param data_layer:          A DataLayer object.
    :type data_layer:           ibmpairs.catalog.DataLayer             
    :rtype:                     dict
    """
    return DataLayer.to_dict_data_layer_put(data_layer)

#
def data_layer_from_json(data_layer_json: Any,
                         client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataLayer to a DataLayer object.
    
    :param data_layer_json:     A dictionary or json string that contains the keys of a DataLayer.
    :type data_layer_json:      Any 
    :param client:              An IBM PAIRS client.
    :type client:               ibmpairs.client.Client             
    :rtype:                     ibmpairs.catalog.DataLayer
    :raises Exception:          If not a dict or a str.
    """
    data_layer = DataLayer.from_json(data_layer_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layer.client = cli
    return data_layer

#
def data_layer_to_json(data_layer: DataLayer):
    """
    The method converts an object of DataLayer to a json string.
    
    :param data_layer:          A DataLayer object.
    :type data_layer:           ibmpairs.catalog.DataLayer             
    :rtype:                     str
    """
    return DataLayer.to_json(data_layer)

#
def data_layer_to_json_post(data_layer: DataLayer):
    """
    The method converts an object of DataLayer to a json string ready for a POST call.
    
    :param data_layer:          A DataLayer object.
    :type data_layer:           ibmpairs.catalog.DataLayer             
    :rtype:                     str
    """
    return DataLayer.to_json_data_layer_post(data_layer)

#
def data_layer_to_json_put(data_layer: DataLayer):
    """
    The method converts an object of DataLayer to a json string ready for a PUT call.
    
    :param data_layer:          A DataLayer object.
    :type data_layer:           ibmpairs.catalog.DataLayer             
    :rtype:                     str
    """
    return DataLayer.to_json_data_layer_put(data_layer)

#
def data_layers_from_dict(data_layers_dictionary: dict,
                         client: cl.Client = None):
    """
    The method converts a dictionary of DataLayers to a DataLayers object.
    
    :param data_layers_dict:     A dictionary that contains the keys of a DataLayers.
    :type data_layers_dict:      dict   
    :param client:               An IBM PAIRS client.
    :type client:                ibmpairs.client.Client           
    :rtype:                      ibmpairs.catalog.DataLayers
    :raises Exception:           If not a dict.
    """
    data_layers = DataLayers.from_dict(data_layers_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layers.client = cli
    return data_layers

#
def data_layers_to_dict(data_layers: DataLayers):
    """
    The method converts an object of DataLayers to a dict.
    
    :param data_layers:          A DataLayers object.
    :type data_layers:           ibmpairs.catalog.DataLayers             
    :rtype:                      dict
    """
    return DataLayers.to_dict(data_layers)
    
#
def data_layers_to_dict_post(data_layers: DataLayers):
    """
    The method converts an object of DataLayers to a dict ready for a POST call.
    
    :param data_layers:          A DataLayers object.
    :type data_layers:           ibmpairs.catalog.DataLayers             
    :rtype:                      dict
    """
    return DataLayers.to_dict_data_layers_post(data_layers)

#
def data_layers_from_json(data_layers_json: Any,
                          client: cl.Client = None):
    """
    The method converts a dictionary or json string of DataLayers to a DataLayers object.
    
    :param data_layers_json:     A dictionary or json string that contains the keys of a DataLayers.
    :type data_layers_json:      Any  
    :param client:               An IBM PAIRS client.
    :type client:                ibmpairs.client.Client            
    :rtype:                      ibmpairs.catalog.DataLayers
    :raises Exception:           If not a dict or a str.
    """
    data_layers = DataLayers.from_json(data_layers_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    data_layers.client = cli
    return data_layers

#
def data_layers_to_json(data_layers: DataLayers):
    """
    The method converts an object of DataLayers to a json string.
    
    :param data_layers:          A DataLayers object.
    :type data_layers:           ibmpairs.catalog.DataLayers             
    :rtype:                      str
    """
    return DataLayers.to_json(data_layers)

#
def data_layers_to_json_post(data_layers: DataLayers):
    """
    The method converts an object of DataLayers to a json string ready for a POST call.
    
    :param data_layers:          A DataLayers object.
    :type data_layers:           ibmpairs.catalog.DataLayers             
    :rtype:                      str
    """
    return DataLayers.to_json_data_layers_post(data_layers)

# fold: Catalog Methods {{{
#
def get_data_sets(client: cl.Client = None,
                  verify: bool      = constants.GLOBAL_SSL_VERIFY
                 ):
    """
    The method gets metadata about all DataSets from the server side.
    
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client 
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataSets
    :raises Exception:     If a global client is not yet and no client is provided
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_sets = DataSets()
    
    data_sets.get(client = cli,
                  verify = verify
                 )
    
    return data_sets

#
def get_data_set(id,
                 client: cl.Client = None,
                 verify: bool      = constants.GLOBAL_SSL_VERIFY
                ):
    """
    The method gets metadata about a DataSet from the server.
    
    :param id:             A DataSet ID number.
    :type id:              int or str 
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client  
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataSet
    :raises Exception:     If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_set = DataSet()
    
    ds = data_set.get(id     = common.check_str(id),
                      client = cli,
                      verify = verify
                     )
    
    return ds
    
#
def create_data_set(data_set: DataSet,
                    client: cl.Client = None,
                    verify: bool      = constants.GLOBAL_SSL_VERIFY
                   ):
    """
    Creates a DataSet from a DataSet object.
    
    :param data_set:       A DataSet object.
    :type data_set:        ibmpairs.catalog.DataSet
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client 
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataSet
    :raises Exception:     If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)

    data_set.create(client = cli,
                    verify = verify
                   )
    
    return data_set
    
#
def update_data_set(data_set: DataSet,
                    id                = None,
                    client: cl.Client = None,
                    verify: bool      = constants.GLOBAL_SSL_VERIFY
                   ):
    """
    Updates a DataSet from a DataSet object.
    
    :param data_set:       A DataSet object.
    :type data_set:        ibmpairs.catalog.DataSet
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client  
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataSet
    :raises Exception:     If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_set.update(id     = id,
                    client = cli,
                    verify = verify
                   )
    
    return data_set

#
def delete_data_set(id,
                    hard_delete: bool = False,
                    client: cl.Client = None,
                    verify: bool      = constants.GLOBAL_SSL_VERIFY
                   ):
    """
    Deletes a DataSet.
    
    :param id:             A DataSet ID number.
    :type id:              ibmpairs.catalog.DataSet
    :param hard_delete:    A flag to indicate whether a hard delete should be performed. 
                           This is necessary where the intention is to re-create a DataSet
                           with the same name. WARNING: when a hard delete is performed
                           any data associated with the DataSet is deleted too.
    :type hard_delete:     bool
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client  
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataSet
    :raises Exception:     If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_set = DataSet()

    data_set.delete(id          = common.check_str(id),
                    hard_delete = hard_delete,
                    client      = cli,
                    verify      = verify
                   )
    
    return data_set

#    
def get_data_layers(data_set_id              = None,
                    data_layer_group_id: str = None,
                    data_layer_group: str    = None,
                    client: cl.Client        = None,
                    verify: bool             = constants.GLOBAL_SSL_VERIFY
                   ):
    """
    The method gets metadata about all DataLayers from the server or a selection by DataSet.
    
    :param data_set_id:         A DataSet ID Number (if desire is to get only DataLayers that belong to a certain DataSet).
    :type data_set_id:          int or str 
    :param data_layer_group_id: The Data Layer Group ID to filter the results on.
    :type data_layer_group_id:  str
    :param data_layer_group:    The Data Layer Group name to filter the results on.
    :type data_layer_group:     str
    :param client:              An IBM PAIRS client.
    :type client:               ibmpairs.client.Client  
    :param verify:              SSL Verification flag.
    :type verify:               bool           
    :rtype:                     ibmpairs.catalog.DataLayers
    :raises Exception:          If a global client is not yet and no client is provided
    """
                    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layers = DataLayers()
    
    data_layers.get(data_set_id         = data_set_id,
                    data_layer_group_id = data_layer_group_id,
                    data_layer_group    = data_layer_group,
                    client              = cli,
                    verify              = verify
                   )
    
    return data_layers
    
#
def create_data_layers(data_layers: DataLayers,
                       data_set_id           = None,
                       data_layer_type: str  = None,
                       data_layer_group: str = None,
                       client: cl.Client     = None,
                       verify: bool          = constants.GLOBAL_SSL_VERIFY
                      ):
    """
    Creates a list of DataLayers from a DataLayers object.
    
    :param data_layers:      A DataLayers object.
    :type data_layers:       ibmpairs.catalog.DataLayer
    :param data_set_id:      A DataSet ID number.
    :type data_set_id:       int or str
    :param data_layer_type:  A DataLayer type (i.e. Raster or VectorPoint or VectorPolygon).
    :type data_layer_type:   str
    :param data_layer_group: A DataLayer group name (if vector).
    :type data_layer_group:  str
    :param client:           An IBM PAIRS client.
    :type client:            ibmpairs.client.Client  
    :param verify:           SSL Verification flag.
    :type verify:            bool           
    :rtype:                  ibmpairs.catalog.DataLayers
    :raises Exception:       If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)

    data_layers.create(data_set_id      = data_set_id,
                       data_layer_type  = data_layer_type,
                       data_layer_group = data_layer_group,
                       client           = cli,
                       verify           = verify
                      )
    
    return data_layers

#
def get_data_layer(id,
                   client:cl.Client = None,
                   verify: bool      = constants.GLOBAL_SSL_VERIFY
                  ):
    """
    The method gets metadata about a DataLayer from the server.
    
    :param data_set_id:    A DataLayer ID number.
    :type data_set_id:     int or str 
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client 
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayer
    :raises Exception:     If a global client is not yet and no client is provided
    """
                    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layer = DataLayer()
    
    dl = data_layer.get(id     = id,
                        client = cli,
                        verify = verify
                       )
    
    return dl
    
#
def create_data_layer(data_layer: DataLayer,
                      data_set_id,
                      data_layer_type: str,
                      data_layer_group: str = None,
                      client: cl.Client     = None,
                      verify: bool          = constants.GLOBAL_SSL_VERIFY
                     ):
    """
    Creates a DataLayer from a DataLayer object.
    
    :param data_layer:     A DataLayer object.
    :type data_layer:      ibmpairs.catalog.DataLayer
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client 
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayer
    :raises Exception:     If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)

    dls = data_layer.create(data_set_id      = data_set_id,
                            data_layer_type  = data_layer_type,
                            data_layer_group = data_layer_group,
                            client           = cli,
                            verify           = verify
                           )
    
    return dls
    
#
def update_data_layer(data_layer: DataLayer,
                      id                = None,
                      client: cl.Client = None,
                      verify: bool      = constants.GLOBAL_SSL_VERIFY
                     ):
    """
    Updates a DataLayer from a DataLayer object.
    
    :param data_layer:     A DataLayer object.
    :type data_layer:      ibmpairs.catalog.DataLayer
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client  
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayer
    :raises Exception:     If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layer.update(id     = id,
                      client = cli,
                      verify = verify
                     )
    
    return data_layer

#
def delete_data_layer(id,
                      hard_delete: bool = False,
                      client: cl.Client = None,
                      verify: bool      = constants.GLOBAL_SSL_VERIFY
                     ):
    """
    Deletes a DataLayer.
    
    :param id:             A DataLayer ID number.
    :type id:              ibmpairs.catalog.DataLayer
    :param hard_delete:    A flag to indicate whether a hard delete should be performed. 
                           This is necessary where the intention is to re-create a DataLayer
                           in a DataSet with the same name. WARNING: when a hard delete is 
                           performed any data associated with the DataLayer is deleted too.
    :type hard_delete:     bool
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client  
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayer
    :raises Exception:     If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layer = DataLayer()

    data_layer.delete(id          = common.check_str(id),
                      hard_delete = hard_delete,
                      client      = cli,
                      verify      = verify
                     )
    
    return data_layer
  
#    
def get_data_layer_dimensions(data_layer_id     = None,
                              client: cl.Client = None,
                              verify: bool      = constants.GLOBAL_SSL_VERIFY
                             ):
    """
    The method gets metadata about all DataLayerDimensions in a DataLayer from the server.
    
    :param data_layer_id:  A DataLayer ID Number.
    :type data_layer_id:   int or str 
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client  
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayerDimesnions
    :raises Exception:     If a global client is not yet and no client is provided
    """
                    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layer_dimensions = DataLayerDimensions()
    
    data_layer_dimensions.get(data_layer_id = data_layer_id,
                              client        = cli,
                              verify        = verify
                             )
    
    return data_layer_dimensions
    
#
def get_data_layer_dimension(id,
                             client:cl.Client = None,
                             verify: bool     = constants.GLOBAL_SSL_VERIFY
                            ):
    """
    The method gets metadata about a DataLayerDimension from the server.
    
    :param id:             A DataLayerDimension ID Number.
    :type id:              int or str 
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client 
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayerDimension
    :raises Exception:     If a global client is not yet and no client is provided
    """
                    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layer_dimension = DataLayerDimension()
    
    dld = data_layer_dimension.get(id     = id,
                                   client = cli,
                                   verify = verify
                                  )
    
    return dld
    
#
def create_data_layer_dimension(data_layer_dimension: DataLayerDimension,
                                data_layer_id,
                                client: cl.Client     = None,
                                verify: bool          = constants.GLOBAL_SSL_VERIFY
                               ):
    """
    Creates a DataLayerDimension in a DataLayer from a DataLayerDimension object.
    
    :param data_layer_dimension:     A DataLayerDimension object.
    :type data_layer_dimension:      ibmpairs.catalog.DataLayerDimension
    :param data_layer_id:            A DataLayer ID number.
    :type data_layer_id:             int or str
    :param client:                   An IBM PAIRS client.
    :type client:                    ibmpairs.client.Client  
    :param verify:                   SSL Verification flag.
    :type verify:                    bool           
    :rtype:                          ibmpairs.catalog.DataLayerDimension
    :raises Exception:               If a global client is not yet and no client is provided
    """
                  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)

    data_layer_dimension.create(data_layer_id = data_layer_id,
                                client        = cli,
                                verify        = verify
                               )
    
    return data_layer_dimension
    
#    
def get_data_layer_properties(data_layer_id     = None,
                              client: cl.Client = None,
                              verify: bool      = constants.GLOBAL_SSL_VERIFY
                             ):
    """
    The method gets metadata about all DataLayerProperties in a DataLayer from the server.
    
    :param data_layer_id:  A DataLayer ID Number.
    :type data_layer_id:   int or str 
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client  
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayerProperties
    :raises Exception:     If a global client is not yet and no client is provided
    """
                    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layer_properties = DataLayerProperties()
    
    data_layer_properties.get(data_layer_id = data_layer_id,
                              client        = cli,
                              verify        = verify
                             )
    
    return data_layer_properties
    
#
def get_data_layer_property(id,
                            client:cl.Client = None,
                            verify: bool     = constants.GLOBAL_SSL_VERIFY
                           ):
    """
    The method gets metadata about a DataLayerProperty from the server.
    
    :param id:             A DataLayerProperty ID Number.
    :type id:              int or str 
    :param client:         An IBM PAIRS client.
    :type client:          ibmpairs.client.Client 
    :param verify:         SSL Verification flag.
    :type verify:          bool           
    :rtype:                ibmpairs.catalog.DataLayerProperty
    :raises Exception:     If a global client is not yet and no client is provided
    """
                    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    data_layer_property = DataLayerProperty()
    
    dlp = data_layer_property.get(id     = id,
                                  client = cli,
                                  verify = verify
                                 )
    
    return dlp
    
#
def create_data_layer_property(data_layer_property: DataLayerProperty,
                               data_layer_id,
                               client: cl.Client     = None,
                               verify: bool          = constants.GLOBAL_SSL_VERIFY
                              ):
    """
    Creates a DataLayerProperty in a DataLayer from a DataLayerProperty object.
    
    :param data_layer_property:      A DataLayerProperty object.
    :type data_layer_property:       ibmpairs.catalog.DataLayerProperty
    :param data_layer_id:            A DataLayer ID number.
    :type data_layer_id:             int or str
    :param client:                   An IBM PAIRS client.
    :type client:                    ibmpairs.client.Client 
    :param verify:                   SSL Verification flag.
    :type verify:                    bool           
    :rtype:                          ibmpairs.catalog.DataLayerProperty
    :raises Exception:               If a global client is not yet and no client is provided
    """
          
    cli = common.set_client(input_client = client,
              global_client = cl.GLOBAL_PAIRS_CLIENT)

    data_layer_property.create(data_layer_id = data_layer_id,
                               client        = cli,
                               verify        = verify
                              )
  
    return data_layer_property

#
def search(search_term: str,
           client: cl.Client = None,
           verify: bool      = constants.GLOBAL_SSL_VERIFY
          ):
    """
    Creates a DataLayerProperty in a DataLayer from a DataLayerProperty object.
    
    :param search_term:      A free text search term used to search DataSets and DataLayers.
    :type search_term:       str
    :param client:           An IBM PAIRS client.
    :type client:            ibmpairs.client.Client 
    :param verify:           SSL verification
    :type verify:            bool          
    :rtype:                  pandas.DataFrame
    :raises Exception:       If a global client is not yet and no client is provided
    """
            
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    so = Search()
    search = so.all(search_term = search_term, 
                    client = cli,
                    verify = verify
                   )
    return search