#!/usr/bin/env python3

import os
from pprint import pprint
from shotgun_api3 import Shotgun
from collections import defaultdict

def pp(data):
    """debug output printing"""
    #pprint(data, indent=2)
    pprint(data)

def dd(obj):
    """inspect available property and method names"""
    pp([symbol for symbol in sorted(dir(obj)) if not symbol.startswith('_')])

SERVER_PATH = os.environ['SG_SERVER_PATH']
SCRIPT_NAME = os.environ['SG_SCRIPT_NAME']
SCRIPT_KEY  = os.environ['SG_SCRIPT_KEY']


# instantiate a Shotgrid object
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

QUERY_FIELDS = ['sg_cut_duration', 'sg_ip_versions']


"""
In [6]: sg.schema_field_read('Sequence', 'sg_cut_duration')
Out[6]:
{'sg_cut_duration': {'name': {'value': 'Cut Duration', 'editable': True},
  'description': {'value': '', 'editable': True},
  'custom_metadata': {'value': '', 'editable': True},
  'entity_type': {'value': 'Sequence', 'editable': False},
  'data_type': {'value': 'summary', 'editable': False},
  'editable': {'value': True, 'editable': False},
  'mandatory': {'value': False, 'editable': False},
  'unique': {'value': False, 'editable': False},
  'properties': {'default_value': {'value': None, 'editable': False},
   'summary_default': {'value': 'average', 'editable': False},
   'summary_value': {'value': None, 'editable': False},
   'summary_field': {'value': 'sg_cut_duration', 'editable': False},
   'query': {'value': {'entity_type': 'Shot',
     'filters': {'logical_operator': 'and',
      'conditions': [{'path': 'sg_sequence',
        'relation': 'is',
        'values': [{'type': 'Sequence',
          'id': 0,
          'name': 'Current Sequence',
          'valid': 'parent_entity_token'}],
        'active': 'true'}]}},
    'editable': False}},
  'visible': {'value': True, 'editable': True},
  'ui_value_displayable': {'value': True, 'editable': False}}}
"""

"""
In [7]: sg.schema_field_read('Sequence', 'sg_ip_versions')
Out[7]:
{'sg_ip_versions': {'name': {'value': 'IP Versions', 'editable': True},
  'description': {'value': '', 'editable': True},
  'custom_metadata': {'value': '', 'editable': True},
  'entity_type': {'value': 'Sequence', 'editable': False},
  'data_type': {'value': 'summary', 'editable': False},
  'editable': {'value': True, 'editable': False},
  'mandatory': {'value': False, 'editable': False},
  'unique': {'value': False, 'editable': False},
  'properties': {'default_value': {'value': None, 'editable': False},
   'summary_default': {'value': 'record_count', 'editable': False},
   'summary_value': {'value': None, 'editable': False},
   'summary_field': {'value': 'id', 'editable': False},
   'query': {'value': {'entity_type': 'Version',
     'filters': {'logical_operator': 'and',
      'conditions': [{'logical_operator': 'or',
        'conditions': [{'path': 'entity',
          'relation': 'is',
          'values': [{'type': 'Sequence',
            'id': 0,
            'name': 'Current Sequence',
            'valid': 'parent_entity_token'}],
          'active': 'true'},
         {'path': 'entity.Shot.sg_sequence',
          'relation': 'is',
          'values': [{'type': 'Sequence',
            'id': 0,
            'name': 'Current Sequence',
            'valid': 'parent_entity_token'}],
          'active': 'true'}]},
       {'logical_operator': 'and',
        'conditions': [{'logical_operator': 'and',
          'conditions': [{'path': 'sg_status_list',
            'active': 'true',
            'relation': 'is_not',
            'values': ['na']},
           {'path': 'sg_status_list',
            'active': 'true',
            'relation': 'is_not',
            'values': ['apr']}],
          'qb_multivalued_condition_subgroup': True,
          'active': 'true'}]}]}},
    'editable': False}},
  'visible': {'value': True, 'editable': True},
  'ui_value_displayable': {'value': True, 'editable': False}}}
"""




if __name__ == "__main__":


    def inspect_and_evaluate_query_field(entity_type, field_name):

        data = defaultdict(dict)
        data['field_name'] = field_name
        data['summary_default'] = sg.schema_field_read('Sequence', field_name)[field_name]['properties']['summary_default']['value']
        return data

        #print(sg.schema_field_read('Sequence', 'sg_ip_versions')['sg_ip_versions']


    for field_name in QUERY_FIELDS:
        pp(inspect_and_evaluate_query_field('Sequence', field_name))



    #dd(sg)

    #filters= [['project','is',{'type': 'Project','id': 85}]]
    #fields=["code", "sg_cut_duration", "sg_ip_versions"]
    #sequences = sg.find("Sequence", filters, fields)

    for sequence in sequences:
        pp(sequence)
        # {'code': 'SATL', 'id': 40, 'type': 'Sequence'}

        """Get shots"""
        filters = [['sg_sequence.Sequence.id', 'is', 40]]
        fields = ['code', 'sg_cut_duration']
        sequence_shots = sg.find("Shot", filters, fields)
        pp(sequence_shots)
        # [ {'code': '0500.0010', 'id': 1162, 'sg_cut_duration': 14, 'type': 'Shot'},
        #   {'code': '0500.0015', 'id': 1163, 'sg_cut_duration': 13, 'type': 'Shot'},
        #   {'code': '0500.0020', 'id': 1164, 'sg_cut_duration': 12, 'type': 'Shot'},
        #   {'code': '0500.0030', 'id': 1165, 'sg_cut_duration': 25, 'type': 'Shot'},
        #   {'code': '0500.0040', 'id': 1166, 'sg_cut_duration': 17, 'type': 'Shot'},
        #   {'code': '0500.0060', 'id': 1167, 'sg_cut_duration': 14, 'type': 'Shot'},
        #   {'code': '0500.0050', 'id': 1168, 'sg_cut_duration': 25, 'type': 'Shot'}]



