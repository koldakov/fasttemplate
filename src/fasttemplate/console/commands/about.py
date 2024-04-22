from fasttemplate.__version__ import __version__
from fasttemplate.console.commands._base import Command


class AboutCommand(Command):
    name = "about"
    description = "Shows information about fasttemplate."

    def handle(self) -> int:
        self.line(
            f"""<info>fasttemplate - project structure builder.

Shall you require to build a project in seconds use fasttemplate!
It has predefined cool features like poetry, mypy configs, ruff configs, pre-commit, etc.

Version: {__version__}</info>

<comment>See <fg=blue>https://github.com/koldakov/fasttemplate</> for more information.</comment>\
"""
        )
        return 0
