from TypeEnforcer.Accepts import accepts
import typing


@accepts(typing.List[str])
def func(a: typing.List[str]):
    return a


func(["al", "bert"])
