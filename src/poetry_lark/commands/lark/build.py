"""Command for building standalone parsers."""

from lark import Lark
from lark.tools.standalone import gen_standalone

from poetry_lark.commands.command import LarkStandaloneCommand


class LarkStandaloneBuild(LarkStandaloneCommand):
    """Command for building standalone parsers."""

    name = 'lark-build'
    description = 'Build parsers specified in <comment>pyproject.toml</>.'

    def __init__(self, ignore_manual: bool = False) -> None:
        """
        Initialize a new instance.

        Arguments:
            ignore_manual: Whether to skip building if not enabled for automatic build (default false).
        """
        super().__init__()

        self.ignore_manual = ignore_manual

    def handle(self) -> int:
        """
        Build parsers specified in the configuration.

        Raises:
            ValueError: If validation fails.
        """
        for parser in self.config.read():
            self.check_build_requirements(parser)
            if not parser.autobuild and self.ignore_manual:
                continue

            lalr = Lark(
                parser.source_file.read_text(),
                parser='lalr',
                start=parser.start,
                lexer=parser.lexer,
                keep_all_tokens=parser.keep_all_tokens,
                propagate_positions=parser.propagate_positions,
                use_bytes=parser.use_bytes,
                maybe_placeholders=parser.use_maybe_placeholders,
                regex=parser.use_regex,
                strict=parser.use_strict,
            )

            parser.module_file.unlink(missing_ok=True)
            gen_standalone(
                lalr,
                out=parser.module_file.open('wt'),
                compress=parser.enable_compress,
            )

        return 0
