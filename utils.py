import boto3
import botocore
import json

def parse_template(template):
    cf = boto3.client('cloudformation')
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()
    cf.validate_template(TemplateBody=template_data)
    return template_data


def parse_parameters(parameters):
    with open(parameters) as parameter_fileobj:
        parameter_data = json.load(parameter_fileobj)
    return parameter_data


def stack_exists(stack_name, region):
    cf = boto3.client('cloudformation', region_name=region)
    stacks = cf.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False

def stackset_exists(stackset_name):
    cf = boto3.client('cloudformation')
    stacksets = cf.list_stack_sets()['Summaries']
    for stackset in stacksets:
        if stackset['Status'] == 'DELETED':
            continue
        if stackset_name == stackset['StackSetName']:
            return True
    return False