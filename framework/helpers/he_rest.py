# coding=utf-8
"""
==============================================================================
Name:           'he_rest'
Purpose:        helper class for restAPI
Author:         WhoAmI
Created:        25-04-2020
Copyright:      (c) WhoAmI 2020
Licence:        All Rights Reserved
==============================================================================
Extra used pypi modules which may need to be installed:
==============================================================================
"""

BASE_URL = "https://api-sandbox-jobs.sandbox.packetfabric.net/"


class RestApiHelper(object):
    """
    helper class for restAPI
    """
    @staticmethod
    def generate_full_endpoint(endpoint, url=BASE_URL):
        """
        generate full url

        :param url: base url
        :param endpoint: endpoint
        :return: full url
        """
        return "{}/{}".format(url, endpoint)

    @staticmethod
    def generate_query_string(query_dict):
        """
        generate a full query string

        :param query_dict: query dict
        :return: full query string
        """
        if isinstance(query_dict, str):
            return query_dict
        q = ''.join("{}={}&".format(k, v) for k, v in query_dict.items() if v)
        return q[:-1]

    @staticmethod
    def is_http_status_code_success(status_code):
        """
        Check whether the HTTP status code is successful.
        (https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), it should be 2xx.

        :param status_code: HTTP status code
        :return: True if success
        """
        status_code_string = str(status_code)
        return status_code_string.startswith("2") and len(status_code_string) == 3
