# Laika SG TD - Solution

## Setup

1. Create and source virtualenv

```bash
% python -V
Python 3.9.18

python -m venv venv
source venv/bin/activate
```

2. Install Python libraries
```bash
make install
```


3. Run main.py and view output/index.html in a browser (on a Mac)
```bash
./main.py && open output/index.html
```

## HTML Output

![Screenshot 2024-11-04 at 2 17 55 PM](https://github.com/user-attachments/assets/2d822827-f735-40e4-bfa3-071ec3a4c5cd)

## Console Output

```bash
% ./main.py && open output/index.html                                                                       [main] laika_sg_td
Sequence:
{'code': 'SATL', 'id': 40, 'type': 'Sequence'}

'----------------------------------------------------------------------'

query_field_name:
'sg_cut_duration'

new_filters:
[['sg_sequence', 'is', {'code': 'SATL', 'id': 40, 'type': 'Sequence'}]]

'----------------------------------------------------------------------'

query_field_name:
'sg_ip_versions'

new_filters:
[ { 'filter_operator': 'or',
    'filters': [ [ 'entity',
                   'is',
                   {'code': 'SATL', 'id': 40, 'type': 'Sequence'}],
                 [ 'entity.Shot.sg_sequence',
                   'is',
                   {'code': 'SATL', 'id': 40, 'type': 'Sequence'}]]},
  { 'filter_operator': 'and',
    'filters': [ { 'filter_operator': 'and',
                   'filters': [ ['sg_status_list', 'is_not', 'na'],
                                ['sg_status_list', 'is_not', 'apr']]}]}]

'----------------------------------------------------------------------'

results:
[ { 'data': [ { 'query_field': 'sg_cut_duration',
                'type': 'Average',
                'value': 17.1429},
              { 'query_field': 'sg_ip_versions',
                'type': 'Record Count',
                'value': 11}],
    'id': 40,
    'name': 'SATL',
    'type': 'Sequence'}]
```

## run pylint

```bash
% make lint                                                                                                 [main] laika_sg_td
pylint --disable=R,C main

-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 9.66/10, +0.34)
```
