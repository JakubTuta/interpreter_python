import parser


class EvaluatorError(Exception):
    pass


class Evaluator:
    def evaluate(self, expression: parser.Expr):
        match expression:
            case parser.Literal(row, col, value):
                return value

            case parser.UnaryOp(row, col, op, operand):
                value = self.evaluate(operand)

                match op:
                    case "-":
                        return -value

                    case _:
                        raise EvaluatorError(
                            f"Unsupported unary operator at line {row}, column {col}: {op}"
                        )

            case parser.BinaryOp(row, col, left, op, right):
                left_value = self.evaluate(left)
                right_value = self.evaluate(right)

                match op:
                    case "+":
                        return left_value + right_value

                    case "-":
                        return left_value - right_value

                    case "*":
                        return left_value * right_value

                    case "/":
                        if right_value == 0:
                            raise EvaluatorError(
                                f"Division by 0 at line {row}, column {col}"
                            )
                        return left_value / right_value

                    case _:
                        raise EvaluatorError(
                            f"Unsupported binary operator at line {row}, column {col}: {op}"
                        )

            case _:
                raise EvaluatorError(
                    f"Unsupported expression: {type(expression).__name__}"
                )
