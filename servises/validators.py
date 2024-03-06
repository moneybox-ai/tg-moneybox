from re import match


def is_number(string):
    '''Валидация что введенные данные число'''
    pattern = r'^[+-]?\d+(\.\d+)?$'
    return bool(match(pattern, string))
