from dataclasses import dataclass
import shlex
import subprocess
from typing import Iterable

from ._streams import Streams, StreamsData


def _parse_command(
    command: str | Iterable[str],
    ignore_errors=False,
) -> list[str]:
    if isinstance(command, str):
        if "\n" in command:
            return [
                "sh",
                "-c" if ignore_errors else "-ec",
                command,
            ]

        return shlex.split(command)

    return list(command)


@dataclass
class RunResult:
    '''Return value of the `run` function.'''
    success: bool
    '''Whether the command executed successfully (i.e. with exit code 0).'''
    console: StreamsData
    '''Captured output.'''
    process: subprocess.CompletedProcess
    '''The completed process object from `subprocess.run`.'''


def run(command,
        log_to_console=False,
        ignore_errors=False,
        **kwargs) -> RunResult:
    '''Run a command or script with `subprocess.run` and capture its stdout and
    stderr using `Streams`.

    Args:
        command: Command to run. Can be a string or a list of strings. If a
            string is passed and it contains newlines, it will be executed as
            a script using `sh -ec` (or `sh -c` if `ignore_errors` is `True`).
        log_to_console: If `True`, the output will be also streamed to the
            console.
        ignore_errors: If `True`, the script will be executed with `sh -c`
            instead of `sh -ec`. No effect when executing a single command.
    '''
    command = _parse_command(command, ignore_errors=ignore_errors)

    with Streams(
        log_to_console=log_to_console
    ) as (stdout, stderr, streams):
        streams.input(command)
        process = subprocess.run(
            command,
            stderr=stderr,
            stdout=stdout,
            bufsize=0,
            **kwargs)

    return RunResult(
        success=process.returncode == 0,
        console=streams.read(wait=True),
        process=process,
    )
