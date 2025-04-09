"""Test's helpers."""

from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

from poetry.poetry import Poetry
from tomlkit import loads

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@contextmanager
def configure_pyproject(mocker: 'MockerFixture', config: str = ''):
    """Mock pyproject.toml with initial data."""
    document = loads(config)

    poetry = mocker.MagicMock(spec=Poetry)
    poetry.pyproject.data = document

    mocker.patch(
        'poetry.console.commands.command.Command.poetry',
        new_callable=mocker.PropertyMock,
        return_value=poetry,
    )

    yield document


@contextmanager
def configure_build(mocker: 'MockerFixture', config: str = '', grammar: str = ''):
    """Mock builder."""
    out = StringIO(newline='\n')

    source_file = mocker.MagicMock(spec=Path)
    source_file.exists.return_value = True
    source_file.read_text.return_value = grammar

    module_file = mocker.MagicMock(spec=Path)
    module_file.unlink.return_value = None
    module_file.open.return_value = out

    mocker.patch(
        'poetry_lark.toml.Parser.source_file',
        new_callable=mocker.PropertyMock,
        return_value=source_file,
    )

    mocker.patch(
        'poetry_lark.toml.Parser.module_file',
        new_callable=mocker.PropertyMock,
        return_value=module_file,
    )

    with configure_pyproject(mocker, config):
        yield out
