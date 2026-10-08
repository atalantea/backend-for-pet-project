from unittest.mock import AsyncMock

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository
from app.services.category_service import CategoryService
from app.services.task_service import TaskService


@pytest_asyncio.fixture
async def db_mock() -> AsyncMock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return AsyncMock(spec=AsyncSession)


@pytest_asyncio.fixture
async def task_repository_mock() -> AsyncMock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""
    return AsyncMock(spec=TaskRepository)


@pytest_asyncio.fixture
async def category_repository_mock() -> AsyncMock:
    """Создаём мок CategoryRepository один раз и переиспользуем в тестах"""
    return AsyncMock(spec=CategoryRepository)


@pytest_asyncio.fixture
async def task_service(
    db_mock: AsyncMock, 
    task_repository_mock: AsyncMock
    ) -> TaskService:
    """Создаём TaskService один раз, чтобы переиспользовать в тестах"""
    task_service = TaskService(db_mock)
    task_service.repository = task_repository_mock
    return task_service


@pytest_asyncio.fixture
async def category_service(
    db_mock: AsyncMock, 
    category_repository_mock: AsyncMock
    ) -> CategoryService:
    """Создаём CategoryService один раз, чтобы переиспользовать в тестах"""
    category_service = CategoryService(db_mock)
    category_service.repository = category_repository_mock
    return category_service
