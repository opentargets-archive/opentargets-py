import click
import json
from opentargets import OpenTargetsClient

#TODO expand to other OpenTargetsClient functions
#TODO implement filter chains using http://click.pocoo.org/6/commands/#multi-command-chaining

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
@click.argument('symbol')
def search(symbol):
    click.echo('searching for %s' % symbol)
    ot = OpenTargetsClient()
    search_result = ot.search(symbol)
    print(json.dumps(search_result[0],sort_keys=True, indent=4))

@cli.command()
@click.argument('symbol')
def map(symbol):
    #TODO handle a list of IDs passed as text file and/or pipe
    click.echo('looking for ENSGID for %s' % symbol)
    ot = OpenTargetsClient()
    search_result = ot.search(symbol)
    print(search_result[0]['data']['id'])
