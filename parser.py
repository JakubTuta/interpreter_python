import models


class Parser:
    def __init__(self):
        self._tokens = []
        self._position = 0

    def parse(self, tokens: list[models.lexer.Token]):
        self._tokens = tokens
        self._position = 0
        self._validate_tokens()

        expression = self._parse_expression()

        if self._tokens[self._position].type != "EOF":
            raise models.parser.ParsingError(
                f"Expression is incorrect. Tokens {self._tokens[self._position:]} are unparsed"
            )

        return expression

    def _parse_prefix(self) -> models.parser.Expr:
        token = self._tokens[self._position]

        if token.type == "NUMBER":
            self._position += 1
            return models.parser.Literal(token.row, token.col, token.value)

        if token.type == "MINUS":
            self._position += 1
            operand = self._parse_expression(3)
            return models.parser.UnaryOp(token.row, token.col, "-", operand)

        if token.type == "LPAREN":
            self._position += 1
            expression = self._parse_expression()

            if self._tokens[self._position].type != "RPAREN":
                raise models.parser.ParsingError(
                    f"Expected ')' at line {1}, column {self._position}"
                )

            self._position += 1
            return expression

        raise models.parser.ParsingError("Expected expression")

    def _parse_expression(self, min_precedence: int = 0) -> models.parser.Expr:
        left_expr = self._parse_prefix()

        while True:
            token = self._tokens[self._position]
            current_precedence = models.parser.PRECEDENCE.get(token.type, -1)

            if current_precedence < min_precedence:
                break

            if token.type not in models.parser.BINARY_OP:
                raise models.parser.ParsingError(f"Unexpected character: {token.type}")

            operator = models.parser.BINARY_OP[token.type]
            self._position += 1

            right_expr = self._parse_expression(current_precedence + 1)

            left_expr = models.parser.BinaryOp(
                token.row, token.col, left_expr, operator, right_expr
            )

        return left_expr

    def _validate_tokens(self):
        if len(self._tokens) == 0:
            raise models.parser.ParsingError("Token list is empty")

        if self._tokens[-1].type != "EOF":
            raise models.parser.ParsingError("Last token has to be EOF")
