from abc import ABC
from os import getlogin
from pathlib import Path
from typing import NamedTuple

from mako.template import Template

from fasttemplate import PROJECT_ROOT_DIR

_ASSETS_DIR: Path = PROJECT_ROOT_DIR / "assets"


class Asset(NamedTuple):
    type: str  # noqa: A003
    name: str


def _populate_assets() -> list[Asset]:
    assets: list[Asset] = []
    asset_type_path: Path
    for asset_type_path in _ASSETS_DIR.iterdir():
        asset_name_path: Path
        for asset_name_path in asset_type_path.iterdir():
            assets.append(Asset(type=asset_type_path.name, name=asset_name_path.name))
    return assets


ASSETS: list[Asset] = _populate_assets()


class Author(NamedTuple):
    name: str | None = None
    email: str | None = None


class Project(NamedTuple):
    name: str
    description: str = ""
    version: str = "0.0.1"


def _render(
    template_path: Path,
    render_file: Path,
    args: dict,
    /,
) -> None:
    if not str(render_file).endswith(".mako"):
        raise ValueError("Render file should end with .mako")

    template: Template = Template(filename=str(template_path))

    render_file.parent.mkdir(parents=True, exist_ok=True)
    relative_file: str = str(render_file).split(".mako")[0]
    with open(relative_file, "w") as file_:
        file_.write(template.render(**args))


class LayoutBaseError(Exception):
    ...


class AssetDoesNotExistError(LayoutBaseError):
    ...


class LayoutBase(ABC):
    assets_dir: Path = _ASSETS_DIR
    assets: list[Asset] = ASSETS
    asset_project_path: Path = Path("src")

    def __init__(
        self,
        project: Project,
        asset: Asset,
        /,
        *,
        author: Author | None = None,
        src: bool = False,
    ) -> None:
        self.project: Project = project
        self.author: Author | None = self._get_author(author)
        self.asset: Asset = asset
        self.src: bool = src

        self._validate_asset()

    def _get_author(self, author: Author | None, /) -> Author | None:
        """
        TODO: Read username/login from GIT
        """
        if author:
            return author

        return Author(
            name=getlogin(),
        )

    def _validate_asset(self) -> None:
        if self.asset not in self.assets:
            raise AssetDoesNotExistError(f"Asset {self.asset} does not exist.")

    def _get_project_fields(self) -> dict:
        mypy_files: list[str] = [
            "src" if self.src else self.fixed_project_name,
            "tests",
        ]
        return {
            "project": self.project._asdict()
            | {
                "mypy_files": mypy_files,
                "src_rel_path": self.src_rel_path,
                "fixed_project_name": self.fixed_project_name,
            }
        }

    @property
    def fields(self):
        return {
            **self._get_project_fields(),
            **{"author": self.author._asdict() if self.author else None},
            **{"asset": self.asset._asdict()},
        }

    @property
    def basedir(self) -> Path:
        return Path()

    @property
    def project_dir(self) -> Path:
        return Path(self.basedir / "-".join(self.project.name.split()))

    @property
    def fixed_project_name(self):
        return "_".join(self.project.name.replace("-", "_").split())

    @property
    def src_dir(self) -> Path:
        if self.src:
            return Path(self.project_dir / Path("src") / self.fixed_project_name)
        return Path(self.project_dir / self.fixed_project_name)

    @property
    def asset_path(self) -> Path:
        return self.assets_dir / self.asset.type / self.asset.name

    @property
    def _src_asset_dir(self) -> Path:
        return Path("src")

    @property
    def src_rel_path(self) -> Path:
        if self.src:
            return Path("src") / self.fixed_project_name
        return Path(self.fixed_project_name)

    def _create_file(self, dir_: Path, file: Path, /) -> None:
        source_dir: Path
        relative_source_path: Path = (dir_ / file).relative_to(self.asset_path)
        relative_file_path: Path = self.project_dir / relative_source_path
        try:
            source_dir = self.src_dir / relative_file_path.relative_to(self.project_dir / self._src_asset_dir)
        except ValueError:
            source_dir = relative_file_path
        _render(dir_ / file, source_dir, self.fields)

    def create(self) -> None:
        current: Path
        files: list[str]
        self.project_dir.mkdir()
        for current, _, files in self.asset_path.walk():
            for file in files:
                if file.endswith(".mako"):
                    self._create_file(current, Path(file))
