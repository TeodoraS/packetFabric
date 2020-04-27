# coding=utf-8
"""
==============================================================================

Name:           'test_rest_engine'

Purpose:        unit tests for rest API engine

Author:         WhoAmI
Created:        25-04-2020
Copyright:      (c) WhoAmI 2020
Licence:        All Rights Reserved

==============================================================================

Extra used pypi modules which may need to be installed:

==============================================================================
"""
from collections import namedtuple
from mock import MagicMock
from unittest.mock import patch

from framework.engines.rest_engine import RestEngine


class TestRestEngine(object):

    mock_requests = MagicMock()
    rest_engine = RestEngine()
    request_value = namedtuple('Value', 'return_code json')

    class DummyClass(MagicMock):
        """
        dummy class to return a dummy json
        """

        dummy_json = {
            "status": 200,
            "message": "GET successful",
            "data": {"key": "/test_param", "value": "parameter_from_rest"},
            "content": {"key": "/frame.jpg", "value": "a_content"},
        }
        text = "test"
        content = "a_content"
        status_code = 200

        def json(self):
            """"
            return dummy json
            """
            return self.dummy_json

    def test_get(self):
        """
        test function for RestEngine.get()
        """
        with patch("framework.engines.rest_engine.RestEngine._session") as session_patch:
            session_patch.get.return_value = self.DummyClass()

            url_test_param = "/test_param"
            json_val = {
                "status": 200,
                "message": "GET successful",
                "data": {"key": "/test_param", "value": "parameter_from_rest"},
                "content": {"key": "/frame.jpg", "value": "a_content"},
            }
            check_val = self.request_value(200, json_val)

            assert (check_val == self.rest_engine.get(url_test_param))
            session_patch.get.assert_called_once_with(url_test_param)

    def test_post(self):
        """
        test function for RestEngine.post()
        """
        with patch("framework.engines.rest_engine.RestEngine._session") as session_patch:
            session_patch.post.return_value = self.DummyClass()

            url_test_param = "/test_param"
            body = {"value": "parameter_from_rest"}
            self.rest_engine.post(url_test_param, value=body)
            session_patch.post.assert_called_once_with(url_test_param, json=body)