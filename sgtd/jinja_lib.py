
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


def generate_html(sgdata=None):

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')
    output_from_parsed_template = template.render(sgdata=sgdata)
    # debug html output
    #pp(output_from_parsed_template)

    # render the results to html file
    with open("output/index.html", "w") as fh:
        fh.write(output_from_parsed_template)
