import pytest
import json, os
import unittest.mock as mock
from unittest.mock import patch
from src.util.dao import DAO

class TestDAO:
    @pytest.fixture
    def sut(self):
        test_dao = DAO("user")
        json_string = {'firstName': 'John', 'lastName': 'Doe', 'email': "john.doe@hotmail.com"}
        obj = test_dao.create(json_string)

        # yield instead of return the system under test
        yield obj

        # clean up the file after all tests have run
        test_dao.delete(obj["_id"]["$oid"])

    def test_create_user(self, sut):
        assert(sut != None)