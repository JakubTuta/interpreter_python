import dataclasses

PRECEDENCE = {
    "PLUS": 1,
    "MINUS": 1,
    "STAR": 2,
    "SLASH": 2,
}

BINARY_OP = {"PLUS": "+", "MINUS": "-", "STAR": "*", "SLASH": "/"}


@dataclasses.dataclass
class Expr:
    row: int | None
    col: int | None


@dataclasses.dataclass
class Literal(Expr):
    value: float | int


@dataclasses.dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr


@dataclasses.dataclass
class UnaryOp(Expr):
    op: str
    operand: Expr


class ParsingError(Exception):
    pass
