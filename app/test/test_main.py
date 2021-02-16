import nest_asyncio
nest_asyncio.apply()
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.utils import Constants
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_200_OK
import json
import pytest
from fastapi_cache.backends.redis import RedisCacheBackend, CACHE_KEY
app = FastAPI()
from app.main import app,connect
client = TestClient(app)
from config.app_config import TEST_HOST, TEST_PORT, TEST_INDEX
from fastapi_cache import  close_caches
from app.helper import redis_cache
from fastapi_cache import caches, close_caches


@pytest.fixture
async def f_backend() -> RedisCacheBackend:
    return await connect(TEST_HOST, TEST_PORT, TEST_INDEX)


def test_create_item_bad_token():
    response = client.post(
        "/api/person",
        headers={"X-Token": "coneofsilence"},
        json={"first_name": "Nithish", "last_name": "Mohan", "age": "28", "favourite_color": "red"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_person(f_backend: RedisCacheBackend ) -> None:
    access_token = await authorization()
    response = await create_person(access_token)
    assert response.status_code == HTTP_200_OK
    caches.remove(CACHE_KEY)


@pytest.mark.asyncio
async def test_fetch_person(f_backend: RedisCacheBackend):
    access_token = await authorization()
    create_response = await create_person(access_token)
    _create_response = json.loads(create_response.content)
    _fetch_response = await fetch_person(_create_response['first_name'],
                                         _create_response['last_name'], access_token)
    assert _fetch_response.status_code == HTTP_200_OK
    assert json.dumps(_create_response, sort_keys=True) == \
           json.dumps(json.loads(_fetch_response.content), sort_keys=True)
    caches.remove(CACHE_KEY)


@pytest.mark.asyncio
async def test_update_person(f_backend: RedisCacheBackend):
    access_token = await authorization()
    create_response = await create_person(access_token)
    _create_response = json.loads(create_response.content)
    update_json = {"first_name": _create_response['first_name'],
                "last_name": _create_response['last_name'],
                "age": "29", "favourite_color": "blue"}
    response = client.put(
        "/api/person",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json=update_json
    )
    fetch_response = await fetch_person(_create_response['first_name'],
                                         _create_response['last_name'], access_token)
    _fetch_response = json.loads(fetch_response.content)
    assert response.status_code == HTTP_201_CREATED
    assert json.dumps(
        _fetch_response, sort_keys=True) == json.dumps(update_json, sort_keys=True)
    caches.remove(CACHE_KEY)


@pytest.mark.asyncio
async def test_delete_person(f_backend: RedisCacheBackend) -> None:
    access_token = await authorization()
    response = client.delete(
        "/api/person",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={"first_name": "nithish", "last_name": "mohan"}
    )
    assert response.status_code == HTTP_200_OK
    caches.remove(CACHE_KEY)


async def authorization():
    result = client.post(
        "/api/login",
        json={"username": Constants.username.value, "password": Constants.password.value}
    )
    return json.loads(result.content)['access_token']


async def create_person(access_token) :
    result = client.post(
        "/api/person",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={"first_name": "Nithish", "last_name": "Mohan", "age": "28", "favourite_color": "red"},
    )
    return result


async def fetch_person(first_name, last_name, access_token):
    response = client.get(
        "/api/person",
        headers={"Authorization": "Bearer {}".format(access_token)},
        params={"first_name": first_name,
               "last_name": last_name},
    )
    return response
