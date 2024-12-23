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
        expected = []
        self.assertEqual(node, expected)

    def test_parse_block_single_statement(self):
        code = "{ a = 5; }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_block()
        expected = [
            {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "5",
                },
            }
        ]
        self.assertEqual(node, expected)

    # this test might be too long
    def test_parse_block_complex(self):
        code = """
        {
            char a = 5;
            char b;
            char b = a + 2;
            my_function();
            if (a) { }
            while (b) { }
            for (a = 0; a < 5; a = a + 1) { }
            {}
            return a;
        }
        """
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_block()
        expected = [
            {
                "node": "declaration",
                "type": "char",
                "name": "a",
                "value": {
                    "node": "number",
                    "value": "5",
                },
            },
            {
                "node": "declaration",
                "type": "char",
                "name": "b",
                "value": None,
            },
            {
                "node": "declaration",
                "type": "char",
                "name": "b",
                "value": {
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
            },
            {
                "node": "function_call",
                "name": "my_function",
                "args": [],
            },
            {
                "node": "if_statement",
                "condition": {
                    "node": "identifier",
                    "value": "a",
                },
                "body": [],
                "else_body": None,
            },
            {
                "node": "while_statement",
                "condition": {
                    "node": "identifier",
                    "value": "b",
                },
                "body": [],
            },
            {
                "node": "for_statement",
                "init": {
                    "node": "assignment",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "0",
                    },
                },
                "condition": {
                    "node": "binary_operator",
                    "op": "<",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "5",
                    },
                },
                "update": {
                    "node": "assignment",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "binary_operator",
                        "op": "+",
                        "left": {
                            "node": "identifier",
                            "value": "a",
                        },
                        "right": {
                            "node": "number",
                            "value": "1",
                        },
                    },
                },
                "body": [],
            },
            [],
            {
                "node": "return_statement",
                "value": {
                    "node": "identifier",
                    "value": "a",
                },
            },
        ]
        self.assertEqual(node, expected)

    # parse_for_statement tests

    def test_parse_for_statement(self):
        code = "for (a = 0; a < 5; a = a + 1) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_for_statement()
        expected = {
            "node": "for_statement",
            "init": {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "0",
                },
            },
            "condition": {
                "node": "binary_operator",
                "op": "<",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "5",
                },
            },
            "update": {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "binary_operator",
                    "op": "+",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "1",
                    },
                },
            },
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_for_statement_decl_init(self):
        code = "for (char a = 0; a < 5; a = a + 1) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_for_statement()
        expected = {
            "node": "for_statement",
            "init": {
                "node": "declaration",
                "type": "char",
                "name": "a",
                "value": {
                    "node": "number",
                    "value": "0",
                },
            },
            "condition": {
                "node": "binary_operator",
                "op": "<",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "5",
                },
            },
            "update": {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "binary_operator",
                    "op": "+",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "1",
                    },
                },
            },
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_for_statement_body(self):
        code = "for (a = 0; a < 5; a = a + 1) { a = 5; }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_for_statement()
        expected = {
            "node": "for_statement",
            "init": {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "0",
                },
            },
            "condition": {
                "node": "binary_operator",
                "op": "<",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "5",
                },
            },
            "update": {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "binary_operator",
                    "op": "+",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "1",
                    },
                },
            },
            "body": [
                {
                    "node": "assignment",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "5",
                    },
                }
            ],
        }
        self.assertEqual(node, expected)

    # parse_while_statement tests

    def test_parse_while_statement(self):
        code = "while (a) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_while_statement()
        expected = {
            "node": "while_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_while_statement_expr(self):
        code = "while (a < 2) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_while_statement()
        expected = {
            "node": "while_statement",
            "condition": {
                "node": "binary_operator",
                "op": "<",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "2",
                },
            },
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_while_statement_body(self):
        code = "while (a) { a = 5; }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_while_statement()
        expected = {
            "node": "while_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [
                {
                    "node": "assignment",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "5",
                    },
                }
            ],
        }
        self.assertEqual(node, expected)

    # parse_if_statement tests

    def test_parse_if_statement(self):
        code = "if (a) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_if_statement()
        expected = {
            "node": "if_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [],
            "else_body": None,
        }
        self.assertEqual(node, expected)

    def test_parse_if_statement_else(self):
        code = "if (a) { } else { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_if_statement()
        expected = {
            "node": "if_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [],
            "else_body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_if_statement_expr(self):
        code = "if (a < 2) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_if_statement()
        expected = {
            "node": "if_statement",
            "condition": {
                "node": "binary_operator",
                "op": "<",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "2",
                },
            },
            "body": [],
            "else_body": None,
        }
        self.assertEqual(node, expected)

    def test_parse_if_statement_body(self):
        code = "if (a) { a = 5; }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_if_statement()
        expected = {
            "node": "if_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [
                {
                    "node": "assignment",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "5",
                    },
                }
            ],
            "else_body": None,
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
        code = ""
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
            },
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

    # parse_function_call tests

    def test_parse_function_call_no_args(self):
        code = "my_function()"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_function_call()
        expected = {
            "node": "function_call",
            "name": "my_function",
            "args": [],
        }
        self.assertEqual(node, expected)

    def test_parse_function_call_single_arg(self):
        code = "my_function(a)"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_function_call()
        expected = {
            "node": "function_call",
            "name": "my_function",
            "args": [
                {
                    "node": "identifier",
                    "value": "a",
                }
            ],
        }
        self.assertEqual(node, expected)

    def test_parse_function_call_multiple_args(self):
        code = "my_function(a, 2, b + 1)"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_function_call()
        expected = {
            "node": "function_call",
            "name": "my_function",
            "args": [
                {
                    "node": "identifier",
                    "value": "a",
                },
                {
                    "node": "number",
                    "value": "2",
                },
                {
                    "node": "binary_operator",
                    "op": "+",
                    "left": {
                        "node": "identifier",
                        "value": "b",
                    },
                    "right": {
                        "node": "number",
                        "value": "1",
                    },
                },
            ],
        }
        self.assertEqual(node, expected)

    # parse_assignment tests

    def test_parse_assignment(self):
        code = "a = 5"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_assignment()
        expected = {
            "node": "assignment",
            "left": {
                "node": "identifier",
                "value": "a",
            },
            "right": {
                "node": "number",
                "value": "5",
            },
        }

    def test_parse_assignment_expression(self):
        code = "a = a + 2"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_assignment()
        expected = {
            "node": "assignment",
            "left": {
                "node": "identifier",
                "value": "a",
            },
            "right": {
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
        }
        self.assertEqual(node, expected)

    # parse_declaration tests

    def test_parse_declaration_no_assign(self):
        code = "char a"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_declaration()
        expected = {
            "node": "declaration",
            "type": "char",
            "name": "a",
            "value": None,
        }
        self.assertEqual(node, expected)

    def test_parse_declaration_assign_num(self):
        code = "char a = 5"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_declaration()
        expected = {
            "node": "declaration",
            "type": "char",
            "name": "a",
            "value": {
                "node": "number",
                "value": "5",
            },
        }
        self.assertEqual(node, expected)

    def test_parse_declaration_assign_expr(self):
        code = "char b = a + 2"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_declaration()
        expected = {
            "node": "declaration",
            "type": "char",
            "name": "b",
            "value": {
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
        }
        self.assertEqual(node, expected)

    # parse_statement tests

    def test_parse_statement_declaration(self):
        code = "char a;"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "declaration",
            "type": "char",
            "name": "a",
            "value": None,
        }
        self.assertEqual(node, expected)

    def test_parse_statement_assignment(self):
        code = "a = 5;"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "assignment",
            "left": {
                "node": "identifier",
                "value": "a",
            },
            "right": {
                "node": "number",
                "value": "5",
            },
        }
        self.assertEqual(node, expected)

    def test_parse_statement_function_call(self):
        code = "foo();"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "function_call",
            "name": "foo",
            "args": [],
        }
        self.assertEqual(node, expected)

    def test_parse_statement_if_statemenet(self):
        code = "if (a) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "if_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [],
            "else_body": None,
        }
        self.assertEqual(node, expected)

    def test_parse_statement_if_else_statemenet(self):
        code = "if (a) { } else { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "if_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [],
            "else_body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_statement_for_statement(self):
        code = "for (a = 0; a < 5; a = a + 1) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "for_statement",
            "init": {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "0",
                },
            },
            "condition": {
                "node": "binary_operator",
                "op": "<",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "number",
                    "value": "5",
                },
            },
            "update": {
                "node": "assignment",
                "left": {
                    "node": "identifier",
                    "value": "a",
                },
                "right": {
                    "node": "binary_operator",
                    "op": "+",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "1",
                    },
                },
            },
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_statement_while_statement(self):
        code = "while (a) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "while_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_statement_return_statement(self):
        code = "return a;"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = {
            "node": "return_statement",
            "value": {
                "node": "identifier",
                "value": "a",
            },
        }
        self.assertEqual(node, expected)

    def test_parse_statement_block(self):
        code = "{ }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_statement()
        expected = []
        self.assertEqual(node, expected)

    # parse_parameters tests

    def test_parse_parameters_single(self):
        code = "char a"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_parameters()
        expected = [
            {
                "node": "parameter",
                "type": "char",
                "name": "a",
            }
        ]
        self.assertEqual(node, expected)

    def test_parse_parameters_multiple(self):
        code = "char a, int b"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_parameters()
        expected = [
            {
                "node": "parameter",
                "type": "char",
                "name": "a",
            },
            {
                "node": "parameter",
                "type": "int",
                "name": "b",
            },
        ]
        self.assertEqual(node, expected)

    # parse_function tests

    def test_parse_function_no_args(self):
        code = "char main() { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_function()
        expected = {
            "node": "function",
            "type": "char",
            "name": "main",
            "params": [],
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_function_single_arg(self):
        code = "char main(int a) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_function()
        expected = {
            "node": "function",
            "type": "char",
            "name": "main",
            "params": [
                {
                    "node": "parameter",
                    "type": "int",
                    "name": "a",
                }
            ],
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_function_multiple_args(self):
        code = "char main(int a, char b) { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_function()
        expected = {
            "node": "function",
            "type": "char",
            "name": "main",
            "params": [
                {
                    "node": "parameter",
                    "type": "int",
                    "name": "a",
                },
                {
                    "node": "parameter",
                    "type": "char",
                    "name": "b",
                },
            ],
            "body": [],
        }
        self.assertEqual(node, expected)

    def test_parse_function_body(self):
        code = "char main() { a = 5; }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_function()
        expected = {
            "node": "function",
            "type": "char",
            "name": "main",
            "params": [],
            "body": [
                {
                    "node": "assignment",
                    "left": {
                        "node": "identifier",
                        "value": "a",
                    },
                    "right": {
                        "node": "number",
                        "value": "5",
                    },
                }
            ],
        }
        self.assertEqual(node, expected)

    # parse_program tests

    def test_parse_program_single_function(self):
        code = "char main() { }"
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_program()
        expected = {
            "node": "program",
            "functions": [
                {
                    "node": "function",
                    "type": "char",
                    "name": "main",
                    "params": [],
                    "body": [],
                }
            ],
        }

        self.assertEqual(node, expected)

    def test_parse_program_multiple_functions(self):
        code = """
        char main() { }
        int foo() { }
        """
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_program()
        expected = {
            "node": "program",
            "functions": [
                {
                    "node": "function",
                    "type": "char",
                    "name": "main",
                    "params": [],
                    "body": [],
                },
                {
                    "node": "function",
                    "type": "int",
                    "name": "foo",
                    "params": [],
                    "body": [],
                },
            ],
        }
        self.assertEqual(node, expected)

    def test_parse_program_complex(self):
        code = """
        char main() {
            char a = 5;
            char b;
            char b = a + 2;
            my_function();
            if (a) { }
            while (b) { }
            for (a = 0; a < 5; a = a + 1) { }
            {}
            return a;
        }
        """
        tokens = tokenize(code)
        parser = Parser(tokens)
        node = parser.parse_program()
        expected = {
            "node": "program",
            "functions": [
                {
                    "node": "function",
                    "type": "char",
                    "name": "main",
                    "params": [],
                    "body": [
                        {
                            "node": "declaration",
                            "type": "char",
                            "name": "a",
                            "value": {
                                "node": "number",
                                "value": "5",
                            },
                        },
                        {
                            "node": "declaration",
                            "type": "char",
                            "name": "b",
                            "value": None,
                        },
                        {
                            "node": "declaration",
                            "type": "char",
                            "name": "b",
                            "value": {
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
                        },
                        {
                            "node": "function_call",
                            "name": "my_function",
                            "args": [],
                        },
                        {
                            "node": "if_statement",
                            "condition": {
                                "node": "identifier",
                                "value": "a",
                            },
                            "body": [],
                            "else_body": None,
                        },
                        {
                            "node": "while_statement",
                            "condition": {
                                "node": "identifier",
                                "value": "b",
                            },
                            "body": [],
                        },
                        {
                            "node": "for_statement",
                            "init": {
                                "node": "assignment",
                                "left": {
                                    "node": "identifier",
                                    "value": "a",
                                },
                                "right": {
                                    "node": "number",
                                    "value": "0",
                                },
                            },
                            "condition": {
                                "node": "binary_operator",
                                "op": "<",
                                "left": {
                                    "node": "identifier",
                                    "value": "a",
                                },
                                "right": {
                                    "node": "number",
                                    "value": "5",
                                },
                            },
                            "update": {
                                "node": "assignment",
                                "left": {
                                    "node": "identifier",
                                    "value": "a",
                                },
                                "right": {
                                    "node": "binary_operator",
                                    "op": "+",
                                    "left": {
                                        "node": "identifier",
                                        "value": "a",
                                    },
                                    "right": {
                                        "node": "number",
                                        "value": "1",
                                    },
                                },
                            },
                            "body": [],
                        },
                        [],
                        {
                            "node": "return_statement",
                            "value": {
                                "node": "identifier",
                                "value": "a",
                            },
                        },
                    ],
                }
            ],
        }
        self.assertEqual(node, expected)
