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
import os
import warnings
import re
from typing import List, Any
from io import StringIO 
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
import ibmpairs.constants as constants
import ibmpairs.messages as messages
import ibmpairs.common as common
import ibmpairs.client as cl
from ibmpairs.logger import logger
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import aiohttp
import asyncio
import numpy as np
#try:
#    from osgeo import gdal
import pandas
import polling
import zipfile
#}}}

QUERY_DEFAULT_WORKERS          = int(os.environ.get('QUERY_DEFAULT_WORKERS', 1))
QUERY_MAX_WORKERS              = int(os.environ.get('QUERY_MAX_WORKERS', 8))
QUERY_MIN_STATUS_INTERVAL      = int(os.environ.get('QUERY_MIN_STATUS_INTERVAL', 15))
QUERY_STATUS_CHECK_INTERVAL    = int(os.environ.get('QUERY_STATUS_CHECK_INTERVAL', 30))

#
class Aggregation:
    #_aoi: List[str]

    """
    A representation of a Query Aggregation.
    
    :param aoi: A definition of areas of interest, part of a query.
    :type aoi:  List[str]
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
                 aoi: List[str] = None
                ):
        self._aoi = aoi
    
    #       
    def get_aoi(self):
        return self._aoi

    #
    def set_aoi(self, aoi):
        self._aoi = common.check_list(aoi)
        
    #    
    def del_aoi(self): 
        del self._aoi

    #    
    aoi = property(get_aoi, set_aoi, del_aoi)
        
    #
    def from_dict(aggregation_dict: Any):

        """
        Create an Aggregation object from a dictionary.
        
        :param aggregation_dict:    A dictionary that contains the keys of an Aggregation.
        :type aggregation_dict:     Any             
        :rtype:                     ibmpairs.query.Aggregation
        :raises Exception:          if not a dictionary.
        """
        
        aoi = None
        
        common.check_dict(aggregation_dict)
        if "aoi" in aggregation_dict:
            if aggregation_dict.get("aoi") is not None:
                aoi = common.from_list(aggregation_dict.get("aoi"), common.check_str)
        return Aggregation(aoi = aoi)

    #
    def to_dict(self):

        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        aggregation_dict: dict = {}
        if self._aoi is not None:
            aggregation_dict["aoi"] = common.from_list(self._aoi, common.check_str)
        return aggregation_dict
    
    #
    def from_json(aggregation_json: Any):
        
        """
        Create an Aggregation object from json (dictonary or str).
        
        :param aggregation_dict:        A json dictionary that contains the keys of an Aggregation or a string representation of a json dictionary.
        :type aggregation_dict:         Any             
        :rtype:                         ibmpairs.query.Aggregation
        :raises Exception:              if not a dictionary or a string.
        """
        

        if isinstance(aggregation_json, dict):
            aggregation = Aggregation.from_dict(aggregation_json)
        elif isinstance(aggregation_json, str):
            aggregation_dict = json.loads(aggregation_json)
            aggregation = Aggregation.from_dict(aggregation_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(aggregation_json), "aggregation_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return aggregation

    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """

        return json.dumps(self.to_dict())

#
class Dimension:
    #_name: str
    #_value: str
    #_operator: str
    #_options: List[str]
    
    """
    A representation of a Query Dimension.
    
    :param name:     A dimension name.
    :type name:      str
    :param value:    A dimension value.
    :type value:     str
    :param operator: A dimension operator.
    :type operator:  str
    :param name:     A list of options.
    :type name:      List[str]
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
                 name: str          = None, 
                 value: str         = None, 
                 operator: str      = None, 
                 options: List[str] = None
                ):
        self._name     = name
        self._value    = value
        self._operator = operator
        self._options  = options

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
    def get_value(self):
        return self._value

    #
    def set_value(self, value):
        self._value = common.check_str(value)
    
    #    
    def del_value(self): 
        del self._value

    #    
    value = property(get_value, set_value, del_value)

    #    
    def get_operator(self):
        return self._operator

    #
    def set_operator(self, operator):
        self._operator = common.check_str(operator)

    #    
    def del_operator(self): 
        del self._operator

    #    
    operator = property(get_operator, set_operator, del_operator)

    #    
    def get_options(self):
        return self._options

    #
    def set_options(self, options):
        self._options = common.check_list(options)
        
    #    
    def del_options(self): 
        del self._options

    #    
    options = property(get_options, set_options, del_options)
       
    # 
    def from_dict(dimension_dict: Any):
        
        """
        Create a Dimension object from a dictionary.
        
        :param dimension_dict:    A dictionary that contains the keys of a Dimension.
        :type dimension_dict:     Any             
        :rtype:                   ibmpairs.query.Dimension
        :raises Exception:        if not a dictionary.
        """
      
        name     = None
        value    = None
        operator = None
        options  = None
        
        common.check_dict(dimension_dict)
        if "name" in dimension_dict:
            if dimension_dict.get("name") is not None:
                name = common.check_str(dimension_dict.get("name"))
        if "value" in dimension_dict:
            if dimension_dict.get("value") is not None:
                value = common.check_str(dimension_dict.get("value"))
        if "operator" in dimension_dict:
            if dimension_dict.get("operator") is not None:
                operator = common.check_str(dimension_dict.get("operator"))
        if "options" in dimension_dict:
            if dimension_dict.get("options") is not None:
                options = common.from_list(dimension_dict.get("options"), common.check_str)
        return Dimension(name     = name, 
                         value    = value, 
                         operator = operator, 
                         options  = options
                        )

    #
    def to_dict(self):

        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        dimension_dict: dict = {}
        if self._name is not None:
            dimension_dict["name"] = self._name
        if self._value is not None:
            dimension_dict["value"] = self._value
        if self._operator is not None:
            dimension_dict["operator"] = self._operator
        if self._options is not None:
            dimension_dict["options"] = common.from_list(self._options, common.check_str)
        return dimension_dict
    
    #
    def from_json(dimension_json: Any):
        
        """
        Create a Dimension object from json (dictonary or str).
        
        :param dimension_dict:        A json dictionary that contains the keys of a Dimension or a string representation of a json dictionary.
        :type dimension_dict:         Any             
        :rtype:                       ibmpairs.query.Dimension
        :raises Exception:            if not a dictionary or a string.
        """
    
        if isinstance(dimension_json, dict):
            dimension = Dimension.from_dict(dimension_json)
        elif isinstance(dimension_json, str):
            dimension_dict = json.loads(dimension_json)
            dimension = Dimension.from_dict(dimension_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(dimension_json), "dimension_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return dimension

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Filter:
    #_value: str
    #_operator: str
    #_expression: str
    
    """
    A representation of a Query Filter.
    
    :param value:      A filter value.
    :type value:       str
    :param operator:   A filter operator.
    :type operator:    str
    :param expression: An expression, used instead of value, operator.
    :type expression:  str
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
                 value: str      = None, 
                 operator: str   = None,
                 expression: str = None
                ):
        self._value      = value
        self._operator   = operator
        self._expression = expression

    #        
    def get_value(self):
        return self._value

    #
    def set_value(self, value):
        self._value = common.check_str(value)
        
    #
    def del_value(self): 
        del self._value

    #
    value = property(get_value, set_value, del_value)
    
    #
    def get_operator(self):
        return self._operator

    #
    def set_operator(self, operator):
        self._operator = common.check_str(operator)
        
    #
    def del_operator(self): 
        del self._operator

    #
    operator = property(get_operator, set_operator, del_operator)
    
    #
    def get_expression(self):
      return self._expression

    #
    def set_expression(self, expression):
      self._expression = common.check_str(expression)
      
    #
    def del_expression(self): 
      del self._expression

    #
    expression = property(get_expression, set_expression, del_expression)
    
    #
    def from_dict(filter_dict: Any):
      
        """
        Create a Filter object from a dictionary.
        
        :param filter_dict:    A dictionary that contains the keys of a Filter.
        :type filter_dict:     Any             
        :rtype:                ibmpairs.query.Filter
        :raises Exception:     if not a dictionary.
        """
        
        value      = None
        operator   = None
        expression = None
        
        common.check_dict(filter_dict)
        if "value" in filter_dict:
            if filter_dict.get("value") is not None:
                value = common.check_str(filter_dict.get("value"))
        if "operator" in filter_dict:
            if filter_dict.get("operator") is not None:
                operator = common.check_str(filter_dict.get("operator"))
        if "expression" in filter_dict:
            if filter_dict.get("expression") is not None:
                expression = common.check_str(filter_dict.get("expression"))
        return Filter(value      = value, 
                      operator   = operator,
                      expression = expression
                     )
    
    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        filter_dict: dict = {}
        if self._value is not None:
            filter_dict["value"] = self._value
        if self._operator is not None:
            filter_dict["operator"] = self._operator
        if self._expression is not None:
            filter_dict["expression"] = self._expression
        return filter_dict
    
    #
    def from_json(filter_json: Any):
        
        """
        Create a Filter object from json (dictonary or str).
        
        :param filter_dict:        A json dictionary that contains the keys of a Filter or a string representation of a json dictionary.
        :type filter_dict:         Any             
        :rtype:                    ibmpairs.query.Filter
        :raises Exception:         if not a dictionary or a string.
        """

        if isinstance(filter_json, dict):
            filter_ = Filter.from_dict(filter_json)
        elif isinstance(filter_json, str):
            filter_dict = json.loads(filter_json)
            filter_ = Filter.from_dict(filter_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(filter_json), "filter_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return filter_

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Interval:
    #_snapshot: str
    #_end: str
    #_start: str
    
    """
    A representation of a Query Interval.
    
    :param snapshot: An interval snapshot.
    :type snapshot:  str
    :param end:      An end date.
    :type end:       str
    :param start:    A start date.
    :type start:     str
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
                 snapshot: str = None, 
                 end: str      = None, 
                 start: str    = None
                ):
        self._snapshot = snapshot
        self._end      = end
        self._start    = start
    
    #
    def get_snapshot(self):
        return self._snapshot

    #
    def set_snapshot(self, snapshot):
        self._snapshot = common.check_str(snapshot)
        
    #
    def del_snapshot(self): 
        del self._snapshot

    #
    snapshot = property(get_snapshot, set_snapshot, del_snapshot)
    
    #
    def get_end(self):
        return self._end

    #
    def set_end(self, end):
        self._end = common.check_str(end)
        
    #
    def del_end(self): 
        del self._end

    #
    end = property(get_end, set_end, del_end)
        
    #
    def get_start(self):
        return self._start

    #
    def set_start(self, start):
        self._start = common.check_str(start)
        
    #
    def del_start(self): 
        del self._start

    #
    start = property(get_start, set_start, del_start)

    #
    def from_dict(interval_dict: Any):
        
        """
        Create an Interval object from a dictionary.
        
        :param interval_dict:    A dictionary that contains the keys of an Interval.
        :type interval_dict:     Any             
        :rtype:                  ibmpairs.query.Interval
        :raises Exception:       if not a dictionary.
        """
        
        snapshot = None
        end      = None
        start    = None
        
        common.check_dict(interval_dict)
        if "snapshot" in interval_dict:
            if interval_dict.get("snapshot") is not None:
                snapshot = common.check_str(interval_dict.get("snapshot"))
        if "end" in interval_dict:
            if interval_dict.get("end") is not None:
                end = common.check_str(interval_dict.get("end"))
        if "start" in interval_dict:
            if interval_dict.get("start") is not None:
                start = common.check_str(interval_dict.get("start"))
        return Interval(snapshot = snapshot, 
                        end      = end, 
                        start    = start
                       )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.            
        :rtype:                     dict
        """
        
        interval_dict: dict = {}
        if self._snapshot is not None:
            interval_dict["snapshot"] = self._snapshot
        if self._end is not None:
            interval_dict["end"] = self._end
        if self._start is not None:
            interval_dict["start"] = self._start
        return interval_dict
       
    #
    def from_json(interval_json: Any):

        """
        Create an Interval object from json (dictonary or str).
        
        :param interval_dict:        A json dictionary that contains the keys of an Interval or a string representation of a json dictionary.
        :type interval_dict:         Any             
        :rtype:                      ibmpairs.query.Interval
        :raises Exception:           if not a dictionary or a string.
        """

        if isinstance(interval_json, dict):
            interval = Interval.from_dict(interval_json)
        elif isinstance(interval_json, str):
            interval_dict = json.loads(interval_json)
            interval = Interval.from_dict(interval_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(interval_json), "interval_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return interval

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Temporal:
    #_intervals: List[Interval]
    
    """
    A representation of a Query Temporal.
    
    :param intervals: A list of temporal intervals.
    :type intervals:  List[ibmpairs.query.Interval]
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
                 intervals: List[Interval] = None
                ):
        self._intervals = intervals
        
    #
    def get_intervals(self):
        return self._intervals

    #
    def set_intervals(self, intervals):
        self._intervals = common.check_list(intervals)
        
    #
    def del_intervals(self): 
        del self._intervals

    #
    intervals = property(get_intervals, set_intervals, del_intervals)
        
    #    
    def from_dict(temporal_dict: Any):

        """
        Create a Temporal object from a dictionary.
        
        :param temporal_dict:    A dictionary that contains the keys of a Temporal.
        :type temporal_dict:     Any             
        :rtype:                  ibmpairs.query.Temporal
        :raises Exception:       if not a dictionary.
        """
        
        intervals = None
        
        common.check_dict(temporal_dict)
        if "intervals" in temporal_dict:
            if temporal_dict.get("intervals") is not None:
                intervals = common.from_list(temporal_dict.get("intervals"), Interval.from_dict)
        return Temporal(intervals = intervals)

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        temporal_dict: dict = {}
        if self._intervals is not None:
            temporal_dict["intervals"] = common.from_list(self._intervals, lambda item: common.class_to_dict(item, Interval))
        return temporal_dict
    
    #
    def from_json(temporal_json: Any):
    
        """
        Create a Temporal object from json (dictonary or str).
        
        :param temporal_dict:        A json dictionary that contains the keys of a Temporal or a string representation of a json dictionary.
        :type temporal_dict:         Any             
        :rtype:                      ibmpairs.query.Temporal
        :raises Exception:           if not a dictionary or a string.
        """

        if isinstance(temporal_json, dict):
            temporal = Temporal.from_dict(temporal_json)
        elif isinstance(temporal_json, str):
            temporal_dict = json.loads(temporal_json)
            temporal = Temporal.from_dict(temporal_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(temporal_json), "temporal_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return temporal

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Layer:
    #_id: str
    #_type: str
    #_temporal: Temporal
    #_alias: str
    #_filter_only: bool
    #_aggregation: str
    #_filter: Filter
    #_dimensions: List[Dimension]
    #_expression: str
    #_output: bool
    
    """
    A representation of a Query Layer.
    
    :param id:          A layer id.
    :type id:           str
    :param type:        A layer type.
    :type type:         str
    :param temporal:    A temporal definition of intervals.
    :type temporal:     ibmpairs.query.Temporal
    :param alias:       An alias name.
    :type alias:        str
    :param filter_only: Filter only.
    :type filter_only:  bool
    :param aggregation: An aggregation definition.
    :type aggregation:  str
    :param filter:      A filter definition.
    :type filter:       ibmpairs.query.Filter
    :param dimensions:  A list of dimensions.
    :type dimensions:   List[ibmpairs.query.Dimension]
    :param expression:  An expression to be applied.
    :type expression:   str
    :param output:      Output.
    :type output:       bool
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
                 id: str = None, 
                 type: str = None, 
                 temporal: Temporal = None, 
                 alias: str = None, 
                 filter_only: bool = None, 
                 aggregation: str = None, 
                 filter: Filter = None, 
                 dimensions: List[Dimension] = None, 
                 expression: str = None, 
                 output: bool = None
                ):
        self._id          = id
        self._type        = type
        self._temporal    = temporal
        self._alias       = alias
        self._filter_only = filter_only
        self._aggregation = aggregation
        self._filter      = filter
        self._dimensions  = dimensions
        self._expression  = expression
        self._output      = output

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
    def get_temporal(self):
        return self._temporal

    #
    def set_temporal(self, temporal):
        self._temporal = common.check_class(temporal, Temporal)
        
    #
    def del_temporal(self): 
        del self._temporal

    #
    temporal = property(get_temporal, set_temporal, del_temporal)

    #
    def get_alias(self):
        return self._alias

    #
    def set_alias(self, alias):
        self._alias = common.check_str(alias)
     
    #
    def del_alias(self): 
        del self._alias

    #
    alias = property(get_alias, set_alias, del_alias)
    
    #   
    def get_filter_only(self):
        return self._filter_only

    #
    def set_filter_only(self, filter_only):
        self._filter_only = common.check_bool(filter_only)
        
    #
    def del_filter_only(self): 
        del self._filter_only

    #
    filter_only = property(get_filter_only, set_filter_only, del_filter_only)
     
    #   
    def get_aggregation(self):
        return self._aggregation

    #
    def set_aggregation(self, aggregation):
        self._aggregation = common.check_str(aggregation)
        
    #
    def del_aggregation(self): 
        del self._aggregation

    #
    aggregation = property(get_aggregation, set_aggregation, del_aggregation)
    
    #
    def get_filter(self):
        return self._filter
    
    #
    def set_filter(self, filter):
        self._filter = common.check_class(filter, Filter)  
        
    #
    def del_filter(self): 
        del self._filter

    #
    filter = property(get_filter, set_filter, del_filter)

    #
    def get_dimensions(self):
        return self._dimensions

    #
    def set_dimensions(self, dimensions):
        self._dimensions = common.check_list(dimensions) 
    
    #
    def del_dimensions(self): 
        del self._dimensions

    #
    dimensions = property(get_dimensions, set_dimensions, del_dimensions)

    #
    def get_expression(self):
        return self._expression

    #
    def set_expression(self, expression):
        self._expression = common.check_str(expression)
        
    #
    def del_expression(self): 
        del self._expression

    #
    expression = property(get_expression, set_expression, del_expression)

    #        
    def get_output(self):
        return self._output

    #
    def set_output(self, output):
        self._output = common.check_bool(output)

    #
    def del_output(self): 
        del self._output

    #
    output = property(get_output, set_output, del_output)

    #
    def from_dict(layer_dict: Any):

        """
        Create a Layer object from a dictionary.
        
        :param layer_dict:    A dictionary that contains the keys of a Layer.
        :type layer_dict:     Any             
        :rtype:               ibmpairs.query.Layer
        :raises Exception:    if not a dictionary.
        """
        
        id          = None
        type        = None
        temporal    = None
        alias       = None
        filter_only = None
        aggregation = None
        filter      = None
        dimensions  = None
        expression  = None
        output      = None
        
        common.check_dict(layer_dict)
        if "id" in layer_dict:
            if layer_dict.get("id") is not None:
                id = common.check_str(layer_dict.get("id"))
        if "type" in layer_dict:
            if layer_dict.get("type") is not None:
                type = common.check_str(layer_dict.get("type"))
        if "temporal" in layer_dict:
            if layer_dict.get("temporal") is not None:
                temporal = Temporal.from_dict(layer_dict.get("temporal"))
        if "alias" in layer_dict:
            if layer_dict.get("alias") is not None:
                alias = common.check_str(layer_dict.get("alias"))
        if "filterOnly" in layer_dict:
            if layer_dict.get("filterOnly") is not None:
                filter_only = common.check_bool(layer_dict.get("filterOnly"))
        elif "filter_only" in layer_dict:
            if layer_dict.get("filter_only") is not None:
                filter_only = common.check_bool(layer_dict.get("filter_only"))
        if "aggregation" in layer_dict:
            if layer_dict.get("aggregation") is not None:
                aggregation = common.check_str(layer_dict.get("aggregation"))
        if "filter" in layer_dict:
            if layer_dict.get("filter") is not None:
                filter = Filter.from_dict(layer_dict.get("filter"))
        if "dimensions" in layer_dict:
            if layer_dict.get("dimensions") is not None:
                dimensions = common.from_list(layer_dict.get("dimensions"), Dimension.from_dict)
        if "expression" in layer_dict:
            if layer_dict.get("expression") is not None:
                expression = common.check_str(layer_dict.get("expression"))
        if "output" in layer_dict:
            if layer_dict.get("output") is not None:
                output = common.check_bool(layer_dict.get("output"))
        return Layer(id          = id, 
                     type        = type, 
                     temporal    = temporal, 
                     alias       = alias, 
                     filter_only = filter_only, 
                     aggregation = aggregation, 
                     filter      = filter, 
                     dimensions  = dimensions, 
                     expression  = expression, 
                     output      = output
                    )

    #
    def to_dict(self):
     
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        layer_dict: dict = {}
        if self._id is not None:
            layer_dict["id"] = self._id
        if self._type is not None:
            layer_dict["type"] = self._type
        if self._temporal is not None:
            layer_dict["temporal"] = common.class_to_dict(self._temporal, Temporal)
        if self._alias is not None:
            layer_dict["alias"] = self._alias
        if self._filter_only is not None:
            layer_dict["filter_only"] = self._filter_only
        if self._aggregation is not None:
            layer_dict["aggregation"] = self._aggregation
        if self._filter is not None:
            layer_dict["filter"] = common.class_to_dict(self._filter, Filter)
        if self._dimensions is not None:
            layer_dict["dimensions"] = common.from_list(self._dimensions, lambda item: common.class_to_dict(item, Dimension))
        if self._expression is not None:
            layer_dict["expression"] = self._expression
        if self._output is not None:
            layer_dict["output"] = self._output
        return layer_dict
        
    #
    def to_dict_layer_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation.
                    
        :rtype:                     dict
        """
      
        layer_dict: dict = {}
        if self._id is not None:
            layer_dict["id"] = self._id
        if self._type is not None:
            layer_dict["type"] = self._type
        if self._temporal is not None:
            layer_dict["temporal"] = common.class_to_dict(self._temporal, Temporal)
        if self._alias is not None:
            layer_dict["alias"] = self._alias
        if self._filter_only is not None:
            layer_dict["filterOnly"] = self._filter_only
        if self._aggregation is not None:
            layer_dict["aggregation"] = self._aggregation
        if self._filter is not None:
            layer_dict["filter"] = common.class_to_dict(self._filter, Filter)
        if self._dimensions is not None:
            layer_dict["dimensions"] = common.from_list(self._dimensions, lambda item: common.class_to_dict(item, Dimension))
        if self._expression is not None:
            layer_dict["expression"] = self._expression
        if self._output is not None:
            layer_dict["output"] = self._output
        return layer_dict
    
    #
    def from_json(layer_json: Any):
        
        """
        Create a Layer object from json (dictonary or str).
        
        :param layer_dict:          A json dictionary that contains the keys of a Layer or a string representation of a json dictionary.
        :type layer_dict:           Any             
        :rtype:                     ibmpairs.query.Layer
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(layer_json, dict):
            layer = Layer.from_dict(layer_json)
        elif isinstance(layer_json, str):
            layer_dict = json.loads(layer_json)
            layer = Layer.from_dict(layer_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(layer_json), "layer_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return layer

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
        
    #
    def to_json_layer_post(self):
        
        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict_layer_post())

#
class Notification:
    #_type: str
    #_host: str
    #_queue: str
    
    """
    A representation of a Query Notification.
    
    :param type:  A type value.
    :type type:   str
    :param host:  A host of the holding GeoServer.
    :type host:   str
    :param queue: A queue name.
    :type queue:  str
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
                 type: str  = None, 
                 host: str  = None, 
                 queue: str = None
                ):
        self._type  = type
        self._host  = host
        self._queue = queue
        
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
    def get_host(self):
        return self._host

    #
    def set_host(self, host):
        self._host = common.check_str(host)
    
    #
    def del_host(self): 
        del self._host

    #
    host = property(get_host, set_host, del_host)
        
    #    
    def get_queue(self):
        return self._queue

    #
    def set_queue(self, queue):
        self._queue = common.check_str(queue)
        
    #
    def del_queue(self): 
        del self._queue

    #
    queue = property(get_queue, set_queue, del_queue)
        
    #
    def from_dict(notification_dict: Any):

        """
        Create a Notification object from a dictionary.
        
        :param notification_dict:    A dictionary that contains the keys of a Notification.
        :type notification_dict:     Any             
        :rtype:                      ibmpairs.query.Notification
        :raises Exception:           if not a dictionary.
        """
        
        type  = None
        host  = None
        queue = None
        
        common.check_dict(notification_dict)
        if "type" in notification_dict:
            if notification_dict.get("type") is not None:
                type = common.check_str(notification_dict.get("type"))
        if "host" in notification_dict:
            if notification_dict.get("host") is not None:
                host = common.check_str(notification_dict.get("host"))
        if "queue" in notification_dict:
            if notification_dict.get("queue") is not None:
                queue = common.check_str(notification_dict.get("queue"))
        return Notification(type  = type, 
                            host  = host, 
                            queue = queue
                           )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
      
        notification_dict: dict = {}
        if self._type is not None:
            notification_dict["type"] = self._type
        if self._host is not None:
            notification_dict["host"] = self._host
        if self._queue is not None:
            notification_dict["queue"] = self._queue
        return notification_dict
    
    #
    def from_json(notification_json: Any):
        
        """
        Create a Notification object from json (dictonary or str).
        
        :param notification_dict:        A json dictionary that contains the keys of a Notification or a string representation of a json dictionary.
        :type notification_dict:         Any             
        :rtype:                          ibmpairs.query.Notification
        :raises Exception:               if not a dictionary or a string.
        """

        if isinstance(notification_json, dict):
            notification = Notification.from_dict(notification_json)
        elif isinstance(notification_json, str):
            notification_dict = json.loads(notification_json)
            notification = Notification.from_dict(notification_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(notification_json), "notification_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return notification

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.   
                 
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Polygon:
    #_wkt: str
    
    """
    A representation of a Query Polygon.
    
    :param wkt:  A Well Known Text (wkt) string.
    :type wkt:   str
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
                 wkt: str = None
                ):
        self._wkt  = wkt
        
    #    
    def get_wkt(self):
        return self._wkt

    #
    def set_wkt(self, wkt):
        self._wkt = common.check_str(wkt)
    
    #
    def del_wkt(self): 
        del self._wkt

    #
    wkt = property(get_wkt, set_wkt, del_wkt)
        
    #
    def from_dict(polygon_dict: Any):

        """
        Create a Polygon object from a dictionary.
        
        :param polygon_dict:    A dictionary that contains the keys of a Polygon.
        :type polygon_dict:     Any             
        :rtype:                 ibmpairs.query.Polygon
        :raises Exception:      if not a dictionary.
        """
        
        wkt  = None
        
        common.check_dict(polygon_dict)
        if "wkt" in polygon_dict:
            if polygon_dict.get("wkt") is not None:
                wkt = common.check_str(polygon_dict.get("wkt"))
        return Polygon(wkt = wkt)

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
        
        polygon_dict: dict = {}
        if self._wkt is not None:
            polygon_dict["wkt"] = self._wkt
        return polygon_dict
    
    #
    def from_json(polygon_json: Any):

        """
        Create a Polygon object from json (dictonary or str).
        
        :param polygon_dict:        A json dictionary that contains the keys of a Polygon or a string representation of a json dictionary.
        :type polygon_dict:         Any             
        :rtype:                     ibmpairs.query.Polygon
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(polygon_json, dict):
            polygon = Polygon.from_dict(polygon_json)
        elif isinstance(polygon_json, str):
            polygon_dict = json.loads(polygon_json)
            polygon = Polygon.from_dict(polygon_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(polygon_json), "polygon_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return polygon

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Spatial:
    #_type: str
    #_aoi: str
    #_polygon: Polygon
    #_coordinates: List[float]
    #_aggregation: Aggregation
    
    """
    A representation of a Query Spatial.
    
    :param type:         Spatial type.
    :type type:          str
    :param aoi:          Area of Interest.
    :type aoi:           str
    :param polygon:      A Query polygon definition.
    :type polygon:       ibmpairs.query.Polygon
    :param coordinates:  A list of coordinates.
    :type coordinates:   list[float]
    :param aggregation:  A spatial aggregation definition.
    :type aggregation:   ibmpairs.query.aggregation
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
                 type: str                = None, 
                 aoi: str                 = None, 
                 polygon: Polygon         = None,
                 coordinates: List[float] = None, 
                 aggregation: Aggregation = None
                ):
        self._type        = type
        self._aoi         = aoi
        self._polygon     = polygon
        self._coordinates = coordinates
        self._aggregation = aggregation
        
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
    def get_aoi(self):
        return self._aoi

    #
    def set_aoi(self, aoi):
        self._aoi = common.check_str(aoi)
        
    #
    def del_aoi(self): 
        del self._aoi

    #
    aoi = property(get_aoi, set_aoi, del_aoi) 
    
    #
    def get_polygon(self):
      return self._polygon

    #
    def set_polygon(self, polygon):
      self._polygon = common.check_class(polygon, Polygon)
      
    #
    def del_polygon(self): 
      del self._polygon

    #
    polygon = property(get_polygon, set_polygon, del_polygon) 
    
    #    
    def get_coordinates(self):
        return self._coordinates

    #
    def set_coordinates(self, coordinates):
        self._coordinates = common.check_list(coordinates)
        
    #
    def del_coordinates(self): 
        del self._coordinates

    #
    coordinates = property(get_coordinates, set_coordinates, del_coordinates) 
        
    #    
    def get_aggregation(self):
        return self._aggregation

    #
    def set_aggregation(self, aggregation):
        self._aggregation = common.check_class(aggregation, Aggregation)
        
    #
    def del_aggregation(self): 
        del self._aggregation

    #
    aggregation = property(get_aggregation, set_aggregation, del_aggregation)
        
    #
    def from_dict(spatial_dict: Any):

        """
        Create a Spatial object from a dictionary.
        
        :param spatial_dict:    A dictionary that contains the keys of a Spatial.
        :type spatial_dict:     Any             
        :rtype:                 ibmpairs.query.Spatial
        :raises Exception:      if not a dictionary.
        """
        
        type        = None
        aoi         = None
        polygon     = None
        coordinates = None
        aggregation = None
        
        common.check_dict(spatial_dict)
        if "type" in spatial_dict:
            if spatial_dict.get("type") is not None:
                type = common.check_str(spatial_dict.get("type"))
        if "aoi" in spatial_dict:
            if spatial_dict.get("aoi") is not None:
                aoi = common.check_str(spatial_dict.get("aoi"))
        if "polygon" in spatial_dict:
            if spatial_dict.get("polygon") is not None:
                polygon = Polygon.from_dict(spatial_dict.get("polygon"))
        if "coordinates" in spatial_dict:
            if spatial_dict.get("coordinates") is not None:
                coordinates = common.from_list(spatial_dict.get("coordinates"), common.check_float)
        if "aggregation" in spatial_dict:
            if spatial_dict.get("aggregation") is not None:
                aggregation = Aggregation.from_dict(spatial_dict.get("aggregation"))
        return Spatial(type        = type, 
                       aoi         = aoi, 
                       polygon     = polygon,
                       coordinates = coordinates, 
                       aggregation = aggregation
                      )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
      
        spatial_dict: dict = {}
        if self._type is not None:
            spatial_dict["type"] = self._type
        if self._aoi is not None:
            spatial_dict["aoi"] = self._aoi
        if self._polygon is not None:
          spatial_dict["polygon"] = common.class_to_dict(self._polygon, Polygon)
        if self._coordinates is not None:
            spatial_dict["coordinates"] = common.from_list(self._coordinates, common.check_float)
        if self._aggregation is not None:
            spatial_dict["aggregation"] = common.class_to_dict(self._aggregation, Aggregation)
        return spatial_dict
        
    #
    def from_json(spatial_json: Any):
        
        """
        Create a Spatial object from json (dictonary or str).
        
        :param spatial_dict:        A json dictionary that contains the keys of a Spatial or a string representation of a json dictionary.
        :type spatial_dict:         Any             
        :rtype:                     ibmpairs.query.Spatial
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(spatial_json, dict):
            spatial = Spatial.from_dict(spatial_json)
        elif isinstance(spatial_json, str):
            spatial_dict = json.loads(spatial_json)
            spatial = Spatial.from_dict(spatial_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(spatial_json), "spatial_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return spatial

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Upload:
    #_provider: str
    #_endpoint: str
    #_bucket: str
    #_token: str
    
    """
    A representation of a Query Upload.
    
    :param provider:  A provider ('ibm' or 'aws').
    :type provider:   str
    :param endpoint:  A bucket endpoint.
    :type endpoint:   str
    :param bucket:    A bucket name.
    :type bucket:     str
    :param token:     An access token.
    :type token:      str
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
                 provider: str = None, 
                 endpoint: str = None, 
                 bucket: str   = None, 
                 token: str    = None
                ):
        self._provider = provider
        self._endpoint = endpoint
        self._bucket   = bucket
        self._token    = token

    #
    def get_provider(self):
        return self._provider

    #
    def set_provider(self, provider):
        self._provider = common.check_str(provider)
        
    #
    def del_provider(self): 
        del self._provider

    #
    provider = property(get_provider, set_provider, del_provider)
        
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
    def get_token(self):
        return self._token
    
    #
    def set_token(self, token):
        self._token = common.check_str(token)
        
    #
    def del_token(self): 
        del self._token
        
    #
    token = property(get_token, set_token, del_token)
        
    #    
    def from_dict(upload_dict: Any):

        """
        Create an Upload object from a dictionary.
        
        :param upload_dict:    A dictionary that contains the keys of an Upload.
        :type upload_dict:     Any             
        :rtype:                ibmpairs.query.Upload
        :raises Exception:     if not a dictionary.
        """
        
        provider = None
        endpoint = None
        bucket   = None
        token    = None
        
        common.check_dict(upload_dict)
        if "provider" in upload_dict:
            if upload_dict.get("provider") is not None:
                provider = common.check_str(upload_dict.get("provider"))
        if "endpoint" in upload_dict:
            if upload_dict.get("endpoint") is not None:
                endpoint = common.check_str(upload_dict.get("endpoint"))
        if "bucket" in upload_dict:
            if upload_dict.get("bucket") is not None:
                bucket = common.check_str(upload_dict.get("bucket"))
        if "token" in upload_dict:
            if upload_dict.get("token") is not None:
                token = common.check_str(upload_dict.get("token"))
        return Upload(provider = provider, 
                      endpoint = endpoint, 
                      bucket   = bucket, 
                      token    = token
                     )

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
      
        upload_dict: dict = {}
        if self._provider is not None:
            upload_dict["provider"] = self._provider
        if self._endpoint is not None:
            upload_dict["endpoint"] = self._endpoint
        if self._bucket is not None:
            upload_dict["bucket"] = self._bucket
        if self._token is not None:
            upload_dict["token"] = self._token
        return upload_dict

    #
    def from_json(upload_json: Any):

        """
        Create an Upload object from json (dictonary or str).
        
        :param upload_dict:         A json dictionary that contains the keys of an Upload or a string representation of a json dictionary.
        :type upload_dict:          Any             
        :rtype:                     ibmpairs.query.Upload
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
class QueryResponseData:
    #_layer_id: int
    #_layer_name: str
    #_dataset: str
    #_timestamp: int
    #_longitude: float
    #_latitude: float
    #_region: str
    #_value: str
    #_unit: str
    #_pty: str
    #_aggregation: str
    #_alias: str
    
    """
    A representation of a the data returned by a response to a Query request.
    
    :param layer_id:    A query.Layer ID.
    :type layer_id:     int
    :param layer_name:  A query.Layer name.
    :type layer_name:   str
    :param dataset:     A Data Set ID.
    :type dataset:      str
    :param timestamp:   A timestamp.
    :type timestamp:    int
    :param longitude:   Longitude.
    :type longitude:    float
    :param latitude:    Latitude.
    :type latitude:     float
    :param region:      Region.
    :type region:       str
    :param value:       Value.
    :type value:        str
    :param unit:        Unit of measurement.
    :type unit:         str
    :param pty:         Property.
    :type pty:          str
    :param aggregation: Aggregation.
    :type aggregation:  str
    :param alias:       Alias.
    :type alias:        str
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
                 layer_id: int    = None, 
                 layer_name: str  = None, 
                 dataset: str     = None, 
                 timestamp: int   = None, 
                 longitude: float = None, 
                 latitude: float  = None, 
                 region: str      = None, 
                 value: str       = None, 
                 unit: str        = None, 
                 pty: str         = None, 
                 aggregation: str = None,
                 alias: str       = None
                ):
        self._layer_id    = layer_id
        self._layer_name  = layer_name
        self._dataset     = dataset
        self._timestamp   = timestamp
        self._longitude   = longitude
        self._latitude    = latitude
        self._region      = region
        self._value       = value
        self._unit        = unit
        self._pty         = pty
        self._aggregation = aggregation
        self._alias       = alias
    
    #
    def get_layer_id(self):
        return self._layer_id

    #
    def set_layer_id(self, layer_id):
        self._layer_id = common.check_int(layer_id)

    #    
    def del_layer_id(self): 
        del self._layer_id

    #
    layer_id = property(get_layer_id, set_layer_id, del_layer_id) 

    #
    def get_layer_name(self):
        return self._layer_name

    #
    def set_layer_name(self, layer_name):
        self._layer_name = common.check_str(layer_name)

    #    
    def del_layer_name(self): 
        del self._layer_name

    #
    layer_name = property(get_layer_name, set_layer_name, del_layer_name)
    
    #
    def get_dataset(self):
        return self._dataset

    #
    def set_dataset(self, dataset):
        self._dataset = common.check_str(dataset)

    #    
    def del_dataset(self): 
        del self._dataset

    #
    dataset = property(get_dataset, set_dataset, del_dataset) 
    
    #
    def get_timestamp(self):
        return self._timestamp

    #
    def set_timestamp(self, timestamp):
        self._timestamp = common.check_int(timestamp)

    #    
    def del_timestamp(self): 
        del self._timestamp

    #
    timestamp = property(get_timestamp, set_timestamp, del_timestamp) 
    
    #
    def get_longitude(self):
        return self._longitude

    #
    def set_longitude(self, longitude):
        self._longitude = common.check_float(longitude)

    #    
    def del_longitude(self): 
        del self._longitude

    #
    longitude = property(get_longitude, set_longitude, del_longitude)
    
    #
    def get_latitude(self):
        return self._latitude

    #
    def set_latitude(self, latitude):
        self._latitude = common.check_float(latitude)

    #    
    def del_latitude(self): 
        del self._latitude

    #
    latitude = property(get_latitude, set_latitude, del_latitude) 
    
    #
    def get_region(self):
        return self._region

    #
    def set_region(self, region):
        self._region = common.check_str(region)

    #    
    def del_region(self): 
        del self._region

    #
    region = property(get_region, set_region, del_region)
    
    #
    def get_value(self):
        return self._value

    #
    def set_value(self, value):
        self._value = common.check_str(value)

    #    
    def del_value(self): 
        del self._value

    #
    value = property(get_value, set_value, del_value)
    
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
    def get_pty(self):
        return self._pty

    #
    def set_pty(self, pty):
        self._pty = common.check_str(pty)

    #    
    def del_pty(self): 
        del self._pty

    #
    pty = property(get_pty, set_pty, del_pty)
    
    #
    def get_aggregation(self):
        return self._aggregation

    #
    def set_aggregation(self, aggregation):
        self._aggregation = common.check_str(aggregation)

    #    
    def del_aggregation(self): 
        del self._aggregation

    #
    aggregation = property(get_aggregation, set_aggregation, del_aggregation)
    
    #
    def get_alias(self):
      return self._alias

    #
    def set_alias(self, alias):
      self._alias = common.check_str(alias)

    #    
    def del_alias(self): 
      del self._alias

    #
    alias = property(get_alias, set_alias, del_alias)

    # 
    def from_dict(query_response_data_dict: Any):

        """
        Create a QueryResponseData object from a dictionary.
        
        :param query_response_data_dict:    A dictionary that contains the keys of a QueryResponseData.
        :type query_response_data_dict:     Any             
        :rtype:                             ibmpairs.query.QueryResponseData
        :raises Exception:                  if not a dictionary.
        """
        
        layer_id    = None
        layer_name  = None
        dataset     = None
        timestamp   = None
        longitude   = None
        latitude    = None
        region      = None
        value       = None
        unit        = None
        pty         = None
        aggregation = None
        alias       = None
        
        common.check_dict(query_response_data_dict)
        if "layerId" in query_response_data_dict:
            if query_response_data_dict.get("layerId") is not None:
                layer_id = common.check_int(query_response_data_dict.get("layerId"))
        elif "layer_id" in query_response_data_dict:
            if query_response_data_dict.get("layer_id") is not None:
                layer_id = common.check_int(query_response_data_dict.get("layer_id"))
        if "layerName" in query_response_data_dict:
            if query_response_data_dict.get("layerName") is not None:
                layer_name = common.check_str(query_response_data_dict.get("layerName"))
        elif "layer_name" in query_response_data_dict:
            if query_response_data_dict.get("layer_name") is not None:
                layer_name = common.check_str(query_response_data_dict.get("layer_name"))
        if "dataset" in query_response_data_dict:
            if query_response_data_dict.get("dataset") is not None:
                dataset = common.check_str(query_response_data_dict.get("dataset"))
        if "timestamp" in query_response_data_dict:
            if query_response_data_dict.get("timestamp") is not None:
                timestamp = common.check_int(query_response_data_dict.get("timestamp"))
        if "longitude" in query_response_data_dict:
            if query_response_data_dict.get("longitude") is not None:
                longitude = common.check_float(query_response_data_dict.get("longitude"))
        if "latitude" in query_response_data_dict:
            if query_response_data_dict.get("latitude") is not None:
                latitude = common.check_float(query_response_data_dict.get("latitude"))
        if "region" in query_response_data_dict:
            if query_response_data_dict.get("region") is not None:
                region = common.check_str(query_response_data_dict.get("region"))
        if "value" in query_response_data_dict:
            if query_response_data_dict.get("value") is not None:
                value = common.check_str(query_response_data_dict.get("value"))
        if "unit" in query_response_data_dict:
            if query_response_data_dict.get("unit") is not None:
                unit = common.check_str(query_response_data_dict.get("unit"))
        if "property" in query_response_data_dict:
            if query_response_data_dict.get("property") is not None:
                pty = common.check_str(query_response_data_dict.get("property"))
        if "aggregation" in query_response_data_dict:
            if query_response_data_dict.get("aggregation") is not None:
                aggregation = common.check_str(query_response_data_dict.get("aggregation"))
        if "alias" in query_response_data_dict:
            if query_response_data_dict.get("alias") is not None:
                alias = common.check_str(query_response_data_dict.get("alias"))
        return QueryResponseData(layer_id    = layer_id,
                                 layer_name  = layer_name,
                                 dataset     = dataset,
                                 timestamp   = timestamp,
                                 longitude   = longitude,
                                 latitude    = latitude,
                                 region      = region,
                                 value       = value,
                                 unit        = unit,
                                 pty         = pty,
                                 aggregation = aggregation,
                                 alias       = alias
                                )
    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
      
        query_response_data_dict: dict = {}
        if self._layer_id is not None:
            query_response_data_dict["layer_id"] = self._layer_id
        if self._layer_name is not None:
            query_response_data_dict["layer_name"] = self._layer_name
        if self._dataset is not None:
            query_response_data_dict["dataset"] = self._dataset
        if self._timestamp is not None:
            query_response_data_dict["timestamp"] = self._timestamp
        if self._longitude is not None:
            query_response_data_dict["longitude"] = self._longitude
        if self._latitude is not None:
            query_response_data_dict["latitude"] = self._latitude
        if self._region is not None:
            query_response_data_dict["region"] = self._region
        if self._value is not None:
            query_response_data_dict["value"] = self._value
        if self._unit is not None:
            query_response_data_dict["unit"] = self._unit
        if self._pty is not None:
            query_response_data_dict["property"] = self._pty
        if self._aggregation is not None:
            query_response_data_dict["aggregation"] = self._aggregation
        if self._alias is not None:
            query_response_data_dict["alias"] = self._alias
        return query_response_data_dict
        
    #
    def from_json(query_response_data_json: Any):

        """
        Create a QueryResponseData object from json (dictonary or str).
        
        :param query_response_data_dict:        A json dictionary that contains the keys of a QueryResponseData or a string representation of a json dictionary.
        :type query_response_data_dict:         Any             
        :rtype:                                 ibmpairs.query.QueryResponseData
        :raises Exception:                      if not a dictionary or a string.
        """

        if isinstance(query_response_data_json, dict):
            query_response_data = QueryResponseData.from_dict(query_response_data_json)
        elif isinstance(query_response_data_json, str):
            query_response_data_dict = json.loads(query_response_data_json)
            query_response_data = QueryResponseData.from_dict(query_response_data_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_response_data_json), "query_response_data_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_response_data

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
      
        return json.dumps(self.to_dict())
        
