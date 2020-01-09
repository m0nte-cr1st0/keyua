# Django imports
from django.template import loader


def generate_html(data, template_name):
    template = loader.get_template(template_name)
    return template.render({'data': data})