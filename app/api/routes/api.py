import json
from fastapi import APIRouter, Depends, Response, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_200_OK
from app.models.index import Person, Admin, Name
from fastapi_cache.backends.redis import RedisCacheBackend
from app.helper import redis_cache
from fastapi_jwt_auth import AuthJWT
from app.utils import Constants


router = APIRouter()


@router.post(
    "/person",
    name="persons:create-user",
    response_model_exclude_unset=True
)
async def person(person: Person, response: Response, cache: RedisCacheBackend = Depends(redis_cache),
                 Authorize: AuthJWT = Depends()) -> Response:
    """

    :param cache:
    :param response:
    :param person:
    :type Authorize: object
    """
    Authorize.jwt_required()
    try:
        await cache.set("{0}_{1}".format(person.first_name.lower(),
                                         person.last_name.lower()), json.dumps(person.__dict__))
        return Response(status_code=HTTP_201_CREATED, content=json.dumps(person.__dict__))
    except Exception as e:
        print(e)
        return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content="Person creation failed")


@router.delete(
    "/person",
    name="persons:delete-user",
    response_model_exclude_unset=True
)
async def person(user: Name, response: Response, cache: RedisCacheBackend = Depends(redis_cache),
                 Authorize: AuthJWT = Depends()) -> Response:
    """

    :param cache:
    :param response:
    :param user:
    :type Authorize: object
    """
    Authorize.jwt_required()
    try:
        await cache.delete("{0}_{1}".format(user.first_name.lower(),
                                            user.last_name.lower()))
        response.status_code = HTTP_200_OK
        return response
    except Exception as e:
        return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content='0')


@router.get(
    "/person",
    name="persons:fetch-user",
    response_model_exclude_unset=True
)
async def person(user: Name, response: Response, cache: RedisCacheBackend = Depends(redis_cache),
                 Authorize: AuthJWT = Depends()) -> Response:
    """

    :param user:
    :param cache:
    :param response:
    :type Authorize: object
    """
    Authorize.jwt_required()
    try:
        _persons = await cache.get("{0}_{1}".format(user.first_name.lower(),
                                                    user.last_name.lower()))
        response.status_code = HTTP_200_OK
        return Response(content=_persons)
    except Exception as e:
        return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content='0')


@router.put(
    "/person",
    name="persons:update-user",
    response_model_exclude_unset=True
)
async def person(person: Person, response: Response, cache: RedisCacheBackend = Depends(redis_cache),
                 Authorize: AuthJWT = Depends()) -> Person:
    """

    :param cache:
    :param response:
    :param person:
    :type Authorize: object
    """
    Authorize.jwt_required()
    try:
        await cache.set("{0}_{1}".format(person.first_name.lower(),
                                         person.last_name.lower()), json.dumps(person.__dict__))
        response.status_code = HTTP_200_OK
        return response
    except Exception as e:
        return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content='0')


@router.post('/login')
def login(admin: Admin, Authorize: AuthJWT = Depends()):
    """

    :param Authorize:
    :type admin: object
    """
    if admin.username != Constants.username.value or admin.password != Constants.password.value:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=admin.username)
    return Response(content=json.dumps({"access_token": access_token}), status_code=HTTP_200_OK)
