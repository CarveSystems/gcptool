from typing import Union, Type, TypeVar, Any
import typing
import dataclasses

def camel(s: str) -> str:
    out = ''

    upper_next = False
    for c in s:
        if c == '_':
            upper_next = True
        else:
            if upper_next:
                c = c.upper()
                upper_next = False
            out += c
    
    return out

T = TypeVar('T')

def parse_field(value: Any, field_type: Type[T]) -> T:
    if typing.get_origin(field_type) == Union:
        for possible_type in typing.get_args(field_type):
            try:
                value = parse_field(value, possible_type)
                break
            except:
                pass
        else:
            raise ValueError(f'Failed to parse {value} as {field_type}')

        return value

    elif typing.get_origin(field_type) == list:
        element_type = typing.get_args(field_type)[0]

        elements = [parse_field(element, element_type) for element in value]
        return elements

    elif dataclasses.is_dataclass(field_type):
        return parse_dataclass(value, field_type)

    else:
        return field_type(value)


def parse_dataclass(item: Any, dclass):
    dc_fields = dataclasses.fields(dclass)

    all_keys = set(item.keys())

    kwargs = {}

    for field in dc_fields:
        if not field.init:
            continue

        json_name = camel(field.name)
        json_value = item.get(json_name, ...)

        if json_name in all_keys:
            all_keys.remove(json_name)

        if json_value == ...:
            if field.default:
                value = field.default
            elif field.default_factory:
                value = field.default_factory()
            else:
                value = parse_field(None, field.type)
        else:
            value = parse_field(json_value, field.type)


        if isinstance(value, dataclasses._MISSING_TYPE):
            value = None

        kwargs[field.name] = value

    if len(all_keys):
        print(f'Warning: extra keys in {dclass}: {all_keys}')

    return dclass(**kwargs)
