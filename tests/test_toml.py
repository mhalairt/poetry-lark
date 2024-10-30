"""Tests for the configurations."""

import pytest

from poetry_lark.toml import Parser, TOMLConfig
from tomlkit.api import loads, dumps


def test_success_read_empty():
    """Test success on a reading empty."""
    document = loads('')

    parsers = TOMLConfig(document).read()

    assert isinstance(parsers, list)
    assert len(parsers) == 0


def test_success_read():
    """Test success on a reading."""
    document = loads(
        '[[tool.lark.standalone]]\n'
        'module = {expose = "parser", from = "src", auto-build = false}\n'
        'source = "grammar.lark"\n'
        'start = ["start"]\n'
        'lexer = "contextual"\n'
        'enable_compress = false\n'
        'keep_all_tokens = false\n'
        'propagate_positions = false\n'
        'use_bytes = false\n'
        'use_maybe_placeholders = true\n'
        'use_regex = false\n'
        'use_strict = false'
    )

    parsers = TOMLConfig(document).read()

    assert isinstance(parsers, list)
    assert len(parsers) == 1

    parser = parsers[0]

    assert parser.data == {
        'module': 'parser',
        'root': 'src',
        'autobuild': False,
        'source': 'grammar.lark',
    }


def test_success_write_empty():
    """Test success on a writing empty."""
    document = loads('')

    TOMLConfig(document).write([])

    content = dumps(document)

    assert content == ''


def test_success_write():
    """Test success on a writing."""
    document = loads('')

    parsers = [
        Parser.create('parser', 'grammar.lark'),
    ]

    TOMLConfig(document).write(parsers)

    content = dumps(document).strip()

    assert content == (
        '[[tool.lark.standalone]]\n'
        'module = "parser"\n'
        'source = "grammar.lark"'
    )


def test_success_append():
    """Test success on a appending."""
    document = loads(
        '[[tool.lark.standalone]]\n'
        'module = "parser_1"\n'
        'source = "grammar.lark"\n'
    )

    parsers = TOMLConfig(document).read()
    parsers.append(Parser.create(
        module='parser_2',
        root='src',
        source='grammar.lark',
    ))

    TOMLConfig(document).write(parsers)

    content = dumps(document).strip()

    assert content == (
        '[[tool.lark.standalone]]\n'
        'module = "parser_1"\n'
        'source = "grammar.lark"\n\n'
        '[[tool.lark.standalone]]\n'
        'module = {expose = "parser_2", from = "src"}\n'
        'source = "grammar.lark"'
    )


@pytest.mark.parametrize('data', (
    ('[tool]\n'
     'lark = "some value"'),
    ('[tool.lark]\n'
     'standalone = true'),
    ('[tool.lark.standalone]\n'
     'module = "parser"\n'
     'source = "grammar.lark"'),
    ('[tool.lark]\n'
     'standalone = ["some value"]'),
))
def test_fail_read(data):
    """Test fail on a reading."""
    document = loads(data)

    with pytest.raises(ValueError):
        TOMLConfig(document).read()
