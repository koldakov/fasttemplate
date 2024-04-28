import pytest
from fasttemplate.layouts._base import Asset, Project
from fasttemplate.layouts.manager import LayoutManager


@pytest.fixture
def fastapi_default_project() -> Project:
    return Project(
        name="fastapi-default-project-name",
    )


@pytest.fixture
def fastapi_default_asset() -> Asset:
    return Asset(
        type="fastapi",
        name="default",
    )


@pytest.fixture
def fastapi_default_layout_manager(fastapi_default_project, fastapi_default_asset) -> LayoutManager:
    return LayoutManager(fastapi_default_project, False, fastapi_default_asset)


@pytest.mark.usefixtures("fastapi_default_layout_manager")
class TestGetLayoutCase:
    def test_get_layout_should_return_fastapi_layout_when_fastapi_layout_provided(
        self,
        fastapi_default_layout_manager,
    ) -> None:
        from fasttemplate.layouts.fastapi.layout import Layout

        assert isinstance(fastapi_default_layout_manager.get_layout(), Layout)
