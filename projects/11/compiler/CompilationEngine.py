from typing import List, Union
from enum import Enum

from JackTokeniser import Tokensiser, Keywords, Symbols, SymbolsLUT, \
    KeywordToken, SymbolToken, IdentifierToken, IntegerValueToken, StringValueToken

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
                assert self.tokens.current_token.symbol == Symbols.RIGHT_CURLY_BRACKET
                self.xml += "<symbol> } </symbol>\n"
                break

            assert type(self.tokens.current_token) == KeywordToken
            assert self.tokens.current_token.keyword in [Keywords.CONSTRUCTOR, Keywords.FUNCTION, Keywords.METHOD]

            self.compileSubroutine()
        self.xml += "</class>\n"
        try:
            self.tokens.advance()
        except StopIteration:
            print("Success")
        else:
            print("More tokens to parse, but ignored")
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
        return self.xml

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

        self.xml += '</letStatement>\n'
        return
    
    def compileIfStatement(self):
        self.xml += '<ifStatement>\n'

        # Check for IF keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.IF
        self.xml += "<keyword> if </keyword>\n"
        self.tokens.advance()

        # Check for (
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_BRACKET
        self.xml += "<symbol> ( </symbol>\n"
        self.tokens.advance()

        self.compileExpression()

        # Check for )
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
        self.xml += "<symbol> ) </symbol>\n"
        self.tokens.advance()

        # Check for {
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_CURLY_BRACKET
        self.xml += "<symbol> { </symbol>\n"
        self.tokens.advance()

        self.compileStatements()

        # Check for }
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.RIGHT_CURLY_BRACKET
        self.xml += "<symbol> } </symbol>\n"
        self.tokens.advance()

        if type(self.tokens.current_token) == KeywordToken:
            if self.tokens.current_token.keyword == Keywords.ELSE:
                self.xml += "<keyword> else </keyword>\n"
                self.tokens.advance()

                # Check for {
                assert type(self.tokens.current_token) == SymbolToken
                assert self.tokens.current_token.symbol == Symbols.LEFT_CURLY_BRACKET
                self.xml += "<symbol> { </symbol>\n"
                self.tokens.advance()

                self.compileStatements()

                # Check for }
                assert type(self.tokens.current_token) == SymbolToken
                assert self.tokens.current_token.symbol == Symbols.RIGHT_CURLY_BRACKET
                self.xml += "<symbol> } </symbol>\n"
                self.tokens.advance()
        
        self.xml += '</ifStatement>\n'
        return
    
    def compileWhileStatement(self):
        self.xml += '<whileStatement>\n'

        # Check for WHILE keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.WHILE
        self.xml += "<keyword> while </keyword>\n"
        self.tokens.advance()

        # Check for (
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_BRACKET
        self.xml += "<symbol> ( </symbol>\n"
        self.tokens.advance()

        self.compileExpression()

        # Check for )
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
        self.xml += "<symbol> ) </symbol>\n"
        self.tokens.advance()

        # Check for {
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_CURLY_BRACKET
        self.xml += "<symbol> { </symbol>\n"
        self.tokens.advance()

        self.compileStatements()

        # Check for }
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.RIGHT_CURLY_BRACKET
        self.xml += "<symbol> } </symbol>\n"
        self.tokens.advance()

        self.xml += '</whileStatement>\n'
        return
    
    def compileDoStatement(self):
        self.xml += '<doStatement>\n'

        # Check for DO keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.DO
        self.xml += "<keyword> do </keyword>\n"
        self.tokens.advance()

        self.compileSubroutineCall()

        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.SEMICOLON
        self.xml += "<symbol> ; </symbol>\n"
        self.tokens.advance()

        self.xml += '</doStatement>\n'
        return
    
    def compileReturnStatement(self):
        self.xml += '<returnStatement>\n'

        # Check for DO keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.RETURN
        self.xml += "<keyword> return </keyword>\n"
        self.tokens.advance()

        if type(self.tokens.current_token) == SymbolToken:
            if self.tokens.current_token.symbol == Symbols.SEMICOLON:
                self.xml += "<symbol> ; </symbol>\n"
                self.xml += '</returnStatement>\n'
                self.tokens.advance()
                return
            
        self.compileExpression()

        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.SEMICOLON
        self.xml += "<symbol> ; </symbol>\n"
        self.tokens.advance()

        self.xml += '</returnStatement>\n'
        return
    
    
    def compileExpression(self):
        self.xml += '<expression>\n'

        self.compileTerm()

        while True:
            if type(self.tokens.current_token ) == SymbolToken:
                if self.tokens.current_token.symbol in [Symbols.PLUS, Symbols.MINUS, Symbols.ASTERISK, Symbols.FORWARDS_SLASH, \
                                                        Symbols.AMPERSAND, Symbols.PIPE, \
                                                        Symbols.LESS_THAN, Symbols.GREATER_THAN, Symbols.EQUALS]:
                    self.xml += f"<symbol> {SymbolsLUT[self.tokens.current_token.symbol]} </symbol>\n"
                    self.tokens.advance()

                    self.compileTerm()
                else:
                    break
            else:
                break

        self.xml += '</expression>\n'
        return
    
    def compileTerm(self):
        self.xml += '<term>\n'
        
        # their own class:          integerConstant | stringConstant | keywordConstant |
        # start with identifier:    varName | varName '[' expression ']' | subroutineCall | 
        # start with symbol:        '(' expression ')' | unaryOp term

        if type(self.tokens.current_token) == IntegerValueToken:
            self.xml += f"<integerConstant> {str(self.tokens.current_token.integerValue)} </integerConstant>\n"
            self.tokens.advance()

        elif type(self.tokens.current_token) == StringValueToken:
            self.xml += f"<stringConstant> {str(self.tokens.current_token.stringValue)} </stringConstant>\n"
            self.tokens.advance()

        elif type(self.tokens.current_token) == KeywordToken:
            assert self.tokens.current_token.keyword in [Keywords.TRUE, Keywords.FALSE, Keywords.NULL, Keywords.THIS]
            self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
            self.tokens.advance()

        elif type(self.tokens.current_token) == IdentifierToken:
            # start with identifier:    varName | varName '[' expression ']' | subroutineCall
            # varname:                      single identifier token
            # varName '[' expression ']':   identifier then symbol '[' then ...
            # subroutineCall:               identifier then symbol '(' then ...

            if type(self.tokens.look_ahead()) == SymbolToken:
                if self.tokens.look_ahead().symbol == Symbols.LEFT_HARD_BRACKET:
                    # varName '[' expression ']':   identifier then symbol '[' then ...
                    self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                    self.tokens.advance()

                    self.xml += "<symbol> [ </symbol>\n"
                    self.tokens.advance()

                    self.compileExpression()

                    assert type(self.tokens.current_token) == SymbolToken
                    assert self.tokens.current_token.symbol == Symbols.RIGHT_HARD_BRACKET
                    self.xml += "<symbol> ] </symbol>\n"
                    self.tokens.advance()

                elif self.tokens.look_ahead().symbol in [Symbols.LEFT_BRACKET, Symbols.PERIOD]:
                    # subroutineCall:               identifier then symbol '(' then ...

                    self.compileSubroutineCall()

                else:
                    # single identifier token
                    self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                    self.tokens.advance()
            else:
                # single identifier token
                self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                self.tokens.advance()
        
        elif type(self.tokens.current_token) == SymbolToken:
            # start with symbol:        '(' expression ')' | unaryOp term
            assert self.tokens.current_token.symbol in [Symbols.LEFT_BRACKET, Symbols.MINUS, Symbols.TILDA]

            if self.tokens.current_token.symbol == Symbols.LEFT_BRACKET:
                self.xml += "<symbol> ( </symbol>\n"
                self.tokens.advance()

                self.compileExpression()

                assert type(self.tokens.current_token) == SymbolToken
                assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
                self.xml += "<symbol> ) </symbol>\n"
                self.tokens.advance()
            else:
                assert self.tokens.current_token.symbol in [Symbols.MINUS, Symbols.TILDA]

                self.xml += f"<symbol> {SymbolsLUT[self.tokens.current_token.symbol]} </symbol>\n"
                self.tokens.advance()

                self.compileTerm()

        self.xml += '</term>\n'
        return
    
    def compileSubroutineCall(self):
        #self.xml += '<subroutineCall>\n'

        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.tokens.advance()

        # Check for ( or .
        assert type(self.tokens.current_token) == SymbolToken
        if self.tokens.current_token.symbol == Symbols.LEFT_BRACKET:
            # Check for (
            self.xml += "<symbol> ( </symbol>\n"
            self.tokens.advance()

            self.compileExpressionList()

            # Check for )
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
            self.xml += "<symbol> ) </symbol>\n"
            self.tokens.advance()
        else:
            assert self.tokens.current_token.symbol == Symbols.PERIOD
            self.xml += "<symbol> . </symbol>\n"
            self.tokens.advance()

            assert type(self.tokens.current_token) == IdentifierToken
            self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
            self.tokens.advance()

            # Check for (
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol == Symbols.LEFT_BRACKET
            self.xml += "<symbol> ( </symbol>\n"
            self.tokens.advance()

            self.compileExpressionList()

            # Check for )
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
            self.xml += "<symbol> ) </symbol>\n"
            self.tokens.advance()

        #self.xml += '</subroutineCall>\n'
        return

    def compileExpressionList(self):
        self.xml += '<expressionList>\n'

        while True:
            if type(self.tokens.current_token) in [IntegerValueToken, StringValueToken, IdentifierToken]:
                self.compileExpression()

                if type(self.tokens.current_token) == SymbolToken:
                    if self.tokens.current_token.symbol == Symbols.COMMA:
                        self.xml += "<symbol> , </symbol>\n"
                        self.tokens.advance()
                    else:
                        break
                else:
                    break
            elif type(self.tokens.current_token) == KeywordToken:
                if self.tokens.current_token.keyword in [Keywords.TRUE, Keywords.FALSE, Keywords.NULL, Keywords.THIS]:
                    self.compileExpression()

                    if type(self.tokens.current_token) == SymbolToken:
                        if self.tokens.current_token.symbol == Symbols.COMMA:
                            self.xml += "<symbol> , </symbol>\n"
                            self.tokens.advance()
                        else:
                            break
                    else:
                        break
                else:
                    break
            elif type(self.tokens.current_token) == SymbolToken:
                if self.tokens.current_token.symbol in [Symbols.LEFT_BRACKET, Symbols.MINUS, Symbols.TILDA]:
                    self.compileExpression()

                    if type(self.tokens.current_token) == SymbolToken:
                        if self.tokens.current_token.symbol == Symbols.COMMA:
                            self.xml += "<symbol> , </symbol>\n"
                            self.tokens.advance()
                        else:
                            break
                    else:
                        break
                else:
                    break
            else:
                break

        self.xml += '</expressionList>\n'
        return