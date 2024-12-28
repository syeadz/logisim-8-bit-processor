import unittest
from cc import CodeGenerator


class TestCCCodeGen(unittest.TestCase):
    def test_generate_number_code(self):
        node = {"name": "number", "value": "123"}
        gen = CodeGenerator(None)
        result = gen.generate_number_code(node)

        self.assertEqual(result, 4)
        self.assertEqual(gen.code, ["LWI $4, 123"])

    def test_generate_identifier_code(self):
        node = {"name": "identifier", "value": "foo"}
        gen = CodeGenerator(None)
        result = gen.generate_identifier_code(node)

        self.assertEqual(result, 4)

    def test_generate_declaration_code_no_assign(self):
        node = {
            "node": "declaration",
            "type": "char",
            "name": "a",
            "value": None,
        }

        gen = CodeGenerator(None)
        result = gen.generate_declaration_code(node)

        self.assertEqual(result, 4)

    def test_generate_declaration_simple_assign(self):
        node = {
            "node": "declaration",
            "type": "char",
            "name": "a",
            "value": {"node": "number", "value": "123"},
        }

        gen = CodeGenerator(None)
        result = gen.generate_declaration_code(node)

        self.assertEqual(result, 5)
        self.assertEqual(gen.code, ["LWI $4, 123", "MOV $5, $4"])

    def test_generate_assignment_code(self):
        node = {
            "node": "assignment",
            "left": {
                "node": "identifier",
                "value": "a",
            },
            "right": {
                "node": "number",
                "value": "123",
            },
        }
        gen = CodeGenerator(None)
        gen.get_free_reg("a")
        result = gen.generate_assignment_code(node)

        self.assertEqual(result, 4)
        self.assertEqual(gen.code, ["LWI $5, 123", "MOV $4, $5"])
