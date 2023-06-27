# SFU Outlines CLI

`sfu-cli` lets you fuzzily interact with the [SFU Outlines REST
API](http://www.sfu.ca/outlines/help/api.html) to retrieve a course outline in
JSON.

`display.py` is a helper that displays the course outline in your terminal with
[rich](https://github.com/Textualize/rich) formatted text.

## Table of Contents

<!--toc:start-->
- [SFU Outlines CLI](#sfu-outlines-cli)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [`sfu-cli`](#sfu-cli)
    - [`display.py`](#displaypy)
      - [Python Virtual Environment](#python-virtual-environment)
  - [Usage](#usage)
    - [`sfu-cli`](#sfu-cli)
      - [Output](#output)
    - [`display.py`](#displaypy)
<!--toc:end-->

## Setup

### `sfu-cli` 

- Dependencies
    - curl
    - [fzf](https://github.com/junegunn/fzf)
    - [jq](https://jqlang.github.io/jq/)

### `display.py`

- Dependencies
    - See [`requirements.txt`](./requirements.txt)

#### Python Virtual Environment

```
python -m venv venv
./venv/bin/pip install -r requirements.txt
```

## Usage

### `sfu-cli`

```
./sfu-cli --help
```

#### Output

The requested outline will be printed as output after the course section is
selected, as well as saved in the `./outlines/` directory using the following 
structure (same as API structure):

```
./outlines/<year>/<term>/<dept>/<num>/<section>/outline.json
```

### `display.py`

```
./venv/bin/python display.py [JSON_OUTLINE_FILE]
```

This can be called directly by `sfu-cli` with the `-p, --pretty` flag (the
python virtual environment must be setup exactly as shown
[above](#python-virtual-environment)).
