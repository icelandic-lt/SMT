"""The command line interface to the package.

See frontend --help for guidance.
"""
from pathlib import Path

import click

from . import api as api
from . import server as s


@click.group()
def cli():
    """The main entry point of the command line client.

    Other commands are attached to this functions.
    """


class PathParamType(click.ParamType):
    """A type to convert strings from command line to Path."""

    def convert(self, value, param, ctx):
        try:
            return Path(value).resolve()
        except TypeError:
            self.fail(
                "expected a path for Path() conversion, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail(f"{value!r} is not a valid path", param, ctx)


PathType = PathParamType()


@cli.command()
@click.argument('sent')
@click.argument('lang', default='is', type=str)
@click.argument('version', default='v2', type=str)
def preprocess(sent: str, lang: str, version: str) -> str:
    """
    Applies the same preprocessing steps to a sentence as specified by the version.
    See api.py for preprocessing step details.
    """
    l_lang = api.to_lang(lang)
    sent = api.preprocess(sent, l_lang, version)
    click.echo(sent)
    return sent


@cli.command()
@click.option('--debug', is_flag=True)
def server(debug: bool) -> None:
    s.app.run(debug=debug, host='0.0.0.0')


if __name__ == '__main__':
    cli()
