import json

import click

from leappctl.cmd import debug_param, target_params
from leappctl.session import post


CMD = "check-target"
CMD_HELP = "This command checks services (like Docker, Rsync) on a target system"


@click.command(CMD, help=CMD_HELP)
@target_params
@click.option('--check-target-service-status',
              '-s',
              is_flag=True,
              default=False,
              help='Check status of services')
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
