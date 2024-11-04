#!/usr/bin/env python3

from pprint import pprint

def pp(data, title='', nl=0):
    """debug output util"""
    if title: print(f'{title}:')
    pprint(data, indent=2)
    for n in range(nl): print()


all_filters = [{ 'conditions': [ { 'conditions': [ { 'active': 'true',
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
            'logical_operator': 'and'},

           { 'conditions': [ { 'active': 'true',
                               'path': 'sg_sequence',
                               'relation': 'is',
                               'values': [ { 'id': 0,
                                             'name': 'Current '
                                                     'Sequence',
                                             'type': 'Sequence',
                                             'valid': 'parent_entity_token'}]}],
             'logical_operator': 'and'}]


def build_filters(filters):

    if 'path' in filters:
        return [filters['path'], filters['relation'], filters['values'][0]]
    else:
        if 'logical_operator' in filters:
            filter = {}
            filter['logical_operator'] = filters['logical_operator']
            filter['filters'] = []
            
            for sub_filter in filters['conditions']:
                filter['filters'].append(build_filters(sub_filter))
            return filter


for filters in all_filters:

    result = build_filters(filters)

    pp(result)

