import click
from pathlib import Path, PurePath


class Samples():
    '''
    Class that performs the function of extracting samples from the core store input workbook
    and transforming them into a new workbook and copying related images
    '''

    def __init__(self, sample_type, sample_file, image_directory):
        self.sample_type = sample_type
        self.sample_file = sample_file
        self.sample_file_exists = Path(sample_file).exists()
        self.image_directory = image_directory
        self.output_workbook = Path(__file__).resolve().parent / 'output' / 'output.xlsx'
        self.out_workbook_exists = self.output_workbook.exists()

    def __str__(self):
        return f'Sample type = {self.sample_type}\nSample file = {self.sample_file} {self.sample_file_exists}\n' \
               f'Output workbook = {self.output_workbook} {self.out_workbook_exists}'


@click.group()
@click.pass_context
def main(ctx):
    """
    A little cli tool to work out how click works
    """
    ctx.obj = {'copex_type': 'copex_type'}


@main.command()
@click.option('-s', '--sample-type', type=click.Choice(['petroleum', 'mineral']))
@click.argument('samples_file', type=click.Path(exists=True))
@click.argument('image_directory')
@click.pass_context
def extract(ctx, sample_type, samples_file, image_directory):
    samples = Samples(sample_type, samples_file, image_directory)
    print(samples)
    click.echo(f'extracting type {sample_type} from {samples_file}')
    click.echo(f'copying images from {image_directory}')


@main.command()
@click.pass_context
@click.option('-c', '--copex-type', type=click.Choice(['flat', 'nested']))
def copex(ctx, copex_type):
    click.echo(f'creating copex of type {copex_type}')

@main.command()
@click.pass_context
def validate(ctx):
    click.echo(f'validating')


if __name__ == '__main__':
    main()