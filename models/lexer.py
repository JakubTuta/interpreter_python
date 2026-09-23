import dataclasses
import typing

TYPES = typing.Literal[
    "NUMBER",
    "PLUS",
    "MINUS",
    "STAR",
    "SLASH",
    "LPAREN",
    "RPAREN",
    "EOF",
]

DIGITS = "0123456789"

OPERATOR_TYPES: dict[str, TYPES] = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "(": "LPAREN",
    ")": "RPAREN",
}


@dataclasses.dataclass
class Token:
    type: TYPES
    row: int | None
    col: int | None
    value: int | float | None = None


class LexicalError(Exception):
    pass
