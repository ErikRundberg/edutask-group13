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


#pytest -m namespaces 
class TestDAO:
    @pytest.fixture
    def sut(self):
        with open(f'./test/static/data/test.json', 'r') as f:
            validator = json.load(f)
        with patch('src.util.dao.getValidator', return_value=validator, autospec=True):
            dao = DAO("test")

            yield dao
            dao.drop()

    def test_create(self, sut):
        to_insert = {
            "email": "pakr20@student.bth.se",
            "firstName": "Patrik",
            "lastName": "Karlsson",
            "ObjecId": "626117e2e52221c92c411ae4"
        }
        # File patch in validator
        assert sut.create(to_insert) == to_insert