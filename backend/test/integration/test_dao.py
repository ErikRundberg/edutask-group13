from operator import truediv
from typing import Collection
import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.util.dao import DAO

# coding=utf-8
import os

import pymongo
from dotenv import dotenv_values
from yaml import CollectionNode

# create a data access object
from src.util.validators import getValidator

import json
from bson import json_util
from bson.objectid import ObjectId

# # load the local mongo URL (something like mongodb://localhost:27017)
#         LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
#         # check out of the environment (which can be overridden by the docker-compose file) also specifies an URL, and use that instead if it exists
#         MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

#         client = pymongo.MongoClient(MONGO_URL)
#         client.drop_database("testedutask")
#         database = client.testedutask

#         validator = getValidator("user")
#         database.create_collection("user", validator=validator)
# client.drop_database("testedutask")

#pytest -m namespaces 
class TestDAO:
    @pytest.fixture
    def sut(self):
        LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
        MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
        client = pymongo.MongoClient(MONGO_URL)

        sut = DAO("test_table")
        with patch('src.util.helpers.DAO.getValidator', autospec=True) as sut.mocked_validator:
            with open(f'./test/static/data/{"test.json"}.json', 'r') as f:
                sut.mocked_validator = json.load(f)
            yield sut
            client.drop("test_table")

    def test_create(self):
        to_insert = [{
            "email": "pakr20@student.bth.se",
            "firstName": "Patrik",
            "lastName": "Karlsson"
        }]
        # File patch in validator
        assert DAO.create(self, to_insert) == to_insert