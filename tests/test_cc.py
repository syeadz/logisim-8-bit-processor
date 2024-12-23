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
