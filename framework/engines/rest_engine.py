# coding=utf-8
"""
==============================================================================
Name:           'rest_engine'
Purpose:        engine class for rest API commands
Author:         WhoAmI
Created:        25-04-2020
Copyright:      (c) WhoAmI 2020
Licence:        All Rights Reserved
==============================================================================
Extra used pypi modules which may need to be installed:
==============================================================================
"""
from collections import namedtuple
import logging
import requests

from framework import config_file
from framework.helpers.he_rest import RestApiHelper


class RestEngine(object):
    """
    rest engine class
    """

    he_rest = RestApiHelper()
    logger = logging.getLogger()
    request_value = namedtuple("Value", "return_code json")

    def __init__(self):
        if not hasattr(type(self), "_session"):
            self._create_session(config_file.login_params)
        self.logger.info("Rest engine initialized")

    @classmethod
    def _create_session(cls, login_params):
        """
        create restAPI session

        :return: session object
        """
        url = cls.he_rest.generate_full_endpoint("login")
        cls._session = requests.Session()
        cls._session.post(url, data=login_params)

    def close_session(self):
        self._session.close()

    def get(self, url):
        resp = None
        retry = 5
        while retry:
            try:
                self.logger.info("GET {}".format(url))
                resp = self._session.get(url)
                if self.he_rest.is_http_status_code_success(resp.status_code):
                    return self.request_value(resp.status_code, resp.json())
                else:
                    raise Exception(resp.status_code, resp.text)
            except requests.exceptions.ConnectionError as e:
                lost_conn_err = e
                retry -= 1
        self.logger.error("Exception while performing 'GET' on {}, response: {}".format(url, resp))
        raise lost_conn_err

    def post(self, url, value=None):
        resp = None
        retry = 5
        while retry:
            try:
                self.logger.info("POST {}".format(url))
                resp = self._session.post(url, json=value)
                if self.he_rest.is_http_status_code_success(resp.status_code):
                    return self.request_value(resp.status_code, resp.json())
                else:
                    raise Exception(resp.status_code, resp.text)
            except requests.exceptions.ConnectionError as e:
                lost_conn_err = e
                retry -= 1
        self.logger.error("Exception while performing 'POST' on {}, response: {}".format(url, resp))
        raise lost_conn_err

    def patch(self, url, value):
        resp = None
        retry = 5
        while retry:
            try:
                self.logger.info("PATCH {}".format(url))
                resp = self._session.patch(url, json=value)
                if self.he_rest.is_http_status_code_success(resp.status_code):
                    return self.request_value(resp.status_code, resp.json())
                else:
                    raise Exception(resp.status_code, resp.text)
            except requests.exceptions.ConnectionError as e:
                lost_conn_err = e
                retry -= 1
        self.logger.error("Exception while performing 'PATCH' on {}, response: {}".format(url, resp))
        raise lost_conn_err

    def delete(self, url):
        resp = None
        retry = 5
        while retry:
            try:
                self.logger.info("DELETE {}".format(url))
                resp = self._session.delete(url)
                if self.he_rest.is_http_status_code_success(resp.status_code):
                    return self.request_value(resp.status_code, resp.json())
                else:
                    raise Exception(resp.status_code, resp.text)
            except requests.exceptions.ConnectionError as e:
                lost_conn_err = e
                retry -= 1
        self.logger.error("Exception while performing 'DELETE' on {}, response: {}".format(url, resp))
        raise lost_conn_err
