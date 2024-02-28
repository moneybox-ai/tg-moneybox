from re import match


def is_number(string):
    pattern = r'^[+-]?\d+(\.\d+)?$'
    return bool(match(pattern, string))
