"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
import json
from typing import Any, Callable, cast, List, Type, TypeVar
from datetime import datetime
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
from ibmpairs.logger import logger
import ibmpairs.messages as messages
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import asyncio
import threading
#}}}

# fold: Exceptions {{{
# A common exception class
class PAWException(Exception):
    def __init__(self,  message):
        self.message = message
#}}}

# fold: Static Variables {{{
#
T = TypeVar("T")
#}}}

# fold: Type Methods {{{
#
def from_list(input_type: Any, input_function: Callable[[Any], T]):
    check_list(input_type)
    output = [input_function(list_type) for list_type in input_type]
    return output

def class_to_dict(instance: Any, 
                  class_type: Type[T]
                 ) -> dict:
    
    """
    The method casts a classes attribute structure to a dict.

    :param instance:    The input instance of a class.
    :type instance:     Any
    :param class_type:  The input class type.
    :type class_type:   Type[T]
    :returns:           A dictionary of the input classes attributes.
    :rtype:             dict
    :raises Exception:  If the class cannot be cast to a dict.
    """          
    
    dict_of_class = None
    
    try:
        check_class(instance, class_type)
        dict_of_class = cast(Any, instance).to_dict()
    except:
        msg = messages.ERROR_COMMON_CLASS_TO_DICT.format(str(instance), str(class_type))
        logger.error(msg)
        raise PAWException(msg)
        
    return dict_of_class

def check_bool(b: Any) -> bool:
    
    """
    The method checks if a boolean value, or a string or int that can validly be inferred to be boolean is found. If 'true' or 'false' (to lowercase) or '0' or '1' are found, they are transformed appropriately to a bool.

    :param b:           The input value to check.
    :type b:            Any
    :returns:           A boolean of appropriate value 'True' or 'False'
    :rtype:             bool
    :raises Exception:  If the type of 'b' is not in ['bool', 'string' or 'int'], 
                        if the value of 'b' is a string but not (when converted to lowercase) 'true' or 'false', 
                        if the value of 'b' is an integer but not '1' or '0'.
    """
    
    bo = None
    
    if isinstance(b, bool):
        bo = b
    elif isinstance(b, str):
        if b.lower() == 'true':
            bo = True;
            msg = messages.INFO_COMMON_CHECK_BOOL_CONVERSION.format(type(b), str(b), 'True')
            logger.info(msg)
        elif b.lower() == 'false':
            bo = False;
            msg = messages.INFO_COMMON_CHECK_BOOL_CONVERSION.format(type(b), str(b), 'False')
            logger.info(msg)
        else:
            msg = messages.ERROR_COMMON_CHECK_BOOL_STRING_NOT_BOOL.format(str(b))
            logger.error(msg)
            raise PAWException(msg)
    elif isinstance(b, int):
        if b == 1:
            bo = True;
            msg = messages.INFO_COMMON_CHECK_BOOL_CONVERSION.format(type(b), str(b), 'True')
            logger.info(msg)
        elif b == 0:
            bo = False;
            msg = messages.INFO_COMMON_CHECK_BOOL_CONVERSION.format(type(b), str(b), 'False')
            logger.info(msg)
        else:
            msg = messages.ERROR_COMMON_CHECK_BOOL_INT_NOT_BOOL.format(str(b))
            logger.error(msg)
            raise PAWException(msg)
    else:
        msg = messages.ERROR_COMMON_CHECK_BOOL.format(type(bo), str(bo))
        logger.error(msg)
        raise PAWException(msg)
    
    return bo
    
#
def check_class(instance: Any, 
                class_type: Type[T]
               ) -> Any:
    
    """
    The method checks if a provided 'instance' is of type 'class_type' with the intention of usage to check classes.

    :param instance:    The input value to check.
    :type istance:      Any
    :param class_type:  The input type to check the input value against.
    :type class_type:   Type[T]
    :returns:           The input value.
    :rtype:             Any
    :raises Exception:  If the value of 'instance' is not type 'class_type'.
    """            
    
    try:
        assert isinstance(instance, class_type)
    except:
        msg = messages.ERROR_COMMON_CHECK_CLASS.format(type(instance), type(class_type))
        logger.error(msg)
        raise PAWException(msg)
    
    return instance

#
def check_dict(d: Any) -> dict:
    
    """
    The method checks if the input value is of type dict.

    :param d:           The input value to check.
    :type d:            dict
    :returns:           The input value.
    :rtype:             dict
    :raises Exception:  If the type of 'd' is not 'dict'.
    """ 
    
    try:
        assert isinstance(d, dict)
    except:
        msg = messages.ERROR_COMMON_CHECK_WRONG_TYPE.format(type(d), str(d), 'dict')
        logger.error(msg)
        raise PAWException(msg)
    
    return d
    
def check_datetime(d: Any):
    assert isinstance(d, datetime)
    return d

#
def check_float(f: Any):
    
    """
    The method checks if the input value is of type float, if the input type is an 'int' or 'str' a cast is attempted.

    :param f:           The input value to check.
    :type f:            float
    :returns:           The input value.
    :rtype:             float
    :raises Exception:  If the type of 'f' is not 'float' or 'int' or 'str', 
                        if the input value cannot be cast to 'float'.
    """ 
    
    fl = None
    
    if isinstance(f, float):
        fl = f
    elif isinstance(f, str):
        try:
            fl = float(f)
        except:
            msg = messages.ERROR_COMMON_STR_TO_FLOAT.format(f)
            logger.error(msg)
            raise PAWException(msg)
    elif isinstance(f, int):
        try:
            fl = float(f)
        except:
            msg = messages.ERROR_COMMON_INT_TO_FLOAT.format(f)
            logger.error(msg)
            raise PAWException(msg)
    else:
        msg = messages.ERROR_COMMON_CHECK_FLOAT.format(type(f), str(f))
        logger.error(msg)
        raise PAWException(msg)        

    return fl

