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


# instantiate a Shotgrid object
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)



def evaluate_query_field(query_field_name, entity, props):
    """
    Use the introspected schema info to construct a new filter structure
    for the given query field.

    This solution recurses though an arbitrarily deep level of filter
    conditions to construct a new query and work for any query fields passed in.

    See the output of the schema properties for the two query fields in
    ./schema.txt

    """

    # Inspect - inspect the filter conditions and build a new filter structure to pass
    # to sg.summarize() -- NOTE: Not yet working for sg_ip_versions:

    data = {}

    data['entity_type'] = props['query']['value']['entity_type']
    data['summary_field'] = props['summary_field']['value']
    data['summary_default'] = props['summary_default']['value']

    filters  = props['query']['value']['filters']

    def build_filters(filters):
        """
        A recursive function to construct a potentially nested 'filters' object.

        (defined as an inner function to have access to 'entity')
        """

        if 'path' in filters:
            values = filters['values'][0]
            if 'name' in filters['values'][0]:
                values = filters['values'][0]['name']
                if values == 'Current Sequence':
                    values = entity
            return [filters['path'], filters['relation'], values]
        else:
            if 'logical_operator' in filters:
                filter = {}
                filter['filter_operator'] = filters['logical_operator']
                filter['filters'] = []

                for sub_filter in filters['conditions']:
                    filter['filters'].append(build_filters(sub_filter))
                return filter


    new_filters = build_filters(filters)

    pp(new_filters['filters'], 'new_filters', 1)

    result = sg.summarize(
        entity_type=data['entity_type'],
        filters=new_filters['filters'],
        summary_fields=[{"field": data['summary_field'], "type": data['summary_default']}]
    )
                
    return {
        'query_field': query_field_name,
        'type': data['summary_default'].replace('_',' ').title(),
        'value': result['summaries'][data['summary_field']]
    }




if __name__ == "__main__":

    # get all Sequences
    filters= [['project','is',{'type': 'Project','id': 85}]]
    sequences = sg.find("Sequence", filters, ["code"])

    sgdata = []

    for sequence in sequences:

        pp(sequence, 'Sequence', 1)
        pp('-'*70, None, 1)

        QUERY_FIELDS = ['sg_cut_duration', 'sg_ip_versions']

        data = []
        for query_field_name in QUERY_FIELDS:

            pp(query_field_name, 'query_field_name', 1)

            props = sg.schema_field_read('Sequence', query_field_name)[query_field_name]['properties']
            data.append(
                evaluate_query_field(query_field_name, sequence, props)
            )

            pp('-'*70, None, 1)

        sgdata.append({
            'type': sequence['type'],
            'id': sequence['id'],
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