#
class QueryResponse:
    #_id: str
    #_url: str
    ##_data: List[QueryResponseData]
    #_data: Any
    #_message: str
    
    """
    A representation of a response to a Query.
    
    :param id:       Query ID.
    :type id:        str
    :param url:      URL.
    :type url:       str
    :param data:     The data provided by a query response.
    :type data:      List[ibmpairs.query.QueryResponseData] or str
    :param message:  A response message.
    :type message:   str
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
                 url: str     = None, 
                 #data: List[QueryResponseData] = None,
                 data: Any    = None,
                 message: str = None
                ):
        self._id      = id
        self._url     = url
        self._data    = data
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
    def get_data(self):
        return self._data

    #
    def set_data(self, data):
        if isinstance(data, str):
            self._data = data
        else:
            self._data = common.check_list(data)

    #    
    def del_data(self): 
        del self._data

    #    
    data = property(get_data, set_data, del_data) 

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
    def from_dict(query_response_dict: Any):
        
        """
        Create a QueryResponse object from a dictionary.
        
        :param query_response_dict:    A dictionary that contains the keys of a QueryResponse.
        :type query_response_dict:     Any             
        :rtype:                        ibmpairs.query.QueryResponse
        :raises Exception:             if not a dictionary.
        """
        
        id      = None
        url     = None
        data    = None
        message = None
        
        common.check_dict(query_response_dict)
        if "id" in query_response_dict:
            if query_response_dict.get("id") is not None:
                id = common.check_str(query_response_dict.get("id"))
        if "url" in query_response_dict:
            if query_response_dict.get("url") is not None:
                url = common.check_str(query_response_dict.get("url"))
        if "data" in query_response_dict:
            if query_response_dict.get("data") is not None:
                if isinstance(query_response_dict.get("data"), str):
                    data = query_response_dict.get("data")
                else:
                    data = common.from_list(query_response_dict.get("data"), QueryResponseData.from_dict)
        if "message" in query_response_dict:
            if query_response_dict.get("message") is not None:
                message = common.check_str(query_response_dict.get("message"))
        return QueryResponse(id      = id,
                             url     = url,
                             data    = data,
                             message = message
                            )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.
                    
        :rtype:                     dict
        """
        
        query_response_dict: dict = {}
        if self._id is not None:
            query_response_dict["id"] = self._id
        if self._url is not None:
            query_response_dict["url"] = self._url
        if self._data is not None:
            if isinstance(self._data, str):
                query_response_dict["data"] = self._data
            else:
                query_response_dict["data"] = common.from_list(self._data, lambda item: common.class_to_dict(item, QueryResponseData))
        if self._message is not None:
            query_response_dict["message"] = self._message
        return query_response_dict
        
    #
    def from_json(query_response_json: Any, 
                  compact_csv: bool = False
                 ):
        """
        Create a QueryResponse object from json (dictonary or str).
        
        :param query_response_dict:        A json dictionary that contains the keys of a QueryResponse or a string representation of a json dictionary.
        :type query_response_dict:         Any    
        :param compact_csv:                A flag to indicate the return of a compact csv format.
        :type compact_csv:                 bool         
        :rtype:                            ibmpairs.query.QueryResponse
        :raises Exception:                 if not a dictionary or a string.
        """
        if isinstance(query_response_json, dict):
            query_response = QueryResponse.from_dict(query_response_json)
        elif isinstance(query_response_json, str):
            if compact_csv:
                query_response = QueryResponse(data = query_response_json)
            else:
                query_response_dict = json.loads(query_response_json)
                query_response = QueryResponse.from_dict(query_response_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_response_json), "query_response_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_response

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
      
        return json.dumps(self.to_dict())
        
#
class QueryJob:
    #_id: str
    #_status: str
    #_start: int
    #_sw_lat: float
    #_sw_lon: float
    #_ne_lat: float
    #_ne_lon: float
    #_nickname: str
    #_ex_percent: int
    #_flag: bool
    #_hadoop_id: str
    #_ready: bool
    #_rt_status: str
    #_pd_status: str
    #_status_code: int
    
    """
    A representation of a Query Job.
    
    :param id:          Query ID.
    :type id:           str
    :param status:      Query status.
    :type status:       str
    :param start:       The start time of the query (UNIX).
    :type start:        int
    :param sw_lat:      The south west latitudinal point of the query.
    :type sw_lat:       float
    :param sw_lon:      The south west longitudinal point of the query.
    :type sw_lon:       float
    :param ne_lat:      The north east latitudinal point of the query.
    :type ne_lat:       float
    :param ne_lon:      The north east longitudinal point of the query.
    :type ne_lon:       float
    :param nickname:    Query name.
    :type nickname:     str
    :param ex_percent:  Execution percentage.
    :type ex_percent:   int
    :param flag:        Favorite flag.
    :type flag:         bool
    :param hadoop_id:   YARN Job execution ID.
    :type hadoop_id:    str    
    :param ready:       Query readiness.
    :type ready:        bool
    :param rt_status:   RT status.
    :type rt_status:    str
    :param pd_status:   PD status.
    :type pd_status:    str
    :param status_code: Status code.
    :type status_code:  int
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
                 id: str          = None, 
                 status: str      = None, 
                 start: int       = None, 
                 sw_lat: float    = None, 
                 sw_lon: float    = None, 
                 ne_lat: float    = None, 
                 ne_lon: float    = None, 
                 nickname: str    = None, 
                 ex_percent: int  = None, 
                 flag: bool       = None, 
                 hadoop_id: str   = None, 
                 ready: bool      = None, 
                 rt_status: str   = None, 
                 pd_status: str   = None, 
                 status_code: int = None
                ):
        self._id          = id
        self._status      = status
        self._start       = start
        self._sw_lat      = sw_lat
        self._sw_lon      = sw_lon
        self._ne_lat      = ne_lat
        self._ne_lon      = ne_lon
        self._nickname    = nickname
        self._ex_percent  = ex_percent
        self._flag        = flag
        self._hadoop_id   = hadoop_id
        self._ready       = ready
        self._rt_status   = rt_status
        self._pd_status   = pd_status
        self._status_code = status_code

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
    def get_start(self):
        return self._start

    #
    def set_start(self, start):
        self._start = common.check_int(start)

    #    
    def del_start(self): 
        del self._start

    #    
    start = property(get_start, set_start, del_start)
    
    #
    def get_sw_lat(self):
        return self._sw_lat

    #
    def set_sw_lat(self, sw_lat):
        self._sw_lat = common.check_float(sw_lat)

    #    
    def del_sw_lat(self): 
        del self._sw_lat

    #    
    sw_lat = property(get_sw_lat, set_sw_lat, del_sw_lat)
    
    #
    def get_sw_lon(self):
        return self._sw_lon

    #
    def set_sw_lon(self, sw_lon):
        self._sw_lon = common.check_float(sw_lon)

    #    
    def del_sw_lon(self): 
        del self._sw_lon

    #    
    sw_lon = property(get_sw_lon, set_sw_lon, del_sw_lon)
    
    #
    def get_ne_lat(self):
        return self._ne_lat

    #
    def set_ne_lat(self, ne_lat):
        self._ne_lat = common.check_float(ne_lat)

    #    
    def del_ne_lat(self): 
        del self._ne_lat

    #    
    ne_lat = property(get_ne_lat, set_ne_lat, del_ne_lat)
    
    #
    def get_ne_lon(self):
        return self._ne_lon

    #
    def set_ne_lon(self, ne_lon):
        self._ne_lon = common.check_float(ne_lon)

    #    
    def del_ne_lon(self): 
        del self._ne_lon

    #    
    ne_lon = property(get_ne_lon, set_ne_lon, del_ne_lon)
    
    #
    def get_nickname(self):
        return self._nickname

    #
    def set_nickname(self, nickname):
        self._nickname = common.check_str(nickname)

    #    
    def del_nickname(self): 
        del self._nickname

    #    
    nickname = property(get_nickname, set_nickname, del_nickname)
    
    #
    def get_ex_percent(self):
        return self._ex_percent

    #
    def set_ex_percent(self, ex_percent):
        self._ex_percent = common.check_float(ex_percent)

    #    
    def del_ex_percent(self): 
        del self._ex_percent

    #    
    ex_percent = property(get_ex_percent, set_ex_percent, del_ex_percent)
    
    #
    def get_flag(self):
        return self._flag

    #
    def set_flag(self, flag):
        self._flag = common.check_bool(flag)

    #    
    def del_flag(self): 
        del self._flag

    #    
    flag = property(get_flag, set_flag, del_flag)
    
    #
    def get_hadoop_id(self):
        return self._hadoop_id

    #
    def set_hadoop_id(self, hadoop_id):
        self._hadoop_id = common.check_str(hadoop_id)

    #    
    def del_hadoop_id(self): 
        del self._hadoop_id

    #    
    hadoop_id = property(get_hadoop_id, set_hadoop_id, del_hadoop_id)
    
    #
    def get_ready(self):
        return self._ready

    #
    def set_ready(self, ready):
        self._ready = common.check_bool(ready)

    #    
    def del_ready(self): 
        del self._ready

    #    
    ready = property(get_ready, set_ready, del_ready)
    
    #
    def get_rt_status(self):
        return self._rt_status

    #
    def set_rt_status(self, rt_status):
        self._rt_status = common.check_str(rt_status)

    #    
    def del_rt_status(self): 
        del self._rt_status

    #    
    rt_status = property(get_rt_status, set_rt_status, del_rt_status)
    
    #
    def get_pd_status(self):
        return self._pd_status

    #
    def set_pd_status(self, pd_status):
        self._pd_status = common.check_str(pd_status)

    #    
    def del_pd_status(self): 
        del self._pd_status

    #    
    pd_status = property(get_pd_status, set_pd_status, del_pd_status)

    #
    def get_status_code(self):
        return self._status_code

    #
    def set_status_code(self, status_code):
        self._status_code = common.check_int(status_code)

    #    
    def del_status_code(self): 
        del self._status_code

    #    
    status_code = property(get_status_code, set_status_code, del_status_code)
    
    #
    def from_dict(query_job_dict: Any):

        """
        Create a QueryJob object from a dictionary.
        
        :param query_job_dict:    A dictionary that contains the keys of a QueryJob.
        :type query_job_dict:     Any             
        :rtype:                   ibmpairs.query.QueryJob
        :raises Exception:        if not a dictionary.
        """
        
        id          = None
        status      = None
        start       = None
        sw_lat      = None
        sw_lon      = None
        ne_lat      = None
        ne_lon      = None
        nickname    = None
        ex_percent  = None
        flag        = None
        hadoop_id   = None
        ready       = None
        rt_status   = None
        pd_status   = None
        status_code = None
        
        common.check_dict(query_job_dict)
        if "id" in query_job_dict:
            if query_job_dict.get("id") is not None:
                id = common.check_str(query_job_dict.get("id"))
        if "status" in query_job_dict:
            if query_job_dict.get("status") is not None:
                status = common.check_str(query_job_dict.get("status"))
        if "start" in query_job_dict:
            if query_job_dict.get("start") is not None:
                start = common.check_int(query_job_dict.get("start"))
        if "swLat" in query_job_dict:
            if query_job_dict.get("swLat") is not None:
                sw_lat = common.check_float(query_job_dict.get("swLat"))
        elif "sw_lat" in query_job_dict:
            if query_job_dict.get("sw_lat") is not None:
                sw_lat = common.check_float(query_job_dict.get("sw_lat"))
        if "swLon" in query_job_dict:
            if query_job_dict.get("swLon") is not None:
                sw_lon = common.check_float(query_job_dict.get("swLon"))
        elif "sw_lon" in query_job_dict:
            if query_job_dict.get("sw_lon") is not None:
                sw_lon = common.check_float(query_job_dict.get("sw_lon"))
        if "neLat" in query_job_dict:
            if query_job_dict.get("neLat") is not None:
                ne_lat = common.check_float(query_job_dict.get("neLat"))
        elif "ne_lat" in query_job_dict:
            if query_job_dict.get("ne_lat") is not None:
                ne_lat = common.check_float(query_job_dict.get("ne_lat"))
        if "neLon" in query_job_dict:
            if query_job_dict.get("neLon") is not None:
                ne_lon = common.check_float(query_job_dict.get("neLon"))
        elif "ne_lon" in query_job_dict:
            if query_job_dict.get("ne_lon") is not None:
                ne_lon = common.check_float(query_job_dict.get("ne_lon"))
        if "nickname" in query_job_dict:
            if query_job_dict.get("nickname") is not None:
                nickname = common.check_str(query_job_dict.get("nickname"))
        if "exPercent" in query_job_dict:
            if query_job_dict.get("exPercent") is not None:
                ex_percent = common.check_float(query_job_dict.get("exPercent"))
        elif "ex_percent" in query_job_dict:
            if query_job_dict.get("ex_percent") is not None:
                ex_percent = common.check_float(query_job_dict.get("ex_percent"))
        if "flag" in query_job_dict:
            if query_job_dict.get("flag") is not None:
                flag = common.check_bool(query_job_dict.get("flag"))
        if "hadoopId" in query_job_dict:
            if query_job_dict.get("hadoopId") is not None:
                hadoop_id = common.check_str(query_job_dict.get("hadoopId"))
        elif "hadoop_id" in query_job_dict:
            if query_job_dict.get("hadoop_id") is not None:
                hadoop_id = common.check_str(query_job_dict.get("hadoop_id"))
        if "ready" in query_job_dict:
            if query_job_dict.get("ready") is not None:
                ready = common.check_bool(query_job_dict.get("ready"))
        if "rtStatus" in query_job_dict:
            if query_job_dict.get("rtStatus") is not None:
                rt_status = common.check_str(query_job_dict.get("rtStatus"))
        elif "rt_status" in query_job_dict:
            if query_job_dict.get("rt_status") is not None:
                rt_status = common.check_str(query_job_dict.get("rt_status"))
        if "pdStatus" in query_job_dict:
            if query_job_dict.get("pdStatus") is not None:
                pd_status = common.check_str(query_job_dict.get("pdStatus"))
        elif "pd_status" in query_job_dict:
            if query_job_dict.get("pd_status") is not None:
                pd_status = common.check_str(query_job_dict.get("pd_status"))
        if "statusCode" in query_job_dict:
            if query_job_dict.get("statusCode") is not None:
                status_code = common.check_int(query_job_dict.get("statusCode"))
        elif "status_code" in query_job_dict:
            if query_job_dict.get("status_code") is not None:
                status_code = common.check_int(query_job_dict.get("status_code"))
        return QueryJob(id          = id,
                        status      = status,
                        start       = start,
                        sw_lat      = sw_lat,
                        sw_lon      = sw_lon,
                        ne_lat      = ne_lat,
                        ne_lon      = ne_lon,
                        nickname    = nickname,
                        ex_percent  = ex_percent,
                        flag        = flag,
                        hadoop_id   = hadoop_id,
                        ready       = ready,
                        rt_status   = rt_status,
                        pd_status   = pd_status,
                        status_code = status_code
                       )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        query_job_dict: dict = {}
        if self._id is not None:
            query_job_dict["id"] = self._id
        if self._status is not None:
            query_job_dict["status"] = self._status            
        if self._start is not None:
            query_job_dict["start"] = self._start
        if self._sw_lat is not None:
            query_job_dict["sw_lat"] = self._sw_lat
        if self._sw_lon is not None:
            query_job_dict["sw_lon"] = self._sw_lon
        if self._ne_lat is not None:
            query_job_dict["ne_lat"] = self._ne_lat
        if self._ne_lon is not None:
            query_job_dict["ne_lon"] = self._ne_lon
        if self._nickname is not None:
            query_job_dict["nickname"] = self._nickname
        if self._ex_percent is not None:
            query_job_dict["ex_percent"] = self._ex_percent
        if self._flag is not None:
            query_job_dict["flag"] = self._flag
        if self._hadoop_id is not None:
            query_job_dict["hadoop_id"] = self._hadoop_id
        if self._ready is not None:
            query_job_dict["ready"] = self._ready
        if self._rt_status is not None:
            query_job_dict["rt_status"] = self._rt_status
        if self._pd_status is not None:
            query_job_dict["pd_status"] = self._pd_status
        if self._status_code is not None:
            query_job_dict["status_code"] = self._status_code
        return query_job_dict
        
    #
    def from_json(query_job_json: Any):

        """
        Create a QueryJob object from json (dictonary or str).
        
        :param query_job_dict:        A json dictionary that contains the keys of a QueryJob or a string representation of a json dictionary.
        :type query_job_dict:         Any             
        :rtype:                      ibmpairs.query.QueryJob
        :raises Exception:           if not a dictionary or a string.
        """

        if isinstance(query_job_json, dict):
            query_job = QueryJob.from_dict(query_job_json)
        elif isinstance(query_job_json, str):
            query_job_dict = json.loads(query_job_json)
            query_job = QueryJob.from_dict(query_job_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_job_json), "query_job_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_job

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
      
        return json.dumps(self.to_dict())

#
class QueryJobs:
    #_tot_pages: int
    #_query_job_list: List[QueryJob]
    
    """
    A representation of a list of Query Jobs.
    
    :param tot_pages:      Total pages.
    :type tot_pages:       int
    :param query_job_list: A list of Query jobs.
    :type query_job_list:  List[ibmpairs.query.QueryJob]
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
                 tot_pages: int                 = None, 
                 query_job_list: List[QueryJob] = None
                ):          
        
        self._tot_pages      = tot_pages
        self._query_job_list = query_job_list
        
    #
    def get_tot_pages(self):
        return self._tot_pages

    #
    def set_tot_pages(self, tot_pages):
        self._tot_pages = common.check_int(tot_pages)

    #    
    def del_tot_pages(self): 
        del self._tot_pages

    #    
    tot_pages = property(get_tot_pages, set_tot_pages, del_tot_pages)
    
    # 
    def get_query_job_list(self):
        return self._query_job_list

    #
    def set_query_job_list(self, query_job_list):
        self._query_job_list = common.check_list(query_job_list)

    #    
    def del_query_job_list(self): 
        del self._query_job_list

    #    
    query_job_list = property(get_query_job_list, set_query_job_list, del_query_job_list) 

    #
    def from_dict(query_jobs_dict: Any):

        """
        Create a QueryJobs object from a dictionary.
        
        :param query_jobs_dict:    A dictionary that contains the keys of a QueryJobs.
        :type query_jobs_dict:     Any             
        :rtype:                    ibmpairs.query.QueryJobs
        :raises Exception:         if not a dictionary.
        """
        
        tot_pages      = None
        query_job_list = None
        
        common.check_dict(query_jobs_dict)
        if "totPages" in query_jobs_dict:
            if query_jobs_dict.get("totPages") is not None:
                tot_pages = common.check_int(query_jobs_dict.get("totPages"))
        elif "tot_pages" in query_jobs_dict:
            if query_jobs_dict.get("tot_pages") is not None:
                tot_pages = common.check_int(query_jobs_dict.get("tot_pages"))
        if "queryJobList" in query_jobs_dict:
            if query_jobs_dict.get("queryJobList") is not None:
                query_job_list = common.from_list(query_jobs_dict.get("queryJobList"), QueryJob.from_dict)
        elif "query_job_list" in query_jobs_dict:
            if query_jobs_dict.get("query_job_list") is not None:
                query_job_list = common.from_list(query_jobs_dict.get("query_job_list"), QueryJob.from_dict)
        return QueryJobs(tot_pages      = tot_pages, 
                         query_job_list = query_job_list
                        )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        query_jobs_dict: dict = {}
        if self._tot_pages is not None:
            query_jobs_dict["tot_pages"] = self._tot_pages
        if self._query_job_list is not None:
            query_jobs_dict["query_job_list"] = common.from_list(self._query_job_list, lambda item: common.class_to_dict(item, QueryJob))
        return query_jobs_dict
    
    #
    def from_json(query_jobs_json: Any):

        """
        Create a QueryJobs object from json (dictonary or str).
        
        :param query_jobs_dict:        A json dictionary that contains the keys of a QueryJobs or a string representation of a json dictionary.
        :type query_jobs_dict:         Any             
        :rtype:                        ibmpairs.query.QueryJobs
        :raises Exception:             if not a dictionary or a string.
        """

        if isinstance(query_jobs_json, dict):
            query_jobs = QueryJobs.from_dict(query_jobs_json)
        elif isinstance(query_jobs_json, str):
            query_jobs_dict = json.loads(query_jobs_json)
            query_jobs = QueryJobs.from_dict(query_jobs_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_jobs_json), "query_jobs_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_jobs

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
      
        return json.dumps(self.to_dict())
        
