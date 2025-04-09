"""Tests for removing of the configurations."""

import sys

import pytest

from cleo.testers.command_tester import CommandTester
from tests.heplers import configure_pyproject

from poetry_lark.commands.lark.remove import LarkStandaloneRemove


@pytest.fixture
def tester() -> CommandTester:
    """Command's tester."""
    return CommandTester(LarkStandaloneRemove())


def test_success_remove(tester, mocker):
    """Test success on a removing."""
    initial = (
        '[[tool.lark.standalone]]\n'
        'module = "parser"\n'
        'source = "grammar.lark"'
    )

    mocker.patch('os.unlink', return_value=None)

    with configure_pyproject(mocker, initial) as config:
        tester.execute('parser')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [],
                },
            },
        }


def test_success_remove_with_src_layout(tester, mocker):
    """Test success on a removing with src-layout."""
    initial = (
        '[[tool.lark.standalone]]\n'
        'module = {expose = "parser", from = "src", auto-build = false}\n'
        'source = "grammar.lark"'
    )

    mocker.patch('os.unlink', return_value=None)

    with configure_pyproject(mocker, initial) as config:
        tester.execute('parser')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [],
                },
            },
        }


def test_success_remove_empty(tester, mocker):
    """Test success on a removing with empty."""
    mocker.patch('os.unlink', return_value=None)

    with configure_pyproject(mocker) as config:
        tester.execute('parser')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [],
                },
            },
        }


def test_success_remove_unknown(tester, mocker):
    """Test success on a removing with unknown."""
    initial = (
        '[[tool.lark.standalone]]\n'
        'module = "parser_1"\n'
        'source = "grammar.lark"\n\n'
        '[[tool.lark.standalone]]\n'
        'module = "parser_2"\n'
        'source = "grammar.lark"'
    )

    mocker.patch('os.unlink', return_value=None)

    with configure_pyproject(mocker, initial) as config:
        tester.execute('parser_3')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [{
                        'module': 'parser_1',
                        'source': 'grammar.lark',
                        }, {
                        'module': 'parser_2',
                        'source': 'grammar.lark',
                    }],
                },
            },
        }


def test_success_remove_with_file(tester, mocker):
    """Test success on a removing with existed module-file."""
    initial = (
        '[[tool.lark.standalone]]\n'
        'module = "parser"\n'
        'source = "grammar.lark"'
    )

    mocker.patch('os.unlink', return_value=None)
    if sys.version_info < (3, 11):
        mocker.patch('pathlib._normal_accessor.unlink', return_value=None)

    with configure_pyproject(mocker, initial) as config:
        tester.execute('parser')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [],
                },
            },
        }


def test_success_remove_with_file_not_found(tester, mocker):
    """Test success on a removing with unexisted module-file."""
    initial = (
        '[[tool.lark.standalone]]\n'
        'module = "parser"\n'
        'source = "grammar.lark"'
    )

    mocker.patch('os.unlink', side_effect=FileNotFoundError)
    if sys.version_info < (3, 11):
        mocker.patch('pathlib._normal_accessor.unlink', side_effect=FileNotFoundError)

    with configure_pyproject(mocker, initial) as config:
        tester.execute('parser')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [],
                },
            },
        }
