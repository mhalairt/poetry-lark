"""Tests for building of the configurations."""

import pytest

from cleo.testers.command_tester import CommandTester
from poetry_lark.commands.build import LarkStandaloneBuild

from tests.heplers import configure_build


@pytest.fixture
def manual_tester() -> CommandTester:
    """Command's tester."""
    return CommandTester(LarkStandaloneBuild(ignore_manual=False))


@pytest.fixture
def auto_tester() -> CommandTester:
    """Command's tester."""
    return CommandTester(LarkStandaloneBuild(ignore_manual=True))


def test_success_build_on_manual(manual_tester, mocker):
    """Test success on a building in manual mode."""
    config = (
        '[[tool.lark.standalone]]\n'
        'module = {expose = "parser", auto-build = false}\n'
        'source = "grammar.lark"'
    )

    grammar = (
        '?start: sum\n'
        '  | NAME "=" sum -> assign_var\n\n'
        '?sum: product\n'
        '   | sum "+" product -> add\n'
        '   | sum "-" product -> sub\n\n'
        '?product: atom\n'
        '   | product "*" atom -> mul\n'
        '   | product "/" atom -> div\n\n'
        '?atom: NUMBER -> number\n'
        '   | "-" atom -> neg\n'
        '   | NAME -> var\n'
        '   | "(" sum ")"\n\n'
        '%import common.CNAME -> NAME\n'
        '%import common.NUMBER\n'
        '%import common.WS_INLINE\n'
        '%ignore WS_INLINE'
    )

    with configure_build(mocker, config, grammar) as result:
        manual_tester.execute('')
        assert manual_tester.status_code == 0
        assert result.getvalue().startswith('# The file was automatically generated by Lark')


def test_success_build_on_auto(auto_tester, mocker):
    """Test success on a building in auto mode."""
    config = (
        '[[tool.lark.standalone]]\n'
        'module = {expose = "parser", auto-build = true}\n'
        'source = "grammar.lark"'
    )

    grammar = (
        '?start: sum\n'
        '  | NAME "=" sum -> assign_var\n\n'
        '?sum: product\n'
        '   | sum "+" product -> add\n'
        '   | sum "-" product -> sub\n\n'
        '?product: atom\n'
        '   | product "*" atom -> mul\n'
        '   | product "/" atom -> div\n\n'
        '?atom: NUMBER -> number\n'
        '   | "-" atom -> neg\n'
        '   | NAME -> var\n'
        '   | "(" sum ")"\n\n'
        '%import common.CNAME -> NAME\n'
        '%import common.NUMBER\n'
        '%import common.WS_INLINE\n'
        '%ignore WS_INLINE'
    )

    with configure_build(mocker, config, grammar) as result:
        auto_tester.execute('')
        assert auto_tester.status_code == 0
        assert result.getvalue().startswith('# The file was automatically generated by Lark')


def test_success_skip_on_auto(auto_tester, mocker):
    """Test success skip on a building in auto mode."""
    config = (
        '[[tool.lark.standalone]]\n'
        'module = {expose = "parser", auto-build = false}\n'
        'source = "grammar.lark"'
    )

    with configure_build(mocker, config) as result:
        auto_tester.execute('')
        assert auto_tester.status_code == 0
        assert not result.getvalue()