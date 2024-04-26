from pathlib import Path
from typing import ClassVar

from cleo.helpers import argument, option
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option

from fasttemplate.console.commands._base import Command
from fasttemplate.layouts._base import Asset, AssetDoesNotExistError, LayoutBase, Project
from fasttemplate.layouts.manager import LayoutManager


class NewCommand(Command):
    name = "new"
    description = "Creates a new project at <path>."

    arguments: ClassVar[list[Argument]] = [
        argument(
            "name",
            description="Project name.",
        )
    ]
    options: ClassVar[list[Option]] = [
        option(
            "src",
            description="Use the src layout for the project.",
        ),
        option(
            "asset-type",
            description="Asset type.",
            flag=False,
            default="fastapi",
        ),
        option(
            "asset-name",
            description="Asset name.",
            flag=False,
            default="default",
        ),
    ]

    @property
    def layout(self) -> LayoutBase:
        asset_type = self.option("asset-type")
        asset_name = self.option("asset-name")
        path: Path = self._get_path()
        src: bool = self.option("src")
        asset: Asset = Asset(
            type=asset_type,
            name=asset_name,
        )

        project: Project = Project(
            name=path.name,
        )

        manager: LayoutManager = LayoutManager(project, src, asset)
        try:
            return manager.get_layout()
        except AssetDoesNotExistError:
            self.line(
                f"""\
<error>Asset does not exist!</error>

<info>Asset:
    type: {asset_type}
    name: {asset_name}</info>\
"""
            )
            raise RuntimeError("Asset does not exist.") from None

    def _print_success(self, layout: LayoutBase, /) -> None:
        name: str = self.argument("name")
        src: bool = self.option("src")

        asset: Asset = layout.asset

        self.line(
            f"""\
Congratulations! Project <info>{name}</info> created.

<info>Project configuration:
    src = {src}
    project path = {layout.project_dir}
    asset type = {asset.type}
    asset name = {asset.name}
</info>
Now you can go to the project: <info>cd {layout.project_dir}</info> and start!

<comment>Happy coding!</comment>\
"""
        )

    def handle(self) -> int:
        layout: LayoutBase = self.layout
        layout.create()

        self._print_success(layout)

        return 0

    def _get_path(self) -> Path:
        path: Path = Path(self.argument("name"))
        if not path.is_absolute():
            path = Path.cwd().joinpath(path)
        if path.exists():
            raise RuntimeError(f'Path "{path}" exists.') from None
        return path
