import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

# Move out mocked_dao into a fixture (?)
TEST_NAME = "First Name"
TEST_MAIL = "test@hotmail.com"

class TestUserController:
    @pytest.fixture
    def one_name_uc(self):
        mocked_dao = mock.MagicMock()
        mocked_dao.find.return_value = [TEST_NAME]
        return UserController(mocked_dao)

    @pytest.fixture
    def multiple_name_uc(self):
        mocked_dao = mock.MagicMock()
        mocked_dao.find.return_value = [TEST_NAME, "Second Name", "Third Name"]
        return UserController(mocked_dao)

    def test_invalid_email(self, one_name_uc):
        with pytest.raises(ValueError):
            one_name_uc.get_user_by_email("test.com")

    def test_one_name(self, one_name_uc, capsys):
        result = one_name_uc.get_user_by_email(TEST_MAIL)
        captured = capsys.readouterr()
        assert result == TEST_NAME
        assert captured.out == ""

    def test_multiple_names(self, capsys, multiple_name_uc):
        result = multiple_name_uc.get_user_by_email(TEST_MAIL)
        captured = capsys.readouterr()
        assert result == TEST_NAME
        assert TEST_MAIL in captured.out
    
    def test_no_names(self):
        mocked_dao = mock.MagicMock()
        mocked_dao.find.return_value = None
        uc = UserController(mocked_dao)

        result = uc.get_user_by_email(TEST_MAIL)
        assert result == None
