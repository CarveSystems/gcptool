import pprint
import re
import requests

snekify = re.compile(r'(?<!^)(?=[A-Z])')

discovery_document = 'https://www.googleapis.com/discovery/v1/apis/compute/v1/rest'

r = requests.get(discovery_document)
schema = r.json()

gs = schema

pp = pprint.PrettyPrinter(indent=2, width=10000)

#pp.pprint(gs)

classes = {}

def capsfirst(s):
    if s:
        return s[0].upper() + s[1:]
    else:
        return ''

def generate_enum(name, type, values):
    if type == 'string':

        decls = []
        for value in values:
            value_name = value.title()

            if value_name in ['None', 'True', 'False']:
                value_name = value_name.upper()

            decls.append(f'    {value_name} = {repr(value)}')

        decls = '\n'.join(decls)
        data = f"""class {name}(enum.Enum):
{decls}
        """
        classes[name] = data
        print(data)


def get_type_name(t, propname = '', parent=''):
    if '$ref' in t:
        if t['$ref'] not in classes:
            generate_dataclass(schema['schemas'][t['$ref']])
        return t['$ref']
    elif t.get('type') == 'array':
        nested_name = get_type_name(t['items'], propname, parent)
        return f'List[{nested_name}]'
    elif t.get('enum'):
        name = f'{parent}{capsfirst(propname)}'
        if name not in classes:
            values = t.get('enum')
            element_type = t.get('type')
            generate_enum(name, element_type, values)
        return name
    elif t.get('type') == 'string':
        return 'str'
    elif t.get('type') == 'number':
        return 'float'
    elif t.get('type') == 'boolean':
        return 'bool'
    elif t.get('type') == 'integer':
        return 'int'
    elif t.get('type') == 'object':
        name = f'{parent}{capsfirst(propname)}'
        if name not in classes:
            generate_dataclass(t, name)
        return name
    else:
        print('!!! unknown')
        print(t)

def generate_dataclass(schema, id=None):
    if not id:
        id = schema['id']

    if id in classes:
        return

    classes[id] = ''

    properties = []

    for prop, value in schema.get('properties', {}).items():
        snek = snekify.sub('_', prop).lower() 
        if '$ref' in value:
            if value['$ref'] not in classes:
                generate_dataclass(gs['schemas'][value['$ref']])
            properties.append(f'    {snek}: {value["$ref"]}')
        elif value.get('type') == 'array':
            tn = get_type_name(value["items"], prop, id)
            properties.append(f'    {snek}: List[{tn}]')
        elif value.get('enum'):
            name = f'{id}{capsfirst(prop)}'
            if name not in classes:
                values = value.get('enum')
                element_type = value.get('type')
                generate_enum(name, element_type, values)
            properties.append(f'    {snek}: {name}')
        elif value.get('type') == 'string':
            properties.append(f'    {snek}: str')
        elif value.get('type') == 'boolean':
            properties.append(f'    {snek}: bool')
        elif value.get('type') == 'integer':
            properties.append(f'    {snek}: int')
        elif value.get('type') == 'number':
            properties.append(f'    {snek}: float')
        elif value.get('type') == 'object':
            name = f'{id}{capsfirst(prop)}'
            if name not in classes:
                generate_dataclass(value, name)
            properties.append(f'    {snek}: {name}')
        else:
            print('---')
            print(prop)
            print(value)

    if not properties: 
        output = f'{id} = dict'
        classes[id] = output
        print(output)
        return

    if schema.get('additionalProperties'):
        print('!!!')
        print(schema['additionalProperties'])

    props = '\n'.join(properties)
    output = f"""@dataclasses.dataclass
class {id}:
{props}

"""
    classes[id] = output
    print(output)


for n in ['Firewall', 'Instance', 'Address']:
    s = schema['schemas'][n]
    generate_dataclass(s)
