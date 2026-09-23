import parser as parser_mod

import evaluator as evaluator_mod
import lexer as lexer_mod

lexer = lexer_mod.Lexer()
parser = parser_mod.Parser()
evaluator = evaluator_mod.Evaluator()

examples = [
    "1 + 2",
]

for example in examples:
    tokens = lexer.tokenize(example)
    expr = parser.parse(tokens)
    result = evaluator.evaluate(expr)
    print(f"{example}\n{tokens}\n{expr}\n{result}")
