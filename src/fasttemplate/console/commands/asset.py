from typing import TYPE_CHECKING, ClassVar

from cleo.helpers import option
from cleo.io.inputs.option import Option

from fasttemplate import PROJECT_ROOT_DIR
from fasttemplate.console.commands._base import Command
from fasttemplate.layouts._base import ASSETS, Asset

if TYPE_CHECKING:
    from pathlib import Path


class AssetCommand(Command):
    name = "asset"
    description = "Shows information about assets."

    options: ClassVar[list[Option]] = [
        option(
            "list",
            description="List all available assets.",
        ),
        option(
            "short",
            description="Show short information.",
        ),
        option(
            "asset-type",
            description="Asset type.",
            flag=False,
        ),
        option(
            "asset-name",
            description="Asset name.",
            flag=False,
        ),
    ]

    def _stdout_asset(self, asset: Asset, idx: int, /):
        if self.option("short"):
            self.line(f"<info>type: {asset.type}, name: {asset.name}.</info>")
            return

        description_file: Path = PROJECT_ROOT_DIR / "assets" / asset.type / asset.name / "DESCRIPTION.md"
        info: str
        try:
            with open(description_file) as f:
                info = f.read()
        except FileNotFoundError:
            info = "Description not available.\n"

        self.line(
            f"""\
<comment>[{idx}]</comment>
<info>Asset:
    type: {asset.type}
    name: {asset.name}

{info}</info><comment>[/{idx}]</comment>\
"""
        )

    def handle_list(self):
        idx: int
        asset: Asset
        for idx, asset in enumerate(ASSETS):
            self._stdout_asset(asset, idx)

    def handle_asset(self):
        asset: Asset
        asset_list: list[Asset] = []
        asset_name: str = self.option("asset-name")
        asset_type: str = self.option("asset-type")
        if asset_type and asset_name:
            asset_list = [asset for asset in ASSETS if asset.type == asset_type and asset.name == asset_name]
        if asset_type:
            asset_list = [asset for asset in ASSETS if asset.type == asset_type]
        if asset_name:
            asset_list = [asset for asset in ASSETS if asset.name == asset_name]

        if not asset_list:
            msg: str = f"type={asset_type} and name={asset_name}"
            if not asset_type:
                msg = f"name={asset_name}"
            if not asset_name:
                msg = f"type={asset_type}"
            raise RuntimeError(f"Assets with {msg} not found.")

        idx: int
        for idx, asset in enumerate(asset_list):
            self._stdout_asset(asset, idx)

    def handle(self) -> int:
        self._validate_options()

        if self.option("list"):
            self.handle_list()
        if self.option("asset-type") or self.option("asset-name"):
            self.handle_asset()

        return 0

    def _validate_short(self):
        return self.option("short") and (
            not self.option("list") and not self.option("asset-type") and not self.option("asset-name")
        )

    def _validate_options(self):
        if self._validate_short():
            raise RuntimeError("--short option can be used only with --list option.")
        if self.option("list") and (self.option("asset-type") or self.option("asset-name")):
            raise RuntimeError("--list option can't be used with --asset-type or --asset-name options.")

        if not self.option("list") and not self.option("asset-type") and not self.option("asset-name"):
            raise RuntimeError(
                """\
Kindly use --list option to list all assets or --asset-type/--asset-name to list specific ones.

For more info use --help option.\
"""
            )
