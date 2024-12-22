import re

# Define token types
# https://learn.microsoft.com/en-us/cpp/c-language/lexical-grammar?view=msvc-170
TOKENS = [
    ("KEYWORD", r"\b(break|continue|char|if|else|for|return|void)\b"),
    ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("CONSTANT", r"\b0[bB][01]+|0[oO][0-7]+|0[xX][0-9a-fA-F]+|\d+\b"),
    ("PUNCTUATOR", r"[;{}()[\],+\-*/=]"),
    ("STRING_LITERAL", r'"[^"]*"'),
    ("WHITESPACE", r"\s+"),  # Ignore whitespace
    ("SINGLE_COMMENT", r"//.*"),
    ("MULTI_COMMENT", r"/\*.*?\*/"),
]

def tokenize(code):
    tokens = []
    while code:
        for token_type, regex in TOKENS:
            match = re.match(regex, code)
            if match:
                if token_type not in ["WHITESPACE", "SINGLE_COMMENT", "MULTI_COMMENT"]:
                    tokens.append((token_type, match.group(0)))
                code = code[match.end():]
                break
        else:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens

code = "char a = 5; return a + 0x10;"
print(tokenize(code))
