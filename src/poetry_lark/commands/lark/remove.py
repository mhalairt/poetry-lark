"""Command for removing a standalone parser."""

from cleo.helpers import argument

from poetry_lark.commands.command import LarkStandaloneCommand


class LarkStandaloneRemove(LarkStandaloneCommand):
    """Command for removing a standalone parser."""

    name = 'lark-remove'
    description = 'Remove the standalone parser configuration from <comment>pyproject.toml</>.'

    arguments = [
        argument('module', description='The module to be removed.'),
    ]

    def handle(self) -> int:
        """
        Remove the parser configuration from the project.

        Raises:
            ValueError: If validation fails.
        """
        parsers = []
        for parser in self.config.read():
            if parser.module != self.argument('module'):
                parsers.append(parser)
            else:
                parser.module_file.unlink(missing_ok=True)

        self.config.write(parsers)
        self.poetry.pyproject.save()

        return 0
