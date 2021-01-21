from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import pytest

from app.database.models import Event, User
from app.routers.dayview import DivAttributes


@pytest.fixture
def user():
    return User(username='test1', email='user@email.com',
                password='1a2b3c4e5f', full_name='test me')


@pytest.fixture
def event1():
    start = datetime(year=2021, month=2, day=1, hour=7, minute=5)
    end = datetime(year=2021, month=2, day=1, hour=9, minute=15)
    return Event(title='test1', content='test',
                 start=start, end=end, owner_id=1)


@pytest.fixture
def event2():
    start = datetime(year=2021, month=2, day=1, hour=13, minute=13)
    end = datetime(year=2021, month=2, day=1, hour=15, minute=46)
    return Event(title='test2', content='test',
                 start=start, end=end, owner_id=1, color='blue')


@pytest.fixture
def multiday_event():
    start = datetime(year=2021, month=2, day=1, hour=13)
    end = datetime(year=2021, month=2, day=3, hour=13)
    return Event(title='test_multiday', content='test',
                 start=start, end=end, owner_id=1, color='blue')


def test_div_attributes(event1):
    div_attr = DivAttributes(event1)
    assert div_attr.total_time == '07:05 - 09:15'
    assert div_attr.grid_position == '34 / 42'
    assert div_attr.length == 130
    assert div_attr.color == 'grey'


def test_div_attr_multiday(multiday_event):
    day = datetime(year=2021, month=2, day=1)
    assert DivAttributes(multiday_event, day).grid_position == '57 / 101'
    day += timedelta(hours=24)
    assert DivAttributes(multiday_event, day).grid_position == '1 / 101'
    day += timedelta(hours=24)
    assert DivAttributes(multiday_event, day).grid_position == '1 / 57'


def test_div_attributes_with_costume_color(event2):
    div_attr = DivAttributes(event2)
    assert div_attr.color == 'blue'


def test_dayview_html(event1, event2, session, user, client):
    session.add_all([user, event1, event2])
    session.commit()
    response = client.get("/day/1-2-2021")
    soup = BeautifulSoup(response.content, 'html.parser')
    assert 'FEBRUARY' in str(soup.find("div", {"id": "toptab"}))
    assert 'event1' in str(soup.find("div", {"id": "event1"}))
    assert 'event2' in str(soup.find("div", {"id": "event2"}))


@pytest.mark.parametrize("day,grid_position", [("1-2-2021", '57 / 101'),
                                               ("2-2-2021", '1 / 101'),
                                               ("3-2-2021", '1 / 57')])
def test_dayview_html_with_multiday_event(multiday_event, session,
                                          user, client, day, grid_position):
    session.add_all([user, multiday_event])
    session.commit()
    response = client.get(f"/day/{day}")
    soup = BeautifulSoup(response.content, 'html.parser')
    grid_pos = f'grid-row: {grid_position};'
    assert grid_pos in str(soup.find("div", {"id": "event1"}))
