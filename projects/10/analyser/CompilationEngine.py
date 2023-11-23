from typing import List, Union
from enum import Enum

from JackTokeniser import Tokensiser, Keywords, Symbols, KeywordToken, SymbolToken, IdentifierToken, IntegerValueToken, StringValueToken

class CompilationEngine:
    def __init__(self, tokensList: Tokensiser.SmartTokenList):
        self.tokens = tokensList
        self.tokens.advance()
        self.xml = ""

    def compileClass(self):
        self.xml += "<class>\n"

        # Check for class keyword
        assert type(self.tokens.current_token) == KeywordToken, "Class definition should start with class keyword. No keyword found."
        assert self.tokens.current_token.keyword == Keywords.CLASS, "Class definition should start with class keyword. Keyword was not CLASS."
        self.xml += "<keyword> class </keyword>\n"
        self.tokens.advance()

        # Check for the classname identifier
        assert type(self.tokens.current_token) == IdentifierToken, "Class name definition should include an identifier."
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check for {
        assert type(self.tokens.current_token) == SymbolToken, "Class definition should start with a '{'. No symbol found."
        assert self.tokens.current_token.symbol == Symbols.LEFT_CURLY_BRACKET, "Class definition should start with a '{'. Symbol was not '{'."
        self.xml += "<symbol> { </symbol>\n"
        self.tokens.advance()

        # Check for class variable declatations *
        while True:
            assert type(self.tokens.current_token) == KeywordToken
            assert self.tokens.current_token.keyword in [Keywords.STATIC, Keywords.FIELD, Keywords.CONSTRUCTOR, Keywords.FUNCTION, Keywords.METHOD]

            # If token is STATIC | FIELD, compile classVarDec
            # Else, start parsing subroutine declarations
            if self.tokens.current_token.keyword in [Keywords.STATIC, Keywords.FIELD]:
                self.compileClassVarDec()
            else:
                break

        # Check for subroutine declarations *
        while True:
            if type(self.tokens.current_token) == SymbolToken:
                # Check for }
                assert self.tokens.current_token == Symbols.RIGHT_CURLY_BRACKET
                self.xml += "<symbol> } </symbol>\n"
                self.tokens.advance()
                break

            assert type(self.tokens.current_token) == KeywordToken
            assert self.tokens.current_token.keyword in [Keywords.CONSTRUCTOR, Keywords.FUNCTION, Keywords.METHOD]

            self.compileSubroutine()
        self.xml += "</class>\n"
        return self.xml

    def compileClassVarDec(self):
        return

    def compileSubroutine(self):
        return