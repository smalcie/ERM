import click
from pathlib import Path


@click.command()
@click.option('-s', '--sample-type', type=click.Choice(['petroleum', 'mineral']))
@click.option('-d', '--drillhole', multiple=True)
@click.argument('file', type=click.Path(exists=True))
@click.argument('directory', type=click.Path(exists=True))
def extract(sample_type, drillhole, file, directory):
    click.echo(f'extracting type {sample_type}')
    click.echo(f'drillhole names {", ".join(drillhole)}')
    click.echo(f'from file {file}')
    click.echo(f'to directory {directory}')


if __name__ == '__main__':
    extract()
