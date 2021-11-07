from typing import Union


def positive(value: Union[int, float]) -> Union[int, float]:
    """
    Returns the given number, but returns 0 if the value is negative
    """
    if value < 0:
        value = 0
    return value


def limit_speed(speed: float, max_speed: Union[int, float]) -> float:
    """
    Limits a value if it is over the given limit
    :param speed: Value that needs to be regulated
    :param max_speed: Maximal value
    :return speed: Modified speed
    """
    if abs(speed) > max_speed:
        if speed > 0:
            speed = max_speed
        else:
            speed = -max_speed
    return speed
