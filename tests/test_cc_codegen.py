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
        gen.get_free_reg("foo")
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

    def test_generate_binary_operator_code_add(self):
        node = {
            "node": "binary_operator",
            "op": "+",
            "left": {
                "node": "number",
                "value": "123",
            },
            "right": {
                "node": "number",
                "value": "456",
            },
        }
        gen = CodeGenerator(None)
        result = gen.generate_binary_operator_code(node)

        self.assertEqual(result, 4)
        self.assertEqual(gen.code, ["LWI $4, 123", "LWI $5, 456", "ADD $4, $5"])

    def test_generate_binary_operator_code_subtract(self):
        node = {
            "node": "binary_operator",
            "op": "-",
            "left": {
                "node": "number",
                "value": "123",
            },
            "right": {
                "node": "number",
                "value": "456",
            },
        }
        gen = CodeGenerator(None)
        result = gen.generate_binary_operator_code(node)

        self.assertEqual(result, 4)
        self.assertEqual(gen.code, ["LWI $4, 123", "LWI $5, 456", "SUB $4, $5"])

    def test_generate_binary_operator_code_less_than(self):
        node = {
            "node": "binary_operator",
            "op": "<",
            "left": {
                "node": "number",
                "value": "123",
            },
            "right": {
                "node": "number",
                "value": "255",
            },
        }
        gen = CodeGenerator(None)
        result = gen.generate_binary_operator_code(node)

        self.assertEqual(result, 4)
        self.assertEqual(
            gen.code,
            [
                "LWI $4, 123",
                "LWI $5, 255",
                "CMP $4, $5",
                "JPNC skip_set_1",
                "MOV $4, $1",
                "skip_set_1:",
            ],
        )

    def test_generate_binary_operator_code_greater_than(self):
        node = {
            "node": "binary_operator",
            "op": ">",
            "left": {
                "node": "number",
                "value": "123",
            },
            "right": {
                "node": "number",
                "value": "255",
            },
        }
        gen = CodeGenerator(None)
        result = gen.generate_binary_operator_code(node)

        self.assertEqual(result, 4)
        self.assertEqual(
            gen.code,
            [
                "LWI $4, 123",
                "LWI $5, 255",
                "CMP $4, $5",
                "JPC skip_set_1",
                "MOV $4, $1",
                "skip_set_1:",
            ],
        )

    def test_generate_function_code(self):
        node = {
            "node": "function",
            "name": "main",
            "body": [
                {
                    "node": "declaration",
                    "type": "char",
                    "name": "a",
                    "value": {"node": "number", "value": "123"},
                },
            ],
        }
        gen = CodeGenerator(None)
        gen.generate_function_code(node)

        self.assertEqual(gen.code, ["main:", "LWI $4, 123", "MOV $5, $4", "HALT"])

    def test_generate_program_code(self):
        node = {
            "node": "program",
            "functions": [
                {
                    "node": "function",
                    "name": "main",
                    "body": [
                        {
                            "node": "declaration",
                            "type": "char",
                            "name": "a",
                            "value": {"node": "number", "value": "123"},
                        },
                    ],
                },
            ],
        }
        gen = CodeGenerator(node)
        gen.generate_program_code()

        self.assertEqual(gen.code, ["main:", "LWI $4, 123", "MOV $5, $4", "HALT"])

    def test_generate_if_statement_code_identifier(self):
        node = {
            "node": "if_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [
                {
                    "node": "declaration",
                    "type": "char",
                    "name": "b",
                    "value": {"node": "number", "value": "1"},
                },
            ],
            "else_body": None,
        }
        gen = CodeGenerator(None)
        gen.get_free_reg("a")
        gen.generate_if_statement_code(node)

        self.assertEqual(
            gen.code,
            [
                "if_1:",
                "CMP $4, $1",
                "JPNZ end_if_1",
                "LWI $5, 1",
                "MOV $6, $5",
                "end_if_1:",
            ],
        )

    def test_generate_if_statement_code_less_than(self):
        node = {
            "node": "if_statement",
            "condition": {
                "node": "binary_operator",
                "op": "<",
                "left": {
                    "node": "number",
                    "value": "123",
                },
                "right": {
                    "node": "number",
                    "value": "255",
                },
            },
            "body": [
                {
                    "node": "declaration",
                    "type": "char",
                    "name": "b",
                    "value": {"node": "number", "value": "1"},
                },
            ],
            "else_body": None,
        }
        gen = CodeGenerator(None)
        gen.generate_if_statement_code(node)

        self.assertEqual(
            gen.code,
            [
                "if_1:",
                "LWI $4, 123",
                "LWI $5, 255",
                "CMP $4, $5",
                "JPNC skip_set_2",
                "MOV $4, $1",
                "skip_set_2:",
                "CMP $4, $1",
                "JPNZ end_if_1",
                "LWI $4, 1",
                "MOV $5, $4",
                "end_if_1:",
            ],
        )

    def test_generate_while_statement_code_identifier(self):
        node = {
            "node": "while_statement",
            "condition": {
                "node": "identifier",
                "value": "a",
            },
            "body": [
                {
                    "node": "declaration",
                    "type": "char",
                    "name": "b",
                    "value": {"node": "number", "value": "1"},
                },
            ],
        }
        gen = CodeGenerator(None)
        gen.get_free_reg("a")
        gen.generate_while_statement_code(node)

        self.assertEqual(
            gen.code,
            [
                "while_1:",
                "CMP $4, $1",
                "JPNZ end_while_1",
                "LWI $5, 1",
                "MOV $6, $5",
                "GOTO while_1",
                "end_while_1:",
            ],
        )