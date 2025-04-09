"""Command for adding a standalone parser."""

from cleo.helpers import argument, option

from poetry_lark.commands.command import LarkStandaloneCommand
from poetry_lark.toml import Parser


class LarkStandaloneAdd(LarkStandaloneCommand):
    """Command for adding a standalone parser."""

    name = 'lark-add'
    description = 'Add the standalone parser configuration to <comment>pyproject.toml</>.'

    arguments = [
        argument('module', description='The module to be geenerated.'),
        argument('source', description='The grammar source file.'),
    ]

    options = [
        option('src', description="Use the 'src' layout for the project."),
        option('no-auto-build', description='Disable automatic build for the project.'),
        option('start', 's', flag=False, multiple=True, default=['start'],
               description="The grammar's start symbol(s)."),
        option('lexer', 'l', flag=False, default='contextual',
               description='The lexer to use (`basic` or `contextual`).'),
        option('enable-compress', 'c',
               description='Enable compression in the generated parser.'),
        option('keep-all-tokens', 'K',
               description="Prevent removal of 'punctuation' tokens in the parse tree."),
        option('propagate-positions', 'P',
               description='Propagate positional attributes into metadata.'),
        option('use-bytes', description='Use `bytes` as input type instead of `str`.'),
        option('no-maybe-placeholders',
               description='Disable `None` as a placeholder for empty optional tokens.'),
        option('use-regex', description='Use the `regex` module instead of the `re` module.'),
        option('use-strict', description='Enable strict mode in parsing.'),
    ]

    def handle(self) -> int:
        """
        Add the parser configuration to the project.

        Raises:
            ValueError: If validation fails.
        """
        parsers = [
            parser for parser in self.config.read()
            if parser.module != self.argument('module')
        ]

        root = None
        if self.option('src', False):
            root = 'src'

        parser = Parser.create(
            module=self.argument('module'),
            root=root,
            autobuild=not self.option('no-auto-build'),
            source=self.argument('source'),
            start=self.option('start'),
            lexer=self.option('lexer'),
            enable_compress=self.option('enable-compress'),
            keep_all_tokens=self.option('keep-all-tokens'),
            propagate_positions=self.option('propagate-positions'),
            use_bytes=self.option('use-bytes'),
            use_maybe_placeholders=not self.option('no-maybe-placeholders'),
            use_regex=self.option('use-regex'),
            use_strict=self.option('use-strict'),
        )

        self.check_build_requirements(parser, ignore_source=True)
        parsers.append(parser)

        self.config.write(parsers)
        self.poetry.pyproject.save()

        return 0
