#!/usr/bin/env python3

import os
from pprint import pprint
from shotgun_api3 import Shotgun
from jinja2 import Environment, FileSystemLoader

def pp(data, title='', nl=0):
    """debug output util"""
    if title: print(f'{title}:')
    pprint(data, indent=2)
    for n in range(nl): print()

def dd(obj):
    """
    inspect available property and method names, e.g. dd(sg)
    """
    pp([symbol for symbol in sorted(dir(obj)) if not symbol.startswith('_')])

SERVER_PATH = os.environ['SG_SERVER_PATH']
SCRIPT_NAME = os.environ['SG_SCRIPT_NAME']
SCRIPT_KEY  = os.environ['SG_SCRIPT_KEY']


# Instantiate a Shotgrid object
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)


def evaluate_query_field(query_field_name, entity, props):
    """
    Goal: Use the introspected schema info to construct a new filter structure
    for each of the two Sequence query fields.

    A programatic solution should (ideally) recurse though an unknown level of
    filter conditions to constuct a new query and work for any query fields
    passed in.

    See the output of the schema properties for the two query fields in
    ./schema.txt

    """

    # Inspect - inspect the filter conditions and build a new filter structure to pass
    # to sg.summarize() -- NOTE: Not yet working for sg_ip_versions:

    data = {}

    pp(query_field_name, 'query_field_name', 1)
    pp(entity, 'Entity', 1)
    #pp(props, 'Properites', 1)

    #data['entity_type'] = entity['type']
    data['entity_type'] = props['query']['value']['entity_type']
    data['summary_field'] = props['summary_field']['value']
    data['summary_default'] = props['summary_default']['value']

    new_filters = []

    if query_field_name == 'sg_cut_duration':

        data['path'] = props['query']['value']['filters']['conditions'][0]['path']
        data['operator'] = props['query']['value']['filters']['conditions'][0]['relation']

        new_filters.append([data['path'], data['operator'], entity])

    elif query_field_name == 'sg_ip_versions':

        data['path'] = props['query']['value']['filters']['conditions'][0]\
                ['conditions'][1]['path']
        data['operator'] = props['query']['value']['filters']['conditions'][0]\
                ['conditions'][1]['relation']

        new_filters.append([data['path'], data['operator'], entity])

    pp(new_filters, 'new_filters', 1)

    result = sg.summarize(
        entity_type=data['entity_type'],
        filters=new_filters,
        summary_fields=[{"field": data['summary_field'], "type": data['summary_default']}]
    )

                
    return {
        'query_field': query_field_name,
        'type': data['summary_default'],
        'result': result['summaries'][data['summary_field']]
    }




if __name__ == "__main__":

    # get all Sequences
    filters= [['project','is',{'type': 'Project','id': 85}]]
    sequences = sg.find("Sequence", filters, ["code"])

    sgdata = []

    for sequence in sequences:

        QUERY_FIELDS = ['sg_cut_duration']
        QUERY_FIELDS = ['sg_ip_versions']
        QUERY_FIELDS = ['sg_cut_duration', 'sg_ip_versions']

        data = []
        for query_field_name in QUERY_FIELDS:
            props = sg.schema_field_read('Sequence', query_field_name)[query_field_name]['properties']
            data.append(
                evaluate_query_field(query_field_name, sequence, props)
            )

        sgdata.append({
            'type': sequence['type'],
            'name': sequence['code'],
            'data': data
        })

    pp(sgdata, 'results')

    ## HTML output:

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')
    output_from_parsed_template = template.render(sgdata=sgdata)
    # debug html output
    #pp(output_from_parsed_template)

    # render the results to html file
    with open("output/index.html", "w") as fh:
        fh.write(output_from_parsed_template)

