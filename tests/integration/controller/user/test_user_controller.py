import json
from uuid import uuid4

import pytest
from requests import Response
from starlette import status

from src.api.controller.user.dto.get_user_output_dto import GetUserOutputDto
from src.core.model.base_models.user_type import UserTypeEnum
from src.infra.adapter.repository.postgres.entity.user_entity import UserEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager
from tests.integration.controller.user.test_constants import USER_CONTROLLER_BASE_PATH
from tests.integration.controller.user.test_input import (
    generate_invalid_create_user_inputs,
)
from tests.integration.test_input_common import (
    delete_all_tables,
    populate_create_user_dto,
)


@pytest.fixture(autouse=True)
def clear_all_tables_before_after_each_method():
    delete_all_tables()
    yield
    delete_all_tables()


class TestUserController:
    def test_should_create_user(self, test_client):
        # given
        create_user_input_dto = populate_create_user_dto()
        # when
        create_user_response: Response = test_client.post(
            USER_CONTROLLER_BASE_PATH,
            data=create_user_input_dto.json(),
        )

        # then
        assert create_user_response.status_code == status.HTTP_201_CREATED
        assert create_user_response.json()["id"] is not None
        user_id = create_user_response.json()["id"]

        with RepositoryManager() as repository_manager:
            user_entity = (
                repository_manager.query(UserEntity)
                .filter(UserEntity.id == user_id)
                .filter(UserEntity.deleted.is_(False))
                .first()
            )
            assert user_entity is not None
            assert str(user_entity.id) == user_id
            assert user_entity.name == create_user_input_dto.name
            assert user_entity.surname == create_user_input_dto.surname
            assert user_entity.email == create_user_input_dto.email
            assert user_entity.type == UserTypeEnum.NORMAL.value

    @pytest.mark.parametrize("create_user_input", generate_invalid_create_user_inputs())
    def test_should_raise_bad_request_error_when_create_user_if_input_dto_is_invalid(
        self, test_client, create_user_input
    ):
        # given
        # when
        create_user_response: Response = test_client.post(
            USER_CONTROLLER_BASE_PATH,
            data=json.dumps(create_user_input),
        )

        # then
        assert create_user_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_get_user(self, test_client):
        # given
        create_user_input_dto = populate_create_user_dto()
        create_user_response: Response = test_client.post(
            USER_CONTROLLER_BASE_PATH,
            data=create_user_input_dto.json(),
        )
        assert create_user_response.status_code == status.HTTP_201_CREATED
        assert create_user_response.json()["id"] is not None
        user_id = create_user_response.json()["id"]

        # when
        get_user_response: Response = test_client.get(
            USER_CONTROLLER_BASE_PATH + f"/{user_id}",
        )

        # then
        assert get_user_response.status_code == status.HTTP_200_OK
        get_user_response_data = get_user_response.json()
        assert GetUserOutputDto(**get_user_response_data) == GetUserOutputDto(
            **create_user_input_dto.dict(), stocks=[], orders=[], id=user_id
        )

    def test_should_raise_not_found_error_when_get_user_if_user_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_user_response: Response = test_client.get(
            USER_CONTROLLER_BASE_PATH + f"/{uuid4()}",
        )

        # then
        assert get_user_response.status_code == status.HTTP_404_NOT_FOUND
