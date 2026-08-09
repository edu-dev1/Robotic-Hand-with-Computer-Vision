'''
Extra functions
'''
def mapping(var:int, range_var:tuple[int, int], new_range:tuple[int, int]) -> int:
    '''
    Convierte los valores del rango `range_var` a valores del `new_range` de manera proporsional.\n
    :param var: La variable que cambiará su valor.
    :type var: int
    :param range_var: Una tupla con el rango (inicio, fin) que toma la variable `var`.
    :type range_var: tuple[int, int]
    :param new_range: El nuevo rango donde se maperará el rango de la variable.
    :type new_range: tuple[int, int]
    '''
    in_min, in_max = range_var
    out_min, out_max = new_range

    value = (var - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    return int(value)
