# poetry-lark

[![Tests](https://github.com/mhalairt/poetry-lark/actions/workflows/tests.yml/badge.svg)](https://github.com/mhalairt/poetry-lark/actions/workflows/tests.yml)

[Lark](https://github.com/lark-parser/lark) is a parsing toolkit for Python, built with a focus on ergonomics, performance and modularity. This plugin integrates Lark into the Poetry build system and provides several commands for configuring standalone parsers using `pyproject.toml` and Poetry.

## Install

    $ poetry add --group dev poetry-lark

The plugin depends only on Lark and Poetry, but you can use Lark's extra features: `interegular` (if it is installed, Lark uses it to check for collisions, and warn about any conflicts that it can find (required for strict mode) and `regex` (if you want to use the `regex` module instead of the `re` module).

## Use

### Add

    $ poetry lark-add <module> <grammar-file>

Also, you can specify additional options:

| Option | Description |
| --- | --- |
| `--src` | Use the 'src' layout for the project, module will be generated in src directory. |
| `--no-auto-build` | Disable automatic build for the project on `poetry build`. |
| `--start`, `-s` | The grammar's start symbol(s), default is `start` |
| `--lexer`, `-l` | The lexer to use (`basic` or `contextual`, default is `contextual`). |
| `--enable-compress`, `-c` | Enable compression in the generated parser. |
| `--keep-all-tokens`, `-K` | Prevent removal of 'punctuation' tokens in the parse tree. |
| `--propagate-positions`, `-P` | Propagate positional attributes into metadata. |
| `--use-bytes` | Use `bytes` as input type instead of `str`. |
| `--no-maybe-placeholders` | Disable `None` as a placeholder for empty optional tokens. |
| `--use-regex` | Use the `regex` module instead of the `re` module, requires the `regex` module. |
| `--use-strict` | Enable strict mode in parsing, requires the `interegular` module. |

### Remove

    $ poetry lark-remove <module>

### Build

    $ poetry lark-build <module>

By default, the plugin is integrated into the Poetry build system and generates all parser modules specified in the configuration.
