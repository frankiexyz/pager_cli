# Overview

pagerduty cli to list/ack/resolve incidents

This project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).

[![Unix Build Status](https://img.shields.io/travis/com/frankiexyz/pager_cli.svg?label=unix)](https://travis-ci.com/frankiexyz/pager_cli)
[![Windows Build Status](https://img.shields.io/appveyor/ci/frankiexyz/pager_cli.svg?label=windows)](https://ci.appveyor.com/project/frankiexyz/pager_cli)
[![Coverage Status](https://img.shields.io/codecov/c/gh/frankiexyz/pager_cli)](https://codecov.io/gh/frankiexyz/pager_cli)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/frankiexyz/pager_cli.svg)](https://scrutinizer-ci.com/g/frankiexyz/pager_cli)
[![PyPI Version](https://img.shields.io/pypi/v/pager_cli.svg)](https://pypi.org/project/pager_cli)
[![PyPI License](https://img.shields.io/pypi/l/pager_cli.svg)](https://pypi.org/project/pager_cli)

# Setup

## Requirements

* Python 3.7+

## Installation

Install it directly into an activated virtual environment:

```text
$ pip install pager_cli
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add pager_cli
```

# Usage

create a file to store your API key
```text
cat ~/.pager_cli -p
userid: YOUR_USER_ID(eg:PBZDORP)
apikey: YOUR_API_KEY
```

List and ACK the incident
```bash
 # pager_cli --help
 Usage: pager_cli [OPTIONS]

   Console script for pager_cli.

   Options:
   --action TEXT  Action list/ack/resolve
   --config TEXT  config file default:~/.pager_cli
   --help         Show this message and exit.
 # pager_cli
 ⠸ Loading...
 🦾 No active incident
```
