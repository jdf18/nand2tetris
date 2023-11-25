from enum import Enum
from typing import List, Tuple, Union, Any
from VMWriter import COMMAND

class Keywords(Enum):
    CLASS = 0
    METHOD = 1
    FUNCTION = 2
    CONSTRUCTOR = 3
    INT = 4
    BOOLEAN = 5
    CHAR = 6
    VOID = 7
    VAR = 8
    STATIC = 9
    FIELD = 10
    LET = 11
    DO = 12
    IF = 13
    ELSE = 14
    WHILE = 15
    RETURN = 16
    TRUE = 17
    FALSE = 18
    NULL = 19
    THIS = 20

class Symbols(Enum):
    LEFT_BRACKET = 1
    RIGHT_BRACKET = 2
    LEFT_HARD_BRACKET = 3
    RIGHT_HARD_BRACKET = 4
    LEFT_CURLY_BRACKET = 5
    RIGHT_CURLY_BRACKET = 6
    PERIOD = 7
    COMMA = 8
    SEMICOLON = 9
    PLUS = COMMAND.ADD
    MINUS = COMMAND.NEG
    ASTERISK = 12
    FORWARDS_SLASH = 13
    AMPERSAND = COMMAND.AND
    PIPE = COMMAND.OR
    LESS_THAN = COMMAND.LT
    GREATER_THAN = COMMAND.GT
    EQUALS = COMMAND.EQ
    TILDA = COMMAND.NOT

SymbolsLUT = {
    Symbols.LEFT_BRACKET: "(",
    Symbols.RIGHT_BRACKET: ")",
    Symbols.LEFT_HARD_BRACKET: "[",
    Symbols.RIGHT_HARD_BRACKET: "]",
    Symbols.LEFT_CURLY_BRACKET: "{",
    Symbols.RIGHT_CURLY_BRACKET: "}",
    Symbols.PERIOD: ".",
    Symbols.COMMA: ",",
    Symbols.SEMICOLON: ";",
    Symbols.PLUS: "+", 
    Symbols.MINUS: "-", 
    Symbols.ASTERISK: "*", 
    Symbols.FORWARDS_SLASH: "/", 
    Symbols.AMPERSAND: "&amp;", 
    Symbols.PIPE: "|", 
    Symbols.LESS_THAN: "&lt;", 
    Symbols.GREATER_THAN: "&gt;", 
    Symbols.EQUALS: "=", 
    Symbols.TILDA: "~", 
}

class Token:
    def __repr__(self) -> str:
        return '<Token>'
class KeywordToken(Token):
    def __init__(self, keyword: Keywords) -> None:
        self.keyword: Keywords = keyword
    def __repr__(self) -> str:
        return f'<KeywordToken {self.keyword.name}>'
class SymbolToken(Token):
    def __init__(self, symbol: Symbols) -> None:
        self.symbol: Symbols = symbol
    def __repr__(self) -> str:
        return f'<SymbolToken {self.symbol.name}>'
class IdentifierToken(Token):
    def __init__(self, identifier: str) -> None:
        self.identifier: str = identifier
    def __repr__(self) -> str:
        return f'<IdentifierToken {self.identifier}>'
class IntegerValueToken(Token):
    def __init__(self, integerValue: int) -> None:
        self.integerValue: int = integerValue
    def __repr__(self) -> str:
        return f'<IntegerValueToken {self.integerValue}>'
class StringValueToken(Token):
    def __init__(self, stringValue: str) -> None:
        self.stringValue: str = stringValue
    def __repr__(self) -> str:
        return f'<StringValueToken {self.stringValue}>'

TOKENS_UNION = Union[KeywordToken, SymbolToken, IdentifierToken, IntegerValueToken, StringValueToken]

