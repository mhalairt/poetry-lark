"""Base command."""

from logging import Logger, getLogger

from poetry.console.commands.command import Command

from poetry_lark.toml import Parser, TOMLConfig


class LarkStandaloneCommand(Command):
    """Base command."""

    loggers = [
        'poetry_lark',
        'lark',
        'interegular',
    ]

    @property
    def logger(self) -> Logger:
        """Logger instance."""
        return getLogger('poetry_lark')

    @property
    def config(self) -> TOMLConfig:
        """TOML configuration for the project."""
        return TOMLConfig(self.poetry.pyproject.data)

    @property
    def has_interegular(self) -> bool:
        """Check if the 'interegular' package is available."""
        try:
            import interegular  # noqa: F401
        except ImportError:
            return False
        else:
            return True

    @property
    def has_regex(self) -> bool:
        """Check if the 'regex' package is available."""
        try:
            import regex  # noqa: F401
        except ImportError:
            return False
        else:
            return True

    def check_build_requirements(self, parser: Parser, *,
                                 ignore_source: bool = False) -> None:
        """
        Check build requirements for a parser.

        Arguments:
            parser: The parser configuration instance.
            ignore_source: Whether to skip checking if the source file exists (default false).

        Raises:
            ValueError: If validation fails.
        """
        if not ignore_source and not parser.source_file.exists():
            raise ValueError
        if parser.use_regex and not self.has_regex:
            raise ValueError
        if parser.use_strict and not self.has_interegular:
            raise ValueError