#
class QueryJobLayer:
    #_name: str
    #_style: str
    #_dataset_id: int
    #_dataset: str
    #_datalayer_id: str
    #_datalayer: str
    #_group: str
    #_timestamp: int
    #_dimensions: List[Dimension]
    #_min: int
    #_max: int
    #_colortable_id: int
    #_options: List[str]
    #_type: str
    #_geoserver_url: str
    #_geoserver_ws: str
    #_units_bl: str
    
    """
    A representation of a Query Job Layer.
    
    :param name:          The name of the Query Job Layer.
    :type name:           str
    :param style:         The Query Job Layer style.
    :type style:          str
    :param dataset_id:    The Data Set ID.
    :type dataset_id:     str
    :param dataset:       The Data Set name.
    :type dataset:        str
    :param datalayer_id:  The Data Layer ID.
    :type datalayer_id:   str
    :param datalayer:     The Data Layer name.
    :type datalayer:      str
    :param group:         The Data Layer group.
    :type group:          str
    :param timestamp:     Timestamp (UNIX).
    :type timestamp:      int
    :param dimensions:    A list of Dimensions that apply.
    :type dimensions:     List[ibmpairs.query.Dimensions]
    :param min:           The minimum value of the data.
    :type min:            int
    :param max:           The maximum value of the data.
    :type max:            int
    :param colortable_id: The Colour Table ID.
    :type colortable_id:  int
    :param options:       A list of applied options.
    :type options:        List[str]
    :param type:          Type.
    :type type:           str
    :param geoserver_url: The GeoServer URL.
    :type geoserver_url:  str
    :param geoserver_ws:  The GeoServer Web Server.
    :type geoserver_ws:   str
    :param units_bl:      Units.
    :type units_bl:       str
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
                 name: str                   = None,
                 style: str                  = None,
                 dataset_id: int             = None,
                 dataset: str                = None,
                 datalayer_id: str           = None,
                 datalayer: str              = None,
                 group: str                  = None,
                 timestamp: int              = None,
                 dimensions: List[Dimension] = None,
                 min: float                  = None,
                 max: float                  = None,
                 colortable_id: int          = None,
                 options: List[str]          = None,
                 type: str                   = None,
                 geoserver_url: str          = None,
                 geoserver_ws: str           = None,
                 units_bl: str               = None
                ):
        self._name          = name
        self._style         = style
        self._dataset_id    = dataset_id
        self._dataset       = dataset
        self._datalayer_id  = datalayer_id
        self._datalayer     = datalayer
        self._group         = group
        self._timestamp     = timestamp
        self._dimensions    = dimensions
        self._min           = min
        self._max           = max
        self._colortable_id = colortable_id
        self._options       = options
        self._type          = type
        self._geoserver_url = geoserver_url
        self._geoserver_ws  = geoserver_ws
        self._units_bl      = units_bl

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
    def get_style(self):
        return self._style

    #
    def set_style(self, style):
        self._style = common.check_str(style)

    #    
    def del_style(self): 
        del self._style

    #    
    style = property(get_style, set_style, del_style)
    
    #
    def get_dataset_id(self):
        return self._dataset_id

    #
    def set_dataset_id(self, dataset_id):
        self._dataset_id = common.check_int(dataset_id)

    #    
    def del_dataset_id(self): 
        del self._dataset_id

    #    
    dataset_id = property(get_dataset_id, set_dataset_id, del_dataset_id)
    
    #
    def get_dataset(self):
        return self._dataset

    #
    def set_dataset(self, dataset):
        self._dataset = common.check_str(dataset)

    #    
    def del_dataset(self): 
        del self._dataset

    #    
    dataset = property(get_dataset, set_dataset, del_dataset)
    
    #
    def get_datalayer_id(self):
        return self._datalayer_id

    #
    def set_datalayer_id(self, datalayer_id):
        self._datalayer_id = common.check_str(datalayer_id)

    #    
    def del_datalayer_id(self): 
        del self._datalayer_id

    #    
    datalayer_id = property(get_datalayer_id, set_datalayer_id, del_datalayer_id)
    
    #
    def get_datalayer(self):
        return self._datalayer

    #
    def set_datalayer(self, datalayer):
        self._datalayer = common.check_str(datalayer)

    #    
    def del_datalayer(self): 
        del self._datalayer

    #    
    datalayer = property(get_datalayer, set_datalayer, del_datalayer)
    
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
    def get_timestamp(self):
        return self._timestamp

    #
    def set_timestamp(self, timestamp):
        self._timestamp = common.check_int(timestamp)

    #    
    def del_timestamp(self): 
        del self._timestamp

    #    
    timestamp = property(get_timestamp, set_timestamp, del_timestamp)
    
    #
    def get_dimensions(self):
        return self._dimensions

    #
    def set_dimensions(self, dimensions):
        self._dimensions = common.check_list(dimensions) 
    
    #
    def del_dimensions(self): 
        del self._dimensions

    #
    dimensions = property(get_dimensions, set_dimensions, del_dimensions)

    #
    def get_min(self):
        return self._min

    #
    def set_min(self, min):
        self._min = common.check_float(min)

    #    
    def del_min(self): 
        del self._min

    #    
    min = property(get_min, set_min, del_min)

    #
    def get_max(self):
        return self._max

    #
    def set_max(self, max):
        self._max = common.check_float(max)

    #    
    def del_max(self): 
        del self._max

    #    
    max = property(get_max, set_max, del_max)
    
    #
    def get_colortable_id(self):
        return self._colortable_id

    #
    def set_colortable_id(self, colortable_id):
        self._colortable_id = common.check_int(colortable_id)

    #    
    def del_colortable_id(self): 
        del self._colortable_id

    #    
    colortable_id = property(get_colortable_id, set_colortable_id, del_colortable_id)
    
    #    
    def get_options(self):
        return self._options

    #
    def set_options(self, options):
        self._options = common.check_list(options)
        
    #    
    def del_options(self): 
        del self._options

    #    
    options = property(get_options, set_options, del_options)
    
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
    def get_geoserver_url(self):
        return self._geoserver_url

    #
    def set_geoserver_url(self, geoserver_url):
        self._geoserver_url = common.check_str(geoserver_url)

    #    
    def del_geoserver_url(self): 
        del self._geoserver_url

    #    
    geoserver_url = property(get_geoserver_url, set_geoserver_url, del_geoserver_url)
    
    #
    def get_geoserver_ws(self):
        return self._geoserver_ws

    #
    def set_geoserver_ws(self, geoserver_ws):
        self._geoserver_ws = common.check_str(geoserver_ws)

    #    
    def del_geoserver_ws(self): 
        del self._geoserver_ws

    #    
    geoserver_ws = property(get_geoserver_ws, set_geoserver_ws, del_geoserver_ws)
    
    #
    def get_units_bl(self):
      return self._units_bl

    #
    def set_units_bl(self, units_bl):
      self._units_bl = common.check_str(units_bl)

    #    
    def del_units_bl(self): 
      del self._units_bl

    #    
    units_bl = property(get_units_bl, set_units_bl, del_units_bl)

    #
    def from_dict(query_job_layer_dict: Any):

        """
        Create a QueryJobLayer object from a dictionary.
        
        :param query_job_layer_dict:    A dictionary that contains the keys of a QueryJobLayer.
        :type query_job_layer_dict:     Any             
        :rtype:                         ibmpairs.query.QueryJobLayer
        :raises Exception:              if not a dictionary.
        """
        
        name          = None
        style         = None
        dataset_id    = None
        dataset       = None
        datalayer_id  = None
        datalayer     = None
        group         = None
        timestamp     = None
        dimensions    = None
        min           = None
        max           = None
        colortable_id = None
        options       = None
        type          = None
        geoserver_url = None
        geoserver_ws  = None
        units_bl      = None
        
        common.check_dict(query_job_layer_dict)
        if "name" in query_job_layer_dict:
            if query_job_layer_dict.get("name") is not None:
                name = common.check_str(query_job_layer_dict.get("name"))
        if "style" in query_job_layer_dict:
            if query_job_layer_dict.get("style") is not None:
                style = common.check_str(query_job_layer_dict.get("style"))
        if "datasetId" in query_job_layer_dict:
            if query_job_layer_dict.get("datasetId") is not None:
                dataset_id = common.check_int(query_job_layer_dict.get("datasetId"))
        elif "dataset_id" in query_job_layer_dict:
            if query_job_layer_dict.get("dataset_id") is not None:
                dataset_id = common.check_int(query_job_layer_dict.get("dataset_id"))
        if "dataset" in query_job_layer_dict:
            if query_job_layer_dict.get("dataset") is not None:
                dataset = common.check_str(query_job_layer_dict.get("dataset"))
        if "datalayerId" in query_job_layer_dict:
            if query_job_layer_dict.get("datalayerId") is not None:
                datalayer_id = common.check_str(query_job_layer_dict.get("datalayerId"))
        elif "datalayer_id" in query_job_layer_dict:
            if query_job_layer_dict.get("datalayer_id") is not None:
                datalayer_id = common.check_str(query_job_layer_dict.get("datalayer_id"))
        if "datalayer" in query_job_layer_dict:
            if query_job_layer_dict.get("datalayer") is not None:
                datalayer = common.check_str(query_job_layer_dict.get("datalayer"))
        if "group" in query_job_layer_dict:
            if query_job_layer_dict.get("group") is not None:
                group = common.check_str(query_job_layer_dict.get("group"))
        if "timestamp" in query_job_layer_dict:
            if query_job_layer_dict.get("timestamp") is not None:
                timestamp = common.check_int(query_job_layer_dict.get("timestamp"))
        if "dimensions" in query_job_layer_dict:
            if query_job_layer_dict.get("dimensions") is not None:
                dimensions = common.from_list(query_job_layer_dict.get("dimensions"), Dimension.from_dict)
        if "min" in query_job_layer_dict:
            if query_job_layer_dict.get("min") is not None:
                min = common.check_float(query_job_layer_dict.get("min"))
        if "max" in query_job_layer_dict:
            if query_job_layer_dict.get("max") is not None:
                max = common.check_float(query_job_layer_dict.get("max"))
        if "colorTableId" in query_job_layer_dict:
            if query_job_layer_dict.get("colorTableId") is not None:
                colortable_id = common.check_int(query_job_layer_dict.get("colorTableId"))
        elif "colortable_id" in query_job_layer_dict:
            if query_job_layer_dict.get("colortable_id") is not None:
                colortable_id = common.check_int(query_job_layer_dict.get("colortable_id"))
        if "options" in query_job_layer_dict:
            if query_job_layer_dict.get("options") is not None:
                options = common.from_list(query_job_layer_dict.get("options"), common.check_str)
        if "type" in query_job_layer_dict:
            if query_job_layer_dict.get("type") is not None:
                type = common.check_str(query_job_layer_dict.get("type"))
        if "geoserverUrl" in query_job_layer_dict:
            if query_job_layer_dict.get("geoserverUrl") is not None:
                geoserver_url = common.check_str(query_job_layer_dict.get("geoserverUrl"))
        elif "geoserver_url" in query_job_layer_dict:
            if query_job_layer_dict.get("geoserver_url") is not None:
                geoserver_url = common.check_str(query_job_layer_dict.get("geoserver_url"))
        if "geoserverWS" in query_job_layer_dict:
            if query_job_layer_dict.get("geoserverWS") is not None:
                geoserver_ws = common.check_str(query_job_layer_dict.get("geoserverWS"))
        elif "geoserver_ws" in query_job_layer_dict:
            if query_job_layer_dict.get("geoserver_ws") is not None:
                geoserver_ws = common.check_str(query_job_layer_dict.get("geoserver_ws"))
        if "unitsbl" in query_job_layer_dict:
          if query_job_layer_dict.get("unitsbl") is not None:
            units_bl = common.check_str(query_job_layer_dict.get("unitsbl"))
        elif "units_bl" in query_job_layer_dict:
          if query_job_layer_dict.get("units_bl") is not None:
            units_bl = common.check_str(query_job_layer_dict.get("units_bl"))

        return QueryJobLayer(name          = name,
                             style         = style,
                             dataset_id    = dataset_id,
                             dataset       = dataset,
                             datalayer_id  = datalayer_id,
                             datalayer     = datalayer,
                             group         = group,
                             timestamp     = timestamp,
                             dimensions    = dimensions,
                             min           = min,
                             max           = max,
                             colortable_id = colortable_id,
                             options       = options,
                             type          = type,
                             geoserver_url = geoserver_url,
                             geoserver_ws  = geoserver_ws,
                             units_bl      = units_bl
                            )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.   
                 
        :rtype:                     dict
        """
      
        query_job_layer_dict: dict = {}
        if self._name is not None:
            query_job_layer_dict["name"] = self._name
        if self._style is not None:
            query_job_layer_dict["style"] = self._style            
        if self._dataset_id is not None:
            query_job_layer_dict["dataset_id"] = self._dataset_id
        if self._dataset is not None:
            query_job_layer_dict["dataset"] = self._dataset
        if self._datalayer_id is not None:
            query_job_layer_dict["datalayer_id"] = self._datalayer_id
        if self._datalayer is not None:
            query_job_layer_dict["datalayer"] = self._datalayer
        if self._group is not None:
            query_job_layer_dict["group"] = self._group
        if self._timestamp is not None:
            query_job_layer_dict["timestamp"] = self._timestamp
        if self._dimensions is not None:
            query_job_layer_dict["dimensions"] = common.from_list(self._dimensions, lambda item: common.class_to_dict(item, Dimension))
        if self._min is not None:
            query_job_layer_dict["min"] = self._min
        if self._max is not None:
            query_job_layer_dict["max"] = self._max
        if self._colortable_id is not None:
            query_job_layer_dict["colortable_id"] = self._colortable_id
        if self._options is not None:
            query_job_layer_dict["options"] = common.from_list(self._options, common.check_str)
        if self._type is not None:
            query_job_layer_dict["type"] = self._type
        if self._geoserver_url is not None:
            query_job_layer_dict["geoserver_url"] = self._geoserver_url
        if self._geoserver_ws is not None:
            query_job_layer_dict["geoserver_ws"] = self._geoserver_ws
        if self._units_bl is not None:
            query_job_layer_dict["units_bl"] = self._units_bl
        return query_job_layer_dict
        
    #
    def from_json(query_job_layer_json: Any):

        """
        Create a QueryJobLayer object from json (dictonary or str).
        
        :param query_job_layer_dict:        A json dictionary that contains the keys of a QueryJobLayer or a string representation of a json dictionary.
        :type query_job_layer_dict:         Any             
        :rtype:                     ibmpairs.query.QueryJobLayer
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(query_job_layer_json, dict):
            query_job_layer = QueryJobLayer.from_dict(query_job_layer_json)
        elif isinstance(query_job_layer_json, str):
            query_job_layer_dict = json.loads(query_job_layer_json)
            query_job_layer = QueryJobLayer.from_dict(query_job_layer_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_job_layer_json), "query_job_layer_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_job_layer

    #
    def to_json(self):
      
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
        
#
class QueryJobLayers:
    #_query_job_layers: List[QueryJobLayer]
    
    """
    A representation of a list of Query Job Layers.
    
    :param query_job_layers: A list of Query Job Layers.
    :type query_job_layers:  List[ibmpairs.query.QueryJobLayer]
    """
    
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
                 query_job_layers: List[QueryJobLayer] = None,
                ):
        self._query_job_layers = query_job_layers
   
    # 
    def get_query_job_layers(self):
        return self._query_job_layers

    #
    def set_query_job_layers(self, query_job_layers):
        self._query_job_layers = common.check_list(query_job_layers)

    #    
    def del_query_job_layers(self): 
        del self._query_job_layers

    #    
    query_job_layers = property(get_query_job_layers, set_query_job_layers, del_query_job_layers)
    
    #
    def from_dict(query_job_layers_dict: Any):
        
        """
        Create a QueryJobLayers object from a dictionary.
        
        :param query_job_layers_input:    A dictionary that contains the keys of a QueryJobLayers.
        :type query_job_layers_input:     Any             
        :rtype:                           ibmpairs.query.QueryJobLayers
        :raises Exception:                if not a dictionary.
        """
        
        query_job_layers = None
        
        if isinstance(query_job_layers_dict, dict):
            common.check_dict(query_job_layers_dict)

            if "query_job_layers" in query_job_layers_dict:
                if query_job_layers_dict.get("query_job_layers") is not None:
                    query_job_layers = common.from_list(query_job_layers_dict.get("query_job_layers"), QueryJobLayer.from_dict)
        elif isinstance(query_job_layers_dict, list):
            query_job_layers = common.from_list(query_job_layers_dict, QueryJobLayer.from_dict)
        else:
            msg = messages.ERROR_QUERY_JOB_LIST_UNKNOWN.format(type(query_job_layers))
            logger.error(msg)
            raise common.PAWException(msg)

        return QueryJobLayers(query_job_layers = query_job_layers)
    
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure.   
                 
        :rtype:                     dict
        """
      
        query_job_layers_dict: dict = {}
        if self._query_job_layers is not None:
            query_job_layers_dict["query_job_layers"] = common.from_list(self._query_job_layers, lambda item: common.class_to_dict(item, QueryJobLayer))
        return query_job_layers_dict
    
    #
    def from_json(query_job_layers_json: Any):
        """
        Create a QueryJobLayers object from json (dictonary or str).
        
        :param query_job_layers_dict:        A json dictionary that contains the keys of a QueryJobLayers or a string representation of a json dictionary.
        :type query_job_layers_dict:         Any             
        :rtype:                              ibmpairs.query.QueryJobLayers
        :raises Exception:                   if not a dictionary or a string.
        """

        if isinstance(query_job_layers_json, dict):
            query_job_layers = QueryJobLayers.from_dict(query_job_layers_json)
        elif isinstance(query_job_layers_json, str):
            query_job_layers_dict = json.loads(query_job_layers_json)
            query_job_layers = QueryJobLayers.from_dict(query_job_layers_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_job_layers_json), "query_job_layers_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_job_layers

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

class Options:
    #_name: str
    #_value: str
    
    """
    A representation of a Processor Option.
    
    :param name:                A name for the option.
    :type name:                 str
    :param name:                A value for the option.
    :type name:                 str
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
                 name: str  = None,
                 value: str = None
                ):    
        self._name  = name
        self._value = value
        
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
    def get_value(self):
        return self._value

    #
    def set_value(self, value):
        self._value = common.check_str(value)
    
    #    
    def del_value(self): 
        del self._value
    
    #    
    value = property(get_value, set_value, del_value)
    
    #
    def from_dict(options_dict: Any):

        """
        Create an Options object from a dictionary.
        
        :param options_dict:          A dictionary that contains the keys of a Options.
        :type options_dict:           Any             
        :rtype:                       ibmpairs.query.Options
        :raises Exception:            if not a dictionary.
        """
        
        name  = None
        value = None
        
        common.check_dict(options_dict)
        if "name" in options_dict:
            if options_dict.get("name") is not None:
                name = common.check_str(options_dict.get("name"))
        if "value" in options_dict:
            if options_dict.get("value") is not None:
                value = common.check_str(options_dict.get("value"))
        return Options(name  = name, 
                       value = value
                      )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        options_dict: dict = {}
        if self._name is not None:
            options_dict["name"] = self._name
        if self._value is not None:
            options_dict["value"] = self._value
        return options_dict
    
    #
    def from_json(options_json: Any):
        """
        Create an Options object from json (dictonary or str).
        
        :param options_json:        A json dictionary that contains the keys of an Options or a string representation of a json dictionary.
        :type options_json:         Any             
        :rtype:                     ibmpairs.query.Options
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