class Tokensiser:
    def __init__(self, input: str):
        self.tokens: List[TOKENS_UNION] = []
        
        input = self.filter_comments(input)
        self.tokenise(input)

        self.tokensList = self.SmartTokenList(self.tokens)
    @staticmethod
    def filter_comments(input: str):
        chars = ""

        is_string = False
        is_multi_line_comment = False
        is_single_line_comment = False

        previous_char = None

        for char in input:
            if is_string:
                if char == '"':
                    is_string = False
                chars += char
            elif is_single_line_comment:
                if char == '\n':
                    chars += '\n'
                    is_single_line_comment = False
            elif is_multi_line_comment:
                if previous_char == '*' and char == '/':
                    is_multi_line_comment = False
            else:
                if char == '/' and previous_char == '/':
                    # single line comment, w/ remove last char from chars
                    is_single_line_comment = True
                    chars = chars[:-1]
                elif char == '*' and previous_char == '/':
                    # multi line comment, w/ remove last char from chars
                    is_multi_line_comment = True
                    chars = chars[:-1]
                else:
                    chars += char

            previous_char = char

        return chars

    def tokenise(self, input: str):
        is_string_value = False
        is_integer_value = False
        is_identifier = False
        buffer = ''

        SYMBOL_LUT = {
            '(' : Symbols.LEFT_BRACKET,
            ')' : Symbols.RIGHT_BRACKET,
            '[' : Symbols.LEFT_HARD_BRACKET,
            ']' : Symbols.RIGHT_HARD_BRACKET,
            '{' : Symbols.LEFT_CURLY_BRACKET,
            '}' : Symbols.RIGHT_CURLY_BRACKET,
            '.' : Symbols.PERIOD,
            ',' : Symbols.COMMA,
            ';' : Symbols.SEMICOLON,
            '+' : Symbols.PLUS,
            '-' : Symbols.MINUS,
            '*' : Symbols.ASTERISK,
            '/' : Symbols.FORWARDS_SLASH,
            '&' : Symbols.AMPERSAND,
            '|' : Symbols.PIPE,
            '<' : Symbols.LESS_THAN,
            '>' : Symbols.GREATER_THAN,
            '=' : Symbols.EQUALS,
            '~' : Symbols.TILDA,
        }
        KEYWORD_LUT = {enum.name.lower() : enum for enum in Keywords}

        for i, char in enumerate(input):
            if char == '"' or is_string_value:
                if char == '"':
                    if not is_string_value:
                        # starting string
                        is_string_value = True
                        buffer = ''
                    else:
                        # ending string
                        is_string_value = False
                        self.tokens.append(StringValueToken(buffer))
                        buffer = None
                else:
                    buffer += char

            elif char in SYMBOL_LUT.keys():
                self.tokens.append(SymbolToken(SYMBOL_LUT[char]))

            elif is_identifier:
                # add char to buffer, send if finished
                buffer += char
                if not (buffer + input[i+1]).isidentifier():
                    # does not contain 0-9a-zA-Z_ (not starting with number)
                    if buffer in KEYWORD_LUT.keys():
                        self.tokens.append(KeywordToken(KEYWORD_LUT[buffer]))
                    else:
                        self.tokens.append(IdentifierToken(buffer))
                    is_identifier = False
            
            elif char.isdigit():
                if not is_integer_value:
                    # previous character was not a digit
                    is_integer_value = True    
                    buffer = int(char)
                else:
                    # previous character was a digit, buffer already setup
                    buffer *= 10
                    buffer += int(char)
                
                if not input[i+1].isdigit():
                    # finished tokenising number, send token
                    is_integer_value = False
                    self.tokens.append(IntegerValueToken(buffer))
                    buffer = None

            elif char in ' \n\t':
                pass
            

            else:
                buffer = char
                if not (buffer + input[i+1]).isidentifier():
                    # does not contain 0-9a-zA-Z_ (not starting with number)
                    if buffer in KEYWORD_LUT.keys():
                        self.tokens.append(KeywordToken(KEYWORD_LUT[buffer]))
                    else:
                        self.tokens.append(IdentifierToken(buffer))
                else:
                    is_identifier = True

    class SmartTokenList:
        def __init__(self, tokens: Tuple[TOKENS_UNION]):
            self.current_index: int = -1
            self.tokens: Tuple[TOKENS_UNION] = tuple(tokens)
            self.current_token: TOKENS_UNION = None
        def advance(self, n: int = 1) -> TOKENS_UNION:
            if self.current_index + n >= len(self.tokens):
                raise StopIteration()
            self.current_index += n
            self.current_token: TOKENS_UNION = self.tokens[self.current_index]
            return self.current_token
        def look_ahead(self, offset: int=1) -> TOKENS_UNION:
            if self.current_index + offset >= len(self.tokens):
                raise IndexError(f'IndexError: Look ahead with current index {self.current_index} and offset {offset}')
            return self.tokens[self.current_index + offset]
        def debug(self, number, offset=0):
            return self.tokens[self.current_index + offset : min(len(self.tokens), self.current_index + offset + number)]


            

