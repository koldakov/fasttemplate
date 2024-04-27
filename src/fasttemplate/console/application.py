from collections.abc import Callable
from importlib import import_module
from typing import TYPE_CHECKING

from cleo.application import Application as ApplicationBase
from cleo.loaders.factory_command_loader import FactoryCommandLoader

from fasttemplate.__version__ import __version__
from fasttemplate.console.commands._base import Command

if TYPE_CHECKING:
    from types import ModuleType

COMMANDS: list[str] = [
    "about",
    "new",
    "asset",
]


def _load_command(name: str) -> Callable[[], Command]:
    def command() -> Command:
        try:
            module: ModuleType = import_module(f"fasttemplate.console.commands.{name}")
        except ModuleNotFoundError as err:
            raise RuntimeError(f'Module "{name}" not found') from err
        try:
            class_: type[Command] = getattr(module, f"{name.title()}Command")
        except AttributeError as err:
            raise RuntimeError(f'Module "{name}" does not have "{name.title()}Command" class') from err
        return class_()

    return command


class Application(ApplicationBase):
    def __init__(self):
        super().__init__("fasttemplate", __version__)

        command_loader: FactoryCommandLoader = FactoryCommandLoader(
            {command: _load_command(command) for command in COMMANDS}
        )
        self.set_command_loader(command_loader)


def main() -> int:
    exit_code: int = Application().run()
    return exit_code


if __name__ == "__main__":
    main()