class Processor:
    #_order: int
    #_type: str
    #_options: List[Options]
    
    """
    A representation of a Processor.
    
    :param order:               A name for the option.
    :type order:                int
    :param type:                A value for the option.
    :type type:                 str
    :param options:             A list of processor options.
    :type options:              List[ibmpairs.query.Options]
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
                 order: int             = None,
                 type: str              = None,
                 options: List[Options] = None
                ):    
        self._order   = order
        self._type    = type
        self._options = options
        
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
    def get_options(self):
        return self._options

    #
    def set_options(self, options):
        self._options = common.check_list(options)

    #    
    def del_options(self): 
        del self._options

    #    
    options = property(get_options, set_options, del_options)
    
    #
    def from_dict(processor_dict: Any):

        """
        Create a Processor object from a dictionary.
        
        :param processor_dict:          A dictionary that contains the keys of a Processor.
        :type processor_dict:           Any             
        :rtype:                         ibmpairs.query.Processor
        :raises Exception:              if not a dictionary.
        """

        order   = None
        type    = None
        options = None
        
        common.check_dict(processor_dict)
        if "order" in processor_dict:
            if processor_dict.get("order") is not None:
                order = common.check_int(processor_dict.get("order"))
        if "type" in processor_dict:
            if processor_dict.get("type") is not None:
                type = common.check_str(processor_dict.get("type"))
        if "options" in processor_dict:
            if processor_dict.get("options") is not None:
                options = common.from_list(processor_dict.get("options"), Options.from_dict)
        return Processor(order   = order, 
                         type    = type,
                         options = options
                        )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        processor_dict: dict = {}
        if self._order is not None:
            processor_dict["order"] = self._order
        if self._type is not None:
            processor_dict["type"] = self._type
        if self._options is not None:
            processor_dict["options"] = common.from_list(self._options, lambda item: common.class_to_dict(item, Options))
        return processor_dict
    
    #
    def from_json(processor_json: Any):
        """
        Create a Processor object from json (dictonary or str).
        
        :param processor_json:      A json dictionary that contains the keys of a Processor or a string representation of a json dictionary.
        :type processor_json:       Any             
        :rtype:                     ibmpairs.query.Processor
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(processor_json, dict):
            processor = Processor.from_dict(processor_json)
        elif isinstance(processor_json, str):
            processor_dict = json.loads(processor_json)
            processor = Processor.from_dict(processor_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(processor_json), "processor_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return processor

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class Query:

    #_client: cl.Client
    
    # Query- Data Structure
    #_name: str
    #_layers: List[Layer]
    #_temporal: Temporal
    #_spatial: Spatial
    #_output_type: str
    #_output_level: int
    #_description: str
    #_publish: bool
    #_notification: Notification
    #_upload: Upload
    #_batch: str
    #_processor: List[Processor]
    
    # Query Submit Response
    #_submit_response: QueryResponse
    #_id: str
    
    # Query Status Response
    #_status_response: QueryJob
    
    # Query Download
    #_download_status: str
    #_download_folder: str
    #_download_file_name: str
    
    # Query Merge Response
    #_merge_response: QueryJobLayers
    #_merge_status: str
    
    """
    A representation of a PAIRS Query.
    
    :param client:              An instance of an ibmpairs.client.Client.
    :type client:               ibmpairs.client.Client
    :param name:                A name for the query.
    :type name:                 str
    :param layers:              A list of layers to query.
    :type layers:               List[ibmpairs.query.Layer]
    :param spatial:             A spatial definition to query.
    :type spatial:              ibmpairs.query.Spatial
    :param temporal:            A temporal definiton to query.
    :type temporal:             ibmpairs.query.Temporal
    :param output_type:         An output type for the query.
    :type output_type:          str
    :param output_level:        An output level for the query.
    :type output_level:         int
    :param description:         A description for the query.
    :type description:          str
    :param publish:             A publish to GeoServer flag.
    :type publish:              bool
    :param notification:        A notification object definition.
    :type notification:         ibmpairs.query.Notification
    :param upload:              An upload object definition.
    :type upload:               ibmpairs.query.Upload
    :param batch:               A batch indicator.
    :type batch:                str
    :param processor:           A list of post processors to apply to a query.
    :type processor:            List[ibmpairs.query.Processor]
    :param id:                  A Query id.
    :type id:                   str
    :param submit_response:     A response from the submit phase.        
    :type submit_response:      ibmpairs.query.QueryResponse
    :param status_response:     A response from the status polling phase.
    :type status_response:      ibmpairs.query.QueryJob
    :param download_status:     A response from the download phase.
    :type download_status:      str
    :param download_folder:     A folder that downloads should be made to (fixed or relative).
    :type download_folder:      str
    :param download_file_name:  A file name for the download.       
    :type download_file_name:   str
    :param merge_response:      A response from a merged query. 
    :type merge_response:       ibmpairs.query.QueryJobLayers
    :param merge_status:        The status of a merge operation.    
    :type merge_status:         str
    :raises Exception:          if no client is provided or found Globally in the environment.
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
                 client: cl.Client              = None,
                 name: str                      = None, 
                 layers: List[Layer]            = None, 
                 temporal: Temporal             = None, 
                 spatial: Spatial               = None, 
                 output_type: str               = None, 
                 output_level: int              = None, 
                 description: str               = None, 
                 publish: bool                  = None, 
                 notification: Notification     = None, 
                 upload: Upload                 = None,
                 batch: str                     = None,
                 processor: List[Processor]     = None,
                 id: str                        = None,
                 submit_response: QueryResponse = None,
                 status_response: QueryJob      = None,
                 download_status: str           = None,
                 download_folder: str           = None,
                 download_file_name: str        = None,
                 merge_response: QueryJobLayers = None,
                 merge_status: str              = None
                ):    
        self._client              = common.set_client(input_client  = client,
                                                      global_client = cl.GLOBAL_PAIRS_CLIENT)
        self._name                = name
        self._layers              = layers
        self._temporal            = temporal
        self._spatial             = spatial
        self._output_type         = output_type
        self._output_level        = output_level
        self._description         = description
        self._publish             = publish
        self._notification        = notification
        self._upload              = upload
        self._batch               = batch
        self._processor           = processor
        self._id                  = id
        
        if submit_response is None:
          self._submit_response   = QueryResponse()
        else:
          self._submit_response   = submit_response
        
        if status_response is None:
            self._status_response = QueryJob()
        else:
            self._status_response = status_response
        
        self._download_status     = download_status
        self._download_folder     = download_folder
        self._download_file_name  = download_file_name
        
        if merge_response is None:
            self._merge_response = QueryJobLayers()
        else:
            self._merge_response = merge_response
            
        self._merge_status       = merge_status

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
    def get_layers(self):
        return self._layers

    #
    def set_layers(self, layers):
        self._layers = common.check_list(layers)

    #    
    def del_layers(self): 
        del self._layers

    #    
    layers = property(get_layers, set_layers, del_layers) 
    
    #
    def get_temporal(self):
        return self._temporal

    #
    def set_temporal(self, temporal):
        self._temporal = common.check_class(temporal, Temporal)

    #    
    def del_temporal(self): 
        del self._temporal

    #    
    temporal = property(get_temporal, set_temporal, del_temporal) 

    #
    def get_spatial(self):
        return self._spatial

    #
    def set_spatial(self, spatial):
        self._spatial = common.check_class(spatial, Spatial)
    
    #    
    def del_spatial(self): 
        del self._spatial

    #    
    spatial = property(get_spatial, set_spatial, del_spatial) 
    
    #
    def get_output_type(self):
        return self._output_type

    #
    def set_output_type(self, output_type):
        self._output_type = common.check_str(output_type)

    #    
    def del_output_type(self): 
        del self._output_type

    #    
    output_type = property(get_output_type, set_output_type, del_output_type) 

    #
    def get_output_level(self):
        return self._output_level

    #
    def set_output_level(self, output_level):
        self._output_level = common.check_int(output_level)

    #    
    def del_output_level(self): 
        del self._output_level

    #    
    output_level = property(get_output_level, set_output_level, del_output_level) 

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
    def get_publish(self):
        return self._publish

    #
    def set_publish(self, publish):
        self._publish = common.check_bool(publish)

    #    
    def del_publish(self): 
        del self._publish

    #    
    publish = property(get_publish, set_publish, del_publish) 
    
    #
    def get_notification(self):
        return self._notification

    #
    def set_notification(self, notification):
        self._notification = common.check_class(notification, Notification)

    #    
    def del_notification(self): 
        del self._notification

    #    
    notification = property(get_notification, set_notification, del_notification) 

    #
    def get_upload(self):
        return self._upload

    #
    def set_upload(self, upload):
        self._upload = common.check_class(upload, Upload)

    #    
    def del_upload(self): 
        del self._upload

    #    
    upload = property(get_upload, set_upload, del_upload) 
    
    #
    def get_batch(self):
        return self._batch

    #
    def set_batch(self, batch):
        self._batch = common.check_str(batch)
    
    #    
    def del_batch(self): 
        del self._batch
    
    #    
    batch = property(get_batch, set_batch, del_batch)
    
    # 
    def get_processor(self):
        return self._processor

    #
    def set_processor(self, processor):
        self._processor = common.check_list(processor)

    #    
    def del_processor(self): 
        del self._processor

    #    
    processor = property(get_processor, set_processor, del_processor) 
    
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
    def get_submit_response(self):
      return self._submit_response

    #
    def set_submit_response(self, submit_response):
      self._submit_response = common.check_class(submit_response, QueryResponse)

    #    
    def del_submit_response(self): 
      del self._submit_response

    #    
    submit_response = property(get_submit_response, set_submit_response, del_submit_response)
    
    #
    def get_status_response(self):
        return self._status_response

    #
    def set_status_response(self, status_response):
        self._status_response = common.check_class(status_response, QueryJob)

    #    
    def del_status_response(self): 
        del self._status_response

    #    
    status_response = property(get_status_response, set_status_response, del_status_response)
    
    #
    def get_download_status(self):
        return self._download_status

    #
    def set_download_status(self, download_status):
        self._download_status = common.check_str(download_status)
    
    #    
    def del_download_status(self): 
        del self._download_status
    
    #    
    download_status = property(get_download_status, set_download_status, del_download_status) 
    
    #
    def get_download_folder(self):
        return self._download_folder

    #
    def set_download_folder(self, download_folder):
        self._download_folder = common.check_str(download_folder)
    
    #    
    def del_download_folder(self): 
        del self._download_folder
    
    #    
    download_folder = property(get_download_folder, set_download_folder, del_download_folder)

    #
    def get_download_file_name(self):
        return self._download_file_name

    #
    def set_download_file_name(self, download_file_name):
        self._download_file_name = common.check_str(download_file_name)
    
    #    
    def del_download_file_name(self): 
        del self._download_file_name
    
    #    
    download_file_name = property(get_download_file_name, set_download_file_name, del_download_file_name)

    #
    def get_merge_response(self):
        return self._merge_response

    #
    def set_merge_response(self, merge_response):
        self._merge_response = common.check_class(merge_response, QueryJobLayers)

    #    
    def del_merge_response(self): 
        del self._merge_response

    #    
    merge_response = property(get_merge_response, set_merge_response, del_merge_response)
    
    #
    def get_merge_status(self):
      return self._merge_status

    #
    def set_merge_status(self, merge_status):
      self._merge_status = common.check_str(merge_status)

    #    
    def del_merge_status(self): 
      del self._merge_status

    #    
    merge_status = property(get_merge_status, set_merge_status, del_merge_status)

    #
    def from_dict(query_dict: Any):

        """
        Create a Query object from a dictionary.
        
        :param query_dict:          A dictionary that contains the keys of a Query.
        :type query_dict:           Any             
        :rtype:                     ibmpairs.query.Query
        :raises Exception:          if not a dictionary.
        """
        
        name               = None
        layers             = None
        temporal           = None
        spatial            = None
        output_type        = None
        output_level       = None
        description        = None
        publish            = None
        notification       = None
        upload             = None
        batch              = None
        processor          = None
        id                 = None
        submit_response    = None
        status_response    = None
        download_status    = None
        download_folder    = None
        download_file_name = None
        merge_response     = None
        merge_status       = None
        
        common.check_dict(query_dict)
        if "name" in query_dict:
            if query_dict.get("name") is not None:
                name = common.check_str(query_dict.get("name"))
        if "layers" in query_dict:
            if query_dict.get("layers") is not None:
                layers = common.from_list(query_dict.get("layers"), Layer.from_dict)
        if "temporal" in query_dict:
            if query_dict.get("temporal") is not None:
                temporal = Temporal.from_dict(query_dict.get("temporal"))
        if "spatial" in query_dict:
            if query_dict.get("spatial") is not None:
                spatial = Spatial.from_dict(query_dict.get("spatial"))
        if "outputType" in query_dict:
            if query_dict.get("outputType") is not None:
                output_type = common.check_str(query_dict.get("outputType"))
        elif "output_type" in query_dict:
            if query_dict.get("output_type") is not None:
                output_type = common.check_str(query_dict.get("output_type"))
        if "outputLevel" in query_dict:
            if query_dict.get("outputLevel") is not None:
                output_level = common.check_int(query_dict.get("outputLevel"))
        elif "output_level" in query_dict:
            if query_dict.get("output_level") is not None:
                output_level = common.check_int(query_dict.get("output_level"))
        if "description" in query_dict:
            if query_dict.get("description") is not None:
                description = common.check_str(query_dict.get("description"))
        if "publish" in query_dict:
            if query_dict.get("publish") is not None:
                publish = common.check_bool(query_dict.get("publish"))
        if "notification" in query_dict:
            if query_dict.get("notification") is not None:
                notification = Notification.from_dict(query_dict.get("notification"))
        if "upload" in query_dict:
            if query_dict.get("upload") is not None:
                upload = Upload.from_dict(query_dict.get("upload"))
        if "batch" in query_dict:
            if query_dict.get("batch") is not None:
                batch = common.check_str(query_dict.get("batch"))
        if "processor" in query_dict:
            if query_dict.get("processor") is not None:
                processor = common.from_list(query_dict.get("processor"), Processor.from_dict)
        if "id" in query_dict:
            if query_dict.get("id") is not None:
                id = common.check_str(query_dict.get("id"))
        if "submit_response" in query_dict:
            if query_dict.get("submit_response") is not None:
                submit_response = QueryResponse.from_dict(query_dict.get("submit_response"))
        if "status_response" in query_dict:
            if query_dict.get("status_response") is not None:
                status_response = QueryJob.from_dict(query_dict.get("status_response"))
        if "download_status" in query_dict:
            if query_dict.get("download_status") is not None:
                download_status = common.check_str(query_dict.get("download_status"))
        if "download_folder" in query_dict:
            if query_dict.get("download_folder") is not None:
                download_folder = common.check_str(query_dict.get("download_folder")) 
        if "download_file_name" in query_dict:
            if query_dict.get("download_file_name") is not None:
                download_file_name = common.check_str(query_dict.get("download_file_name"))
        if "merge_response" in query_dict:
            if query_dict.get("merge_response") is not None:
                merge_response = QueryJobLayers.from_dict(query_dict.get("merge_response"))
        if "merge_status" in query_dict:
            if query_dict.get("merge_status") is not None:
                merge_status = common.check_str(query_dict.get("merge_status"))
        return Query(name               = name, 
                     layers             = layers, 
                     temporal           = temporal, 
                     spatial            = spatial, 
                     output_type        = output_type, 
                     output_level       = output_level, 
                     description        = description, 
                     publish            = publish, 
                     notification       = notification, 
                     upload             = upload,
                     batch              = batch,
                     processor          = processor,
                     id                 = id,
                     submit_response    = submit_response,
                     status_response    = status_response,
                     download_status    = download_status,
                     download_folder    = download_folder,
                     download_file_name = download_file_name,
                     merge_response     = merge_response,
                     merge_status       = merge_status
                    )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.  
                  
        :rtype:                     dict
        """
        
        query_dict: dict = {}
        if self._name is not None:
            query_dict["name"] = self._name
        if self._layers is not None:
            query_dict["layers"] = common.from_list(self._layers, lambda item: common.class_to_dict(item, Layer))
        if self._temporal is not None:
            query_dict["temporal"] = common.class_to_dict(self._temporal, Temporal)
        if self._spatial is not None:
            query_dict["spatial"] = common.class_to_dict(self._spatial, Spatial)
        if self._output_type is not None:
            query_dict["output_type"] = self._output_type
        if self._output_level is not None:
            query_dict["output_level"] = self._output_level
        if self._description is not None:
            query_dict["description"] = self._description
        if self._publish is not None:
            query_dict["publish"] = self._publish
        if self._notification is not None:
            query_dict["notification"] = common.class_to_dict(self._notification, Notification)
        if self._upload is not None:
            query_dict["upload"] = common.class_to_dict(self._upload, Upload)
        if self._batch is not None:
            query_dict["batch"] = self._batch
        if self._processor is not None:
            query_dict["processor"] = common.from_list(self._processor, lambda item: common.class_to_dict(item, Processor))
        if self._id is not None:
            query_dict["id"] = self._id
        if self._submit_response is not None:
            query_dict["submit_response"] = common.class_to_dict(self._submit_response, QueryResponse)
        if self._status_response is not None:
            query_dict["status_response"] = common.class_to_dict(self._status_response, QueryJob)
        if self._download_status is not None:
            query_dict["download_status"] = self._download_status
        if self._download_folder is not None:
            query_dict["download_folder"] = self._download_folder
        if self._download_file_name is not None:
            query_dict["download_file_name"] = self._download_file_name
        if self._merge_response is not None:
            query_dict["merge_response"] = common.class_to_dict(self._merge_response, QueryJobLayers)
        if self._merge_status is not None:
            query_dict["merge_status"] = self._merge_status
        return query_dict
        
    #
    def to_dict_query_post(self):
        
        """
        Create a dictionary from the objects structure ready for a POST operation.   
                 
        :rtype:                     dict
        """
      
        query_dict: dict = {}
        if self._name is not None:
            query_dict["name"] = self._name
        if self._layers is not None:
            #query_dict["layers"] = common.from_list(self._layers, lambda item: common.class_to_dict(item, Layer))
            query_dict["layers"] = common.from_list(self._layers, lambda item: item.to_dict_layer_post())
        if self._temporal is not None:
            query_dict["temporal"] = common.class_to_dict(self._temporal, Temporal)
        if self._spatial is not None:
            query_dict["spatial"] = common.class_to_dict(self._spatial, Spatial)
        if self._output_type is not None:
            query_dict["outputType"] = self._output_type
        if self._output_level is not None:
            query_dict["outputLevel"] = self._output_level
        if self._description is not None:
            query_dict["description"] = self._description
        if self._publish is not None:
            query_dict["publish"] = self._publish
        if self._notification is not None:
            query_dict["notification"] = common.class_to_dict(self._notification, Notification)
        if self._upload is not None:
            query_dict["upload"] = common.class_to_dict(self._upload, Upload)
        if self._batch is not None:
            query_dict["batch"] = self._batch
        if self._processor is not None:
            query_dict["processor"] = common.from_list(self._processor, lambda item: item.to_dict())
        return query_dict
        
    #
    def from_json(query_json: Any):
        
        """
        Create a Query object from json (dictonary or str).
        
        :param query_dict:          A json dictionary that contains the keys of a Query or a string representation of a json dictionary.
        :type query_dict:           Any             
        :rtype:                     ibmpairs.query.Query
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(query_json, dict):
            query = Query.from_dict(query_json)
        elif isinstance(query_json, str):
            query_dict = json.loads(query_json)
            query = Query.from_dict(query_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_json), "query_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
        
    #
    def to_json_query_post(self):
        
        """
        Create a string representation of a json dictionary from the objects structure ready for a POST operation. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict_query_post())
    
    #
    def favorite(self,
                 id: str           = None,
                 client: cl.Client = None,
                 favorite_flag     = True,
                 verify: bool      = constants.GLOBAL_SSL_VERIFY
                ):
                  
        """
        A method to favorite a Query.
        
        :param id:            The Query ID to be made a favorite.
        :type id:             str
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param favorite_flag: Favorite flag.
        :type favorite_flag:  bool
        :param verify:        SSL verification
        :type verify:         bool
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              an ID is not provided or already held in the object, 
                              the status of the request is not 200.
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        if id is None:
            if self._id is not None:
                id = self._id
            else:
                msg = messages.ERROR_QUERY_FAVORITE_NO_ID
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            id = common.check_str(id)
            
        if favorite_flag == False:
            fav = "false"
        else:
            fav = "true"
            
        payload = "{\"flag\":" +  fav + "}"
        
        response = cli.put(url    = cli.get_host() + 
                                    constants.QUERY_JOBS_API + 
                                    id, 
                           body   = payload,
                           verify = verify)
                        
        if response.status_code != 200:
            msg = messages.ERROR_FAVORITE_STATUS_NOT_SUCCESSFUL.format('PUT', 'request', cli.get_host() + constants.QUERY_JOBS_API + id, response.status_code)
            logger.error(msg)
            raise common.PAWException(msg)

        else:            
            msg = messages.INFO_FAVORITE_STATUS_SUCCESS.format(id, fav)            
            logger.info(msg)


    #
    def unfavorite(self,
                   id: str           = None,
                   client: cl.Client = None,
                   verify: bool      = constants.GLOBAL_SSL_VERIFY
                  ):
                    
        """
        A method to unfavorite a Query.
        
        :param id:            The Query ID to be made not a favorite.
        :type id:             str
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              an ID is not provided or already held in the object, 
                              the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        self.favorite(id             = id,
                      client         = cli,
                      favorite_flag  = False,
                      verify         = verify
                     )
    
    #
    def replace_dates(self,
                      start_date: datetime,
                      end_date: datetime,
                      name = None
                     ):
        
        """
        A method to replace the dates in the Query object.
        
        :param start_date:  The new start date value.
        :type start_date:   str
        :param end_date:    The new end date value.
        :type end_date:     str
        :param name:        A new query name.
        :type name:         str
        """

        if name is not None:
            self._name = name     
        elif ((name is None) and (self._name is not None)):
            self._name = self._name
        else:
            self._name = "no_name"

        for layer in self._layers:
            temporal = Temporal(intervals = [])
            if layer.temporal is not None:
                if layer.temporal.intervals is not None:
                    for interval in layer.temporal.intervals:
                        interval._start = start_date.strftime(constants.QUERY_DATE_FORMAT)
                        interval._end   = end_date.strftime(constants.QUERY_DATE_FORMAT)
                        temporal._intervals.append(interval)
                
                    layer.set_temporal(temporal)
            if layer.alias is not None:
                alias_search = re.search(layer.id + '.[0-9]{1,13}>[0-9]{1,13}$', layer.alias, re.IGNORECASE)
                if alias_search is not None:
                    layer.alias = layer.id + "." + str(int(start_date.timestamp() * 1000)) + ">" + str(int(end_date.timestamp() * 1000))
                    
        temporal = Temporal(intervals = [])
            
        if self._temporal is not None:
            if self._temporal.intervals is not None:
                for interval in self._temporal.intervals:
                    interval._start = start_date.strftime(constants.QUERY_DATE_FORMAT)
                    interval._end   = end_date.strftime(constants.QUERY_DATE_FORMAT)
                    temporal._intervals.append(interval)
                
                self.set_temporal(temporal)
        else:
            interval = Interval(start = start_date.strftime(constants.QUERY_DATE_FORMAT),
                                end   = end_date.strftime(constants.QUERY_DATE_FORMAT)
                               )
            temporal._intervals.append(interval)
            self.set_temporal(temporal)

    #
    def is_bulk(self):
      
        """
        An internal method to determine if query is 'online' or bulk.
        
        :returns: A bulk flag indicator
        :rtype:   bool
        """

        bulk = False
        
        if ((self._spatial is not None) and (self._spatial.type is not None)):
            if self._spatial.type.lower() in ['point']:
                if ((self._batch is None) or (self._batch.lower() == 'false')):
                    bulk = False
                else:
                    bulk = True
            elif self._spatial.type.lower() in ['square', 'poly']:
                bulk = True
            else:
                msg = messages.ERROR_QUERY_TYPE_NOT_RECOGNIZED.format(str(self._spatial.type.lower()))
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            bulk = True 
            
        return bulk
        
    #        
    def list_files(self):
      
        """
        A method to list Query result files from the zip.
        
        :returns: A list of file paths for Query result files.
        :rtype:   List[str]
        """
        
        layer_files = []
        
        directory = self.get_download_folder() + self.get_download_file_name()
        for filename in os.listdir(directory):
            if filename.endswith(".tiff") or \
               filename.endswith(".tif") or  \
               filename.endswith(".csv") or  \
               filename.endswith(".json") or \
               filename.endswith(".png") or  \
               filename.endswith(".svg"):
                layer_files.append(os.path.join(directory, filename))
            else:
                continue
        
        return layer_files
        
    def point_data_as_dataframe(self):
        
        if self.submit_response.data is None:
            msg = messages.ERROR_QUERY_NO_POINT_DATA
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            try:
                if isinstance(self.submit_response.to_dict()["data"], str):
                    return pandas.read_csv(StringIO(str(self.submit_response.to_dict()["data"])))
                else:
                    return pandas.DataFrame(self.submit_response.to_dict()["data"])
            except Exception as e:
                msg = messages.ERROR_QUERY_COULD_NOT_LOAD_POINT_QUERY.format(e)
                logger.error(msg)
                raise common.PAWException(msg)

    #
    def submit(self,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY,
               compact_csv: bool = False
              ):
                
        """
        A method to submit a Query.

        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :param compact_csv:   A flag to indicate the return of a compact csv format.
        :type compact_csv:    bool
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              error making request to server, 
                              the status of the request is not 200.
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
            
            common.run_async_in_thread(self.async_submit, 
                                       query       = self, 
                                       client      = cli,
                                       verify      = verify,
                                       compact_csv = compact_csv)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("submit")
            logger.info(msg)
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_submit(query       = self, 
                                          client      = cli,
                                          verify      = verify,
                                          compact_csv = compact_csv
                                         )
                       )
        
        return self
                
    #
    def status(self,
               client: cl.Client    = None,
               id: str              = None,
               poll: bool           = True,
               status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
               verify: bool         = constants.GLOBAL_SSL_VERIFY
              ):
                
        """
        A method to check the status of a Query.

        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param id:              A Query ID, if None will use id in object.
        :type id:               str
        :param poll:            Whether the operation should poll until success.
        :type poll:             bool
        :param status_interval: How often the async run operation should call back.
        :type status_interval:  int
        :param verify:          SSL verification
        :type verify:           bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                the Query failed, 
                                error making request to server, 
                                the status of the request is not 200.
        """
        
        if id is not None:
            self.id = id
        
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
            
            msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("status")
            logger.info(msg)
            
            common.run_async_in_thread(self.async_status, query           = self, 
                                                          client          = cli,
                                                          poll            = poll,
                                                          status_interval = status_interval,
                                                          verify          = verify)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("status")
            logger.info(msg)
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_status(query           = self, 
                                          client          = cli,
                                          poll            = poll,
                                          status_interval = status_interval,
                                          verify          = verify
                                         )
                       )
        
        return self
    
    #
    def download(self,
                 client: cl.Client    = None,
                 id: str              = None,
                 status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                 download_folder      = None,
                 download_file_name   = None,
                 verify: bool         = constants.GLOBAL_SSL_VERIFY
                ):
                  
        """
        A method to download and unzip a Query result.
        
        :param client:             An IBM PAIRS Client.
        :type client:              ibmpairs.client.Client
        :param id:                 A Query ID, if None will use id in object.
        :type id:                  str
        :param status_interval:    How often the async run operation should call back.
        :type status_interval:     int
        :param download_folder:    A download folder (fixed or relative).
        :type download_folder:     str
        :param download_file_name: A file name for the download.
        :type download_file_name:  str
        :param verify:             SSL verification
        :type verify:              bool
        :raises Exception:         A ibmpairs.client.Client is not found, 
                                   the Query status failed, 
                                   the download folder could not be made or identified, 
                                   the download failed, 
                                   error making request to server, 
                                   the status of the request is not 200.
        """
                  
        if id is not None:
            self.id = id
        
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
            
            msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("download")
            logger.info(msg)
            
            common.run_async_in_thread(self.async_download, query              = self, 
                                                            client             = cli,
                                                            status_interval    = status_interval,
                                                            download_folder    = download_folder,
                                                            download_file_name = download_file_name,
                                                            verify             = verify)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("download")
            logger.info(msg)
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)        
            asyncio.run(self.async_download(query              = self, 
                                            client             = cli,
                                            status_interval    = status_interval,
                                            download_folder    = download_folder,
                                            download_file_name = download_file_name,
                                            verify             = verify
                                           )
                       )
        
        return self
                
    #
    def submit_and_check_status(self,
                                client: cl.Client    = None,
                                poll: bool           = True,
                                status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                                verify: bool         = constants.GLOBAL_SSL_VERIFY,
                                compact_csv: bool    = False
                               ):
                                
        """
        A method to submit and check the status of a Query.

        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param poll:            Whether the operation should poll until success.
        :type poll:             bool
        :param status_interval: How often the async run operation should check for status (seconds).
        :type status_interval:  int
        :param verify:          SSL verification
        :type verify:           bool
        :param compact_csv:     A flag to indicate the return of a compact csv format.
        :type compact_csv:      bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                the Query failed, 
                                error making request to server, 
                                the status of the request is not 200.
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
            
            common.run_async_in_thread(self.async_submit_and_check_status, query              = self, 
                                                                           client             = cli,
                                                                           poll               = poll,
                                                                           status_interval    = status_interval,
                                                                           verify             = verify,
                                                                           compact_csv        = compact_csv)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("submit_and_check_status")
            logger.info(msg)
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_submit_and_check_status(query              = self, 
                                                           client             = cli,
                                                           poll               = poll,
                                                           status_interval    = status_interval,
                                                           verify             = verify,
                                                           compact_csv        = compact_csv
                                                          )
                       )
        
        return self
                
    #
    def check_status_and_download(self,
                                  client: cl.Client    = None,
                                  id: str              = None,
                                  poll: bool           = True,
                                  status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                                  download_folder      = 'download',
                                  download_file_name   = None,
                                  verify: bool         = constants.GLOBAL_SSL_VERIFY
                                 ):
                                  
        """
        A method to check the status of a Query then download the result.

        :param client:             An IBM PAIRS Client.
        :type client:              ibmpairs.client.Client
        :param id:                 A Query ID, if None will use id in object.
        :type id:                  str
        :param poll:               Whether the operation should poll until success.
        :type poll:                bool
        :param status_interval:    How often the async run operation should call back.
        :type status_interval:     int
        :param download_folder:    A download folder (fixed or relative).
        :type download_folder:     str
        :param download_file_name: A file name for the download.
        :type download_file_name:  str
        :param verify:             SSL verification
        :type verify:              bool
        :param compact_csv:        A flag to indicate the return of a compact csv format.
        :type compact_csv:         bool
        :raises Exception:         A ibmpairs.client.Client is not found, 
                                   the Query status failed, 
                                   the download folder could not be made or identified, 
                                   the download failed, 
                                   error making request to server, 
                                   the status of the request is not 200.
        """
        
        if id is not None:
            self.id = id
        
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
            
            msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("check_status_and_download")
            logger.info(msg)
            
            common.run_async_in_thread(self.async_check_status_and_download, query              = self, 
                                                                             client             = cli,
                                                                             poll               = poll,
                                                                             status_interval    = status_interval,
                                                                             download_folder    = download_folder,
                                                                             download_file_name = download_file_name,
                                                                             verify             = verify)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("check_status_and_download")
            logger.info(msg)
        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_check_status_and_download(query              = self, 
                                                             client             = cli,
                                                             poll               = poll,
                                                             status_interval    = status_interval,
                                                             download_folder    = download_folder,
                                                             download_file_name = download_file_name,
                                                             verify             = verify))
        
        return self
                
    
    def submit_check_status_and_download(self,
                                         client: cl.Client    = None,
                                         poll: bool           = True,
                                         status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                                         download_folder      = None,
                                         download_file_name   = None,
                                         verify: bool         = constants.GLOBAL_SSL_VERIFY,
                                         compact_csv: bool    = False
                                        ):
                                          
        """
        A method to submit a Query check the status then download the result.

        :param client:             An IBM PAIRS Client.
        :type client:              ibmpairs.client.Client
        :param poll:               Whether the operation should poll until success.
        :type poll:                bool
        :param status_interval:    How often the async run operation should call back.
        :type status_interval:     int
        :param download_folder:    A download folder (fixed or relative).
        :type download_folder:     str
        :param download_file_name: A file name for the download.
        :type download_file_name:  str
        :param verify:             SSL verification
        :type verify:              bool
        :param compact_csv:        A flag to indicate the return of a compact csv format.
        :type compact_csv:         bool
        :raises Exception:         A ibmpairs.client.Client is not found, 
                                   the Query status failed, 
                                   the download folder could not be made or identified, 
                                   the download failed, 
                                   error making request to server, 
                                   the status of the request is not 200.
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
            
            msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("submit_check_status_and_download")
            logger.info(msg)
            
            common.run_async_in_thread(self.async_submit_check_status_and_download, query              = self, 
                                                                                    client             = cli,
                                                                                    poll               = poll,
                                                                                    status_interval    = status_interval,
                                                                                    download_folder    = download_folder,
                                                                                    download_file_name = download_file_name,
                                                                                    verify             = verify,
                                                                                    compact_csv        = compact_csv)
            
            msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("submit_check_status_and_download")
            logger.info(msg)

        else:
            msg = messages.INFO_STARTING_EVENT_LOOP
            logger.info(msg)
            asyncio.run(self.async_submit_check_status_and_download(query              = self, 
                                                                    client             = cli,
                                                                    poll               = poll,
                                                                    status_interval    = status_interval,
                                                                    download_folder    = download_folder,
                                                                    download_file_name = download_file_name,
                                                                    verify             = verify,
                                                                    compact_csv        = compact_csv))
        
        return self

    #
    def merge_query_into_base(self,
                              other_job_id,
                              base_job_id    = None,
                              client         = None,
                              verify: bool   = constants.GLOBAL_SSL_VERIFY
                             ):
                              
        """
        A method to merge a Query into a base Query on the server side.
        
        :param other_job_id:  The ID of the job to be merged.
        :type other_job_id:   str or int
        :param base_job_id:   The ID of the base job to be merged to.
        :type base_job_id:    str or int
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              other job ID is not provided, 
                              base job ID is not provided or already held in the object, 
                              the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        base_id  = None
        other_id = None

        if other_job_id is not None:
            if isinstance(other_job_id, Query):
                other_id = common.check_str(other_job_id.id)
            elif isinstance(other_job_id, str):
                other_id = common.check_str(other_job_id)
            else:
                msg = messages.ERROR_QUERY_MERGE_ID_NOT_RECOGNIZED.format('other')
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            msg = messages.ERROR_QUERY_MERGE_OTHER_ID_MISSING
            logger.error(msg)
            raise common.PAWException(msg)

        if base_job_id is not None:
            if isinstance(base_job_id, Query):
                base_id = common.check_str(base_job_id.id)
            elif isinstance(base_job_id, str):
                base_id = common.check_str(base_job_id)
            else:
                msg = messages.ERROR_QUERY_MERGE_ID_NOT_RECOGNIZED.format('base')
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            if self.id is not None:
                base_id = self._id
            else:
                msg = messages.ERROR_QUERY_MERGE_BASE_ID_MISSING
                logger.error(msg)
                raise common.PAWException(msg)
        
        response = cli.put(url = cli.get_host() +
                                 constants.QUERY_JOBS_API +
                                 str(base_id) +
                                 constants.QUERY_JOBS_API_MERGE +
                                 str(other_id),
                           verify = verify
                          )
        
        if response.status_code != 200:
            error_message = 'failed'
            
            if response.status_code == 401:
                error_message = messages.ERROR_QUERY_MERGE_UNAUTHORIZED
            elif response.status_code == 404:
                error_message = messages.ERROR_QUERY_MERGE_NOT_FOUND
            elif response.status_code == 412:
                error_message = messages.ERROR_QUERY_MERGE_PRECONDITION
            
            self.merge_status   = "FAILED"
            
            msg = messages.ERROR_QUERY_MERGE_NOT_SUCCESSFUL.format('PUT', 'request', constants.QUERY_JOBS_API + str(base_id) + constants.QUERY_JOBS_API_MERGE + str(other_id), response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
            
        else:
            msg = messages.INFO_QUERY_MERGE_SUCCESS.format(other_id, base_id)
            logger.info(msg)
            query_merge_json = response.json()

            self.merge_response = query_job_layers_from_dict(query_merge_json)
            self.merge_status   = "SUCCEEDED"
        
        return self
    
    #
    async def async_submit(self,
                           query,
                           client: cl.Client = None,
                           verify: bool      = constants.GLOBAL_SSL_VERIFY,
                           compact_csv: bool = False
                          ):
                            
        """
        An asynchronous method to submit a Query.
        
        :param query:         The Query to submit.
        :type query:          ibmpairs.query.Query
        :param client:        An IBM PAIRS Client.
        :type client:         ibmpairs.client.Client
        :param verify:        SSL verification
        :type verify:         bool
        :param compact_csv:   A flag to indicate the return of a compact csv format.
        :type compact_csv:    bool
        :raises Exception:    A ibmpairs.client.Client is not found, 
                              query is not present, 
                              error making request to server, 
                              the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
                            
        query_json = query.to_dict_query_post()

        try:
            if compact_csv:
                headers = constants.CLIENT_PUT_AND_POST_HEADER_CSV
            else:
                headers = constants.CLIENT_PUT_AND_POST_HEADER
                
            response = await cli.async_post(url = cli.get_host() + 
                                            constants.QUERY_API,
                                            headers = headers,
                                            body    = query_json,
                                            verify  = verify
                                           )

        except Exception as e:
            msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('POST', 'request', cli.get_host() + constants.QUERY_API, e)
            logger.error(msg)
            raise common.PAWException(msg)

        if response.status != 200:
            error_message = 'FAILED'
            
            if response.body is not None:
                try:
                    query_response = query_response_from_json(response.body, 
                                                              compact_csv = compact_csv)
                    error_message = query_response.message
                    query.submit_response = query_response
                except:
                    msg = messages.INFO_QUERY_RESPONSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE
                    logger.info(msg)
            else:
                error_response = {"message":"FAILED"}
                query_response = query_response_from_dict(error_response)
                query.submit_response = query_response

            msg = messages.ERROR_QUERY_RESPOSE_NOT_SUCCESSFUL.format('POST', 'request', cli.get_host() + 
                            constants.QUERY_API, response.status, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
        else:
            query_response = query_response_from_json(response.body,
                                                      compact_csv = compact_csv)
            
            query.submit_response = query_response
            
            bulk = self.is_bulk()

            if bulk is True:
                query.id = query_response.id
                msg = messages.INFO_QUERY_SUBMIT_SUCCESS.format(str(query.id))            
                logger.info(msg)
            
    #
    async def async_status(self,
                           query,
                           client: cl.Client    = None,
                           poll: bool           = True,
                           status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                           verify: bool         = constants.GLOBAL_SSL_VERIFY
                          ):
                            
        """
        An asynchronous method to check the status of a Query.
        
        :param query:           The Query to check the status of.
        :type query:            ibmpairs.query.Query
        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param poll:            Whether the operation should poll until success.
        :type poll:             bool
        :param status_interval: How often the async run operation should call back.
        :type status_interval:  int
        :param verify:          SSL verification
        :type verify:           bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                query is not present, 
                                the Query failed, 
                                error making request to server, 
                                the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
                            
        bulk = self.is_bulk()

        if bulk is True:
            
            if query.id is None:
                msg = messages.ERROR_QUERY_STATUS_ID_NOT_PRESENT
                logger.error(msg)
              
                qj = QueryJob(status = msg)
                query.status_response = qj
                poll       = False
                incomplete = False
              
                raise common.PAWException(msg)
        
            incomplete = True

            while incomplete:
                
                try:
                    response = await cli.async_get(url = cli.get_host() +
                                                         constants.QUERY_JOBS_API +
                                                         str(query.id),
                                                   verify = verify
                                                  )
                except Exception as e:
                    msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.QUERY_JOBS_API + str(query.id), e)
                    logger.error(msg)
                    response = cl.ClientResponse(status = -999, 
                                                 body = r"""{"status":"Unspecified Server Error"}"""
                                                )
                
                if response.status == 200:
                    query.status_response = query_job_from_json(response.body)
                    
                    msg = messages.INFO_QUERY_STATUS.format(query.id, query.status_response.status)
                    logger.info(msg)
                    
                    if poll == False:
                        incomplete = False
                    
                    # Queued(0)
                    # Initializing(1)
                    # Running(10)
                    # Writing(11)
                    # Packaging(12)
                    # Succeeded(20)
                    # NoDataFound(21)
                    # Killed(30)
                    # Deleted(31)
                    # Failed(40)
                    # FailedConversion(41)
                    
                    if query.status_response.status_code in constants.QUERY_STATUS_RUNNING_CODES:
                        pass
                    elif query.status_response.status_code in constants.QUERY_STATUS_SUCCESS_CODES:
                        msg = messages.INFO_QUERY_SUCCESS.format(query.id)
                        logger.info(msg)

                        incomplete = False

                    elif query.status_response.status_code in constants.QUERY_STATUS_FAILURE_CODES:
                        msg = messages.ERROR_QUERY_FAILED.format(query.id, query.status_response.status, '.')
                        logger.error(msg)

                        incomplete = False  

                    else:
                        msg = messages.ERROR_QUERY_UNKNOWN_STATE.format(query.id, query.status_response.status_code)
                        logger.error(msg)
                        
                        incomplete = False

                else:
                    msg = messages.ERROR_QUERY_STATUS_HTTP_RESPONSE_CODE.format(response.status)
                    logger.error(msg)
                    
                    qj = QueryJob(status = "FAILED: " + str(response.status))
                    query.status_response = qj

                    incomplete = False
                    
                    raise common.PAWException(msg)
                
                if poll == True:
                    await asyncio.sleep(status_interval)
        
        else:
            msg = messages.INFO_REAL_TIME_POINT_QUERY_STATUS_SKIP
            logger.info(msg)
            
            qj = QueryJob(status = msg)
            query.status_response = qj
            poll       = False
            incomplete = False
            
    #    
    async def async_download(self,
                             query,
                             client: cl.Client    = None,
                             status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                             download_folder      = None,
                             download_file_name   = None,
                             verify: bool         = constants.GLOBAL_SSL_VERIFY
                            ):
                              
        """
        An asynchronous method to download and unzip a Query result.
        
        :param query:              The Query to check the status of and download.
        :type query:               ibmpairs.query.Query
        :param client:             An IBM PAIRS Client.
        :type client:              ibmpairs.client.Client
        :param status_interval:    How often the async run operation should call back.
        :type status_interval:     int
        :param download_folder:    A download folder (fixed or relative).
        :type download_folder:     str
        :param download_file_name: A file name for the download.
        :type download_file_name:  str
        :param verify:             SSL verification
        :type verify:              bool
        :raises Exception:         A ibmpairs.client.Client is not found, 
                                   query is not present, 
                                   the Query status failed, 
                                   the download folder could not be made or identified, 
                                   the download failed, 
                                   error making request to server, 
                                   the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
                        
        self.download_status = "SKIPPED"
        
        bulk = self.is_bulk()

        if bulk is True:
          
            self.download_status = "INDETERMINATE"
          
            if download_folder is not None:
                self.download_folder     = common.ensure_slash(download_folder, -1)
            else:
                if self.download_folder is None:
                    self.download_folder = constants.QUERY_DOWNLOAD_DEFAULT_FOLDER

            if download_file_name is not None:
                self.download_file_name  = download_file_name
            
            if self.download_file_name is None:
                self.download_file_name  = self.id
            
            incomplete = True

            while incomplete:
            
                await query.async_status(query  = query,
                                         client = cli,
                                         poll   = False,
                                         verify = verify
                                        )
            
                # Queued(0)
                # Initializing(1)
                # Running(10)
                # Writing(11)
                # Packaging(12)
                # Succeeded(20)
                # NoDataFound(21)
                # Killed(30)
                # Deleted(31)
                # Failed(40)
                # FailedConversion(41)

                if query.status_response.status_code == 20:
                    
                    # Check download_path exists as relative, fixed or create.
                    if os.path.exists(os.path.join(os.getcwd(), self.download_folder)):
                        
                        self.download_folder = common.ensure_slash(os.path.join(os.getcwd(), self.download_folder), -1)
                        
                        msg = messages.INFO_QUERY_DOWNLOAD_PATH_SET.format(self.download_folder)
                        logger.info(msg)

                    elif os.path.exists(self.download_folder):
                        
                        self.download_folder = common.ensure_slash(self.download_folder, -1)
                                            
                        msg = messages.INFO_QUERY_DOWNLOAD_PATH_SET.format(self.download_folder)
                        logger.info(msg)

                    else:
                        try: 
                            msg = messages.WARN_QUERY_DOWNLOAD_PATH_CREATE.format(self.download_folder)
                            logger.warn(msg)
                            
                            self.download_folder = common.ensure_slash(os.path.join(os.getcwd(), self.download_folder), -1)
                            
                            msg = messages.INFO_QUERY_DOWNLOAD_PATH_SET.format(self.download_folder)
                            logger.info(msg)
                                                
                            os.makedirs(os.path.join(os.getcwd(), self.download_folder))
                                                
                            msg = messages.INFO_QUERY_DOWNLOAD_PATH_CREATED.format(self.download_folder)
                            logger.info(msg)

                        except:
                            self.download_status = "FAILED"
                                                
                            msg = messages.ERROR_QUERY_DOWNLOAD_PATH_CREATED.format(self.download_folder)
                            logger.error(msg)
                            raise common.PAWException(msg)
                                                
                            incomplete = False
                    
                    download_zip    = self.get_download_folder() + self.get_download_file_name() + '.zip'
                    download_target = self.get_download_folder() + self.get_download_file_name()
                    
                    try:
                        response = await cli.async_get(url           = cli.get_host() +
                                                                       constants.QUERY_JOBS_DOWNLOAD_API +
                                                                       str(query.id),
                                                       verify        = verify,
                                                       response_type = 'bytes'
                                                      )
                    except Exception as e:
                        self.download_status = "FAILED"
                        msg = messages.ERROR_CLIENT_UNSPECIFIED_ERROR.format('GET', 'request', cli.get_host() + constants.QUERY_JOBS_DOWNLOAD_API + str(query.id), e)
                        logger.error(msg)
                        raise common.PAWException(msg)
                    
                    # Download file
                    try:
                      
                        msg = messages.INFO_QUERY_DOWNLOAD_FILE_SAVE.format(query.id, download_zip)
                        logger.info(msg)
                        
                        with open(download_zip, 'wb') as f:
                            f.write(response.body)
                        f.close
                        
                        msg = messages.INFO_QUERY_DOWNLOAD_FILE_SAVED.format(query.id, download_zip)
                        logger.info(msg)
                        
                    except:
                        self.download_status = "FAILED"
                        
                        msg = messages.ERROR_QUERY_DOWNLOAD_UNSUCCESSFUL.format(query.id, download_zip)
                        logger.error(msg)
                        raise common.PAWException(msg)
                        
                        incomplete = False
                    
                    # Unzip file
                    try:
                        msg = messages.INFO_QUERY_DOWNLOAD_FILE_UNZIP.format(download_zip, download_target)
                        logger.info(msg)
                        
                        with zipfile.ZipFile(download_zip, 'r') as z:
                            z.extractall(download_target)
                        z.close  
                        
                        msg = messages.INFO_QUERY_DOWNLOAD_FILE_UNZIPPED.format(download_zip, download_target)
                        logger.info(msg)
                        
                        self.download_status = "SUCCEEDED"
                        
                        incomplete = False
                        
                    except:
                        self.download_status = "FAILED"
                        
                        messages.ERROR_QUERY_DOWNLOAD_UNSUCCESSFUL_UNZIP.format(download_zip, download_target)
                        logger.error(msg)
                        raise common.PAWException(msg)
                        
                        incomplete = False
                    
                elif query.status_response.status_code in [0, 1, 10, 11, 12]:
                    await query.async_status(query  = query,
                                             client = cli
                                            )
                                            
                elif query.status_response.status_code == 31:
                    self.download_status = "FAILED"
                    
                    msg = messages.ERROR_QUERY_DELETED.format(query.id)
                    logger.error(msg)
                    raise common.PAWException(msg)
                    
                    incomplete = False 
                    
                else:
                    self.download_status = "FAILED"
                    
                    msg = messages.ERROR_QUERY_FAILED.format(query.id, query.status_response.status, ' and therefore cannot be downloaded.')
                    logger.error(msg)
                    raise common.PAWException(msg)
                    
                    incomplete = False
                    
                await asyncio.sleep(status_interval)

        else:
            if self.submit_response is not None and self.submit_response.data is not None:
                  
                  if len(self.submit_response.data) > 0:
                      
                      if download_folder is not None:
                          self.download_folder        = common.ensure_slash(download_folder, -1)
                      else:
                          if self.download_folder is None:
                              self.download_folder    = common.ensure_slash(constants.QUERY_DOWNLOAD_DEFAULT_FOLDER, -1)

                      if download_file_name is not None:
                          self.download_file_name     = download_file_name
                      
                      if self.download_file_name is None:
                          if self.name is not None:
                              self.download_file_name = self.name
                          else:
                              file_name = "point_query_" + datetime.now().strftime("%Y%m%d-%H%M%S")
                              self.download_file_name = file_name
                      try:
                          download_target = self.get_download_folder() + self.get_download_file_name()
                      
                          with open(download_target, 'w') as f:
                              f.write(str(self.submit_response.data))
                          f.close
                      
                          msg = messages.INFO_POINT_QUERY_DOWNLOAD_FILE_SAVED.format(download_target)
                          logger.info(msg)
                      
                          self.download_status = "SUCCEEDED"
                      except:
                          self.download_status = "FAILED"
                          
                          messages.ERROR_POINT_QUERY_DOWNLOAD_UNSUCCESSFUL.format(download_target)
                          logger.error(msg)
                          raise common.PAWException(msg)
                      
                  else:
                      msg = messages.INFO_REAL_TIME_POINT_QUERY_NO_DATA
                      logger.info(msg)
            else:
                msg = messages.INFO_REAL_TIME_POINT_QUERY_NO_DATA
                logger.info(msg)
            
    #
    async def async_submit_and_check_status(self,
                                            query,
                                            client: cl.Client    = None,
                                            poll: bool           = True,
                                            status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                                            verify: bool         = constants.GLOBAL_SSL_VERIFY,
                                            compact_csv: bool    = False
                                           ):
                                            
        """
        An asynchronous method to submit and check the status of a Query.
        
        :param query:           The Query to perform the operations on.
        :type query:            ibmpairs.query.Query
        :param client:          An IBM PAIRS Client.
        :type client:           ibmpairs.client.Client
        :param poll:            Whether the operation should poll until success.
        :type poll:             bool
        :param status_interval: How often the async run operation should check for status (seconds).
        :type status_interval:  int
        :param verify:          SSL verification
        :type verify:           bool
        :param compact_csv:     A flag to indicate the return of a compact csv format.
        :type compact_csv:      bool
        :raises Exception:      A ibmpairs.client.Client is not found, 
                                query is not present, 
                                the Query failed, 
                                error making request to server, 
                                the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        await self.async_submit(query       = query, 
                                client      = cli,
                                verify      = verify,
                                compact_csv = compact_csv
                               )

        await self.async_status(query           = query, 
                                client          = cli,
                                poll            = poll,
                                status_interval = status_interval,
                                verify          = verify
                               )
    
    #
    async def async_check_status_and_download(self,
                                              query,
                                              client: cl.Client    = None,
                                              poll: bool           = True,
                                              status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                                              download_folder      = None,
                                              download_file_name   = None,
                                              verify: bool         = constants.GLOBAL_SSL_VERIFY
                                             ):
        
        """
        An asynchronous method to check the status of a Query then download the result.
        
        :param query:              The Query to perform the operations on.
        :type query:               ibmpairs.query.Query
        :param client:             An IBM PAIRS Client.
        :type client:              ibmpairs.client.Client
        :param poll:               Whether the operation should poll until success.
        :type poll:                bool
        :param status_interval:    How often the async run operation should call back.
        :type status_interval:     int
        :param download_folder:    A download folder (fixed or relative).
        :type download_folder:     str
        :param download_file_name: A file name for the download.
        :type download_file_name:  str
        :param verify:             SSL verification
        :type verify:              bool
        :raises Exception:         A ibmpairs.client.Client is not found, 
                                   query is not present, 
                                   the Query status failed, 
                                   the download folder could not be made or identified, 
                                   the download failed, 
                                   error making request to server, 
                                   the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        await self.async_status(query           = query, 
                                client          = cli,
                                poll            = poll,
                                status_interval = status_interval,
                                verify          = verify
                               )
                            
        await self.async_download(query              = query, 
                                  client             = cli,
                                  status_interval    = status_interval,
                                  download_folder    = download_folder,
                                  download_file_name = download_file_name,
                                  verify             = verify
                                 )

    #
    async def async_submit_check_status_and_download(self,
                                                     query,
                                                     client: cl.Client    = None,
                                                     poll: bool           = True,
                                                     status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                                                     download_folder      = None,
                                                     download_file_name   = None,
                                                     verify: bool         = constants.GLOBAL_SSL_VERIFY,
                                                     compact_csv: bool    = False
                                                    ):

        """
        An asynchronous method to submit a Query check the status then download the result.
        
        :param query:              The Query to perform the operations on.
        :type query:               ibmpairs.query.Query
        :param client:             An IBM PAIRS Client.
        :type client:              ibmpairs.client.Client
        :param poll:               Whether the operation should poll until success.
        :type poll:                bool
        :param status_interval:    How often the async run operation should call back.
        :type status_interval:     int
        :param download_folder:    A download folder (fixed or relative).
        :type download_folder:     str
        :param download_file_name: A file name for the download.
        :type download_file_name:  str
        :param verify:             SSL verification
        :type verify:              bool
        :param compact_csv:        A flag to indicate the return of a compact csv format.
        :type compact_csv:         bool
        :raises Exception:         A ibmpairs.client.Client is not found, 
                                   query is not present, 
                                   the Query status failed, 
                                   the download folder could not be made or identified, 
                                   the download failed, 
                                   error making request to server, 
                                   the status of the request is not 200.
        """                                     
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
        
        await self.async_submit(query       = query, 
                                client      = cli,
                                verify      = verify,
                                compact_csv = compact_csv
                               )

        await self.async_status(query           = query, 
                                client          = cli,
                                poll            = poll,
                                status_interval = status_interval,
                                verify          = verify
                               )
                            
        await self.async_download(query              = query, 
                                  client             = cli,
                                  status_interval    = status_interval,
                                  download_folder    = download_folder,
                                  download_file_name = download_file_name,
                                  verify             = verify
                                 )
                
#        
async def query_worker(queries: List[Query],
                       client: cl.Client,
                       status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                       workers: int         = QUERY_DEFAULT_WORKERS,
                       submit: bool         = True,
                       status: bool         = True,
                       download: bool       = True,
                       verify: bool         = constants.GLOBAL_SSL_VERIFY,
                       compact_csv: bool    = False
                      ):
                        
    """
    An asynchronous method to operate and await a number of submit, status and download calls.
    
    :param queries:         A list of queries.
    :type queries:          List[ibmpairs.query.Query]
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param status_interval: How often the async run operation should call back.
    :type status_interval:  int
    :param workers:         How many async operations should run contemporaneously.
    :type workers:          int
    :param submit:          Whether submit should be run.
    :type submit:           bool
    :param status:          Whether status check should be run.
    :type status:           bool
    :param download:        Whether download should be run.
    :type download:         bool
    :param verify:          SSL verification
    :type verify:           bool
    :param compact_csv:     A flag to indicate the return of a compact csv format.
    :type compact_csv:      bool
    :returns:               A list of queries.
    :rtype:                 List[ibmpairs.query.Query]
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    cli.session()

    tasks = set()
    for query in queries:
        if len(tasks) >= workers:
            # Wait for some download to finish before adding a new one
            _done, tasks = await asyncio.wait(tasks, 
                                              return_when = asyncio.FIRST_COMPLETED
                                             )
        if ((submit and status and download) or ((submit and download) and not (status))):
            msg = messages.INFO_QUERY_RUNNER_MUST_CHECK_STATUS
            logger.info(msg)
            tasks.add(asyncio.create_task(query.async_submit_check_status_and_download(query = query, 
                                                                                       client = cli,
                                                                                       status_interval = status_interval,
                                                                                       verify = verify,
                                                                                       compact_csv = compact_csv
                                                                                      )))
        elif (status and download) and not (submit):
            tasks.add(asyncio.create_task(query.async_submit_and_check_status(query = query, 
                                                                              client = cli,
                                                                              status_interval = status_interval,
                                                                              verify = verify,
                                                                              compact_csv = compact_csv
                                                                             )))
        elif (submit and status) and not (download):
            tasks.add(asyncio.create_task(query.async_check_status_and_download(query = query, 
                                                                                client = cli,
                                                                                status_interval = status_interval,
                                                                                verify = verify
                                                                               )))
        elif (status) and not (submit and download):
            tasks.add(asyncio.create_task(query.async_status(query = query, 
                                                             client = cli,
                                                             status_interval = status_interval,
                                                             verify = verify
                                                            )))
        elif (download) and not (submit and status):
            tasks.add(asyncio.create_task(query.async_download(query = query, 
                                                               client = cli,
                                                               status_interval = status_interval,
                                                               verify = verify
                                                              )))
        else:
            msg = messages.ERROR_QUERY_RUNNER_CHOICE_INVALID.format(submit, status, download)
            logger.error(msg)
            raise common.PAWException(msg)
            

    # Wait for the remaining uploads to finish
    await asyncio.wait(tasks)

    return(queries)

