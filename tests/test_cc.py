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
            ("PUNCTUATOR", "("),
            ("PUNCTUATOR", ")"),
            ("PUNCTUATOR", "{"),
            ("KEYWORD", "char"),
            ("IDENTIFIER", "a"),
            ("PUNCTUATOR", "="),
            ("CONSTANT", "5"),
            ("PUNCTUATOR", ";"),
            ("KEYWORD", "return"),
            ("IDENTIFIER", "a"),
            ("PUNCTUATOR", "+"),
            ("CONSTANT", "0x10"),
            ("PUNCTUATOR", ";"),
            ("PUNCTUATOR", "}"),
        ]
        self.assertEqual(tokens, expected)
