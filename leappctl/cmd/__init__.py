import functools

import click

from leappctl.utils import to_port_spec


def source_params(func):
    """ Default options to define source host """
    @click.option('--source-host',
                  '-s',
                  required=True,
                  prompt=True,
                  help='Host from which data will be retrieved.')
    @click.option('--source-user',
                  '-u',
                  required=True,
                  default='root',
                  help='User in source host to connect via SSH.')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def target_params(func):
    """ Default options to define target host """
    @click.option('--target-host',
                  '-t',
                  required=True,
                  prompt=True,
                  default='localhost',
                  help='Host in which action will be executed.')
    @click.option('--target-user',
                  '-U',
                  default='root',
                  help='User in target host to connect via SSH.')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def tcp_ports_map_params(func):
    """ Default options to define TCP ports mapping """
    @click.option('--tcp-ports',
                  '-p',
                  default=None,
                  multiple=True,
                  type=to_port_spec,
                  help='(Re)define target tcp ports - [target_port:source_port]')
    @click.option('--excluded-ports',
                  '-e',
                  default=None,
                  multiple=True,
                  type=to_port_spec,
                  help='Define tcp ports which will be excluded from the mapped ports [[target_port]:source_port>]')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def container_name_param(func):
    """ Default option to define container name """
    @click.option('--container-name',
                  '-n',
                  help='Container name to be used')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def debug_param(func):
    """ Default option to enable debug logging """
    @click.option('--debug',
                  '-D',
                  is_flag=True,
                  default=False,
                  help='Turn on debug logging on stderr')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
