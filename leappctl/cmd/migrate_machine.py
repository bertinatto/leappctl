import json

import click

from leappctl.cmd import container_name_param, debug_param, source_params, target_params, tcp_ports_map_params
from leappctl.session import post
from leappctl.utils import to_port_map


CMD = "migrate-machine"
CMD_SHORT_HELP = "Executes the migration of an OS into a macrocontainer"
CMD_LONG_HELP = """
This command migrates one or more application into containers by creating a macrocontainer.

This means that the entire system will be converted into a container, possibly bringing all the dirty with it.
"""


@click.command(CMD, help=CMD_LONG_HELP, short_help=CMD_SHORT_HELP)
@source_params
@target_params
@tcp_ports_map_params
@container_name_param
@click.option('--disable-start',
              '-d',
              is_flag=True,
              default=False,
              help='Don\'t start the container')
@click.option('--force-create',
              '-f',
              is_flag=True,
              default=True,
              help='Force container creation in the target.')
@click.option('--excluded_paths',
              '-E',
              multiple=True,
              type=click.Path(),
              help='Define paths which will be excluded from the source')
@debug_param
def cli(**kwargs):
    req_body = kwargs

    # Transformations
    req_body['tcp_ports'] = to_port_map(req_body.pop('tcp_ports'))
    req_body['excluded_tcp_ports'] = {"tcp": {str(x[0]): {"name": ""} for x in req_body['excluded_ports'] or ()}}
    req_body['default_port_map'] = True
    req_body['start_container'] = not req_body['disable_start']

    # POST collected data to the appropriate endpoint in leapp-daemon
    resp = post(CMD, req_body)

    # Pretty-print response
    resp_body = resp.json()
    json_pprint = json.dumps(resp_body, sort_keys=True, indent=4, separators=(',', ': '))
    click.secho(
        'Response:\n{0}\n'.format(json_pprint),
        bold=True,
        fg='green' if resp.status_code == 200 else 'red'
    )
