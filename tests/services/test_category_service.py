from unittest.mock import AsyncMock

import pytest

from app.models.category_model import CategoryORM
from app.schemas.category_schema import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryNotFoundError, CategoryService


@pytest.mark.asyncio
async def test_list_categories_returns_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: AsyncMock,
) -> None:
    # Имитируем, что метод get_all репозитория вернет эти задачи
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="task-1", title="Изучить pytest"),
        CategoryORM(id="task-2", title="Написать первый тест"),
    ]

    result = await category_service.list_categories()

    assert result == [
        CategoryRead(id="task-1", title="Изучить pytest"),
        CategoryRead(id="task-2", title="Написать первый тест"),
    ]


@pytest.mark.asyncio
async def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: AsyncMock,
    category_repository_mock: AsyncMock,
) -> None:
    created_category = CategoryORM(id="task-1", title="Новая задача")
    category_repository_mock.create.return_value = created_category

    result = await category_service.create_category(
        CategoryCreate(title="Новая задача")
    )

    category_repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": "Новая задача",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("payload", "expected_title"),
    [
        pytest.param(
            CategoryUpdate(title="Обновить заголовок"),  # payload
            "Обновить заголовок",  # expected_title
        ),
    ],
)
async def test_update_category_updates_only_passed_fields(
    category_service: CategoryService,
    db_mock: AsyncMock,
    category_repository_mock: AsyncMock,
    payload: CategoryUpdate,
    expected_title: str,
) -> None:
    category = CategoryORM(id="task-1", title="Старая задача")
    category_repository_mock.get_by_id.return_value = category

    result = await category_service.update_category("task-1", payload)

    category_repository_mock.get_by_id.assert_called_once_with(category_id="task-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": expected_title,
    }


@pytest.mark.asyncio
async def test_update_category_raises_when_category_not_found(
    category_service: CategoryService,
    db_mock: AsyncMock,
    category_repository_mock: AsyncMock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):  # Должна произойти указанная ошибка
        await category_service.update_category(
            "missing-task", CategoryUpdate(title="Неважно")
        )

    db_mock.commit.assert_not_called()
