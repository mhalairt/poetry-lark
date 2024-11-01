"""Tests for adding of the configurations."""

import pytest

from cleo.testers.command_tester import CommandTester
from poetry_lark.commands.lark.add import LarkStandaloneAdd

from tests.heplers import configure_pyproject


@pytest.fixture
def tester() -> CommandTester:
    """Command's tester."""
    return CommandTester(LarkStandaloneAdd())


def test_success_add_with_required_arguments(tester, mocker):
    """Test success on a adding with required arguments."""
    with configure_pyproject(mocker) as config:
        tester.execute('parser parser.lark')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [{
                        'module': 'parser',
                        'source': 'parser.lark',
                    }],
                },
            },
        }


def test_success_add_with_src_layout(tester, mocker):
    """Test success on a adding with src-layout."""
    with configure_pyproject(mocker) as config:
        tester.execute('--src parser parser.lark')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [{
                        'module': {
                            'expose': 'parser',
                            'from': 'src',
                        },
                        'source': 'parser.lark',
                    }],
                },
            },
        }


@pytest.mark.parametrize('option', (
    ('--start start'),
    ('--lexer contextual'),
))
def test_success_add_with_default_options(option, tester, mocker):
    """Test success on a adding with default options."""
    with configure_pyproject(mocker) as config:
        tester.execute(f'{option} parser parser.lark')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [{
                        'module': 'parser',
                        'source': 'parser.lark',
                    }],
                },
            },
        }


@pytest.mark.parametrize(('option', 'target'), (
    ('--no-auto-build', {'module': {'expose': 'parser', 'auto-build': False}}),
    ('--start root', {'start': ['root']}),
    ('--lexer basic', {'lexer': 'basic'}),
    ('--enable-compress', {'enable-compress': True}),
    ('--keep-all-tokens', {'keep-all-tokens': True}),
    ('--propagate-positions', {'propagate-positions': True}),
    ('--use-bytes', {'use-bytes': True}),
    ('--no-maybe-placeholders', {'use-maybe-placeholders': False}),
))
def test_success_add_with_options(option, target, tester, mocker):
    """Test success on a adding with default options."""
    with configure_pyproject(mocker) as config:
        tester.execute(f'{option} parser parser.lark')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [{
                        'module': 'parser',
                        'source': 'parser.lark',
                        **target,
                    }],
                },
            },
        }


@pytest.mark.parametrize(('option', 'requirement', 'target'), (
    ('--use-regex', 'regex', {'use-regex': True}),
    ('--use-strict', 'interegular', {'use-strict': True}),
))
def test_success_add_with_options_and_requirements(option, requirement, target, tester, mocker):
    """Test success on a adding with default options."""
    mocker.patch.dict('sys.modules', {
        requirement: mocker.MagicMock(),
    })

    with configure_pyproject(mocker) as config:
        tester.execute(f'{option} parser parser.lark')
        assert tester.status_code == 0
        assert config == {
            'tool': {
                'lark': {
                    'standalone': [{
                        'module': 'parser',
                        'source': 'parser.lark',
                        **target,
                    }],
                },
            },
        }


@pytest.mark.parametrize(('option', 'requirement'), (
    ('--use-regex', 'regex'),
    ('--use-strict', 'interegular'),
))
def test_fail_add_with_options_and_requirements(option, requirement, tester, mocker):
    """Test success on a adding with default options."""
    mocker.patch.dict('sys.modules', {
        requirement: None,
    })

    with configure_pyproject(mocker):
        with pytest.raises(ValueError):
            tester.execute(f'{option} parser parser.lark')
