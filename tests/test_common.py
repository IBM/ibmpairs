"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019-2020 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

import unittest
import json

from ibmpairs.logger import logger
import ibmpairs.common as common

class CommonUnitTest(unittest.TestCase):

    def setUp(self):
        self.logger = logger
        self.logger.info('setup')

    def tearDown(self):
        self.logger.info('teardown')
        
    def test_check_bool(self):
        self.logger.info('test_check_bool')
        
        self.assertTrue(common.check_bool(True))

        self.assertFalse(common.check_bool(False))

        self.assertTrue(common.check_bool('True'))

        self.assertFalse(common.check_bool('False'))

        self.assertTrue(common.check_bool('true'))

        self.assertFalse(common.check_bool('false'))

        self.assertTrue(common.check_bool('TrUe'))

        self.assertFalse(common.check_bool('FaLsE'))

        self.assertFalse(common.check_bool(0))

        self.assertTrue(common.check_bool(1))

        got_exception = False
        try:
            common.check_bool("Hello World!")
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
        got_exception = False
        try:
            common.check_bool(None)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
    def test_check_class(self):
        
        self.logger.info('test_check_class')
        
        test_class = TestClass()
        
        self.assertTrue(common.check_class(test_class, TestClass))
        
        test_class = TestClass(string = 'string', integer = 0)
        
        self.assertTrue(common.check_class(test_class, TestClass))

        example_dict: dict = {}
        example_dict["string"] = "string"
        example_dict["integer"] = 0

        got_exception = False
        try:
            common.check_class(example_dict, TestClass)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)

        got_exception = False
        try:
            common.check_class("string", TestClass)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True

        self.assertTrue(got_exception)
        
        got_exception = False
        try:
            common.check_class(0, TestClass)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True

        self.assertTrue(got_exception)
        
    def test_check_dict(self):
        
        self.logger.info('test_check_dict')
        
        self.assertEqual(common.check_float(1.0), 1.0)
        
        json_example = r'''{"name":"hello world"}'''

        example_dict_from_json = json.loads(json_example)

        self.assertIsInstance(common.check_dict(example_dict_from_json), dict)

        example_dict: dict = {}
        example_dict["id"] = 1
        example_dict["name"] = "Hello World!"

        self.assertIsInstance(common.check_dict(example_dict), dict)

        got_exception = False
        try:
            common.check_dict('Hello World!')
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
        got_exception = False
        try:
            common.check_dict(0)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
        got_exception = False
        try:
            a_list_not_dict = ["A", "B", "C"]
            common.check_dict(a_list_not_dict)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
        got_exception = False
        try:
            common.check_dict(None)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
    
    def test_check_float(self):
        
        self.logger.info('test_check_float')
        
        self.assertEqual(common.check_float(1.0), 1.0)

        self.assertEqual(common.check_float(1.01010), 1.01010)

        self.assertEqual(common.check_float(1), 1.0)

        self.assertEqual(common.check_float("1.0"), 1.0)

        self.assertEqual(common.check_float("1"), 1.0)

        got_exception = False
        try:
            common.check_float('Hello World!')
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
        got_exception = False
        try:
            common.check_float(None)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)

    def test_check_int(self):
        self.logger.info('test_check_int')
        
        self.assertEqual(common.check_int(0), 0)

        self.assertEqual(common.check_int(1000), 1000)

        self.assertEqual(common.check_int('0'), 0)

        self.assertEqual(common.check_int('1000'), 1000)

        got_exception = False
        try:
            common.check_int('Hello World!')
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
        got_exception = False
        try:
            common.check_int(None)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)
        
    def test_check_list(self):
        
        self.logger.info('test_check_list')
        
        str_list = ["A", "B", "C"]

        int_list = [0, 1, 2]

        not_a_list = "Hello World!"

        self.assertIsInstance(common.check_list(str_list), list)
        
        self.assertIsInstance(common.check_list(int_list), list)

        got_exception = False
        try:
            common.check_list(not_a_list)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)

        got_exception = False
        try:
            common.check_list(None)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)

    def test_check_str(self):
        
        self.logger.info('test_check_str')
        
        self.assertEqual(common.check_str(0), '0')

        self.assertEqual(common.check_str(1000), '1000')

        self.assertEqual(common.check_str('0'), '0')

        self.assertEqual(common.check_str('1000'), '1000')
        
        self.assertEqual(common.check_str('Hello World!'), 'Hello World!')
        
        got_exception = False
        try:
            common.check_str(None)
        except Exception as ex:
            self.logger.error(ex)
            got_exception = True
        
        self.assertTrue(got_exception)


class TestClass:
    _string: str
    _integer: int

    #
    def __str__(self):
        return json.dumps(self.to_dict())

    #
    def __repr__(self):
        return json.dumps(self.to_dict())

    #
    def __init__(self, 
                 string: str  = None,
                 integer: int = None
                ) -> None:
        self._string = string
        self._integer = integer
    
    #       
    def get_string(self):
        return self._string

    #
    def set_string(self, string):
        self._string = common.check_str(string)
        
    #    
    def del_string(self): 
        del self._string

    #    
    string = property(get_string, set_string, del_string)
        
    #       
    def get_integer(self):
        return self._integer

    #
    def set_integer(self, integer):
        self._integer = common.check_int(integer)
        
    #    
    def del_integer(self): 
        del self._integer

    #    
    integer = property(get_integer, set_integer, del_integer)
