#!/usr/bin/env python3

import os
from pprint import pprint
from shotgun_api3 import Shotgun
from collections import defaultdict

def pp(data):
    """debug output printing"""
    pprint(data, indent=2)

def dd(obj):
    """inspect available property and method names"""
    pp([symbol for symbol in sorted(dir(obj)) if not symbol.startswith('_')])

SERVER_PATH = os.environ['SG_SERVER_PATH']
SCRIPT_NAME = os.environ['SG_SCRIPT_NAME']
SCRIPT_KEY  = os.environ['SG_SCRIPT_KEY']


# instantiate a Shotgrid object
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)


def evaluate_sequence_query_field(sequence, query_field_name):
    """
	Goal: Use the introspected schema info to construct a new filter structure for each
	of the two Sequence query fields.

	notes:

	'sg_cut_duration':

		{ 'default_value': {'editable': False, 'value': None},
		  'query': { 'editable': False,
					 'value': { 'entity_type': 'Shot',
								'filters': { 'conditions': [ { 'active': 'true',
															   'path': 'sg_sequence',
															   'relation': 'is',
															   'values': [ { 'id': 0,
																			 'name': 'Current '
																					 'Sequence',
																			 'type': 'Sequence',
																			 'valid': 'parent_entity_token'}]}],
											 'logical_operator': 'and'}}},
		  'summary_default': {'editable': False, 'value': 'average'},
		  'summary_field': {'editable': False, 'value': 'sg_cut_duration'},
		  'summary_value': {'editable': False, 'value': None}}

	'sg_ip_versions':

		{ 'default_value': {'editable': False, 'value': None},
		  'query': { 'editable': False,
					 'value': { 'entity_type': 'Version',
								'filters': { 'conditions': [ { 'conditions': [ { 'active': 'true',
																				 'path': 'entity',
																				 'relation': 'is',
																				 'values': [ { 'id': 0,
																							   'name': 'Current '
																									   'Sequence',
																							   'type': 'Sequence',
																							   'valid': 'parent_entity_token'}]},
																			   { 'active': 'true',
																				 'path': 'entity.Shot.sg_sequence',
																				 'relation': 'is',
																				 'values': [ { 'id': 0,
																							   'name': 'Current '
																									   'Sequence',
																							   'type': 'Sequence',
																							   'valid': 'parent_entity_token'}]}],
															   'logical_operator': 'or'},
															 { 'conditions': [ { 'active': 'true',
																				 'conditions': [ { 'active': 'true',
																								   'path': 'sg_status_list',
																								   'relation': 'is_not',
																								   'values': [ 'na']},
																								 { 'active': 'true',
																								   'path': 'sg_status_list',
																								   'relation': 'is_not',
																								   'values': [ 'apr']}],
																				 'logical_operator': 'and',
																				 'qb_multivalued_condition_subgroup': True}],
															   'logical_operator': 'and'}],
											 'logical_operator': 'and'}}},
		  'summary_default': {'editable': False, 'value': 'record_count'},
		  'summary_field': {'editable': False, 'value': 'id'},
		  'summary_value': {'editable': False, 'value': None}}

    """

    data = {}
    # inspect
    data['properties'] = sg.schema_field_read('Sequence', query_field_name)[query_field_name]['properties']

    pp(data['properties'])

    data['entity_type'] = data['properties']['query']['value']['entity_type']
    if query_field_name == 'sg_cut_duration':
        data['path'] = data['properties']['query']['value']['filters']['conditions'][0]['path']
        data['type'] = data['properties']['query']['value']['filters']['conditions'][0]['values'][0]['type']
        data['id'] = data['properties']['query']['value']['filters']['conditions'][0]['values'][0]['id']
        data['operator'] = data['properties']['query']['value']['filters']['conditions'][0]['relation']
    data['summary_field'] = data['properties']['summary_field']['value']
    data['summary_default'] = data['properties']['summary_default']['value']

    new_filters = [['sg_sequence.Sequence.id', 'is', sequence['id']]]

    new_filters = [
        ['.'.join([data['path'], data['type'], "id"]),  data['operator'], sequence['id']]
    ]

    pp('new_filters:')
    pp(new_filters)

    result = sg.summarize(
        entity_type=data['entity_type'],
        filters = new_filters,
        summary_fields=[{"field": query_field_name, "type": data['summary_default']}]
    )

    return result['summaries']




if __name__ == "__main__":

    filters= [['project','is',{'type': 'Project','id': 85}]]
    fields=["code", "sg_cut_duration", "sg_ip_versions"]
    sequences = sg.find("Sequence", filters, fields)

    for sequence in sequences:
        #pp(sequence)

        #QUERY_FIELDS = ['sg_cut_duration', 'sg_ip_versions']
        QUERY_FIELDS = ['sg_cut_duration']
        #QUERY_FIELDS = ['sg_ip_versions']

        for field_name in QUERY_FIELDS:
            pp(evaluate_sequence_query_field(sequence, field_name))

