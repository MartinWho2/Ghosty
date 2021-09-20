from typing import Union


def positive(value: Union[int, float]) -> Union[int, float]:
    if value < 0:
        value = 0
    return value


def limit_speed(speed: float, value: int) -> float:
    if abs(speed) > value:
        if speed > 0:
            speed = value
        else:
            speed = -value
    return speed
