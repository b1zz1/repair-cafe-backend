import pytest
from sqlmodel import Session
from db import DB
from model import Tasks, TaskStatus

@pytest.fixture
def user1():
    """
    Define a task1
    """
    task1= Tasks(
        title="Ir na academia",
        description="Falar com professor para aumentar o treino",
        status=TaskStatus.NAO_INICIADO
    )
    yield task1