import logging

import click

from detectem.response import get_har
from detectem.plugin import load_plugins
from detectem.core import Detector

# Set up logging
logger = logging.getLogger('detectem')
ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


@click.command()
@click.option(
    '--debug',
    default=False,
    is_flag=True,
    help='Include this flag to enable debug messages.'
)
@click.option(
    '--format',
    default=None,
    type=click.Choice(['json']),
    help='Set the format of the results.'
)
@click.option(
    '--metadata',
    default=False,
    is_flag=True,
    help='Include this flag to return plugin metadata.'
)
@click.argument('url')
def main(debug, format, metadata, url):
    if debug:
        click.echo("[+] Enabling debug mode.")
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.ERROR)

    print(get_detection_results(url, format, metadata))


def get_detection_results(url, format, metadata):
    har_data = get_har(url)
    plugins = load_plugins()

    det = Detector(har_data, plugins, url)
    det.start_detection()
    return det.get_results(format=format, metadata=metadata)


if __name__ == "__main__":
    main()
