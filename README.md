# poetry-lark

[Lark](https://github.com/lark-parser/lark) is a parsing toolkit for Python, built with a focus on ergonomics, performance and modularity. This plugin integrates Lark into the Poetry build system and provides several commands for configuring standalone parsers using `pyproject.toml` and Poetry.

## Install

    $ poetry self add poetry-lark

The plugin depends only on Lark and Poetry, but you can use Lark's extra features: 

- `interegular` (if it is installed, Lark uses it to check for collisions, and warn about any conflicts that it can find)
- `regex` (if you want to use the `regex` module instead of the `re` module).

## Usage

    $ poetry lark-add <module> <grammar-file>
    $ poetry lark-remove <module>
    $ poetry lark-build <module>

By default, the plugin is integrated into the Poetry build system and generates all parser modules specified in the `pyproject.toml` (if `auto-build` option is not configured as `false` for parser module).
