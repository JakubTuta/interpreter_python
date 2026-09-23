import models


class Evaluator:
    def evaluate(self, expression: models.parser.Expr):
        match expression:
            case models.parser.Literal(row, col, value):
                return value

            case models.parser.UnaryOp(row, col, op, operand):
                value = self.evaluate(operand)

                match op:
                    case "-":
                        return -value

                    case _:
                        raise models.evaluator.EvaluatorError(
                            f"Unsupported unary operator at line {row}, column {col}: {op}"
                        )

            case models.parser.BinaryOp(row, col, left, op, right):
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
                            raise models.evaluator.EvaluatorError(
                                f"Division by 0 at line {row}, column {col}"
                            )
                        return left_value / right_value

                    case _:
                        raise models.evaluator.EvaluatorError(
                            f"Unsupported binary operator at line {row}, column {col}: {op}"
                        )

            case _:
                raise models.evaluator.EvaluatorError(
                    f"Unsupported expression: {type(expression).__name__}"
                )
