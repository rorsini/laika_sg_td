#!/usr/bin/env python3

import os
from pprint import pprint
from shotgun_api3 import Shotgun
from sgtd import generate_html

def pp(pdata, title='', nl=0):
    """debug output util"""
    if title: print(f'{title}:')
    pprint(pdata, indent=2)
    for _ in range(nl): print()

def dd(obj):
    """
    inspect available property and method names, e.g. dd(sg)
    """
    pp([symbol for symbol in sorted(dir(obj)) if not symbol.startswith('_')])

SERVER_PATH = os.environ['SG_SERVER_PATH']
SCRIPT_NAME = os.environ['SG_SCRIPT_NAME']
SCRIPT_KEY  = os.environ['SG_SCRIPT_KEY']

# instantiate a Shotgrid object
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

def evaluate_query_field(field_name, entity, props):
    """
    Use the introspected schema info to construct a new filter structure
    for the given query field.

    This solution recurses though an arbitrarily deep level of filter
    conditions to construct a new query and work for any query fields passed in.

    See the output of the schema properties for the two query fields in
    ./schema.txt

    """

    data = {}

    data['entity_type'] = props['query']['value']['entity_type']
    data['summary_field'] = props['summary_field']['value']
    data['summary_default'] = props['summary_default']['value']

    filters  = props['query']['value']['filters']

    def build_query_field_filters(schema_filters):
        """
        A recursive function to construct a potentially nested 'filters' object.

        (defined as an inner function to have access to 'entity')
        """

        if 'path' in schema_filters:
            values = schema_filters['values'][0]
            if 'name' in schema_filters['values'][0]:
                values = schema_filters['values'][0]['name']
                if values == 'Current Sequence':
                    values = entity
            return [schema_filters['path'], schema_filters['relation'], values]
        else:
            if 'logical_operator' in schema_filters:
                new_filter = {}
                new_filter['filter_operator'] = schema_filters['logical_operator']
                new_filter['filters'] = []

                for sub_filter in schema_filters['conditions']:
                    new_filter['filters'].append(build_query_field_filters(sub_filter))
                return new_filter


    new_filters = build_query_field_filters(filters)

    pp(new_filters['filters'], 'new_filters', 1)

    result = sg.summarize(
        entity_type=data['entity_type'],
        filters=new_filters['filters'],
        summary_fields=[{"field": data['summary_field'], "type": data['summary_default']}]
    )
                
    return {
        'query_field': field_name,
        'type': data['summary_default'].replace('_',' ').title(),
        'value': result['summaries'][data['summary_field']]
    }


if __name__ == "__main__":

    # get all Sequences
    seq_filters= [['project','is',{'type': 'Project','id': 85}]]
    sequences = sg.find("Sequence", seq_filters, ["code"])

    sgdata = []

    for sequence in sequences:

        pp(sequence, 'Sequence', 1)
        pp('-'*70, None, 1)

        QUERY_FIELDS = ['sg_cut_duration', 'sg_ip_versions']

        evaluated_data = []
        for query_field_name in QUERY_FIELDS:

            pp(query_field_name, 'query_field_name', 1)

            # inspect the sg schema for current query field filter conditions
            properties = sg.schema_field_read('Sequence', query_field_name)[query_field_name]['properties']
            evaluated_data.append(
                evaluate_query_field(query_field_name, sequence, properties)
            )

            pp('-'*70, None, 1)

        sgdata.append({
            'type': sequence['type'],
            'id': sequence['id'],
            'name': sequence['code'],
            'data': evaluated_data
        })

    pp(sgdata, 'results')

    ## HTML output:
    generate_html(sgdata)
