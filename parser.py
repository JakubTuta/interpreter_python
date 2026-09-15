import dataclasses

import lexer

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


class Parser:
    def __init__(self):
        self._tokens = []
        self._position = 0

    def parse(self, tokens: list[lexer.Token]):
        self._tokens = tokens
        self._position = 0
        self._validate_tokens()

        expression = self._parse_expression()

        if self._tokens[self._position].type != "EOF":
            raise ParsingError(
                f"Expression is incorrect. Tokens {self._tokens[self._position:]} are unparsed"
            )

        return expression

    def _parse_prefix(self) -> Expr:
        token = self._tokens[self._position]

        if token.type == "NUMBER":
            self._position += 1
            return Literal(token.row, token.col, token.value)

        if token.type == "MINUS":
            self._position += 1
            operand = self._parse_expression(3)
            return UnaryOp(token.row, token.col, "-", operand)

        if token.type == "LPAREN":
            self._position += 1
            expression = self._parse_expression()

            if self._tokens[self._position].type != "RPAREN":
                raise ParsingError(f"Expected ')' at line {1}, column {self._position}")

            self._position += 1
            return expression

        raise ParsingError("Expected expression")

    def _parse_expression(self, min_precedence: int = 0) -> Expr:
        left_expr = self._parse_prefix()

        while True:
            token = self._tokens[self._position]
            current_precedence = PRECEDENCE.get(token.type, -1)

            if current_precedence < min_precedence:
                break

            if token.type not in BINARY_OP:
                raise ParsingError(f"Unexpected character: {token.type}")

            operator = BINARY_OP[token.type]
            self._position += 1

            right_expr = self._parse_expression(current_precedence + 1)

            left_expr = BinaryOp(token.row, token.col, left_expr, operator, right_expr)

        return left_expr

    def _validate_tokens(self):
        if len(self._tokens) == 0:
            raise ParsingError("Token list is empty")

        if self._tokens[-1].type != "EOF":
            raise ParsingError("Last token has to be EOF")
