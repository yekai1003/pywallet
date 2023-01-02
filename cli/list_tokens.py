import click
from configuration import Configuration


@click.command()
def list_tokens():
    """List all added tokens."""
    configuration = Configuration().load_configuration()

    tokens = configuration.contracts
    click.echo('ETH')
    for token in tokens:
        click.echo('%s' % token)

if __name__ == '__main__':
    list_tokens()