#
def batch_query(queries: List[Query],
                client: cl.Client    = None,
                status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                workers: int         = QUERY_DEFAULT_WORKERS,
                submit: bool         = True,
                status: bool         = True,
                download: bool       = True,
                verify: bool         = constants.GLOBAL_SSL_VERIFY,
                compact_csv: bool    = False
               ):
                
    """
    A method to gather a number of batched queries using the query_worker method.
    
    :param queries:         A list of queries.
    :type queries:          List[ibmpairs.query.Query]
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param status_interval: How often the async run operation should call back.
    :type status_interval:  int
    :param workers:         How many async operations should run contemporaneously.
    :type workers:          int
    :param submit:          Whether submit should be run.
    :type submit:           bool
    :param status:          Whether status check should be run.
    :type status:           bool
    :param download:        Whether download should be run.
    :type download:         bool
    :param verify:          SSL verification
    :type verify:           bool
    :param compact_csv:     A flag to indicate the return of a compact csv format.
    :type compact_csv:      bool
    :returns:               A list of queries.
    :rtype:                 List[ibmpairs.query.Query]
    """
                
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)

    if status_interval < constants.QUERY_MIN_STATUS_INTERVAL:
        msg = messages.ERROR_QUERY_STATUS_INTERVAL.format(status_interval, constants.QUERY_MIN_STATUS_INTERVAL)
        logger.error(msg)
        raise common.PAWException(msg)

    if workers > constants.QUERY_MAX_WORKERS:
        msg = messages.ERROR_QUERY_EXCEED_MAX_WORKERS.format(workers, constants.QUERY_MAX_WORKERS)
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
      
        msg = messages.INFO_FOUND_EVENT_LOOP_STARTING_TASK.format("batch_query")
        logger.info(msg)
      
        result = common.run_async_in_thread(query_worker, queries         = queries, 
                                                          client          = cli,
                                                          status_interval = status_interval,
                                                          workers         = workers,
                                                          submit          = submit,
                                                          status          = status,
                                                          download        = download,
                                                          verify          = verify,
                                                          compact_csv     = compact_csv
                                            )
      
        msg = messages.INFO_FOUND_EVENT_LOOP_COMPLETED_TASK.format("batch_query")
        logger.info(msg)
    else:
        msg = messages.INFO_STARTING_EVENT_LOOP
        logger.info(msg)
        result = asyncio.run(query_worker(queries         = queries, 
                                          client          = cli,
                                          status_interval = status_interval,
                                          workers         = workers,
                                          submit          = submit,
                                          status          = status,
                                          download        = download,
                                          verify          = verify,
                                          compact_csv     = compact_csv
                                         ),
                             debug = constants.QUERY_WORKER_DEBUG
                            )

    return(result)

