import unittest
from cc import tokenize, Parser


class TestCC(unittest.TestCase):
    def test_tokenize(self):
        code = """
        char main() {
            char a = 5;
            return a + 0x10;
        }
        """
        tokens = tokenize(code)
        expected = [
            ("TYPE", "char"),
            ("ID", "main"),
            ("LPAREN", "("),
            ("RPAREN", ")"),
            ("LBRACE", "{"),
            ("TYPE", "char"),
            ("ID", "a"),
            ("ASSIGN", "="),
            ("NUMBER", "5"),
            ("SEMICOLON", ";"),
            ("KEYWORD", "return"),
            ("ID", "a"),
            ("OP", "+"),
            ("NUMBER", "0x10"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
        ]
        self.assertEqual(tokens, expected)

    # parse_term tests

    def test_parse_term_identifier(self):
        code = "a"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_term()
        expected = {
            "node": "identifier",
            "value": "a",
        }
        self.assertEqual(node, expected)

    def test_parse_term_number(self):
        code = "5"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_term()
        expected = {
            "node": "number",
            "value": "5",
        }
        self.assertEqual(node, expected)

    def test_parse_term_function_call(self):
        code = "foo()"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_term()
        expected = {
            "node": "function_call",
            "name": "foo",
            "args": [],
        }
        self.assertEqual(node, expected)

    def test_parse_term_parentheses(self):
        code = "(a)"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_term()
        expected = {
            "node": "parentheses",
            "value": {
                "node": "identifier",
                "value": "a",
            },
        }
        self.assertEqual(node, expected)

    # parse_expression tests

    def test_parse_expression_single_term(self):
        code = "a"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_expression()
        expected = {
            "node": "identifier",
            "value": "a",
        }
        self.assertEqual(node, expected)

    def test_parse_expression_plus_2_terms(self):
        code = "a + 2"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_expression()
        expected = {
            "node": "binary_operator",
            "op": "+",
            "left": {
                "node": "identifier",
                "value": "a",
            },
            "right": {
                "node": "number",
                "value": "2",
            },
        }
        self.assertEqual(node, expected)

    def test_parse_expression_minus_2_terms(self):
        code = "a - 2"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_expression()
        expected = {
            "node": "binary_operator",
            "op": "-",
            "left": {
                "node": "identifier",
                "value": "a",
            },
            "right": {
                "node": "number",
                "value": "2",
            },
        }
        self.assertEqual(node, expected)

    def test_parse_expression_plus_3_terms(self):
        code = "a + 2 + c"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_expression()
        expected = {
            "node": "binary_operator",
            "op": "+",
            "left": {
                "node": "binary_operator",
                "op": "+",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "2",
                },
            },
            "right": {
                "node": "identifier",
                "value": "c",
            },
        }
        self.assertEqual(node, expected)

    def test_parse_expression_minus_3_terms(self):
        code = "a - 2 - c"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_expression()
        expected = {
            "node": "binary_operator",
            "op": "-",
            "left": {
                "node": "binary_operator",
                "op": "-",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "2",
                },
            },
            "right": {
                "node": "identifier",
                "value": "c",
            },
        }
        self.assertEqual(node, expected)

    def test_parse_expression_complex(self):
        code = "a + (2 - 1) + (main() + b)"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_expression()
        expected = {
            "node": "binary_operator",
            "op": "+",
            "left": {
                "node": "binary_operator",
                "op": "+",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "parentheses",
                    "value": {
                        "node": "binary_operator",
                        "op": "-",
                        "left": {
                            "node": "number",
                            "value": "2",
                        },
                        "right": {
                            "node": "number",
                            "value": "1",
                        },
                    },
                },
            },
            "right": {
                "node": "parentheses",
                "value": {
                    "node": "binary_operator",
                    "op": "+",
                    "left": {
                        "node": "function_call",
                        "name": "main",
                        "args": [],
                    },
                    "right": {
                        "node": "identifier",
                        "value": "b",
                    },
                },
            },
        }
        self.assertEqual(node, expected)

    # parse_block tests

    def test_parse_block_empty(self):
        code = "{ }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_block()
        expected = {
            "node": "block",
            "body": [],
        }
        self.assertEqual(node, expected)

    # parse_return_statement tests

    def test_parse_return_statement(self):
        code = "return a;"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_return_statement()
        expected = {
            "node": "return_statement",
            "value": {
                "node": "identifier",
                "value": "a",
            },
        }
        self.assertEqual(node, expected)

    # parse_arguments tests

    def test_parse_arguments_empty(self):
        code = "()"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_arguments()
        expected = []
        self.assertEqual(node, expected)

    def test_parse_arguments_single(self):
        code = "a"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_arguments()
        expected = [
            {
                "node": "identifier",
                "value": "a",
            }
        ]
        self.assertEqual(node, expected)

    def test_parse_arguments_double(self):
        code = "a, 2"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_arguments()
        expected = [
            {
                "node": "identifier",
                "value": "a",
            },
            {
                "node": "number",
                "value": "2",
            }
        ]
        self.assertEqual(node, expected)

    def test_parse_arguments_multiple(self):
        code = "a, 2 + 1, my_function()"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_arguments()
        expected = [
            {
                "node": "identifier",
                "value": "a",
            },
            {
                "node": "binary_operator",
                "op": "+",
                "left": {
                    "node": "number",
                    "value": "2",
                },
                "right": {
                    "node": "number",
                    "value": "1",
                },
            },
            {
                "node": "function_call",
                "name": "my_function",
                "args": [],
            },
        ]
        self.assertEqual(node, expected)
