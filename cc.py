import re

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
        return functions

    def parse_function(self):
        """
        <function> = <type> <identifier> "(" <parameters>? ")" "{" <statement>* "}"
        """
        type_ = self.expect("KEYWORD")
        name = self.expect("ID")
        self.expect("LPAREN")
        params = []
        if self.peek()[1] != ")":
            params = self.parse_parameters()
        self.expect("RPAREN")
        self.expect("LBRACE")
        body = []
        while self.lookahead()[1] != "}":
            body.append(self.parse_statement())
        self.expect("RBRACE")
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
        params.append({
            "node": "parameter",
            "type": self.consume("TYPE")[1],
            "name": self.consume("ID")[1],
        })
        while self.peek() and self.peek()[1] == ",":
            self.consume("COMMA")
            params.append({
                "node": "parameter",
                "type": self.consume("TYPE")[1],
                "name": self.consume("ID")[1],
            })
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
            val =  self.parse_declaration()
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
            else: # this is not implemented yet, like i++
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
