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


class Lexer:
    def __init__(self):
        self._source = ""
        self._position = 0

    def tokenize(self, source: str) -> list[Token]:
        tokens = []
        self._source = source
        self._position = 0

        while self._position < len(self._source):
            char = self._source[self._position]

            if char in DIGITS:
                token = self._consume_number()
                tokens.append(token)
                continue

            elif char.isspace():
                pass

            elif char in OPERATOR_TYPES:
                tokens.append(Token(OPERATOR_TYPES[char], 1, self._position))

            else:
                raise LexicalError(
                    f"Incorrect character at line {1}, column {self._position}: {char}"
                )

            self._position += 1

        tokens.append(Token("EOF", None, None))
        return tokens

    def _consume_number(self) -> Token:
        index = self._position

        while index < len(self._source) and self._source[index] in DIGITS:
            index += 1

        if index < len(self._source) and self._source[index] == ".":
            decimal_index = index
            index += 1

            if index == len(self._source) or self._source[index] not in DIGITS:
                raise LexicalError(
                    f"Incorrect character at line {1}, column {decimal_index}: {self._source[decimal_index]}"
                )

            while index < len(self._source) and self._source[index] in DIGITS:
                index += 1

        if index < len(self._source) and not (
            self._source[index].isspace() or self._source[index] in OPERATOR_TYPES
        ):
            raise LexicalError(
                f"Incorrect character at line {1}, column {index}: {self._source[index]}"
            )

        number = self._cast_number(self._source[self._position : index])
        start = self._position
        self._position = index
        return Token("NUMBER", 1, start, number)

    def _cast_number(self, number: str) -> float | int:
        return float(number) if "." in number else int(number)
