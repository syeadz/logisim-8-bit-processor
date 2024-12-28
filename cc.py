import re
import sys

# Define token types
TOKENS = [
    ("KEYWORD", r"\b(break|continue|if|else|for|while|return)\b"),
    ("TYPE", r"\b(int|char|void)\b"),
    ("ID", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("NUMBER", r"\b0[bB][01]+|0[oO][0-7]+|0[xX][0-9a-fA-F]+|\d+\b"),
    ("OP", r"[+\-<>]|==|!="),
    ("ASSIGN", r"="),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("STRING_LITERAL", r'"[^"]*"'),
    ("WHITESPACE", r"\s+"),
    ("SINGLE_COMMENT", r"//.*"),
    ("MULTI_COMMENT", r"/\*.*?\*/"),
]


def tokenize(code):
    """
    Tokenize the given C code.
    """
    tokens = []
    while code:
        for token_type, regex in TOKENS:
            match = re.match(regex, code)
            if match:
                if token_type not in ["WHITESPACE", "SINGLE_COMMENT", "MULTI_COMMENT"]:
                    tokens.append((token_type, match.group(0)))
                code = code[match.end() :]
                break
        else:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ast = []
        self.pos = 0

    def peek(self):
        """
        Return the next token without consuming it, or None if there are no more tokens.
        """
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek_next(self):
        """
        Return the token after the next token without consuming it, or None if there are no more tokens.
        """
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None

    def peek_at(self, at):
        """
        Return the nth token without consuming it, or None if there are no more tokens.
        """
        return self.tokens[self.pos + at] if self.pos + at < len(self.tokens) else None

    def consume(self, token_type, token_value=None):
        """
        Consume the next token if it matches the given type and value.
        """
        token = self.peek()
        if (
            token
            and token[0] == token_type
            and (token_value is None or token[1] == token_value)
        ):
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected ({token_type}, {token_value}) but got {token}")

    def parse_program(self):
        """
        <program> = <function>+
        """
        functions = []
        while self.peek():
            functions.append(self.parse_function())
        return {
            "node": "program",
            "functions": functions,
        }

    def parse_function(self):
        """
        <function> = <type> <identifier> "(" <parameters>? ")" "{" <statement>* "}"
        """
        type_ = self.consume("TYPE")[1]
        name = self.consume("ID")[1]
        self.consume("LPAREN")
        params = []
        if self.peek()[1] != ")":
            params = self.parse_parameters()
        self.consume("RPAREN")
        body = self.parse_block()
        return {
            "node": "function",
            "type": type_,
            "name": name,
            "params": params,
            "body": body,
        }

    def parse_parameters(self):
        """
        <parameters> = <type> <identifier> ("," <type> <identifier)*
        """
        params = []
        params.append(
            {
                "node": "parameter",
                "type": self.consume("TYPE")[1],
                "name": self.consume("ID")[1],
            }
        )
        while self.peek() and self.peek()[1] == ",":
            self.consume("COMMA")
            params.append(
                {
                    "node": "parameter",
                    "type": self.consume("TYPE")[1],
                    "name": self.consume("ID")[1],
                }
            )
        return params

    def parse_statement(self):
        """
        <statement> = <declaration> ";"
                    | <assignment> ";"
                    | <function_call> ";"
                    | <if_statement>
                    | <for_statement>
                    | <while_statement>
                    | <return_statement> ";"
                    | <block>
        """
        if self.peek()[0] == "TYPE":
            val = self.parse_declaration()
            self.consume("SEMICOLON")
            return val
        elif self.peek()[0] == "ID" and self.peek_next()[1] == "=":
            val = self.parse_assignment()
            self.consume("SEMICOLON")
            return val
        elif self.peek()[0] == "KEYWORD" and self.peek()[1] == "if":
            return self.parse_if_statement()
        elif self.peek()[0] == "KEYWORD" and self.peek()[1] == "while":
            return self.parse_while_statement()
        elif self.peek()[0] == "KEYWORD" and self.peek()[1] == "for":
            return self.parse_for_statement()
        elif self.peek()[0] == "ID" and self.peek_next()[1] == "(":
            val = self.parse_function_call()
            self.consume("SEMICOLON")
            return val
        elif self.peek()[0] == "KEYWORD" and self.peek()[1] == "return":
            val = self.parse_return_statement()
            self.consume("SEMICOLON")
            return val
        elif self.peek()[0] == "LBRACE":
            return self.parse_block()
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")

    def parse_declaration(self):
        """
        <declaration> = <type> <identifier> ("=" <expression>)?
        """
        type_ = self.consume("TYPE")[1]
        name = self.consume("ID")[1]
        value = None
        if self.peek() and self.peek()[1] == "=":
            self.consume("ASSIGN")
            value = self.parse_expression()
        return {
            "node": "declaration",
            "type": type_,
            "name": name,
            "value": value,
        }

    def parse_assignment(self):
        """
        <assignment> = <identifier> "=" <expression>
        """
        name = self.consume("ID")[1]
        self.consume("ASSIGN")
        value = self.parse_expression()
        return {
            "node": "assignment",
            "left": {
                "node": "identifier",
                "value": name,
            },
            "right": value,
        }

    def parse_function_call(self):
        """
        <function_call> = <identifier> "(" <arguments>? ")"
        """
        name = self.consume("ID")[1]
        self.consume("LPAREN")
        args = []
        if self.peek()[1] != ")":
            args = self.parse_arguments()
        self.consume("RPAREN")
        return {
            "node": "function_call",
            "name": name,
            "args": args,
        }

    def parse_arguments(self):
        """
        <arguments> = <expression> ("," <expression>)*
        """
        if not self.peek():
            return []
        args = [self.parse_expression()]
        while self.peek() and self.peek()[0] == "COMMA":
            self.consume("COMMA")
            args.append(self.parse_expression())
        return args

    def parse_return_statement(self):
        """
        <return_statement> = "return" <expression>?
        """
        self.consume("KEYWORD", "return")
        value = None
        if self.peek()[1] != ";":
            value = self.parse_expression()
        return {
            "node": "return_statement",
            "value": value,
        }

    def parse_if_statement(self):
        """
        <if_statement> = "if" "(" <expression> ")" <block> ("else" <block>)?
        """
        self.consume("KEYWORD", "if")
        self.consume("LPAREN")
        condition = self.parse_expression()
        self.consume("RPAREN")
        body = self.parse_block()
        else_body = None
        if self.peek() and self.peek()[1] == "else":
            self.consume("KEYWORD", "else")
            else_body = self.parse_block()
        return {
            "node": "if_statement",
            "condition": condition,
            "body": body,
            "else_body": else_body,
        }

    def parse_while_statement(self):
        """
        <while_statement> = "while" "(" <expression> ")" <block>
        """
        self.consume("KEYWORD", "while")
        self.consume("LPAREN")
        condition = self.parse_expression()
        self.consume("RPAREN")
        body = self.parse_block()
        return {
            "node": "while_statement",
            "condition": condition,
            "body": body,
        }

    def parse_for_statement(self):
        """
        <for_statement> = "for" "(" <declaration>? ";" <expression>? ";" <expression>? ")" <block>
        """
        self.consume("KEYWORD", "for")
        self.consume("LPAREN")
        init = None
        if self.peek()[1] != ";":
            if self.peek()[0] == "TYPE":
                init = self.parse_declaration()
            else:
                init = self.parse_assignment()
        self.consume("SEMICOLON")
        condition = None
        if self.peek()[1] != ";":
            condition = self.parse_expression()
        self.consume("SEMICOLON")
        update = None
        if self.peek()[1] != ")":
            if self.peek_next()[0] == "ASSIGN":
                update = self.parse_assignment()
            else:  # this is not implemented yet, like i++
                update = self.parse_expression()
        self.consume("RPAREN")
        body = self.parse_block()
        return {
            "node": "for_statement",
            "init": init,
            "condition": condition,
            "update": update,
            "body": body,
        }

    def parse_block(self):
        """
        <block> = "{" <statement>* "}"
        """
        self.consume("LBRACE")
        body = []
        while self.peek()[1] != "}":
            body.append(self.parse_statement())
        self.consume("RBRACE")
        return body

    def parse_expression(self):
        """
        <expression> = <term> (<binary_operator> <term>)*
        """
        term = self.parse_term()
        while self.peek() and self.peek()[0] == "OP":
            op = self.consume("OP")[1]
            term = {
                "node": "binary_operator",
                "op": op,
                "left": term,
                "right": self.parse_term(),
            }
        return term

    def parse_term(self):
        """
        <term> = <identifier> | <number> | <function_call> | "(" <expression> ")"
        """
        if self.peek()[0] == "ID":
            if self.peek_next() and self.peek_next()[1] == "(":
                return self.parse_function_call()
            else:
                return {
                    "node": "identifier",
                    "value": self.consume("ID")[1],
                }
        elif self.peek()[0] == "NUMBER":
            return {
                "node": "number",
                "value": self.consume("NUMBER")[1],
            }
        elif self.peek()[1] == "(":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return {
                "node": "parentheses",
                "value": expr,
            }

    def parse(self):
        """
        Parse the tokens and return the AST.
        """
        self.ast = self.parse_program()

    def pretty_print(self):
        """
        Pretty print the AST.
        """

        def _pretty_print(node, indent=0):
            if isinstance(node, list):
                for item in node:
                    _pretty_print(item, indent)
            elif isinstance(node, dict):
                for key, value in node.items():
                    if key == "node":
                        print("  " * indent + value)
                    else:
                        print("  " * indent + f"{key}:")
                        _pretty_print(value, indent + 2)
            else:
                print("  " * indent + str(node))

        _pretty_print(self.ast)


if __name__ == "__main__":
    code = """
    int main() {
        int a = 10;
        int b = 20;
        int c = a + b;
        return c;
    }
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    parser.parse()
    parser.pretty_print()


class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = []
        self.label_counter = 0

        self.register_pool = {i: None for i in range(4, 16)}
        self.free_regs = 12

    def get_free_reg(self, var) -> int:
        """
        Get a free register for a variable.
        """
        if self.free_regs == 0:
            # TODO: add logic for spilling
            raise Exception("No free registers available")
        for reg, value in self.register_pool.items():
            if value == None:
                self.register_pool[reg] = var
                self.free_regs -= 1
                return reg

    def release_reg(self, reg):
        """
        Release a register.
        """
        self.register_pool[reg] = None
        self.free_regs += 1

    def is_var_in_reg(self, var) -> int:
        """
        Check if a variable is stored in a register. If so, return the register.
        """
        for reg, value in self.register_pool.items():
            if value == var:
                return reg
        return None

    def generate_program_code(self):
        for function in self.ast["functions"]:
            self.generate_function_code(function)

    def generate_function_code(self, node):
        # TODO: implement parameter and return value handling
        self.code.append(f"{node['name']}:")
        self.generate_block_code(node["body"])

    def generate_block_code(self, block):
        # Could push and pop registers here, for now just free all previously unused registers at the end of the block
        list_of_used_args = []
        for reg, value in self.register_pool.items():
            if value:
                list_of_used_args.append(reg)

        for item in block:
            if item["node"] == "declaration":
                self.generate_declaration_code(item)
            elif item["node"] == "assignment":
                self.generate_assignment_code(item)
            elif item["node"] == "function_call":
                self.generate_function_call_code(item)
            elif item["node"] == "if_statement":
                self.generate_if_statement_code(item)
            elif item["node"] == "while_statement":
                self.generate_while_statement_code(item)
            elif item["node"] == "for_statement":
                self.generate_for_statement_code(item)
            elif item["node"] == "return_statement":
                self.generate_return_statement_code(item)

        # Free all registers that were not used previously since they are not needed
        for reg in list_of_used_args:
            if self.register_pool[reg] not in [item["name"] for item in block]:
                self.release_reg(reg)

    def generate_declaration_code(self, node) -> int:
        """
        Generate code for a declaration, returns the register where the result/variable is stored.
        """
        if node["value"]:
            value_reg = self.generate_expression_code(node["value"])
            reg = self.get_free_reg(node["name"])
            self.code.append(f"MOV ${reg}, ${value_reg}")
            self.release_reg(value_reg)
            return reg
        else:
            return self.get_free_reg(node["name"])

    def generate_assignment_code(self, node) -> int:
        """
        Generate code for an assignment, returns the register where the result is stored.
        """
        value_reg = self.generate_expression_code(node["right"])
        reg = self.is_var_in_reg(node["left"]["value"])
        if reg:
            self.code.append(f"MOV ${reg}, ${value_reg}")
            self.release_reg(value_reg)
            return reg
        else:
            raise Exception(
                f"Variable {node['left']['value']} not found, should have been declared or assigned"
            )

    def generate_function_call_code(self, node):
        pass

    def generate_if_statement_code(self, node):
        """
        Generate code for an if statement
        """
        self.label_counter += 1
        if_label = f"if_{self.label_counter}"
        end_label = f"end_if_{self.label_counter}"
        else_label = f"else_{self.label_counter}"
        self.code.append(f"{if_label}:")

        condition_reg = self.generate_expression_code(node["condition"])
        self.code.append(f"CMP ${condition_reg}, $1")  # 1 means true
        if node["else_body"]:
            self.code.append(f"JPNZ {else_label}")  # Jump if not zero, meaning false
        else:
            self.code.append(f"JPNZ {end_label}")

        self.generate_block_code(node["body"])

        if node["else_body"]:
            self.code.append(f"GOTO {end_label}")
            self.code.append(f"{else_label}:")
            self.generate_block_code(node["else_body"])

        self.code.append(f"{end_label}:")

    def generate_while_statement_code(self, node):
        pass

    def generate_for_statement_code(self, node):
        pass

    def generate_return_statement_code(self, node):
        pass

    def generate_expression_code(self, node):
        """
        Generate code for an expression, returns the register where the result is stored.
        """
        if node["node"] == "binary_operator":
            return self.generate_binary_operator_code(node)
        elif node["node"] == "identifier":
            return self.generate_identifier_code(node)
        elif node["node"] == "number":
            return self.generate_number_code(node)
        else:
            raise Exception("TODO: Implement other expression types")

    def generate_binary_operator_code(self, node) -> int:
        """
        Generate code for a binary operator, returns the register where the result is stored.
        """
        left = self.generate_expression_code(node["left"])
        right = self.generate_expression_code(node["right"])

        if node["op"] in ["+", "-"]:
            operation = {
                "+": "ADD",
                "-": "SUB",
            }[node["op"]]
            self.code.append(f"{operation} ${left}, ${right}")
            self.release_reg(right)
            return left
        if node["op"] in ["<", ">"]:
            self.label_counter += 1
            label = f"skip_set_{self.label_counter}"

            self.code.append(f"CMP ${left}, ${right}")
            if node["op"] == "<":
                self.code.append(f"JPNC {label}")
            if node["op"] == ">":
                self.code.append(f"JPC {label}")
            self.release_reg(right)

            self.code.append(f"MOV ${left}, $1")
            self.code.append(f"{label}:")
            return left

    def generate_identifier_code(self, node) -> int:
        """
        Generate code for an identifier, returns the register where the result is stored.
        """
        reg = self.is_var_in_reg(node["value"])
        if reg:
            return reg
        else:
            raise Exception(
                f"Variable {node['value']} not found, should have been declared or assigned"
            )

    def generate_number_code(self, node) -> int:
        """
        Generate code for a number, returns the register where the result is stored.
        """
        reg = self.get_free_reg(node["value"])
        self.code.append(f"LWI ${reg}, {node['value']}")
        return reg

    def pretty_print(self):
        for line in self.code:
            if line.endswith(":"):
                print(line)
            else:
                print(f"\t{line}")


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "test.c"

    try:
        output_file = sys.argv[2]
    except IndexError:
        just_file_name = file_name.split("/")[-1]
        output_file = f"{just_file_name[:-2]}.asm"

    with open(file_name, "r") as file:
        code = file.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    parser.parse()
    parser.pretty_print()

    generator = CodeGenerator(parser.ast)
    generator.generate_program_code()
    generator.pretty_print()

    with open(output_file, "w") as file:
        for line in generator.code:
            if line.endswith(":"):
                file.write(f"{line}\n")
            else:
                file.write(f"\t{line}\n")
