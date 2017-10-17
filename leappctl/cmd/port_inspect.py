import click
import json

from leappctl.cmd import debug_param, target_params
from leappctl.session import post


CMD = "port-inspect"
CMD_HELP = "This command scans ports on a target system"


@click.command(CMD, help=CMD_HELP)
@target_params
@click.option('--port-range',
              '-r',
              required=True,
              prompt=True,
              help='Specify port range to scan')
@click.option('--shallow-scan',
              '-s',
              is_flag=True,
              default=False,
              help='Should execute a shallow scan')
@debug_param
def cli(**kwargs):
    req_body = kwargs

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