#
class Group:
    #_id: int
    #_name: str
    
    """
    A representation of a Group.
    
    :param id:   The Group ID.
    :type id:    int
    :param name: The Group name.
    :type name:  str
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
    def from_dict(group_dict: Any):

        """
        Create a Group object from a dictionary.
        
        :param group_dict:          A dictionary that contains the keys of an Group.
        :type group_dict:           Any             
        :rtype:                     ibmpairs.query.Group
        :raises Exception:          if not a dictionary.
        """
        
        id   = None
        name = None
        
        common.check_dict(group_dict)
        if "id" in group_dict:
            if group_dict.get("id") is not None:
                id = common.check_int(group_dict.get("id"))
        if "name" in group_dict:
            if group_dict.get("name") is not None:
                name = common.check_str(group_dict.get("name"))

        return Group(id   = id, 
                     name = name
                    )

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure.            
        :rtype:                     dict
        """
        
        group_dict: dict = {}
        if self._id is not None:
            group_dict["id"] = self._id
        if self._name is not None:
            group_dict["name"] = self._name
        return group_dict
        
    #
    def from_json(group_json: Any):

        """
        Create a Group object from json (dictonary or str).
        
        :param group_dict:        A json dictionary that contains the keys of a Group or a string representation of a json dictionary.
        :type group_dict:         Any             
        :rtype:                     ibmpairs.query.Group
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(group_json, dict):
            group = Group.from_dict(group_json)
        elif isinstance(group_json, str):
            group_dict = json.loads(group_json)
            group = Group.from_dict(group_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(group_json), "group_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return group

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
    
#
class User:
    #_id: str
    #_login: str
    #_group: Group
    #_email: str
    #_company: str
    #_admin: str
    #_secondary_groups: List[Group]
    
    """
    A representation of a User.
    
    :param id:               The User ID.
    :type id:                int
    :param login:            The User login name.
    :type login:             str
    :param group:            A Users primary Group.
    :type group:             ibmpairs.query.Group
    :param email:            A Users email address.
    :type email:             str
    :param company:          The Users company name.
    :type company:           str
    :param admin:            Whether a user is an administrator.
    :type admin:             str
    :param secondary_groups: A list of secondary groups to which a user belongs.
    :type secondary_groups:  List[ibmpairs.query.Group]
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
                 id: str                       = None, 
                 login: str                    = None,
                 group: Group                  = None,
                 email: str                    = None,
                 company: str                  = None,
                 admin: str                    = None,
                 secondary_groups: List[Group] = None
                ):
        self._id               = id
        self._login            = login
        self._group            = group
        self._email            = email
        self._company          = company
        self._admin            = admin
        self._secondary_groups = secondary_groups

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
    def get_login(self):
        return self._login

    #
    def set_login(self, login):
        self._login = common.check_str(login)

    #    
    def del_login(self): 
        del self._login

    #    
    login = property(get_login, set_login, del_login) 
    
    #
    def get_group(self):
        return self._group

    #
    def set_group(self, group):
        self._group = common.check_class(group, Group)

    #    
    def del_group(self): 
        del self._group

    #    
    group = property(get_group, set_group, del_group)
    
    #
    def get_email(self):
        return self._email

    #
    def set_email(self, email):
        self._email = common.check_str(email)

    #    
    def del_email(self): 
        del self._email

    #    
    email = property(get_email, set_email, del_email) 
    
    #
    def get_company(self):
        return self._company

    #
    def set_company(self, company):
        self._company = common.check_str(company)

    #    
    def del_company(self): 
        del self._company

    #    
    company = property(get_company, set_company, del_company) 
    
    #
    def get_admin(self):
        return self._admin

    #
    def set_admin(self, admin):
        self._admin = common.check_str(admin)

    #    
    def del_admin(self): 
        del self._admin

    #    
    admin = property(get_admin, set_admin, del_admin) 
    
    #
    def get_secondary_groups(self):
        return self._secondary_groups

    #
    def set_secondary_groups(self, secondary_groups):
        self._secondary_groups = common.check_list(secondary_groups)

    #    
    def del_secondary_groups(self): 
        del self._secondary_groups

    #    
    secondary_groups = property(get_secondary_groups, set_secondary_groups, del_secondary_groups) 

    #
    def from_dict(user_dict: Any):
        
        """
        Create a User object from a dictionary.
        
        :param user_dict:           A dictionary that contains the keys of an User.
        :type user_dict:            Any             
        :rtype:                     ibmpairs.query.User
        :raises Exception:          if not a dictionary.
        """
        
        id               = None 
        login            = None
        group            = None
        email            = None
        company          = None
        admin            = None
        secondary_groups = None
        
        common.check_dict(user_dict)
        if "id" in user_dict:
            if user_dict.get("id") is not None:
                id = common.check_str(user_dict.get("id"))
        if "login" in user_dict:
            if user_dict.get("login") is not None:
                login = common.check_str(user_dict.get("login"))
        if "group" in user_dict:
            if user_dict.get("group") is not None:
                group = Group.from_dict(user_dict.get("group"))
        if "email" in user_dict:
            if user_dict.get("email") is not None:
                email = common.check_str(user_dict.get("email"))
        if "company" in user_dict:
            if user_dict.get("company") is not None:
                company = common.check_str(user_dict.get("company"))
        if "admin" in user_dict:
            if user_dict.get("admin") is not None:
                admin = common.check_str(user_dict.get("admin"))
        if "secondary_groups" in user_dict:
            if user_dict.get("secondary_groups") is not None:
                secondary_groups = common.from_list(user_dict.get("secondary_groups"), Group.from_dict)       

        return User(id               = id, 
                    login            = login,
                    group            = group,
                    email            = email,
                    company          = company,
                    admin            = admin,        
                    secondary_groups = secondary_groups
                   )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        user_dict: dict = {}
        if self._id is not None:
            user_dict["id"] = self._id
        if self._login is not None:
            user_dict["login"] = self._login
        if self._group is not None:
            user_dict["group"] = common.class_to_dict(self._group, Group)
        if self._email is not None:
            user_dict["email"] = self._email
        if self._company is not None:
            user_dict["company"] = self._company
        if self._admin is not None:
            user_dict["admin"] = self._admin
        if self._secondary_groups is not None:
            user_dict["secondary_groups"] = common.from_list(self._secondary_groups, lambda item: common.class_to_dict(item, Group))
        return user_dict
        
    #
    def from_json(user_json: Any):
        """
        Create a User object from json (dictonary or str).
        
        :param user_dict:        A json dictionary that contains the keys of a User or a string representation of a json dictionary.
        :type user_dict:         Any             
        :rtype:                     ibmpairs.query.User
        :raises Exception:          if not a dictionary or a string.
        """

        if isinstance(user_json, dict):
            user = User.from_dict(user_json)
        elif isinstance(user_json, str):
            user_dict = json.loads(user_json)
            user = User.from_dict(user_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(user_json), "user_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return user

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.  
                  
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

#
class QueryHistory:
    #_client: cl.Client
    #_id: int
    #_user: User
    #_type: str
    #_date: int
    #_query_job: str
    #_api_json: str
    #_size_total: int
    #_size_raw: int
    #_size_zip: int
    #_count_total: int
    
    """
    A representation of a Query History.
    
    :param client:      An IBM PAIRS Client.
    :type client:       ibmpairs.client.Client
    :param id:          The Query ID.
    :type id:           int
    :param user:        The User that Queried.
    :type user:         ibmpairs.query.Query
    :param type:        Type.
    :type type:         str
    :param date:        The date of the query (UNIX).
    :type date:         int
    :param query_job:   The Query Job ID.
    :type query_job:    str
    :param api_json:    The JSON request body sent to the API.
    :type api_json:     str
    :param size_total:  The total query size.
    :type size_total:   int
    :param size_raw:    The size of the raw data.
    :type size_raw:     int
    :param size_zip:    The size of the query zip.
    :type size_zip:     int
    :param count_total: Count total.
    :type count_total:  int
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
                 client: cl.Client = None, 
                 id: int           = None, 
                 user: User        = None, 
                 type: str         = None, 
                 date: int         = None, 
                 query_job: str    = None, 
                 api_json: str     = None, 
                 size_total: int   = None, 
                 size_raw: int     = None, 
                 size_zip: int     = None, 
                 count_total: int  = None
                ):
        
        self._client      = common.set_client(input_client  = client,
                                              global_client = cl.GLOBAL_PAIRS_CLIENT)
        
        self._id          = id
        self._user        = user
        self._type        = type
        self._date        = date
        self._query_job   = query_job
        self._api_json    = api_json
        self._size_total  = size_total
        self._size_raw    = size_raw
        self._size_zip    = size_zip
        self._count_total = count_total
        
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
    def get_user(self):
        return self._user

    #
    def set_user(self, user):
        self._user = common.check_class(user, User)

    #    
    def del_user(self): 
        del self._user

    #    
    user = property(get_user, set_user, del_user)
    
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
    def get_date(self):
        return self._date

    #
    def set_date(self, date):
        self._date = common.check_str(date)

    #    
    def del_date(self): 
        del self._date

    #    
    date = property(get_date, set_date, del_date)
    
    #
    def get_query_job(self):
        return self._query_job

    #
    def set_query_job(self, query_job):
        self._query_job = common.check_str(query_job)

    #    
    def del_query_job(self): 
        del self._query_job

    #    
    query_job = property(get_query_job, set_query_job, del_query_job)
    
    #
    def get_api_json(self):
        return self._api_json

    #
    def set_api_json(self, api_json):
        self._api_json = common.check_str(api_json)

    #    
    def del_api_json(self): 
        del self._api_json

    #    
    api_json = property(get_api_json, set_api_json, del_api_json)
    
    #
    def get_size_total(self):
        return self._size_total

    #
    def set_size_total(self, size_total):
        self._size_total = common.check_int(size_total)

    #    
    def del_size_total(self): 
        del self._size_total

    #    
    size_total = property(get_size_total, set_size_total, del_size_total)
    
    #
    def get_size_raw(self):
        return self._size_raw

    #
    def set_size_raw(self, size_raw):
        self._size_raw = common.check_int(size_raw)

    #    
    def del_size_raw(self): 
        del self._size_raw

    #    
    size_raw = property(get_size_raw, set_size_raw, del_size_raw)
    
    #
    def get_size_zip(self):
        return self._size_zip

    #
    def set_size_zip(self, size_zip):
        self._size_zip = common.check_int(size_zip)

    #    
    def del_size_zip(self): 
        del self._size_zip

    #    
    size_zip = property(get_size_zip, set_size_zip, del_size_zip)
    
    #
    def get_count_total(self):
        return self._count_total

    #
    def set_count_total(self, count_total):
        self._count_total = common.check_int(count_total)

    #    
    def del_count_total(self): 
        del self._count_total

    #    
    count_total = property(get_count_total, set_count_total, del_count_total)

    #
    def from_dict(query_history_dict: Any):
        
        """
        Create a QueryHistory object from a dictionary.
        
        :param query_history_dict:    A dictionary that contains the keys of a QueryHistory.
        :type query_history_dict:     Any             
        :rtype:                       ibmpairs.query.QueryHistory
        :raises Exception:            if not a dictionary.
        """
        
        id          = None
        user        = None
        type        = None
        date        = None
        query_job   = None
        api_json    = None
        size_total  = None
        size_raw    = None
        size_zip    = None
        count_total = None
        
        common.check_dict(query_history_dict)
        if "id" in query_history_dict:
            if query_history_dict.get("id") is not None:
                id = common.check_int(query_history_dict.get("id"))
        if "user" in query_history_dict:
            if query_history_dict.get("user") is not None:
                user = User.from_dict(query_history_dict.get("user"))
        if "type" in query_history_dict:
            if query_history_dict.get("type") is not None:
                type = common.check_str(query_history_dict.get("type"))
        if "date" in query_history_dict:
            if query_history_dict.get("date") is not None:
                date = common.check_str(query_history_dict.get("date"))
        if "queryjob" in query_history_dict:
            if query_history_dict.get("queryjob") is not None:
                query_job = common.check_str(query_history_dict.get("queryjob"))
        elif "queryJob" in query_history_dict:
            if query_history_dict.get("queryJob") is not None:
                query_job = common.check_str(query_history_dict.get("queryJob"))
        elif "query_job" in query_history_dict:
            if query_history_dict.get("query_job") is not None:
                query_job = common.check_str(query_history_dict.get("query_job"))
        if "apiJson" in query_history_dict:
            if query_history_dict.get("apiJson") is not None:
                api_json = common.check_str(query_history_dict.get("apiJson"))
        elif "api_json" in query_history_dict:
            if query_history_dict.get("api_json") is not None:
                api_json = common.check_str(query_history_dict.get("api_json"))
        if "sizeTotal" in query_history_dict:
            if query_history_dict.get("sizeTotal") is not None:
                size_total = common.check_int(query_history_dict.get("sizeTotal"))
        elif "size_total" in query_history_dict:
            if query_history_dict.get("size_total") is not None:
                size_total = common.check_int(query_history_dict.get("size_total"))
        if "sizeRaw" in query_history_dict:
            if query_history_dict.get("sizeRaw") is not None:
                size_raw = common.check_int(query_history_dict.get("sizeRaw"))
        elif "size_raw" in query_history_dict:
            if query_history_dict.get("size_raw") is not None:
                size_raw = common.check_int(query_history_dict.get("size_raw"))
        if "sizeZip" in query_history_dict:
            if query_history_dict.get("sizeZip") is not None:
                size_zip = common.check_int(query_history_dict.get("sizeZip"))
        elif "size_zip" in query_history_dict:
            if query_history_dict.get("size_zip") is not None:
                size_zip = common.check_int(query_history_dict.get("size_zip"))
        if "countTotal" in query_history_dict:
            if query_history_dict.get("countTotal") is not None:
                count_total = common.check_int(query_history_dict.get("countTotal"))
        elif "count_total" in query_history_dict:
            if query_history_dict.get("count_total") is not None:
                count_total = common.check_int(query_history_dict.get("count_total"))
        return QueryHistory(id          = id, 
                            user        = user, 
                            type        = type, 
                            date        = date, 
                            query_job   = query_job, 
                            api_json    = api_json, 
                            size_total  = size_total, 
                            size_raw    = size_raw, 
                            size_zip    = size_zip, 
                            count_total = count_total
                           )
        
    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        query_history_dict: dict = {}
        if self._id is not None:
            query_history_dict["id"] = self._id
        if self._user is not None:
            query_history_dict["user"] = common.class_to_dict(self._user, User)
        if self._type is not None:
            query_history_dict["type"] = self._type
        if self._date is not None:
            query_history_dict["date"] = self._date
        if self._query_job is not None:
            query_history_dict["query_job"] = self._query_job
        if self._api_json is not None:
            query_history_dict["api_json"] = self._api_json
        if self._size_total is not None:
            query_history_dict["size_total"] = self._size_total
        if self._size_raw is not None:
            query_history_dict["size_raw"] = self._size_raw
        if self._size_zip is not None:
            query_history_dict["size_zip"] = self._size_zip
        if self._count_total is not None:
            query_history_dict["count_total"] = self._count_total
        return query_history_dict
        
    #
    def from_json(query_history_json: Any):

        """
        Create a QueryHistory object from json (dictonary or str).
        
        :param query_history_dict:        A json dictionary that contains the keys of a QueryHistory or a string representation of a json dictionary.
        :type query_history_dict:         Any             
        :rtype:                           ibmpairs.query.QueryHistory
        :raises Exception:                if not a dictionary or a string.
        """

        if isinstance(query_history_json, dict):
            query_history = QueryHistory.from_dict(query_history_json)
        elif isinstance(query_history_json, str):
            query_history_dict = json.loads(query_history_json)
            query_history = QueryHistory.from_dict(query_history_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_history_json), "query_history_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_history

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())

    #
    def get(self,
            id: str           = None,
            client: cl.Client = None,
            verify: bool      = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a query history result.
        
        :param id:         Query ID.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A query history result set.
        :rtype:            ibmpairs.query.QueryHistory
        :raises Exception: A ibmpairs.client.Client is not found, 
                           the status of the request is not 200.
        """

        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)
                                
        if id is None:
            if self._id is not None:
                id = self._id
            else:
                msg = messages.ERROR_QUERY_HISTORY_NO_ID
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            id = common.check_str(id)
        
        response = cli.get(url = cli.get_host() +
                                 "/v2/queryhistories/full/queryjob/" +
                                 id,
                           verify = verify
                          )

        if response.status_code != 200:
            error_message = 'failed'
          
            msg = messages.ERROR_QUERY_HISTORY_GET_FAILED.format('GET', 'request', cli.get_host() + "/v2/queryhistories/full/queryjob/" + id, response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
          
        else:
            query_history_json = response.json()
            query_history = query_history_from_dict(query_history_json)
            
            return query_history
        
    #
    def get_query_by_id(self,
                        id: str           = None,
                        client: cl.Client = None,
                        verify: bool      = constants.GLOBAL_SSL_VERIFY
                       ):
        
        """
        A method to get a Query object that has previously ran by ID.
        
        :param id:         Query ID.
        :type id:          str
        :param client:     An IBM PAIRS Client.
        :type client:      ibmpairs.client.Client
        :param verify:     SSL verification
        :type verify:      bool
        :returns:          A query history result set.
        :rtype:            ibmpairs.query.Query
        :raises Exception: A ibmpairs.client.Client is not found, 
                           the status of the request is not 200.
        """
        
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        if id is None:
            if self._id is not None:
                id = self._id
            else:
                msg = messages.ERROR_QUERY_HISTORY_NO_ID
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            id = common.check_str(id)
      
        query_history = self.get(id     = id,
                                 client = client,
                                 verify = verify
                                )

        query_api_json = query_history.get_api_json()
      
        q = query_from_json(query_api_json)

        return q

        
#
class LatestQueries: 
    #_client: cl.Client
    #_latest_queries: List[Query]
    
    """
    A representation of the Latest Queries made by a user.
    
    :param client:         An IBM PAIRS Client.
    :type client:          ibmpairs.client.Client
    :param latest_queries: The latest queries made by a user.
    :type latest_queries:  List[ibmpairs.query.Query]
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
    def __getitem__(self, query_name):
        
        """
        A method to overload the default behaviour of the slice on this object to be an
        element from the latest_queries attribute.
        
        :param query_name:    The name of a Query to search for, if this is numeric,
                              the method simply returns the default (list order).
        :type query_name:     str
        :raises Exception:    If less than one value is found, 
                              if more than one value is found.
        """ 
      
        if isinstance(query_name, int):
            return self._latest_queries[query_name]
        elif isinstance(query_name, str):
            index_list = []
            index      = 0
            foundCount = 0

            for query in self._latest_queries:
                if query.name is not None:
                    if (query.name == query_name):
                        foundCount = foundCount + 1
                        index_list.append(index)
                else:
                    msg = messages.WARN_QUERY_LATEST_QUERIES_QUERY_OBJECT_NO_NAME.format(query_name)
                    logger.warning(msg)
                  
                index = index + 1

            if foundCount == 0:
                msg = messages.ERROR_QUERY_LATEST_QUERIES_NO_QUERY.format(query_name)
                logger.error(msg)
                raise common.PAWException(msg)
            elif foundCount == 1:
                return self._latest_queries[index_list[0]]
            else:
                msg = messages.ERROR_QUERY_LATEST_QUERIES_MULTIPLE_IDENTICAL_NAMES.format(query_name)
                logger.error(msg)
                raise common.PAWException(msg)
        else:
            msg = messages.ERROR_QUERY_LATEST_QUERIES_TYPE_UNKNOWN.format(type(query_name))
            logger.error(msg)
            raise common.PAWException(msg)

    #
    def __init__(self,
                 client: cl.Client = None,
                 latest_queries: List[Query] = None,
                ):
        self._client         = common.set_client(input_client  = client,
                                                 global_client = cl.GLOBAL_PAIRS_CLIENT)

        self._latest_queries = latest_queries
        
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
    def get_latest_queries(self):
        return self._latest_queries

    #
    def set_latest_queries(self, latest_queries):
        self._latest_queries = common.check_list(latest_queries)

    #    
    def del_latest_queries(self): 
        del self._latest_queries

    #    
    latest_queries = property(get_latest_queries, set_latest_queries, del_latest_queries)
    
    #
    def from_dict(latest_queries_input: Any):

        """
        Create an LatestQueries object from a dictionary.
        
        :param latest_queries_dict:    A dictionary that contains the keys of an LatestQueries.
        :type latest_queries_dict:     Any             
        :rtype:                        ibmpairs.query.LatestQueries
        :raises Exception:             If not a dictionary.
        """
        
        latest_queries = None
        
        if isinstance(latest_queries_input, dict):
            common.check_dict(latest_queries_input)

            if "latest_queries" in latest_queries_input:
                if latest_queries_input.get("latest_queries") is not None:
                    latest_queries = common.from_list(latest_queries_input.get("latest_queries"), Query.from_dict)

        return LatestQueries(latest_queries = latest_queries)
    
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure. 
                   
        :rtype:                     dict
        """
      
        latest_queries_dict: dict = {}
        if self._latest_queries is not None:
            latest_queries_dict["latest_queries"] = common.from_list(self._latest_queries, lambda item: common.class_to_dict(item, Query))
        return latest_queries_dict

    #
    def from_json(latest_queries_json: Any):

        """
        Create a LatestQueries object from json (dictonary or str).
        
        :param latest_queries_dict:        A json dictionary that contains the keys of a LatestQueries or a string representation of a json dictionary.
        :type latest_queries_dict:         Any             
        :rtype:                            ibmpairs.query.LatestQueries
        :raises Exception:                 If not a dictionary or a string.
        """

        if isinstance(latest_queries_json, dict):
            latest_queries = LatestQueries.from_dict(latest_queries_json)
        elif isinstance(latest_queries_json, str):
            latest_queries_dict = json.loads(latest_queries_json)
            latest_queries = LatestQueries.from_dict(latest_queries_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(latest_queries_json), "latest_queries_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return latest_queries

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())
    
    #
    def get(self,
            client: cl.Client      = None,
            favorite_flag: bool    = False, 
            number_of_queries: int = 10,
            verify: bool           = constants.GLOBAL_SSL_VERIFY
           ):
            
        """
        A method to get a list of latest queries.

        :param client:            An IBM PAIRS Client.
        :type client:             ibmpairs.client.Client
        :param favorite_flag:     Whether only favorites should be searched.
        :type favorite_flag:      bool
        :param number_of_queries: Number of latest queries to gather.
        :type number_of_queries:  int
        :param verify:            SSL verification
        :type verify:             bool
        :raises Exception:        A ibmpairs.client.Client is not found, 
                                  the status of the request is not 200, 
                                  if queries could not be retrieved. 
        """
                            
        cli = common.set_client(input_client  = client,
                                global_client = cl.GLOBAL_PAIRS_CLIENT,
                                self_client   = self._client)

        if favorite_flag == True:
            fav = "true"
        else:
            fav = "false"

        response = cli.get(url = cli.get_host() +
                                 "/v2/queryjobs/list?flag=" +
                                 fav +
                                 "&page=1&size=" +
                                 str(number_of_queries),
                           verify = verify
                          )
        
        if response.status_code != 200:
            error_message = 'failed'
          
            msg = messages.ERROR_QUERY_MERGE_NOT_SUCCESSFUL.format('GET', 'request', cli.get_host() + "/v2/queryjobs/list?flag=" + fav + "&page=1&size=" + str(number_of_queries), response.status_code, error_message)
            logger.error(msg)
            raise common.PAWException(msg)
          
        else:
            lq: List[Query] = []
            
            query_jobs_json = response.json() 
            query_jobs = query_jobs_from_dict(query_jobs_json)
            query_job_list = query_jobs.query_job_list
          
            try:
                for query_job in query_job_list:
                    q = get_query_by_id(query_job.id,
                                        client = cli,
                                        verify = verify
                                       )
                    lq.append(q)
            except Exception as ex:
                msg = messages.ERROR_LATEST_QUERIES_FAILED_TO_RETRIEVE_QUERIES.format(ex)
                logger.error(msg)
                raise common.PAWException(msg)

            self.set_latest_queries(lq)
        
#
class QueryOutputInfoFile:
    #_name: str
    #_dataset_id: int
    #_dataset_name: str
    #_datalayer_id: str
    #_datalayer_name: str
    #_datalayer_alias: str
    #_temporal_aggregation: str
    #_spatial_aggregation: str
    #_dimension: str
    #_timestamp: str
    #_layer_type: str
    
    """
    A representation of the output.info file returned in a Query zip.
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
                 name: str                 = None,
                 dataset_id: int           = None,
                 dataset_name: str         = None,
                 datalayer_id: str         = None,
                 datalayer_name: str       = None,
                 datalayer_alias: str      = None,
                 temporal_aggregation: str = None,
                 spatial_aggregation: str  = None,
                 dimension: str            = None,
                 timestamp: str            = None,
                 layer_type: str           = None,
                ):
        self._name                 = name
        self._dataset_id           = dataset_id
        self._dataset_name         = dataset_name
        self._datalayer_id         = datalayer_id
        self._datalayer_name       = datalayer_name
        self._datalayer_alias      = datalayer_alias
        self._temporal_aggregation = temporal_aggregation
        self._spatial_aggregation  = spatial_aggregation
        self._dimension            = dimension
        self._timestamp            = timestamp
        self._layer_type           = layer_type
        
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
    def get_dataset_id(self):
        return self._dataset_id

    #
    def set_dataset_id(self, dataset_id):
        self._dataset_id = common.check_int(dataset_id)
        
    #    
    def del_dataset_id(self): 
        del self._dataset_id

    #    
    dataset_id = property(get_dataset_id, set_dataset_id, del_dataset_id)
    
    #       
    def get_dataset_name(self):
        return self._dataset_name

    #
    def set_dataset_name(self, dataset_name):
        self._dataset_name = common.check_str(dataset_name)
        
    #    
    def del_dataset_name(self): 
        del self._dataset_name

    #    
    dataset_name = property(get_dataset_name, set_dataset_name, del_dataset_name)
    
    #       
    def get_datalayer_id(self):
        return self._datalayer_id

    #
    def set_datalayer_id(self, datalayer_id):
        self._datalayer_id = common.check_str(datalayer_id)
        
    #    
    def del_datalayer_id(self): 
        del self._datalayer_id

    #    
    datalayer_id = property(get_datalayer_id, set_datalayer_id, del_datalayer_id)
    
    #       
    def get_datalayer_name(self):
        return self._datalayer_name

    #
    def set_datalayer_name(self, datalayer_name):
        self._datalayer_name = common.check_str(datalayer_name)
        
    #    
    def del_datalayer_name(self): 
        del self._datalayer_name

    #    
    datalayer_name = property(get_datalayer_name, set_datalayer_name, del_datalayer_name)
    
    #       
    def get_datalayer_alias(self):
        return self._datalayer_alias

    #
    def set_datalayer_alias(self, datalayer_alias):
        self._datalayer_alias = common.check_str(datalayer_alias)
        
    #    
    def del_datalayer_alias(self): 
        del self._datalayer_alias

    #    
    datalayer_alias = property(get_datalayer_alias, set_datalayer_alias, del_datalayer_alias)
    
    #       
    def get_temporal_aggregation(self):
        return self._temporal_aggregation

    #
    def set_temporal_aggregation(self, temporal_aggregation):
        self._temporal_aggregation = common.check_str(temporal_aggregation)
        
    #    
    def del_temporal_aggregation(self): 
        del self._temporal_aggregation

    #    
    temporal_aggregation = property(get_temporal_aggregation, set_temporal_aggregation, del_temporal_aggregation)
    
    #       
    def get_spatial_aggregation(self):
        return self._spatial_aggregation

    #
    def set_spatial_aggregation(self, spatial_aggregation):
        self._spatial_aggregation = common.check_str(spatial_aggregation)
        
    #    
    def del_spatial_aggregation(self): 
        del self._spatial_aggregation

    #    
    spatial_aggregation = property(get_spatial_aggregation, set_spatial_aggregation, del_spatial_aggregation)
    
    #       
    def get_dimension(self):
        return self._dimension

    #
    def set_dimension(self, dimension):
        self._dimension = common.check_str(dimension)
        
    #    
    def del_dimension(self): 
        del self._dimension

    #    
    dimension = property(get_dimension, set_dimension, del_dimension)
    
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
    def from_dict(query_output_info_dict: Any):

        """
        Create an QueryOutputInfoFile object from a dictionary.
        
        :param query_output_info_file_dict:    A dictionary that contains the keys of an QueryOutputInfoFile.
        :type query_output_info_file_dict:     Any             
        :rtype:                                ibmpairs.query.QueryOutputInfoFile
        :raises Exception:                     if not a dictionary.
        """
        
        name                 = None     
        dataset_id           = None
        dataset_name         = None
        datalayer_id         = None
        datalayer_name       = None
        datalayer_alias      = None
        temporal_aggregation = None
        spatial_aggregation  = None
        dimension            = None
        timestamp            = None
        layer_type           = None
        
        common.check_dict(query_output_info_dict)
        if "name" in query_output_info_dict:
            if query_output_info_dict.get("name") is not None:
                name = common.check_str(query_output_info_dict.get("name"))
        if "datasetId" in query_output_info_dict:
            if query_output_info_dict.get("datasetId") is not None:
                dataset_id = common.check_int(query_output_info_dict.get("datasetId"))
        elif "dataset_id" in query_output_info_dict:
            if query_output_info_dict.get("dataset_id") is not None:
                dataset_id = common.check_int(query_output_info_dict.get("dataset_id"))
        if "datasetName" in query_output_info_dict:
            if query_output_info_dict.get("datasetName") is not None:
                dataset_name = common.check_str(query_output_info_dict.get("datasetName"))
        elif "dataset_name" in query_output_info_dict:
            if query_output_info_dict.get("dataset_name") is not None:
                dataset_name = common.check_str(query_output_info_dict.get("dataset_name"))
        if "datalayerId" in query_output_info_dict:
            if query_output_info_dict.get("datalayerId") is not None:
                datalayer_id = common.check_str(query_output_info_dict.get("datalayerId"))
        elif "datalayer_id" in query_output_info_dict:
            if query_output_info_dict.get("datalayer_id") is not None:
                datalayer_id = common.check_str(query_output_info_dict.get("datalayer_id"))
        if "datalayerName" in query_output_info_dict:
            if query_output_info_dict.get("datalayerName") is not None:
                datalayer_name = common.check_str(query_output_info_dict.get("datalayerName"))
        elif "datalayer_name" in query_output_info_dict:
            if query_output_info_dict.get("datalayer_name") is not None:
                datalayer_name = common.check_str(query_output_info_dict.get("datalayer_name"))
        if "datalayerAlias" in query_output_info_dict:
            if query_output_info_dict.get("datalayerAlias") is not None:
                datalayer_alias = common.check_str(query_output_info_dict.get("datalayerAlias"))
        elif "datalayer_alias" in query_output_info_dict:
            if query_output_info_dict.get("datalayer_alias") is not None:
                datalayer_alias = common.check_str(query_output_info_dict.get("datalayer_alias"))
        if "temporalAggregation" in query_output_info_dict:
            if query_output_info_dict.get("temporalAggregation") is not None:
                temporal_aggregation = common.check_str(query_output_info_dict.get("temporalAggregation"))
        elif "temporal_aggregation" in query_output_info_dict:
            if query_output_info_dict.get("temporal_aggregation") is not None:
                temporal_aggregation = common.check_str(query_output_info_dict.get("temporal_aggregation"))
        if "spatialAggregation" in query_output_info_dict:
            if query_output_info_dict.get("spatialAggregation") is not None:
                spatial_aggregation = common.check_str(query_output_info_dict.get("spatialAggregation"))
        elif "spatial_aggregation" in query_output_info_dict:
            if query_output_info_dict.get("spatial_aggregation") is not None:
                spatial_aggregation = common.check_str(query_output_info_dict.get("spatial_aggregation"))
        if "dimension" in query_output_info_dict:
            if query_output_info_dict.get("dimension") is not None:
                dimension = common.check_str(query_output_info_dict.get("dimension"))
        if "timestamp" in query_output_info_dict:
            if query_output_info_dict.get("timestamp") is not None:
                timestamp = common.check_str(query_output_info_dict.get("timestamp"))
        if "layerType" in query_output_info_dict:
            if query_output_info_dict.get("layerType") is not None:
                layer_type = common.check_str(query_output_info_dict.get("layerType"))
        elif "layer_type" in query_output_info_dict:
            if query_output_info_dict.get("layer_type") is not None:
                layer_type = common.check_str(query_output_info_dict.get("layer_type"))
        return QueryOutputInfoFile(name,     
                                   dataset_id,
                                   dataset_name,
                                   datalayer_id,
                                   datalayer_name,
                                   datalayer_alias,
                                   temporal_aggregation,
                                   spatial_aggregation,
                                   dimension,
                                   timestamp,
                                   layer_type
                                  )

    #
    def to_dict(self):
        
        """
        Create a dictionary from the objects structure.   
                 
        :rtype:                     dict
        """
      
        query_output_info_dict: dict = {}
        if self._name is not None:
            query_output_info_dict["name"] = self._name
        if self._dataset_id is not None:
            query_output_info_dict["dataset_id"] = self._dataset_id
        if self._dataset_name is not None:
            query_output_info_dict["dataset_name"] = self._dataset_name
        if self._datalayer_id is not None:
            query_output_info_dict["datalayer_id"] = self._datalayer_id
        if self._datalayer_name is not None:
            query_output_info_dict["datalayer_name"] = self._datalayer_name
        if self._datalayer_alias is not None:
            query_output_info_dict["datalayer_alias"] = self._datalayer_alias
        if self._temporal_aggregation is not None:
            query_output_info_dict["temporal_aggregation"] = self._temporal_aggregation
        if self._spatial_aggregation is not None:
            query_output_info_dict["spatial_aggregation"] = self._spatial_aggregation
        if self._dimension is not None:
            query_output_info_dict["dimension"] = self._dimension
        if self._timestamp is not None:
            query_output_info_dict["timestamp"] = self._timestamp
        if self._dataset_name is not None:
            query_output_info_dict["dataset_name"] = self._dataset_name
        if self._layer_type is not None:
            query_output_info_dict["layer_type"] = self._layer_type
        return query_output_info_dict
        
    #
    def from_json(query_output_info_file_json: Any):

        """
        Create a QueryOutputInfoFile object from json (dictonary or str).
        
        :param query_output_info_file_dict:        A json dictionary that contains the keys of a QueryOutputInfoFile or a string representation of a json dictionary.
        :type query_output_info_file_dict:         Any             
        :rtype:                                    ibmpairs.query.QueryOutputInfoFile
        :raises Exception:                         if not a dictionary or a string.
        """

        if isinstance(query_output_info_file_json, dict):
            query_output_info_file = QueryOutputInfoFile.from_dict(query_output_info_file_json)
        elif isinstance(query_output_info_file_json, str):
            query_output_info_file_dict = json.loads(query_output_info_file_json)
            query_output_info_file = QueryOutputInfoFile.from_dict(query_output_info_file_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(query_output_info_file_json), "query_output_info_file_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return query_output_info_file
    

    #
    def to_json(self):
        
        """
        Create a string representation of a json dictionary from the objects structure.
                    
        :rtype:                     string
        """
        
        return json.dumps(self.to_dict())


def submit(query: Any,
           client: cl.Client = None,
           verify: bool      = constants.GLOBAL_SSL_VERIFY,
           compact_csv: bool = False
          ):
            
    """
    A helper method to submit a query.
    
    :param query:         A query to submit.
    :type query:          ibmpairs.query.Query or dict or str
    :param client:        An IBM PAIRS Client.
    :type client:         ibmpairs.client.Client
    :param verify:        SSL verification
    :type verify:         bool
    :param compact_csv:   A flag to indicate the return of a compact csv format.
    :type compact_csv:    bool
    :returns:             A query object.
    :rtype:               ibmpairs.query.Query
    :raises Exception:    A ibmpairs.client.Client is not found, 
                          error making request to server, 
                          the status of the request is not 200, 
                          the type or format of Query is incorrect.
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(query, Query):
        pass
    elif isinstance(query, dict):
        query = query_from_dict(query)
    elif isinstance(query, str):
        query = query_from_json(query)
    else:
        msg = messages.ERROR_QUERY_TYPE_NOT_RECOGNIZED.format(type(query))
        logger.error(msg)
        raise common.PAWException(msg)
        
    query.submit(client      = cli,
                 verify      = verify,
                 compact_csv = compact_csv
                )
    
    return query

def status(query: Any           = None,
           client: cl.Client    = None,
           id: str              = None,
           poll: bool           = True,
           status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
           verify: bool         = constants.GLOBAL_SSL_VERIFY
          ):
            
    """
    A helper method to check the status of a query.
    
    :param query:           A query (must contain ID) to check the status of.
    :type query:            ibmpairs.query.Query or dict or str
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param id:              A Query ID, if None will use id in object.
    :type id:               str
    :param poll:            Whether the operation should poll until success.
    :type poll:             bool
    :param status_interval: How often the async run operation should call back.
    :type status_interval:  int
    :param verify:          SSL verification
    :type verify:           bool
    :returns:               A query object.
    :rtype:                 ibmpairs.query.Query
    :raises Exception:      A ibmpairs.client.Client is not found, 
                            the Query failed, 
                            error making request to server, 
                            the status of the request is not 200, 
                            the type or format of Query is incorrect.
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(query, Query):
        pass
    elif isinstance(query, dict):
        query = query_from_dict(query)
    elif isinstance(query, str):
        query = query_from_json(query)
    else:
        query = Query()
    
    query.status(client          = cli,
                 id              = id,
                 poll            = poll,
                 status_interval = status_interval,
                 verify          = verify
                )
    
    return query
  
  
def download(query: Any           = None,
             client: cl.Client    = None,
             id: str              = None,
             status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
             download_folder      = None,
             download_file_name   = None,
             verify: bool         = constants.GLOBAL_SSL_VERIFY
            ):
                
    """
    A helper method to download and unzip a query result.
        
    :param query:              A query (must contain ID) to check the status of and download.
    :type query:               ibmpairs.query.Query
    :param client:             An IBM PAIRS Client.
    :type client:              ibmpairs.client.Client
    :param id:                 A Query ID, if None will use id in object.
    :type id:                  str
    :param status_interval:    How often the async run operation should call back.
    :type status_interval:     int
    :param download_folder:    A download folder (fixed or relative).
    :type download_folder:     str
    :param download_file_name: A file name for the download.
    :type download_file_name:  str
    :param verify:             SSL verification
    :type verify:              bool
    :returns:                  A query object.
    :rtype:                    ibmpairs.query.Query
    :raises Exception:         A ibmpairs.client.Client is not found, 
                               the Query status failed, 
                               the download folder could not be made or identified, 
                               the download failed, 
                               error making request to server, 
                               the status of the request is not 200, 
                               the type or format of Query is incorrect.
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(query, Query):
        pass
    elif isinstance(query, dict):
        query = query_from_dict(query)
    elif isinstance(query, str):
        query = query_from_json(query)
    else:
        query = Query()
    
    query.download(client             = cli,
                   id                 = id,
                   status_interval    = status_interval,
                   download_folder    = download_folder,
                   download_file_name = download_file_name,
                   verify             = verify
                  )
    
    return query
  
def submit_and_check_status(query: Any,
                            client: cl.Client    = None,
                            poll: bool           = True,
                            status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                            verify: bool         = constants.GLOBAL_SSL_VERIFY,
                            compact_csv: bool    = False
                           ):
                            
    """
    A helper method to submit and check the status of a query.

    :param query:           A query to submit.
    :type query:            ibmpairs.query.Query or dict or str
    :param client:          An IBM PAIRS Client.
    :type client:           ibmpairs.client.Client
    :param poll:            Whether the operation should poll until success.
    :type poll:             bool
    :param status_interval: How often the async run operation should check for status (seconds).
    :type status_interval:  int
    :param verify:          SSL verification
    :type verify:           bool
    :param compact_csv:     A flag to indicate the return of a compact csv format.
    :type compact_csv:      bool
    :returns:               A query object.
    :rtype:                 ibmpairs.query.Query
    :raises Exception:      A ibmpairs.client.Client is not found, 
                            the Query failed, 
                            error making request to server, 
                            the status of the request is not 200, 
                            the type or format of Query is incorrect.
    """

    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(query, Query):
        pass
    elif isinstance(query, dict):
        query = query_from_dict(query)
    elif isinstance(query, str):
        query = query_from_json(query)
    else:
        msg = messages.ERROR_QUERY_TYPE_NOT_RECOGNIZED.format(type(query))
        logger.error(msg)
        raise common.PAWException(msg)
        
    query.submit_and_check_status(client          = cli,
                                  poll            = poll,
                                  status_interval = status_interval,
                                  verify          = verify,
                                  compact_csv     = compact_csv
                                 )
    
    return query
  
def check_status_and_download(query: Any           = None,
                              client: cl.Client    = None,
                              id: str              = None,
                              poll: bool           = True,
                              status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                              download_folder      = 'download',
                              download_file_name   = None,
                              verify: bool         = constants.GLOBAL_SSL_VERIFY
                             ):
                                
    """
    A helper method to check the status of a query then download the result.

    :param query:              A query (must contain ID) to check the status of and download.
    :type query:               ibmpairs.query.Query
    :param client:             An IBM PAIRS Client.
    :type client:              ibmpairs.client.Client
    :param id:                 A Query ID, if None will use id in object.
    :type id:                  str
    :param poll:               Whether the operation should poll until success.
    :type poll:                bool
    :param status_interval:    How often the async run operation should call back.
    :type status_interval:     int
    :param download_folder:    A download folder (fixed or relative).
    :type download_folder:     str
    :param download_file_name: A file name for the download.
    :type download_file_name:  str
    :param verify:             SSL verification
    :type verify:              bool
    :returns:                  A query object.
    :rtype:                    ibmpairs.query.Query
    :raises Exception:         A ibmpairs.client.Client is not found, 
                               the Query status failed, 
                               the download folder could not be made or identified, 
                               the download failed, 
                               error making request to server, 
                               the status of the request is not 200, 
                               the type or format of Query is incorrect.
    """

    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(query, Query):
        pass
    elif isinstance(query, dict):
        query = query_from_dict(query)
    elif isinstance(query, str):
        query = query_from_json(query)
    else:
        query = Query()
    
    query.check_status_and_download(client             = cli,
                                    id                 = id,
                                    poll               = poll,
                                    status_interval    = status_interval,
                                    download_folder    = download_folder,
                                    download_file_name = download_file_name,
                                    verify             = verify
                                   )
    
    return query

def submit_check_status_and_download(query: Any,
                                     client: cl.Client    = None,
                                     poll: bool           = True,
                                     status_interval: int = QUERY_STATUS_CHECK_INTERVAL,
                                     download_folder      = None,
                                     download_file_name   = None,
                                     verify: bool         = constants.GLOBAL_SSL_VERIFY,
                                     compact_csv: bool    = False
                                    ):

    """
    A helper method to submit a query check the status then download the result.

    :param query:              A query to submit, check the status of and download.
    :type query:               ibmpairs.query.Query or dict or str
    :param client:             An IBM PAIRS Client.
    :type client:              ibmpairs.client.Client
    :param poll:               Whether the operation should poll until success.
    :type poll:                bool
    :param status_interval:    How often the async run operation should call back.
    :type status_interval:     int
    :param download_folder:    A download folder (fixed or relative).
    :type download_folder:     str
    :param download_file_name: A file name for the download.
    :type download_file_name:  str
    :param verify:             SSL verification
    :type verify:              bool
    :param compact_csv:        A flag to indicate the return of a compact csv format.
    :type compact_csv:         bool
    :returns:                  A query object.
    :rtype:                    ibmpairs.query.Query
    :raises Exception:         A ibmpairs.client.Client is not found, 
                               the Query status failed, 
                               the download folder could not be made or identified, 
                               the download failed, 
                               error making request to server, 
                               the status of the request is not 200, 
                               the type or format of Query is incorrect.
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    if isinstance(query, Query):
        pass
    elif isinstance(query, dict):
        query = query_from_dict(query)
    elif isinstance(query, str):
        query = query_from_json(query)
    else:
        msg = messages.ERROR_QUERY_TYPE_NOT_RECOGNIZED.format(type(query))
        logger.error(msg)
        raise common.PAWException(msg)
    
    query.submit_check_status_and_download(client             = cli,
                                           poll               = poll,
                                           status_interval    = status_interval,
                                           download_folder    = download_folder,
                                           download_file_name = download_file_name,
                                           verify             = verify,
                                           compact_csv        = compact_csv
                                          )
    
    return query
    
def merge_query_into_base(other_job_id,
                          base_job_id        = None,
                          client : cl.Client = None,
                          verify: bool       = constants.GLOBAL_SSL_VERIFY
                         ):
                              
    """
    A helper method to merge a query into a base query on the server side.
        
    :param other_job_id:  The ID of the job to be merged.
    :type other_job_id:   str or int
    :param base_job_id:   The ID of the base job to be merged to.
    :type base_job_id:    str or int
    :param client:        An IBM PAIRS Client.
    :type client:         ibmpairs.client.Client
    :param verify:        SSL verification
    :type verify:         bool
    :returns:             A query object.
    :rtype:               ibmpairs.query.Query
    :raises Exception:    A ibmpairs.client.Client is not found, 
                          other job ID is not provided, 
                          base job ID is not provided or already held in the object, 
                          the status of the request is not 200.
    """
    
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    query = Query()
    
    query.merge(other_job_id = other_job_id,
                base_job_id  = base_job_id,
                client       = cli,
                verify       = verify
               )
    
    return query

def favorite(id: str,
             client: cl.Client = None,
             verify: bool      = constants.GLOBAL_SSL_VERIFY
            ):

    """
    A helper method to favorite a Query.
    
    :param id:            The Query ID to be made a favorite.
    :type id:             str
    :param client:        An IBM PAIRS Client.
    :type client:         ibmpairs.client.Client
    :param verify:        SSL verification
    :type verify:         bool
    :raises Exception:    A ibmpairs.client.Client is not found, 
                          an ID is not provided or already held in the object, 
                          the status of the request is not 200.
    """
  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
  
    q = Query()
  
    q.favorite(id     = id,
               client = cli,
               verify = verify
              )
  
def unfavorite(id: str,
               client: cl.Client = None,
               verify: bool      = constants.GLOBAL_SSL_VERIFY
              ):

    """
    A helper method to unfavorite a Query.
    
    :param id:            The Query ID to be made not a favorite.
    :type id:             str
    :param client:        An IBM PAIRS Client.
    :type client:         ibmpairs.client.Client
    :param verify:        SSL verification
    :type verify:         bool
    :raises Exception:    A ibmpairs.client.Client is not found, 
                          an ID is not provided or already held in the object, 
                          the status of the request is not 200.
    """
  
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
  
    q = Query()
  
    q.unfavorite(id     = id,
                 client = cli,
                 verify = verify
                )

# 
def get_query_by_id(id: str,
                    client: cl.Client = None,
                    verify: bool      = constants.GLOBAL_SSL_VERIFY
                   ):
    
    """
    A helper method to get a previously run Query object by an ID number.

    :param client:            An IBM PAIRS Client.
    :type client:             ibmpairs.client.Client
    :param verify:            SSL verification
    :type verify:             bool
    :returns:                 A Query object.
    :rtype:                   ibmpairs.query.Query
    :raises Exception:        A ibmpairs.client.Client is not found, 
                              the status of the request is not 200. 
    """

    cli = common.set_client(input_client = client,
                global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    qh = QueryHistory()
    
    q = qh.get_query_by_id(id     = id,
                           client = cli,
                           verify = verify
                          )
    return q
    
# 
def get_latest_queries(client: cl.Client      = None,
                       favorite_flag: bool    = False, 
                       number_of_queries: int = 10,
                       verify: bool           = constants.GLOBAL_SSL_VERIFY
                      ):
                        
    """
    A helper method to get a list of latest queries.

    :param client:            An IBM PAIRS Client.
    :type client:             ibmpairs.client.Client
    :param favorite_flag:     Whether only favorites should be searched.
    :type favorite_flag:      bool
    :param number_of_queries: Number of latest queries to gather.
    :type number_of_queries:  int
    :param verify:            SSL verification
    :type verify:             bool
    :returns:                 A list of the latest queries a user has run.
    :rtype:                   ibmpairs.query.LatestQueries
    :raises Exception:        A ibmpairs.client.Client is not found, 
                              the status of the request is not 200, 
                              if queries could not be retrieved. 
    """

    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    lq = LatestQueries()
    
    lq.get(client            = cli,
           favorite_flag     = favorite_flag, 
           number_of_queries = number_of_queries,
           verify            = verify
          )
    return lq
    
#
def get_latest_favorites(client: cl.Client      = None,
                         number_of_queries: int = 10,
                         verify: bool           = constants.GLOBAL_SSL_VERIFY 
                        ):
                          
    """
    A helper method to get a list of latest favorite queries.

    :param client:            An IBM PAIRS Client.
    :type client:             ibmpairs.client.Client
    :param number_of_queries: Number of latest queries to gather.
    :type number_of_queries:  int
    :param verify:            SSL verification
    :type verify:             bool
    :returns:                 A list of the latest favorite queries a user has run.
    :rtype:                   ibmpairs.query.LatestQueries
    :raises Exception:        A ibmpairs.client.Client is not found, 
                              the status of the request is not 200, 
                              if queries could not be retrieved. 
    """
                          
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    
    lf =  get_latest_queries(client              = cli,
                             favorite_flag       = True,
                             number_of_queries   = number_of_queries,
                             verify              = verify
                            )
    return lf

#
def aggregation_from_dict(aggregation_dictionary: dict):
    """
    The function converts a dictionary of Aggregation to an Aggregation object.
    
    :param aggregation_dict:    A dictionary that contains the keys of an Aggregation.
    :type aggregation_dict:     dict             
    :rtype:                     ibmpairs.query.Aggregation
    :raises Exception:          if not a dict.
    """
    return Aggregation.from_dict(aggregation_dictionary)

#
def aggregation_to_dict(aggregation: Aggregation):
    """
    The function converts an object of Aggregation to a dict.
    
    :param aggregation:    An Aggregation object.
    :type aggregation:     ibmpairs.query.Aggregation             
    :rtype:                dict
    """
    return Aggregation.to_dict(aggregation)

#
def aggregation_from_json(aggregation_json: Any):
    """
    The function converts a dictionary or json string of Aggregation to an Aggregation object.
    
    :param aggregation_json:    A dictionary or json string that contains the keys of an Aggregation.
    :type aggregation_json:     Any             
    :rtype:                     ibmpairs.query.Aggregation
    :raises Exception:          if not a dict or a str.
    """
    return Aggregation.from_json(aggregation_json)

#
def aggregation_to_json(aggregation: Aggregation):
    """
    The function converts an object of Aggregation to a json string.
    
    :param aggregation:    An Aggregation object.
    :type aggregation:     ibmpairs.query.Aggregation             
    :rtype:                str
    """
    return Aggregation.to_json(aggregation)

#
def dimension_from_dict(dimension_dictionary: dict):
    """
    The function converts a dictionary of Dimension to a Dimension object.
    
    :param dimension_dict:    A dictionary that contains the keys of a Dimension.
    :type dimension_dict:     dict             
    :rtype:                   ibmpairs.query.Dimension
    :raises Exception:        if not a dict.
    """
    return Dimension.from_dict(dimension_dictionary)

#
def dimension_to_dict(dimension: Dimension):
    """
    The function converts an object of Dimension to a dict.
    
    :param dimension:    A Dimension object.
    :type dimension:     ibmpairs.query.Dimension             
    :rtype:              dict
    """
    return Dimension.to_dict(dimension)

#
def dimension_from_json(dimension_json: Any):
    """
    The function converts a dictionary or json string of Dimension to a Dimension object.
    
    :param dimension_json:    A dictionary or json string that contains the keys of a Dimension.
    :type dimension_json:     Any             
    :rtype:                   ibmpairs.query.Dimension
    :raises Exception:        if not a dict or a str.
    """
    return Dimension.from_json(dimension_json)

#
def dimension_to_json(dimension: Dimension):
    """
    The function converts an object of Dimension to a json string.
    
    :param dimension:    A Dimension object.
    :type dimension:     ibmpairs.query.Dimension             
    :rtype:              str
    """
    return Dimension.to_json(dimension)

#
def filter_from_dict(filter_dictionary: dict):
    """
    The function converts a dictionary of Filter to a Filter object.
    
    :param filter_dict:    A dictionary that contains the keys of a Filter.
    :type filter_dict:     dict             
    :rtype:                ibmpairs.query.Filter
    :raises Exception:     if not a dict.
    """
    return Filter.from_dict(filter_dictionary)

#
def filter_to_dict(filter: Filter):
    """
    The function converts an object of Filter to a dict.
    
    :param filter:    A Filter object.
    :type filter:     ibmpairs.query.Filter             
    :rtype:           dict
    """
    return Filter.to_dict(filter)

#
def filter_from_json(filter_json: Any):
    """
    The function converts a dictionary or json string of Filter to a Filter object.
    
    :param filter_json:    A dictionary or json string that contains the keys of a Filter.
    :type filter_json:     Any             
    :rtype:                ibmpairs.query.Filter
    :raises Exception:     if not a dict or a str.
    """
    return Filter.from_json(filter_json)

#
def filter_to_json(filter: Filter):
    """
    The function converts an object of Filter to a json string.
    
    :param filter:    A Filter object.
    :type filter:     ibmpairs.query.Filter             
    :rtype:           str
    """
    return Filter.to_json(filter)

#
def interval_from_dict(interval_dictionary: dict):
    """
    The function converts a dictionary of Interval to an Interval object.
    
    :param interval_dict:    A dictionary that contains the keys of an Interval.
    :type interval_dict:     dict             
    :rtype:                  ibmpairs.query.Interval
    :raises Exception:       if not a dict.
    """
    return Interval.from_dict(interval_dictionary)

#
def interval_to_dict(interval: Interval):
    """
    The function converts an object of Interval to a dict.
    
    :param interval:    An Interval object.
    :type interval:     ibmpairs.query.Interval             
    :rtype:             dict
    """
    return Interval.to_dict(interval)

#
def interval_from_json(interval_json: Any):
    """
    The function converts a dictionary or json string of Interval to an Interval object.
    
    :param interval_json:    A dictionary or json string that contains the keys of an Interval.
    :type interval_json:     Any             
    :rtype:                  ibmpairs.query.Interval
    :raises Exception:       if not a dict or a str.
    """
    return Interval.from_json(interval_json)

#
def interval_to_json(interval: Interval):
    """
    The function converts an object of Interval to a json string.
    
    :param interval:    An Interval object.
    :type interval:     ibmpairs.query.Interval             
    :rtype:             str
    """
    return Interval.to_json(interval)

#
def temporal_from_dict(temporal_dictionary: dict):
    """
    The function converts a dictionary of Temporal to a Temporal object.
    
    :param temporal_dict:    A dictionary that contains the keys of a Temporal.
    :type temporal_dict:     dict             
    :rtype:                  ibmpairs.query.Temporal
    :raises Exception:       if not a dict.
    """
    return Temporal.from_dict(temporal_dictionary)

#
def temporal_to_dict(temporal: Temporal):
    """
    The function converts an object of Temporal to a dict.
    
    :param temporal:    A Temporal object.
    :type temporal:     ibmpairs.query.Temporal             
    :rtype:             dict
    """
    return Temporal.to_dict(temporal)

#
def temporal_from_json(temporal_json: Any):
    """
    The function converts a dictionary or json string of Temporal to a Temporal object.
    
    :param temporal_json:    A dictionary or json string that contains the keys of a Temporal.
    :type temporal_json:     Any             
    :rtype:                  ibmpairs.query.Temporal
    :raises Exception:       if not a dict or a str.
    """
    return Temporal.from_json(temporal_json)

#
def temporal_to_json(temporal: Temporal):
    """
    The function converts an object of Temporal to a json string.
    
    :param temporal:    A Temporal object.
    :type temporal:     ibmpairs.query.Temporal             
    :rtype:             str
    """
    return Temporal.to_json(temporal)

#
def layer_from_dict(layer_dictionary: dict):
    """
    The function converts a dictionary of Layer to a Layer object.
    
    :param layer_dict:    A dictionary that contains the keys of a Layer.
    :type layer_dict:     dict             
    :rtype:               ibmpairs.query.Layer
    :raises Exception:    if not a dict.
    """
    return Layer.from_dict(layer_dictionary)
    
#
def layer_from_dict_post(layer_dictionary: dict):
    """
    The function converts a dictionary of Layer to a Layer object.
    
    :param layer_dict:    A dictionary that contains the keys of a Layer.
    :type layer_dict:     dict             
    :rtype:               ibmpairs.query.Layer
    :raises Exception:    if not a dict.
    """
    return Layer.from_dict_layer_post(layer_dictionary)

#
def layer_to_dict(layer: Layer):
    """
    The function converts an object of Layer to a dict.
    
    :param layer:    A Layer object.
    :type layer:     ibmpairs.query.Layer             
    :rtype:          dict
    """
    return Layer.to_dict(layer)

#
def layer_from_json(layer_json: Any):
    """
    The function converts a dictionary or json string of Layer to a Layer object.
    
    :param layer_json:    A dictionary or json string that contains the keys of a Layer.
    :type layer_json:     Any             
    :rtype:               ibmpairs.query.Layer
    :raises Exception:    if not a dict or a str.
    """
    return Layer.from_json(layer_json)
    
#
def layer_from_json_post(layer_json: Any):
    """
    The function converts a dictionary or json string of Layer to a Layer object, ready for post.
    
    :param layer_json:    A dictionary or json string that contains the keys of a Layer.
    :type layer_json:     Any             
    :rtype:               ibmpairs.query.Layer
    :raises Exception:    if not a dict or a str.
    """
    return Layer.from_json_layer_post(layer_json)

#
def layer_to_json(layer: Layer):
    """
    The function converts an object of Layer to a json string.
    
    :param layer:    A Layer object.
    :type layer:     ibmpairs.query.Layer             
    :rtype:          str
    """
    return Layer.to_json(layer)

#
def notification_from_dict(notification_dictionary: dict):
    """
    The function converts a dictionary of Notification to a Notification object.
    
    :param notification_dict:    A dictionary that contains the keys of a Notification.
    :type notification_dict:     dict             
    :rtype:                      ibmpairs.query.Notification
    :raises Exception:           if not a dict.
    """
    return Notification.from_dict(notification_dictionary)

#
def notification_to_dict(notification: Notification):
    """
    The function converts an object of Notification to a dict.
    
    :param notification:    A Notification object.
    :type notification:     ibmpairs.query.Notification             
    :rtype:                 dict
    """
    return Notification.to_dict(notification)

#
def notification_from_json(notification_json: Any):
    """
    The function converts a dictionary or json string of Notification to a Notification object.
    
    :param notification_json:    A dictionary or json string that contains the keys of a Notification.
    :type notification_json:     Any             
    :rtype:                      ibmpairs.query.Notification
    :raises Exception:           if not a dict or a str.
    """
    return Notification.from_json(notification_json)

#
def notification_to_json(notification: Notification):
    """
    The function converts an object of Notification to a json string.
    
    :param notification:    A Notification object.
    :type notification:     ibmpairs.query.Notification             
    :rtype:                 str
    """
    return Notification.to_json(notification)

#
def polygon_from_dict(polygon_dictionary: dict):
    """
    The function converts a dictionary of Polygon to a Polygon object.
    
    :param polygon_dict:    A dictionary that contains the keys of a Polygon.
    :type polygon_dict:     dict             
    :rtype:                 ibmpairs.query.Polygon
    :raises Exception:      if not a dict.
    """
    return Polygon.from_dict(polygon_dictionary)

#
def polygon_to_dict(polygon: Polygon):
    """
    The function converts an object of Polygon to a dict.
    
    :param polygon:    A Polygon object.
    :type polygon:     ibmpairs.query.Polygon             
    :rtype:            dict
    """
    return Polygon.to_dict(polygon)

#
def polygon_from_json(polygon_json: Any):
    """
    The function converts a dictionary or json string of Polygon to a Polygon object.
    
    :param polygon_json:    A dictionary or json string that contains the keys of a Polygon.
    :type polygon_json:     Any             
    :rtype:                 ibmpairs.query.Polygon
    :raises Exception:      if not a dict or a str.
    """
    return Polygon.from_json(polygon_json)

#
def polygon_to_json(polygon: Polygon):
    """
    The function converts an object of Polygon to a json string.
    
    :param polygon:    A Polygon object.
    :type polygon:     ibmpairs.query.Polygon             
    :rtype:            str
    """
    return Polygon.to_json(polygon)

#
def spatial_from_dict(spatial_dictionary: dict):
    """
    The function converts a dictionary of Spatial to a Spatial object.
    
    :param spatial_dict:    A dictionary that contains the keys of a Spatial.
    :type spatial_dict:     dict             
    :rtype:                 ibmpairs.query.Spatial
    :raises Exception:      if not a dict.
    """
    return Spatial.from_dict(spatial_dictionary)

#
def spatial_to_dict(spatial: Spatial):
    """
    The function converts an object of Spatial to a dict.
    
    :param spatial:    A Spatial object.
    :type spatial:     ibmpairs.query.Spatial             
    :rtype:            dict
    """
    return Spatial.to_dict(spatial)

#
def spatial_from_json(spatial_json: Any):
    """
    The function converts a dictionary or json string of Spatial to a Spatial object.
    
    :param spatial_json:    A dictionary or json string that contains the keys of a Spatial.
    :type spatial_json:     Any             
    :rtype:                 ibmpairs.query.Spatial
    :raises Exception:      if not a dict or a str.
    """
    return Spatial.from_json(spatial_json)

#
def spatial_to_json(spatial: Spatial):
    """
    The function converts an object of Spatial to a json string.
    
    :param spatial:    A Spatial object.
    :type spatial:     ibmpairs.query.Spatial             
    :rtype:            str
    """
    return Spatial.to_json(spatial)

#
def upload_from_dict(upload_dictionary: dict):
    """
    The function converts a dictionary of Upload to a Upload object.
    
    :param upload_dict:    A dictionary that contains the keys of a Upload.
    :type upload_dict:     dict             
    :rtype:                ibmpairs.query.Upload
    :raises Exception:     if not a dict.
    """
    return Upload.from_dict(upload_dictionary)

#
def upload_to_dict(upload: Upload):
    """
    The function converts an object of Upload to a dict.
    
    :param upload:    A Upload object.
    :type upload:     ibmpairs.query.Upload             
    :rtype:           dict
    """
    return Upload.to_dict(upload)

#
def upload_from_json(upload_json: Any):
    """
    The function converts a dictionary or json string of Upload to a Upload object.
    
    :param upload_json:    A dictionary or json string that contains the keys of a Upload.
    :type upload_json:     Any             
    :rtype:                ibmpairs.query.Upload
    :raises Exception:     if not a dict or a str.
    """
    return Upload.from_json(upload_json)

#
def upload_to_json(upload: Upload):
    """
    The function converts an object of Upload to a json string.
    
    :param upload:    A Upload object.
    :type upload:     ibmpairs.query.Upload             
    :rtype:           str
    """
    return Upload.to_json(upload)

#
def query_response_data_from_dict(query_response_data_dictionary: dict):
    """
    The function converts a dictionary of QueryResponseData to a QueryResponseData object.
    
    :param query_response_data_dict:    A dictionary that contains the keys of a QueryResponseData.
    :type query_response_data_dict:     dict             
    :rtype:                             ibmpairs.query.QueryResponseData
    :raises Exception:                  if not a dict.
    """
    return QueryResponseData.from_dict(query_response_data_dictionary)

#
def query_response_data_to_dict(query_response_data: QueryResponseData):
    """
    The function converts an object of QueryResponseData to a dict.
    
    :param query_response_data:    A QueryResponseData object.
    :type query_response_data:     ibmpairs.query.QueryResponseData             
    :rtype:                        dict
    """
    return QueryResponseData.to_dict(query_response_data)

#
def query_response_data_from_json(query_response_data_json: Any):
    """
    The function converts a dictionary or json string of QueryResponseData to a QueryResponseData object.
    
    :param query_response_data_json:    A dictionary or json string that contains the keys of a QueryResponseData.
    :type query_response_data_json:     Any             
    :rtype:                             ibmpairs.query.QueryResponseData
    :raises Exception:                  if not a dict or a str.
    """
    return QueryResponseData.from_json(query_response_data_json)

#
def query_response_data_to_json(query_response_data: QueryResponseData):
    """
    The function converts an object of QueryResponseData to a json string.
    
    :param query_response_data:    A QueryResponseData object.
    :type query_response_data:     ibmpairs.query.QueryResponseData             
    :rtype:                        str
    """
    return QueryResponseData.to_json(query_response_data)

#
def query_response_from_dict(query_response_dictionary: dict):
    """
    The function converts a dictionary of QueryResponse to a QueryResponse object.
    
    :param query_response_dict:    A dictionary that contains the keys of a QueryResponse.
    :type query_response_dict:     dict             
    :rtype:                        ibmpairs.query.QueryResponse
    :raises Exception:             if not a dict.
    """
    return QueryResponse.from_dict(query_response_dictionary)

#
def query_response_to_dict(query_response: QueryResponse):
    """
    The function converts an object of QueryResponse to a dict.
    
    :param query_response:    A QueryResponse object.
    :type query_response:     ibmpairs.query.QueryResponse             
    :rtype:                   dict
    """
    return QueryResponse.to_dict(query_response)

#
def query_response_from_json(query_response_json: Any,
                             compact_csv: bool = False
                            ):
    """
    The function converts a dictionary or json string of QueryResponse to a QueryResponse object.
    
    :param query_response_json:    A dictionary or json string that contains the keys of a QueryResponse.
    :type query_response_json:     Any     
    :param compact_csv:            A flag to indicate the return of a compact csv format.
    :type compact_csv:             bool        
    :rtype:                        ibmpairs.query.QueryResponse
    :raises Exception:             if not a dict or a str.
    """
    return QueryResponse.from_json(query_response_json,
                                   compact_csv = compact_csv)

#
def query_response_to_json(query_response: QueryResponse):
    """
    The function converts an object of QueryResponse to a json string.
    
    :param query_response:    A QueryResponse object.
    :type query_response:     ibmpairs.query.QueryResponse             
    :rtype:                   str
    """
    return QueryResponse.to_json(query_response)

#
def query_job_from_dict(query_job_dictionary: dict):
    """
    The function converts a dictionary of QueryJob to a QueryJob object.
    
    :param query_job_dict:    A dictionary that contains the keys of a QueryJob.
    :type query_job_dict:     dict             
    :rtype:                   ibmpairs.query.QueryJob
    :raises Exception:        if not a dict.
    """
    return QueryJob.from_dict(query_job_dictionary)

#
def query_job_to_dict(query_job: QueryJob):
    """
    The function converts an object of QueryJob to a dict.
    
    :param query_job:    A QueryJob object.
    :type query_job:     ibmpairs.query.QueryJob             
    :rtype:              dict
    """
    return QueryJob.to_dict(query_job)

#
def query_job_from_json(query_job_json: Any):
    """
    The function converts a dictionary or json string of QueryJob to a QueryJob object.
    
    :param query_job_json:    A dictionary or json string that contains the keys of a QueryJob.
    :type query_job_json:     Any             
    :rtype:                   ibmpairs.query.QueryJob
    :raises Exception:        if not a dict or a str.
    """
    return QueryJob.from_json(query_job_json)

#
def query_job_to_json(query_job: QueryJob):
    """
    The function converts an object of QueryJob to a json string.
    
    :param query_job:    A QueryJob object.
    :type query_job:     ibmpairs.query.QueryJob             
    :rtype:              str
    """
    return QueryJob.to_json(query_job)

#
def query_jobs_from_dict(query_jobs_dictionary: dict):
    """
    The function converts a dictionary of QueryJobs to a QueryJobs object.
    
    :param query_jobs_dict:    A dictionary that contains the keys of a QueryJobs.
    :type query_jobs_dict:     dict             
    :rtype:                    ibmpairs.query.QueryJobs
    :raises Exception:         if not a dict.
    """
    return QueryJobs.from_dict(query_jobs_dictionary)

#
def query_jobs_to_dict(query_jobs: QueryJobs):
    """
    The function converts an object of QueryJobs to a dict.
    
    :param query_jobs:    A QueryJobs object.
    :type query_jobs:     ibmpairs.query.QueryJobs             
    :rtype:               dict
    """
    return QueryJobs.to_dict(query_jobs)

#
def query_jobs_from_json(query_jobs_json: Any):
    """
    The function converts a dictionary or json string of QueryJobs to a QueryJobs object.
    
    :param query_jobs_json:    A dictionary or json string that contains the keys of a QueryJobs.
    :type query_jobs_json:     Any             
    :rtype:                    ibmpairs.query.QueryJobs
    :raises Exception:         if not a dict or a str.
    """
    return QueryJobs.from_json(query_jobs_json)

#
def query_jobs_to_json(query_jobs: QueryJobs):
    """
    The function converts an object of QueryJobs to a json string.
    
    :param query_jobs:    A QueryJobs object.
    :type query_jobs:     ibmpairs.query.QueryJobs             
    :rtype:               str
    """
    return QueryJobs.to_json(query_jobs)

#
def query_job_layer_from_dict(query_job_layer_dictionary: dict):
    """
    The function converts a dictionary of QueryJobLayer to a QueryJobLayer object.
    
    :param query_job_layer_dict:    A dictionary that contains the keys of a QueryJobLayer.
    :type query_job_layer_dict:     dict             
    :rtype:                         ibmpairs.query.QueryJobLayer
    :raises Exception:              if not a dict.
    """
    return QueryJobLayer.from_dict(query_job_layer_dictionary)

#
def query_job_layer_to_dict(query_job_layer: QueryJobLayer):
    """
    The function converts an object of QueryJobLayer to a dict.
    
    :param query_job_layer:    A QueryJobLayer object.
    :type query_job_layer:     ibmpairs.query.QueryJobLayer             
    :rtype:                    dict
    """
    return QueryJobLayer.to_dict(query_job_layer)

#
def query_job_layer_from_json(query_job_layer_json: Any):
    """
    The function converts a dictionary or json string of QueryJobLayer to a QueryJobLayer object.
    
    :param query_job_layer_json:    A dictionary or json string that contains the keys of a QueryJobLayer.
    :type query_job_layer_json:     Any             
    :rtype:                         ibmpairs.query.QueryJobLayer
    :raises Exception:              if not a dict or a str.
    """
    return QueryJobLayer.from_json(query_job_layer_json)

#
def query_job_layer_to_json(query_job_layer: QueryJobLayer):
    """
    The function converts an object of QueryJobLayer to a json string.
    
    :param query_job_layer:    A QueryJobLayer object.
    :type query_job_layer:     ibmpairs.query.QueryJobLayer             
    :rtype:                    str
    """
    return QueryJobLayer.to_json(query_job_layer)

#
def query_job_layers_from_dict(query_job_layers_dictionary: dict):
    """
    The function converts a dictionary of QueryJobLayers to a QueryJobLayers object.
    
    :param query_job_layers_dict:    A dictionary that contains the keys of a QueryJobLayers.
    :type query_job_layers_dict:     dict             
    :rtype:                          ibmpairs.query.QueryJobLayers
    :raises Exception:               if not a dict.
    """
    return QueryJobLayers.from_dict(query_job_layers_dictionary)

#
def query_job_layers_to_dict(query_job_layers: QueryJobLayers):
    """
    The function converts an object of QueryJobLayers to a dict.
    
    :param query_job_layers:    A QueryJobLayers object.
    :type query_job_layers:     ibmpairs.query.QueryJobLayers             
    :rtype:                     dict
    """
    return QueryJobLayers.to_dict(query_job_layers)

#
def query_job_layers_from_json(query_job_layers_json: Any):
    """
    The function converts a dictionary or json string of QueryJobLayers to a QueryJobLayers object.
    
    :param query_job_layers_json:    A dictionary or json string that contains the keys of a QueryJobLayers.
    :type query_job_layers_json:     Any             
    :rtype:                          ibmpairs.query.QueryJobLayers
    :raises Exception:               if not a dict or a str.
    """
    return QueryJobLayers.from_json(query_job_layers_json)

#
def query_job_layers_to_json(query_job_layers: QueryJobLayers):
    """
    The function converts an object of QueryJobLayers to a json string.
    
    :param query_job_layers:    A QueryJobLayers object.
    :type query_job_layers:     ibmpairs.query.QueryJobLayers             
    :rtype:                     str
    """
    return QueryJobLayers.to_json(query_job_layers)

#
def group_from_dict(group_dictionary: dict):
    """
    The function converts a dictionary of Group to a Group object.
    
    :param group_dict:    A dictionary that contains the keys of a Group.
    :type group_dict:     dict             
    :rtype:               ibmpairs.query.Group
    :raises Exception:    if not a dict.
    """
    return Group.from_dict(group_dictionary)

#
def group_to_dict(group: Group):
    """
    The function converts an object of Group to a dict.
    
    :param group:    A Group object.
    :type group:     ibmpairs.query.Group             
    :rtype:          dict
    """
    return Group.to_dict(group)

#
def group_from_json(group_json: Any):
    """
    The function converts a dictionary or json string of Group to a Group object.
    
    :param group_json:    A dictionary or json string that contains the keys of a Group.
    :type group_json:     Any             
    :rtype:               ibmpairs.query.Group
    :raises Exception:    if not a dict or a str.
    """
    return Group.from_json(group_json)

#
def group_to_json(group: Group):
    """
    The function converts an object of Group to a json string.
    
    :param group:    A Group object.
    :type group:     ibmpairs.query.Group             
    :rtype:          str
    """
    return Group.to_json(group)

#
def user_from_dict(user_dictionary: dict):
    """
    The function converts a dictionary of User to a User object.
    
    :param user_dict:    A dictionary that contains the keys of a User.
    :type user_dict:     dict             
    :rtype:              ibmpairs.query.User
    :raises Exception:   if not a dict.
    """
    return User.from_dict(user_dictionary)

#
def user_to_dict(user: User):
    """
    The function converts an object of User to a dict.
    
    :param user:    A User object.
    :type user:     ibmpairs.query.User             
    :rtype:         dict
    """
    return User.to_dict(user)

#
def user_from_json(user_json: Any):
    """
    The function converts a dictionary or json string of User to a User object.
    
    :param user_json:    A dictionary or json string that contains the keys of a User.
    :type user_json:     Any             
    :rtype:              ibmpairs.query.User
    :raises Exception:   if not a dict or a str.
    """
    return User.from_json(user_json)

#
def user_to_json(user: User):
    """
    The function converts an object of User to a json string.
    
    :param user:    A User object.
    :type user:     ibmpairs.query.User             
    :rtype:         str
    """
    return User.to_json(user)

#
def query_output_info_file_from_dict(query_output_info_file_dictionary: dict):
    """
    The function converts a dictionary of QueryOutputInfoFile to a QueryOutputInfoFile object.
    
    :param query_output_info_file_dict:    A dictionary that contains the keys of a QueryOutputInfoFile.
    :type query_output_info_file_dict:     dict             
    :rtype:                                ibmpairs.query.QueryOutputInfoFile
    :raises Exception:                     if not a dict.
    """
    return QueryOutputInfoFile.from_dict(query_output_info_file_dictionary)

#
def query_output_info_file_to_dict(query_output_info_file: QueryOutputInfoFile):
    """
    The function converts an object of QueryOutputInfoFile to a dict.
    
    :param query_output_info_file:    A QueryOutputInfoFile object.
    :type query_output_info_file:     ibmpairs.query.QueryOutputInfoFile             
    :rtype:                           dict
    """
    return QueryOutputInfoFile.to_dict(query_output_info_file)

#
def query_output_info_file_from_json(query_output_info_file_json: Any):
    """
    The function converts a dictionary or json string of QueryOutputInfoFile to a QueryOutputInfoFile object.
    
    :param query_output_info_file_json:    A dictionary or json string that contains the keys of a QueryOutputInfoFile.
    :type query_output_info_file_json:     Any             
    :rtype:                                ibmpairs.query.QueryOutputInfoFile
    :raises Exception:                     if not a dict or a str.
    """
    return QueryOutputInfoFile.from_json(query_output_info_file_json)

#
def query_output_info_file_to_json(query_output_info_file: QueryOutputInfoFile):
    """
    The function converts an object of QueryOutputInfoFile to a json string.
    
    :param query_output_info_file:    A QueryOutputInfoFile object.
    :type query_output_info_file:     ibmpairs.query.QueryOutputInfoFile             
    :rtype:                           str
    """
    return QueryOutputInfoFile.to_json(query_output_info_file)

#
def query_history_from_dict(query_history_dictionary: dict,
                            client: cl.Client = None):
    """
    The function converts a dictionary of QueryHistory to a QueryHistory object.
    
    :param query_history_dict:    A dictionary that contains the keys of a QueryHistory.
    :type query_history_dict:     dict    
    :param client:                An IBM PAIRS client.
    :type client:                 ibmpairs.client.Client         
    :rtype:                       ibmpairs.query.QueryHistory
    :raises Exception:            if not a dict.
    """
    query_history = QueryHistory.from_dict(query_history_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    query_history.client = cli
    return query_history

#
def query_history_to_dict(query_history: QueryHistory):
    """
    The function converts an object of QueryHistory to a dict.
    
    :param query_history:    A QueryHistory object.
    :type query_history:     ibmpairs.query.QueryHistory             
    :rtype:                  dict
    """
    return QueryHistory.to_dict(query_history)

#
def query_history_from_json(query_history_json: Any,
                            client: cl.Client = None):
    """
    The function converts a dictionary or json string of QueryHistory to a QueryHistory object.
    
    :param query_history_json:    A dictionary or json string that contains the keys of a QueryHistory.
    :type query_history_json:     Any 
    :param client:                An IBM PAIRS client.
    :type client:                 ibmpairs.client.Client      
    :rtype:                       ibmpairs.query.QueryHistory
    :raises Exception:            if not a dict or a str.
    """
    query_history = QueryHistory.from_json(query_history_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    query_history.client = cli
    return query_history

#
def query_history_to_json(query_history: QueryHistory):
    """
    The function converts an object of QueryHistory to a json string.
    
    :param query_history:    A QueryHistory object.
    :type query_history:     ibmpairs.query.QueryHistory             
    :rtype:                  str
    """
    return QueryHistory.to_json(query_history)

#
def latest_queries_from_dict(latest_queries_dictionary: dict,
                             client: cl.Client = None):
    """
    The function converts a dictionary of LatestQueries to a LatestQueries object.
    
    :param latest_queries_dict:    A dictionary that contains the keys of a LatestQueries.
    :type latest_queries_dict:     dict 
    :param client:                 An IBM PAIRS client.
    :type client:                  ibmpairs.client.Client             
    :rtype:                        ibmpairs.query.LatestQueries
    :raises Exception:             if not a dict.
    """
    latest_queries = LatestQueries.from_dict(latest_queries_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    latest_queries.client = cli
    return latest_queries

#
def latest_queries_to_dict(latest_queries: LatestQueries):
    """
    The function converts an object of LatestQueries to a dict.
    
    :param latest_queries:    A LatestQueries object.
    :type latest_queries:     ibmpairs.query.LatestQueries             
    :rtype:                   dict
    """
    return LatestQueries.to_dict(latest_queries)

#
def latest_queries_from_json(latest_queries_json: Any,
                             client: cl.Client = None):
    """
    The function converts a dictionary or json string of LatestQueries to a LatestQueries object.
    
    :param latest_queries_json:    A dictionary or json string that contains the keys of a LatestQueries.
    :type latest_queries_json:     Any
    :param client:                 An IBM PAIRS client.
    :type client:                  ibmpairs.client.Client              
    :rtype:                        ibmpairs.query.LatestQueries
    :raises Exception:             if not a dict or a str.
    """
    latest_queries = LatestQueries.from_json(latest_queries_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    latest_queries.client = cli
    return latest_queries

#
def latest_queries_to_json(latest_queries: LatestQueries):
    """
    The function converts an object of LatestQueries to a json string.
    
    :param latest_queries:    A LatestQueries object.
    :type latest_queries:     ibmpairs.query.LatestQueries             
    :rtype:                   str
    """
    return LatestQueries.to_json(latest_queries)

#
def query_from_dict(query_dictionary: dict,
                    client: cl.Client = None):
    """
    The function converts a dictionary of Query to a Query object.
    
    :param query_dict:          A dictionary that contains the keys of a Query.
    :type query_dict:           dict            
    :param client:              An IBM PAIRS client.
    :type client:               ibmpairs.client.Client  
    :rtype:                     ibmpairs.query.Query
    :raises Exception:          if not a dict.
    """
    query = Query.from_dict(query_dictionary)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    query.client = cli
    return query

#
def query_to_dict(query: Query):
    """
    The function converts an object of Query to a dict.
    
    :param query:    A Query object.
    :type query:     ibmpairs.query.Query             
    :rtype:          dict
    """
    return Query.to_dict(query)

#
def query_to_dict_post(query: Query):
    """
    The function converts an object of Query to a dict, ready for post.
    
    :param query:    A Query object.
    :type query:     ibmpairs.query.Query             
    :rtype:          dict
    """
    return Query.to_dict_query_post(query)

#
def query_from_json(query_json: Any,
                    client: cl.Client = None):
    """
    The function converts a dictionary or json string of Query to a Query object.
    
    :param query_json:          A dictionary or json string that contains the keys of a Query.
    :type query_json:           Any
    :param client:              An IBM PAIRS client.
    :type client:               ibmpairs.client.Client 
    :rtype:                     ibmpairs.query.Query
    :raises Exception:          if not a dict or a str.
    """
    query = Query.from_json(query_json)
    cli = common.set_client(input_client = client,
                            global_client = cl.GLOBAL_PAIRS_CLIENT)
    query.client = cli
    return query

#
def query_to_json(query: Query):
    """
    The function converts an object of Query to a json string.
    
    :param query:    A Query object.
    :type query:     ibmpairs.query.Query             
    :rtype:          str
    """
    return Query.to_json(query)

#
def query_to_json_post(query: Query):
    """
    The function converts an object of Query to a json string, ready to post.
    
    :param query:    A Query object.
    :type query:     ibmpairs.query.Query             
    :rtype:          str
    """
    return Query.to_json_query_post(query)
