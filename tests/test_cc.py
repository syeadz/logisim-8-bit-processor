import unittest
from cc import tokenize


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
            ("KEYWORD", "char"),
            ("IDENTIFIER", "main"),
            ("LPAREN", "("),
            ("RPAREN", ")"),
            ("LBRACE", "{"),
            ("KEYWORD", "char"),
            ("IDENTIFIER", "a"),
            ("ASSIGN", "="),
            ("NUMBER", "5"),
            ("SEMICOLON", ";"),
            ("KEYWORD", "return"),
            ("IDENTIFIER", "a"),
            ("OP", "+"),
            ("NUMBER", "0x10"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
        ]
        self.assertEqual(tokens, expected)
