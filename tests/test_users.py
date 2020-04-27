import os
import yaml
import logging
import pytest

from framework.engines.rest_engine import RestEngine
from framework.helpers.he_rest import RestApiHelper

logger = logging.getLogger()


@pytest.fixture(scope='class')
def session(request):
    logger.info("Initialize RestApi Engine")
    session = RestEngine()

    def close_session():
        session.close_session()

    request.addfinalizer(close_session)
    return session


@pytest.mark.usefixtures('session')
class TestUsers:

    helper = RestApiHelper()

    def test_get_all_users(self, session):
        """
        validate keys from rest call to get all users
        """
        get_users = session.get(self.helper.generate_full_endpoint("users"))
        print(get_users)
        assert (get_users.return_code == 200)
        with open(os.getcwd() + r'\framework\endpoints\users\all-users.yaml') as yml_file:
            entries = yaml.full_load(yml_file)
            for i in range(0, len(get_users.json)):
                assert(get_users.json[i].keys() == entries.keys())

    def test_get_all_api_keys(self, session):
        """
        validate keys from rest call to get all api keys
        """
        all_api_keys = session.get(self.helper.generate_full_endpoint("/api-keys"))
        assert (all_api_keys.return_code == 200)
        with open(os.getcwd() + r'\framework\endpoints\users\all-api-keys.yaml') as yml_file:
            entries = yaml.full_load(yml_file)
            for i in range(0, len(all_api_keys.json)):
                assert(all_api_keys.json[i].keys() == entries.keys())

    @pytest.mark.xfail
    def test_create_user(self, session):
        with open(os.getcwd() + r'\framework\endpoints\users\create_user.yaml') as yml_file:
            entries = yaml.full_load(yml_file)
            create_user = session.post(self.helper.generate_full_endpoint("users/"), value=entries)
            assert(create_user.return_code == 201)

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
                break
        altered_users = session.get(self.helper.generate_full_endpoint('users'))
        assert(removed_user not in altered_users.json)

    def test_get_non_existent_user(self, session):
        """
        get non-existent user
        """
        error_message = {"errors": [
                          {
                              "type": "authorization",
                              "message": "Route does not exist",
                              "key": "user\/None.read"
                          }]}
        with pytest.raises(Exception):
            get_request = session.get(self.helper.generate_full_endpoint('users/0000'))
            assert (get_request.return_code == 404)
            assert (get_request.json == error_message)



