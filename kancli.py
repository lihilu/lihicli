import click
import logging
import logging.handlers
import requests
import json
from tabulate import tabulate

myUrl = 'https://kandula.ops.club/'

@click.group()
@click.option('--debug/--no-debug', is_flag=True, default=False, help="Print debugging messages. Default is False")
@click.pass_context
def kancli(ctx, debug):
     click.secho('Welcome to kancli \n', fg="cyan", bold=True, underline=True)
     ctx.obj['DEBUG'] = debug
     init_logging(debug)
     ctx.obj['logger'] = logging.getLogger()

def init_logging(debug_enabled: bool):
    logging.basicConfig(
        format='%(asctime)s %(filename)s[%(levelname)s]: %(message)s')
    logger = logging.getLogger()
    logging.StreamHandler(stream=None)
    logger.setLevel(logging.INFO)
    file_handler = logging.handlers.RotatingFileHandler(
        filename='kancli.log', maxBytes=5000000, backupCount=10)
    logger.addHandler(file_handler)
    if debug_enabled:
        logger.setLevel(logging.DEBUG)
    logger.propagate = False


def exception_print(ex):
    click.secho("Error!", fg="red", bold=True)
    click.secho((str(ex).split(':', 1)[1])[1:], fg="red")

@click.command()
@click.version_option (version='27.07.84', prog_name='kancli', help="Displays version")
@click.pass_context


@kancli.command()
@click.pass_context
@click.option('-i', '--instance-id', type=str, required=True, prompt="Enter instance ID", help= "Instance you want to stop")
def stop_instance(ctx, instance_id):
    """Stop Instnace"""
    ctx.obj['logger'].debug("Running function 'stop_instance'")
    click.secho(f'stop instance: {instance_id}',fg="blue")
    value = click.confirm('Are you sure?')
    if value:
        try:
            ctx.obj['logger'].debug(f'Request to stop instance: {instance_id}')
            requests.get(myUrl+"instances/"+instance_id+"/stop")
            ctx.obj['logger'].info(f'Instance: {instance_id} has been stopped')
            click.secho('Instance ' +instance_id+ ' has been stopped successfully',fg="green")
        except Exception as ex:
            ctx.obj['logger'].error(ex)
            exception_print(ex)
    else:
        click.secho("Cancelling",fg="red")

@kancli.command()
@click.pass_context
@click.option('-i', '--instance-id', type=str, required=True, prompt="Enter instance ID", help= "Instance you want to start")
def start_instance(ctx, instance_id):
    """Start Instnace"""
    ctx.obj['logger'].debug("Running function 'start_instance'")
    click.secho(f'start instance: {instance_id}',fg="blue")
    value = click.confirm('Are you sure?')
    if value:
        try:
            ctx.obj['logger'].debug(f'Request to start instance: {instance_id}')
            requests.get(myUrl+"instances/"+instance_id+"/start")
            ctx.obj['logger'].info(f'Instance: {instance_id} has been started')
            click.secho('Instance ' +instance_id+ ' has been started successfully',fg="green")
        except Exception as ex:
            ctx.obj['logger'].error(ex)
            exception_print(ex)
    else:
        click.secho("Cancelling",fg="red")

@kancli.command()
@click.pass_context
@click.option('-i', '--instance-id', type=str, required=True, prompt="Enter instance ID", help= "Instance you want to start")
def terminate_instance(ctx, instance_id):
    """Terminate Instnace"""
    ctx.obj['logger'].debug("Running function 'terminate_instance'")
    click.secho(f'terminate instance: {instance_id}',fg="blue")
    value = click.confirm('Are you sure?')
    if value:
        try:
            ctx.obj['logger'].debug(f'Request to terminate instance: {instance_id}')
            requests.get(myUrl+"instances/"+instance_id+"/terminate")
            ctx.obj['logger'].info(f'Instance: {instance_id} has been terminated')
            click.secho('Instance ' +instance_id+ ' has been terminated successfully',fg="green")
        except Exception as ex:
            ctx.obj['logger'].error(ex)
            exception_print(ex)
    else:
        click.secho("Cancelling",fg="red")

@kancli.command()
@click.pass_context
def get_instance_list(ctx):
    """Get instances info"""
    ctx.obj['logger'].debug("Running function 'get_all_instances'")
    try:
        ctx.obj['logger'].debug(f"Request to get instance list")
        instances = requests.get(myUrl+"instance_list")
        click.echo(tabulate(instances.json(), headers=[
                   "ID", "Type", "Region", "State", "IP Address"]))
        click.secho('Instance list retrieved',fg="green")
    except Exception as ex:
        ctx.obj['logger'].error(ex)
        exception_print(ex)


if __name__ == '__main__':
    kancli(obj={})
