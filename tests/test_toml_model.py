"""Tests for the configuration's model."""

import pathlib
import pytest

from poetry_lark.toml import Parser


@pytest.mark.parametrize(('module', 'root', 'target'), (
    ('parser', None, pathlib.Path('parser.py')),
    ('tests.parser', None, pathlib.Path('tests/parser.py')),
    ('parser', 'src', pathlib.Path('src/parser.py')),
))
def test_success_parser_module(module, root, target):
    """Test success on a parser's module and root."""
    parser = Parser.create(module, 'grammar.lark', root=root)
    assert 'module' in parser.data
    assert root is None or 'root' in parser.data
    assert parser.module_file == target
    assert parser.source_file == pathlib.Path('grammar.lark')


@pytest.mark.parametrize('name', ('.', '$', 'test-parser', True, 42, 1, -1))
def test_fail_parser_module_name(name):
    """Test fail on a parser's module."""
    with pytest.raises(ValueError):
        Parser.create(name, 'grammar.lark')


@pytest.mark.parametrize('root', (True, 1, -1))
def test_fail_parser_module_root(root):
    """Test fail on a parser's root."""
    with pytest.raises(ValueError):
        Parser.create('parser', 'grammar.lark', root=root)


@pytest.mark.parametrize('start', (None, [], ['start'], ['r_start', 's']))
def test_success_parser_start(start):
    """Test success on a parser's start symbols."""
    parser = Parser.create('parser', 'grammar.lark', start=start)
    default = Parser._field_defaults['start']
    assert start is None or start == default or 'start' in parser.data


@pytest.mark.parametrize('start', ([1], ['valid', None], ['_hidden', 'TOKEN'], True, 42, 1, -1))
def test_fail_parser_start(start):
    """Test fail on a parser's start symbols."""
    with pytest.raises(ValueError):
        Parser.create('parser', 'grammar.lark', start=start)


@pytest.mark.parametrize('lexer', (None, 'basic', 'contextual'))
def test_success_parser_lexer(lexer):
    """Test success on a parser's lexer."""
    parser = Parser.create('parser', 'grammar.lark', lexer=lexer)
    default = Parser._field_defaults['lexer']
    assert lexer is None or lexer == default or 'lexer' in parser.data


@pytest.mark.parametrize('lexer', ('random_string', True, 42, 1, -1))
def test_fail_parser_lexer(lexer):
    """Test fail on a parser's lexer."""
    with pytest.raises(ValueError):
        Parser.create('parser', 'grammar.lark', lexer=lexer)


@pytest.mark.parametrize('value', (None, True, False, 0, 1))
@pytest.mark.parametrize('flag', (
    'autobuild',
    'enable_compress',
    'keep_all_tokens',
    'propagate_positions',
    'use_bytes',
    'use_maybe_placeholders',
    'use_regex',
    'use_strict',
))
def test_success_parser_flag(flag, value):
    """Test success on a parser's flag."""
    parser = Parser.create('parser', 'grammar.lark', **{flag: value})
    default = Parser._field_defaults[flag]
    assert value is None or value == default or flag in parser.data


@pytest.mark.parametrize('value', ('random_string', 42, -1))
@pytest.mark.parametrize('flag', (
    'autobuild',
    'enable_compress',
    'keep_all_tokens',
    'propagate_positions',
    'use_bytes',
    'use_maybe_placeholders',
    'use_regex',
    'use_strict',
))
def test_fail_parser_flag(flag, value):
    """Test fail on a parser's flag."""
    with pytest.raises(ValueError):
        Parser.create('parser', 'grammar.lark', **{flag: value})
