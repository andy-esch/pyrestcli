import pytest
from datetime import datetime

from pyrestcli.exceptions import NotFoundException

from models import Question, QuestionManager


@pytest.fixture(scope="module")
def question_manager(basic_auth_client):
    """
    Returns a dataset manager that can be reused in tests
    :param api_key_auth_client: Fixture that provides a valid BasicAuthClient object
    :return: QuestionManager instance
    """
    return QuestionManager(basic_auth_client)


def test_get_questions(question_manager):
    """
    Returns a list of questions
    :param question_manager: Fixture that provides a question manager to work with
    """
    questions = question_manager.all()

    assert len(questions) >= 0
    assert isinstance(questions[0], Question)
    assert isinstance(questions[1], Question)


def test_get_one_question(question_manager):
    """
    Test retrieval of a single user from the API
    :param user: There is a fixture that returns a user object, so let's use it instead of specifically requesting a user
    """
    question = question_manager.get(1)

    assert question.question_text == "OLA K ASE"


def test_modify_question(question_manager):
    """
    Test modifying a user
    :param user_manager: User manager to work with
    :param user: User to be modified
    """
    question = question_manager.get(1)
    assert question.question_text == "OLA K ASE"
    question.question_text = "HOLA QUE HACES"
    question.save()

    question = question_manager.get(1)
    assert question.question_text == "HOLA QUE HACES"

    # Let's undo the change
    question.question_text = "OLA K ASE"
    question.save()

    question = question_manager.get(1)
    assert question.question_text == "OLA K ASE"


def test_create_and_delete_question(question_manager):
    """
    Test creating a user and then deleting it
    :param user_manager: User manager to work with
    """
    new_question = question_manager.create(question_text="OLA K ARAS", pub_date=datetime.now())
    assert new_question.id is not None

    new_question = question_manager.get(new_question.id)
    assert new_question.question_text == "OLA K ARAS"

    pytest.set_trace()
    new_question.delete()
    with pytest.raises(NotFoundException):
        question_manager.get(new_question.id)
