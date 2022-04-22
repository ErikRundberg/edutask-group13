import pytest, json
from bson.objectid import ObjectId
from unittest.mock import patch
from src.util.dao import DAO
import pymongo

TASK_OBJECT = ObjectId("000000000000000000000000")

@pytest.mark.erik
class TestDAOerik:
    @pytest.fixture
    def sut(self):
        with open(f'./test/static/data/erik.json', 'r') as f:
            validator = json.load(f)
        with patch('src.util.dao.getValidator', return_value=validator, autospec=True):
            dao = DAO("test")

            yield dao
            dao.drop()

    def test_create(self, sut):
        test_json = {"name": "Test", "email": "test@email.com"}
        entry = sut.create(test_json)
        assert(type(entry) == dict)

    def test_duplicate(self, sut):
        test_json = {"name": "Test", "email": "test@email.com", "tasks": [TASK_OBJECT, TASK_OBJECT]}
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(test_json)

    def test_wrong_validator(self, sut):
        test_json = {"firstName": "Thor"}
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(test_json)
