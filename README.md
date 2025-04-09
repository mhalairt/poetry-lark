# poetry-lark

[![Tests](https://github.com/mhalairt/poetry-lark/actions/workflows/tests.yml/badge.svg)](https://github.com/mhalairt/poetry-lark/actions/workflows/tests.yml)

[Lark](https://github.com/lark-parser/lark) is an amazing parsing toolkit for Python, built with a focus on ergonomics, performance and modularity. Lark can parse all context-free languages. To put it simply, it means that it is capable of parsing almost any programming language out there, and to some degree most natural languages too.

Lark can generate a stand-alone LALR(1) parser from a grammar. This plugin integrates Lark into the Poetry build system and provides several commands for configuring standalone parsers using `pyproject.toml` and Poetry.

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

In the simplest case, when adding a parser, you will get:

```toml
[[tool.lark.standalone]]
module = "parser"
source = "grammar.lark"
```

In a more complex case you can use all features of Lark standalone parser:

```toml
[[tool.lark.standalone]]
module = {expose = "parser", from = "src", auto-build = true}
source = "grammar.lark"
start = ["start"]
lexer = "contextual"
enable_compress = false
keep_all_tokens = false
propagate_positions = false
use_bytes = false
use_maybe_placeholders = true
use_regex = false
use_strict = false
```

These options are available on `lark-add` command:

| Argument | Description |
| --- | --- |
| `--src` | use the 'src' layout for the project |
| `-s <symbol>`, `--start <symbol>` | the grammar's start symbols, default `start`, can be multiple |
| `-l <lexer>`, `--lexer <lexer>` | the lexer to use, `basic` or `contextual`, default `contextual` |
| `-c`, `--enable-compress` | enable compression in the generated parser |
| `-K`, `--keep-all-tokens` | prevent removal of 'punctuation' tokens in the parse tree |
| `-P`, `--propagate-positions` | propagate positional attributes into metadata |
| `--use-bytes` | use `bytes` as input type instead of `str` |
| `--use-regex` | use the `regex` module instead of the `re` module |
| `--use-strict` | use strict mode in parsing |
| `--no-maybe-placeholders` | disable placeholders for empty optional tokens |
| `--no-auto-build` | disable automatic build for the module |
