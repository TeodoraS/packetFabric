# coding=utf-8
"""
==============================================================================
Name:           'test_users'
Purpose:        test users endpoint
Author:         WhoAmI
Created:        26-04-2020
Copyright:      (c) WhoAmI 2020
Licence:        All Rights Reserved
==============================================================================
Extra used pypi modules which may need to be installed:
yaml
==============================================================================
"""
import json
import yaml
import logging
import pytest

from framework.helpers.he_rest import RestApiHelper

logger = logging.getLogger()


class TestUsers:

    helper = RestApiHelper()

    def test_get_all_users(self, session, build_path):
        """
        validate keys from rest call to get all users
        """
        get_users = session.get(self.helper.generate_full_endpoint("users"))
        for element in get_users.json:
            print(element["user_email"], element["user_login"])
        assert (get_users.return_code == 200)
        with open(build_path.join("framework", "endpoints", "users", "all-users.yaml")) as yml_file:
            entries = yaml.full_load(yml_file)
            for i in range(0, len(get_users.json)):
                assert(get_users.json[i].keys() == entries.keys())

    def test_get_all_api_keys(self, session, build_path):
        """
        validate keys from rest call to get all api keys
        """
        all_api_keys = session.get(self.helper.generate_full_endpoint("api-keys"))
        assert (all_api_keys.return_code == 200)
        with open(build_path.join("framework", "endpoints", "users", "all-api-keys.yaml")) as yml_file:
            entries = yaml.full_load(yml_file)
            for i in range(0, len(all_api_keys.json)):
                assert(all_api_keys.json[i].keys() == entries.keys())

    def test_get_non_existent_user(self, session):
        """
        get non-existent user
        """
        error_message = {"error": {
                             "http_status": 404,
                             "message": "User not found",
                             "errors": [
                                 {
                                     "param_name": "user_id",
                                     "param_type": "integer",
                                     "param_value": "1111",
                                     "message": "expected: valid user ID"
                                 }
                             ]}}

        with pytest.raises(Exception) as e:
            pytest.raises(session.get(self.helper.generate_full_endpoint("users/1111")))
        err_json_resp = json.loads(e.value.args[-1])
        err_status_code = e.value.args[0]
        assert(err_status_code == 404)
        assert(err_json_resp == error_message)

    @pytest.mark.xfail
    def test_create_invalid_user_empty_user_login(self, session, build_path):
        """
        create invalid user with empty user_login
        """
        error_message = {"error": {
                            "http_status": 400,
                            "message": "Invalid user",
                            "errors": [
                                {
                                    "param_name": "user_login",
                                    "param_type": "string",
                                    "param_value": "",
                                    "message": "expected: non-empty string"
                                }
                            ]}}
        with open(build_path.join("framework", "endpoints", "users", "create-user.yaml")) as yml_file:
            entries = yaml.full_load(yml_file)
            entries["user_login"] = ""
        with pytest.raises(Exception) as e:
            session.post(self.helper.generate_full_endpoint("users/"), value=entries)
        err_json_resp = json.loads(e.value.args[-1])
        err_status_code = e.value.args[0]
        assert(err_status_code == 400)
        assert(err_json_resp == error_message)

    @pytest.mark.skip
    def test_create_user(self, session, build_path):
        with open(build_path.join("framework", "endpoints", "users", "create-user.yaml")) as yml_file:
            entries = yaml.full_load(yml_file)
            create_user = session.post(self.helper.generate_full_endpoint("users/"), value=entries)
            assert (create_user.return_code == 201)

    @pytest.mark.skip
    def test_delete_existing_user(self, session):
        """
        delete new created user
        """
        success_message = {"message": "User deleted"}

        initial_users = session.get(self.helper.generate_full_endpoint('users'))
        for user in initial_users.json:
            if user["user_email"] == "testerdoe@nobody.com":
                removed_user = user
                delete_user_id = user["user_id"]
                del_request = session.delete(self.helper.generate_full_endpoint('users/{}'.format(delete_user_id)))
                assert (del_request.return_code == 200)
                assert (del_request.json == success_message)
        altered_users = session.get(self.helper.generate_full_endpoint('users'))
        assert(removed_user not in altered_users.json)