#
def check_int(i: Any):
    
    """
    The method checks if the input value is of type int, if the input type is str a 
    cast is attempted.

    :param s:           The input value to check.
    :type s:            int
    :returns:           The input value.
    :rtype:             int
    :raises Exception:  If the type of 'i' is not 'int' or 'str', 
                        if the input value cannot be cast to 'int'.
    """ 
    
    integer = None
    
    if isinstance(i, int):
        integer = i
    elif isinstance(i, str):
        try:
            integer = int(i)
        except:
            msg = messages.ERROR_COMMON_STR_TO_INT.format(i)
            logger.error(msg)
            raise PAWException(msg)
    else:
        msg = messages.ERROR_COMMON_CHECK_INT.format(type(i), str(i))
        logger.error(msg)
        raise PAWException(msg)
    return integer
    
#
def check_list(l: Any) -> list:
    
    """
    The method checks if the input value is of type list.

    :param l:           The input value to check.
    :type l:            list
    :returns:           The input value.
    :rtype:             list
    :raises Exception:  If the type of 'l' is not 'list'.
    """ 
    
    try:
        assert isinstance(l, list)
        
    except:
        msg = messages.ERROR_COMMON_CHECK_WRONG_TYPE.format(type(l), str(l), 'list')
        logger.error(msg)
        raise PAWException(msg)
    
    return l

#
def check_str(s: Any) -> str:
    
    """
    The method checks if the input value is of type str, if the input type is int a 
    cast is attempted.

    :param s:           The input value to check.
    :type s:            str
    :returns:           The input value.
    :rtype:             str
    :raises Exception:  If the type of 's' is not 'str' or 'int', 
                        if the input value cannot be cast to 'str'.
    """ 
    
    string = None
    
    if isinstance(s, str):
        string = s
    elif isinstance(s, int):
        try:
            string = str(s)
        except:
            msg = messages.ERROR_COMMON_INT_TO_STR.format(s)
            logger.error(msg)
            raise PAWException(msg)
    else:
        msg = messages.ERROR_COMMON_CHECK_STR.format(type(s), str(s))
        logger.error(msg)
        raise PAWException(msg)
    
    return string
#}}}

#
def ensure_slash(directory: str, 
                 position: int
                ):
    
    """
    The method ensures a slash is present.

    :param directory:   The directory string to check.
    :type directory:    str
    :param position:    The position to check for slash.
    :type position:     int
    :returns:           A directory path with slash.
    :rtype:             str
    """ 
    
    if directory[position] != "/":
        directory = directory + "/"
    else:
        directory = directory
    return directory
    
class AsyncThreadWrapper(threading.Thread):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        super().__init__()

    def run(self):
        
        """
        The method runs an arbitrarily declared asyncio function from information held 
        in the AsyncThreadWrapper object.
        """
        
        self.result = asyncio.run(self.func(*self.args, **self.kwargs))

def run_async_in_thread(func, *args, **kwargs):
    
    """
    The method runs an arbitrarily declared asyncio function in a new thread.

    :param func:        The name of the function to run.
    :type func:         str
    :param *args:       The arguments of the function.
    :type *args:        
    :param **kwargs:    The arguments of the function.
    :type **kwargs:     
    :returns:           the result of the execution of the thread
    :rtype:             AsyncThreadWrapper.result
    """ 
    
    thread = AsyncThreadWrapper(func, args, kwargs)
    thread.start()
    thread.join()
    if thread.result is not None:
       res = thread.result
    else:
       res = None
    return res

def set_client(input_client,
               global_client,
               self_client = None
              ):
                
    """
    The method selects a ibmpairs.client.Client from a few choices.

    :param input_client:   A client input into the method that calls set_client().
    :type input_client:    ibmpairs.client.Client
    :param global_client:  The global client in the environment.
    :type global_client:   ibmpairs.client.Client 
    :param self_client:    The client held in the object that calls the method that calls set_client().
    :type self_client:     ibmpairs.client.Client
    :returns:              the selected client from the hierarchy.
    :rtype:                ibmpairs.client.Client
    :raises Exception:     If no client is present.
    """ 
    
    if input_client is not None:
        msg = messages.DEBUG_CLIENT_PROVIDED_FOUND
        logger.debug(msg)
        return input_client
    elif (input_client is None) and (self_client is not None):
        msg = messages.DEBUG_CLIENT_IN_OBJECT_FOUND
        logger.debug(msg)
        return self_client
    elif (input_client is None) and (self_client is None) and (global_client is not None):
        msg = messages.DEBUG_CLIENT_GLOBAL_FOUND
        logger.debug(msg)
        return global_client
    else:
        msg = messages.ERROR_NO_CLIENT
        logger.error(msg)
        raise PAWException(msg)

#
def strip_protocol(host: str):
    
    """
    Removes https:// or http:// from a string.

    :param host:   The host string.
    :type host:    str
    :returns:      The host string with the protocol removed.
    :rtype:        str
    """ 

    protocol = 'https://'
    host     = host
    
    if host.startswith('https://'):
        host = host[8:]
    elif host.startswith('http://'):
        host = host[7:]
    
    return host

#
def ensure_protocol(host: str):
    
    """
    Ensures https:// or https:// is prepended to a string.

    :param host:   The host string.
    :type host:    str
    :returns:      The host string with the protocol added.
    :rtype:        str
    """ 
    
    if host.startswith('pairs.res') or host.startswith('http://pairs.res'):
        return "https://" + strip_protocol(host)
    else:
        if host.startswith('http://'):
            return "http://" + strip_protocol(host)
        else:
            return "https://" + strip_protocol(host)
