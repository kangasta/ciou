# CLI input and output utils (ciou)

[![CI](https://github.com/kangasta/ciou/actions/workflows/ci.yml/badge.svg)](https://github.com/kangasta/ciou/actions/workflows/ci.yml)
[![Docs](https://github.com/kangasta/ciou/actions/workflows/docs.yml/badge.svg)](https://github.com/kangasta/ciou/actions/workflows/docs.yml)
[![Release](https://github.com/kangasta/ciou/actions/workflows/release.yml/badge.svg)](https://github.com/kangasta/ciou/actions/workflows/release.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/b1f0abcbbb4d64f8b683/maintainability)](https://codeclimate.com/github/kangasta/ciou/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b1f0abcbbb4d64f8b683/test_coverage)](https://codeclimate.com/github/kangasta/ciou/test_coverage)

Utilities for working with inputs and outputs of command-line interfaces.

## Testing

Check and automatically fix formatting with:

```sh
pycodestyle ciou
autopep8 -aaar --in-place ciou
```

Run static analysis with:

```sh
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance ciou tst
```

Run unit tests with command:

```sh
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```sh
coverage run --branch --source ciou/ -m unittest discover -s tst/
coverage report -m
```

Generate the documentation with:

```sh
pdoc -d google -o docs ./ciou
```
