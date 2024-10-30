"""Configurations."""

from pathlib import Path
from re import match, IGNORECASE
from tomlkit.api import aot, inline_table, item, table
from tomlkit.items import Item, Table
from tomlkit.toml_document import TOMLDocument
from typing import NamedTuple

from typing import Any, Dict, List, Literal, Optional, Union


class Parser(NamedTuple):
    """Parser configuration."""

    module: str
    source: str

    root: Optional[str] = None

    autobuild: bool = True

    start: List[str] = ['start']
    lexer: Literal['basic', 'contextual'] = 'contextual'

    enable_compress: bool = False
    keep_all_tokens: bool = False
    propagate_positions: bool = False
    use_bytes: bool = False
    use_maybe_placeholders: bool = True
    use_regex: bool = False
    use_strict: bool = False

    @property
    def module_file(self) -> Path:
        """Module filename."""
        value = Path(*self.module.split('.')).with_suffix('.py')
        if self.module_dir:
            return self.module_dir.joinpath(value)

        return value

    @property
    def module_dir(self) -> Optional[Path]:
        """Module directory."""
        if self.root:
            return Path(self.root)

    @property
    def source_file(self) -> Path:
        """Source filename."""
        return Path(self.source)

    @property
    def data(self) -> Dict[str, Any]:
        """Dictionary of the parser data."""
        return self._options(**self._asdict())

    @classmethod
    def create(cls, module: str, source: str,
               root: Optional[str] = None,
               autobuild: Optional[bool] = None,
               start: Optional[List[str]] = None,
               lexer: Optional[Literal['basic', 'contextual']] = None,
               enable_compress: Optional[bool] = None,
               keep_all_tokens: Optional[bool] = None,
               propagate_positions: Optional[bool] = None,
               use_bytes: Optional[bool] = None,
               use_maybe_placeholders: Optional[bool] = None,
               use_regex: Optional[bool] = None,
               use_strict: Optional[bool] = None) -> 'Parser':
        """
        Create a new instance of the parser.

        Arguments:
            module: Module name.
            source: Grammar source.

        Raises:
            ValueError: If validation fails.
        """
        if not all((
            isinstance(module, str),
            isinstance(source, str),
            root is None or isinstance(root, str),
            start is None or isinstance(start, list),
            lexer is None or lexer in (
                'basic',
                'contextual',
            ),
        )):
            raise ValueError

        for flag in (
            autobuild,
            enable_compress,
            keep_all_tokens,
            propagate_positions,
            use_bytes,
            use_maybe_placeholders,
            use_regex,
            use_strict,
        ):
            if flag not in (True, False, None):
                raise ValueError

        for segment in module.split('.'):
            if not match(r'^[a-z][\w]*$', segment, IGNORECASE):
                raise ValueError

        if start is not None:
            for rule in start:
                if not isinstance(rule, str) or not match(r'^[a-z][_a-z0-9]*$', rule):
                    raise ValueError

        options = cls._options(
            root=root,
            autobuild=autobuild,
            start=start,
            lexer=lexer,
            enable_compress=enable_compress,
            keep_all_tokens=keep_all_tokens,
            propagate_positions=propagate_positions,
            use_bytes=use_bytes,
            use_maybe_placeholders=use_maybe_placeholders,
            use_regex=use_regex,
            use_strict=use_strict,
        )

        return cls(module, source, **options)

    @classmethod
    def _is_significant(cls, field: str, value: Any) -> bool:
        """
        Check if a field's value is significant.

        Arguments:
            field: Field name.
            value: Field value.
        """
        if field not in cls._fields or value is None:
            return False
        if field in cls._field_defaults:
            return value != cls._field_defaults.get(field)
        return True

    @classmethod
    def _options(cls, **data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construct optional parameters.

        Arguments:
            data: Dictionary of parameters.
        """
        return {
            field: value for field, value in data.items()
            if cls._is_significant(field, value)
        }


class ParserSerializer:
    """Serializer for parsers to a configuration."""

    @classmethod
    def serialize_module(cls, parser: Parser) -> Item:
        """
        Serialize the parser module.

        Arguments:
            parser: The parser instance.
        """
        if not parser.root and parser.autobuild:
            return item(parser.module)

        module = inline_table()

        module.update({
            key: parser.data.get(source)
            for source, key in (
                ('module', 'expose'),
                ('root', 'from'),
                ('autobuild', 'auto-build'),
            )
            if source in parser.data
        })

        return module

    @classmethod
    def serialize(cls, parser: Parser) -> Item:
        """
        Serialize the parser.

        Arguments:
            parser: The parser instance.
        """
        options = {
            source.replace('_', '-'): parser.data.get(source)
            for source in (
                'source',
                'start',
                'lexer',
                'enable_compress',
                'keep_all_tokens',
                'propagate_positions',
                'use_bytes',
                'use_maybe_placeholders',
                'use_regex',
                'use_strict',
            )
            if source in parser.data
        }

        return item({
            'module': cls.serialize_module(parser),
            **options,
        })


class ParserLoader:
    """Loader for parsers from a configuration."""

    @classmethod
    def load_module(cls, data: Optional[Union[str, Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Load the parser module.

        Arguments:
            data: Parser data from the configuration.
        """
        if isinstance(data, str):
            return {'module': data}

        if isinstance(data, dict):
            return {
                source: data.get(key)
                for source, key in (
                    ('module', 'expose'),
                    ('root', 'from'),
                    ('autobuild', 'auto-build'),
                )
                if key in data
            }

        return {}

    @classmethod
    def load(cls, data: Dict[str, Any]) -> Parser:
        """
        Load the parser.

        Arguments:
            data: Parser data from the configuration.

        Raises:
            ValueError: If validation fails.
        """
        options = {
            source: data.get(source.replace('_', '-'))
            for source in (
                'source',
                'start',
                'lexer',
                'enable_compress',
                'keep_all_tokens',
                'propagate_positions',
                'use_bytes',
                'use_maybe_placeholders',
                'use_regex',
                'use_strict',
            )
        }

        return Parser.create(
            **cls.load_module(data.get('module')),
            **options,
        )


class TOMLConfig:
    """Configuration."""

    def __init__(self, document: TOMLDocument) -> None:
        """
        Initialize a new instance.

        Arguments:
            document: Root document.
        """
        self.document = document

    def read(self) -> List[Parser]:
        """
        Read parsers from the configuration.

        Raises:
            ValueError: If validation fails.
        """
        section = self.get_section()
        if not section:
            return []

        items = section.get('standalone', [])
        if not isinstance(items, list):
            raise ValueError

        parsers = []

        for data in items:
            if not isinstance(data, dict):
                raise ValueError

            parser = ParserLoader.load(data)
            parsers.append(parser)

        return parsers

    def write(self, parsers: List[Parser]) -> None:
        """
        Write parsers to the configuration.

        Arguments:
            parsers: List of parsers.

        Raises:
            ValueError: If validation fails.
        """
        section = self.get_section(create=True)
        if 'standalone' in section:
            section.remove('standalone')

        items = aot()
        for parser in parsers:
            items.append(
                ParserSerializer.serialize(parser),
            )

        section.append('standalone', items)

    def get_section(self, *, create: bool = False) -> Optional[Table]:
        """
        Return the main section.

        Arguments:
            create: Create if it does not exist.

        Raises:
            ValueError: If validation fails.
        """
        container = self.document

        for key in ('tool', 'lark'):
            if key not in container:
                if not create:
                    return
                container[key] = table()

            container = container[key]
            if not isinstance(container, Table):
                raise ValueError

        return container
