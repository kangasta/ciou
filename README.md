# CLI input and output utils (ciou)

[![CI](https://github.com/kangasta/ciou/actions/workflows/ci.yml/badge.svg)](https://github.com/kangasta/ciou/actions/workflows/ci.yml)
[![Release](https://github.com/kangasta/ciou/actions/workflows/release.yml/badge.svg)](https://github.com/kangasta/ciou/actions/workflows/release.yml)

Utilities for working with inputs and outputs of command-line interfaces.

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle ciou
autopep8 -aaar --in-place ciou
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance ciou tst
```

Run unit tests with command:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --branch --source ciou/ -m unittest discover -s tst/
coverage report -m
```
