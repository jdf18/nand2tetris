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
        self.tokens.advance()
        return self.xml

    def compileClassVarDec(self):
        self.xml += "<classVarDec>\n"

        # Check first token is STATIC | FIELD
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword in [Keywords.STATIC, Keywords.FIELD]
        self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
        self.tokens.advance()

        # Next token is a type
        assert type(self.tokens.current_token) in [KeywordToken, IdentifierToken]
        if type(self.tokens.current_token) == KeywordToken:
            assert self.tokens.current_token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
            self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
        else: # type is identifier
            self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check varName
        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check ( ',' varName ) *
        while True:
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol in [Symbols.COMMA, Symbols.SEMICOLON]
            if self.tokens.current_token.symbol == Symbols.COMMA:
                self.xml += "<symbol> , </symbol>\n"
                self.tokens.advance()

                assert type(self.tokens.current_token) == IdentifierToken
                self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                self.tokens.advance()
            else: # Symbol is ;
                break

        self.xml += "<symbol> ; </symbol>\n"
        self.xml += "</classVarDec>\n"
        self.tokens.advance()
        return

    def compileSubroutine(self):
        self.xml += "<subroutineDec>\n"

        # Check first symbol is CONSTRUCTOR | FUNCTION | METHOD
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword in [Keywords.CONSTRUCTOR, Keywords.FUNCTION, Keywords.METHOD]
        self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
        self.tokens.advance()
        
        # Next is a type thingy again or VOID
        assert type(self.tokens.current_token) in [KeywordToken, IdentifierToken]
        if type(self.tokens.current_token) == KeywordToken:
            assert self.tokens.current_token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN, Keywords.VOID]
            self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
        else: # type is identifier
            self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check subroutineName
        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check for (
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_BRACKET
        self.xml += "<symbol> ( </symbol>\n"
        self.tokens.advance()

        self.compileParameterList()

        # Check for )
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
        self.xml += "<symbol> ) </symbol>\n"
        self.tokens.advance()

        self.compileSubroutineBody()

        self.xml += "</subroutineDec>\n"
        return
    
    def compileParameterList(self):
        # Check next token is a type
        self.xml += "<parameterList>\n"

        if type(self.tokens.current_token) in [KeywordToken, IdentifierToken]:
            while True:
                if type(self.tokens.current_token) == KeywordToken:
                    assert self.tokens.current_token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
                    self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
                else: # type is identifier
                    self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                self.tokens.advance()

                # Check varName
                assert type(self.tokens.current_token) == IdentifierToken
                self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                self.tokens.advance()

                assert type(self.tokens.current_token) == SymbolToken
                if self.tokens.current_token.symbol != Symbols.COMMA:
                    break
                assert self.tokens.current_token.symbol == Symbols.COMMA
                self.xml += "<symbol> , </symbol>\n"
                self.tokens.advance()

        self.xml += "</parameterList>\n"
        return
    
    def compileSubroutineBody(self):
        self.xml += "<subroutineBody>\n"

        # Check for {
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_CURLY_BRACKET
        self.xml += "<symbol> { </symbol>\n"
        self.tokens.advance()

        # Check VarDec *
        while True:
            if type(self.tokens.current_token) == KeywordToken:
                if self.tokens.current_token.keyword == Keywords.VAR:
                    self.compileVarDec()
                else:
                    break
            else:
                break
        
        # Compile subroutine statements
        self.compileStatements()

        # Check for }
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.RIGHT_CURLY_BRACKET
        self.xml += "<symbol> } </symbol>\n"
        self.tokens.advance()

        self.xml += "</subroutineBody>\n"
        return
    
    def compileVarDec(self):
        self.xml += "<varDec>\n"
        
        # VAR Keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.VAR
        self.xml += "<keyword> var </keyword>\n"
        self.tokens.advance()

        # Next token is a type
        assert type(self.tokens.current_token) in [KeywordToken, IdentifierToken]
        if type(self.tokens.current_token) == KeywordToken:
            assert self.tokens.current_token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
            self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
        else: # type is identifier
            self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check varName
        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check ( ',' varName ) *
        while True:
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol in [Symbols.COMMA, Symbols.SEMICOLON]
            if self.tokens.current_token.symbol == Symbols.COMMA:
                self.xml += "<symbol> , </symbol>\n"
                self.tokens.advance()

                assert type(self.tokens.current_token) == IdentifierToken
                self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                self.tokens.advance()
            else: # Symbol is ;
                break

        self.xml += "<symbol> ; </symbol>\n"
        self.tokens.advance()
        self.xml += "</varDec>\n"
        return
    
    def compileStatements(self):
        self.xml += "<statements>\n"

        while True:
            if type(self.tokens.current_token) == KeywordToken:
                if self.tokens.current_token.keyword in [Keywords.LET, Keywords.IF, Keywords.WHILE, Keywords.DO, Keywords.RETURN]:
                    if self.tokens.current_token.keyword == Keywords.LET:
                        self.compileLetStatement()
                    elif self.tokens.current_token.keyword == Keywords.IF:
                        self.compileIfStatement()
                    elif self.tokens.current_token.keyword == Keywords.WHILE:
                        self.compileWhileStatement()
                    elif self.tokens.current_token.keyword == Keywords.DO:
                        self.compileDoStatement()
                    elif self.tokens.current_token.keyword == Keywords.RETURN:
                        self.compileReturnStatement()
                    else:
                        raise AssertionError()
                else:
                    break
            else:
                break

        self.xml += "</statements>\n"
        return
    
    def compileLetStatement(self):
        self.xml += '<letStatement>\n'

        # Check for LET keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.LET
        self.xml += "<keyword> let </keyword>\n"
        self.tokens.advance()

        # Check varName
        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # ( '[' expression ']' )?
        assert type(self.tokens.current_token) == SymbolToken
        if self.tokens.current_token.symbol == Symbols.LEFT_HARD_BRACKET:
            self.xml += "<symbol> [ </symbol>\n"
            self.tokens.advance()

            self.compileExpression()

            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol == Symbols.RIGHT_HARD_BRACKET
            self.xml += "<symbol> ] </symbol>\n"
            self.tokens.advance()

            assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.EQUALS
        self.xml += "<symbol> = </symbol>\n"
        self.tokens.advance()

        self.compileExpression()

        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.SEMICOLON
        self.xml += "<symbol> ; </symbol>\n"
        self.tokens.advance()
        return
    
    def compileIfStatement(self):
        return
    
    def compileWhileStatement(self):
        return
    
    def compileDoStatement(self):
        return
    
    def compileReturnStatement(self):
        return
    
    
    def compileExpression(self):
        return