import json

import click

from leappctl.cmd import debug_param, source_params, target_params, tcp_ports_map_params
from leappctl.session import post
from leappctl.utils import to_port_map


CMD = "port-map"
CMD_HELP = "Commmand that scans ports on source and target system and create a port mapping"


@click.command(CMD, help=CMD_HELP)
@source_params
@target_params
@tcp_ports_map_params
@debug_param
def cli(**kwargs):
    req_body = kwargs

    # Transformations
    req_body['tcp_ports'] = to_port_map(req_body.pop('tcp_ports'))
    req_body['excluded_tcp_ports'] = {"tcp": {str(x[0]): {"name": ""} for x in req_body['excluded_ports'] or ()}}
    req_body['default_port_map'] = True

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
