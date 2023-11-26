from typing import List, Union
from enum import Enum

from JackTokeniser import Tokensiser, Keywords, Symbols, SymbolsLUT, \
    KeywordToken, SymbolToken, IdentifierToken, IntegerValueToken, StringValueToken

from VMWriter import VMWriter, SEGMENT, COMMAND
from SymbolTable import SymbolTable, KIND

class CompilationEngine:
    def __init__(self, tokensList: Tokensiser.SmartTokenList):
        self.tokens = tokensList
        self.tokens.advance()
        self.xml = ""
        self.symbol_table = SymbolTable()
        self.vm_code = None
        self.classname = "A"
        self.label_count = 0

    def get_new_label(self):
        label = self.classname + str(self.label_count)
        self.label_count += 1
        return label

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
        self.classname = self.tokens.current_token.identifier
        self.vm_code = VMWriter(self.classname)
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
        return self.vm_code.vm_code

    def compileClassVarDec(self):
        self.xml += "<classVarDec>\n"

        # Check first token is STATIC | FIELD
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword in [Keywords.STATIC, Keywords.FIELD]
        self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
        var_kind = (KIND.STATIC if self.tokens.current_token.keyword == Keywords.STATIC else KIND.FIELD)
        self.tokens.advance()

        # Next token is a type
        assert type(self.tokens.current_token) in [KeywordToken, IdentifierToken]
        if type(self.tokens.current_token) == KeywordToken:
            assert self.tokens.current_token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
            self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
            var_type = self.tokens.current_token.keyword.name.lower()
        else: # type is identifier
            self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
            var_type = self.tokens.current_token.identifier
        self.tokens.advance()

        # Check varName
        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.symbol_table.define(self.tokens.current_token.identifier, var_type, var_kind)
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
                self.symbol_table.define(self.tokens.current_token.identifier, var_type, var_kind)
                self.tokens.advance()
            else: # Symbol is ;
                break

        self.xml += "<symbol> ; </symbol>\n"
        self.xml += "</classVarDec>\n"
        
        self.tokens.advance()
        return

    def compileSubroutine(self):
        self.xml += "<subroutineDec>\n"

        self.symbol_table.startSubroutine()
        self.is_method = False

        # Check first symbol is CONSTRUCTOR | FUNCTION | METHOD
        self.is_constructor = False
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword in [Keywords.CONSTRUCTOR, Keywords.FUNCTION, Keywords.METHOD]
        self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
        if self.tokens.current_token.keyword == Keywords.METHOD:
            self.symbol_table.define('this', self.classname, KIND.ARG)
            self.is_method = True
        elif self.tokens.current_token.keyword == Keywords.CONSTRUCTOR:
            self.symbol_table.define('this', self.classname, KIND.VAR)
            self.is_constructor = True
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
        self.subroutine_name = self.tokens.current_token.identifier
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

        locals_count = 0

        if type(self.tokens.current_token) in [KeywordToken, IdentifierToken]:
            while True:
                if type(self.tokens.current_token) == KeywordToken:
                    assert self.tokens.current_token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
                    self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
                    var_type = self.tokens.current_token.keyword.name.lower()
                else: # type is identifier
                    self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                    var_type = self.tokens.current_token.identifier
                self.tokens.advance()

                # Check varName
                assert type(self.tokens.current_token) == IdentifierToken
                self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                self.symbol_table.define(self.tokens.current_token.identifier, var_type, KIND.ARG)
                locals_count += 1
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

        locals_count = 0
        # Check VarDec *
        while True:
            if type(self.tokens.current_token) == KeywordToken:
                if self.tokens.current_token.keyword == Keywords.VAR:
                    locals_count += self.compileVarDec()
                else:
                    break
            else:
                break

        self.vm_code.write_function(self.subroutine_name, locals_count)
        if self.is_constructor:
            self.vm_code.write_push(
                SEGMENT.CONST, 
                self.symbol_table.var_count(KIND.FIELD)
            )
            self.vm_code.write_call("Memory.alloc", 1)
            self.vm_code.write_pop(SEGMENT.POINTER, 0)
        elif self.is_method:
            self.vm_code.write_push(SEGMENT.ARG, 0)
            self.vm_code.write_pop(SEGMENT.POINTER, 0)
        
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

        locals_count = 0
        
        # VAR Keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.VAR
        self.xml += "<keyword> var </keyword>\n"
        var_kind = KIND.VAR
        self.tokens.advance()

        # Next token is a type
        assert type(self.tokens.current_token) in [KeywordToken, IdentifierToken]
        if type(self.tokens.current_token) == KeywordToken:
            assert self.tokens.current_token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
            self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
            var_type = self.tokens.current_token.keyword.name.lower()
        else: # type is identifier
            self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
            var_type = self.tokens.current_token.identifier
        self.tokens.advance()

        # Check varName
        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        self.symbol_table.define(self.tokens.current_token.identifier, var_type, var_kind)
        locals_count += 1
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
                self.symbol_table.define(self.tokens.current_token.identifier, var_type, var_kind)
                locals_count += 1
                self.tokens.advance()
            else: # Symbol is ;
                break

        self.xml += "<symbol> ; </symbol>\n"
        
        self.tokens.advance()
        self.xml += "</varDec>\n"
        return locals_count
    
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
        store_token = self.tokens.current_token.identifier
        self.tokens.advance()

        # ( '[' expression ']' )?
        array_magic = False
        assert type(self.tokens.current_token) == SymbolToken
        if self.tokens.current_token.symbol == Symbols.LEFT_HARD_BRACKET:
            array_magic = True
            self.xml += "<symbol> [ </symbol>\n"
            self.tokens.advance()

            self.vm_code.write_push(
                self.symbol_table.kind_of(store_token).value,
                self.symbol_table.index_of(store_token)
            )

            self.compileExpression()

            self.vm_code.write_arithmetic(COMMAND.ADD)

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

        if array_magic:
            self.vm_code.write_pop(SEGMENT.TEMP, 1)
            self.vm_code.write_pop(SEGMENT.POINTER, 1)
            self.vm_code.write_push(SEGMENT.TEMP, 1)
            self.vm_code.write_pop(SEGMENT.THAT, 0)
        else:
            self.vm_code.write_pop(
                self.symbol_table.kind_of(store_token).value,
                self.symbol_table.index_of(store_token)
            )
        self.tokens.advance()

        self.xml += '</letStatement>\n'
        return
    
    def compileIfStatement(self):
        self.xml += '<ifStatement>\n'

        has_else = False

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

        #top_label = self.get_new_label()
        neg_label = self.get_new_label()

        #self.vm_code.write_label(top_label)

        self.compileExpression()

        # Conditional jump logic. Expression result should be on top of the stack
        self.vm_code.write_arithmetic(COMMAND.NOT)
        self.vm_code.write_if(neg_label)
        # Carry of executing if true, else, go to not marker

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
                has_else = True
                end_label = self.get_new_label()

                self.xml += "<keyword> else </keyword>\n"
                self.tokens.advance()

                # If there is an else, before NOT marker, unconditional jump to end label
                self.vm_code.write_goto(end_label)

                # Check for {
                assert type(self.tokens.current_token) == SymbolToken
                assert self.tokens.current_token.symbol == Symbols.LEFT_CURLY_BRACKET
                self.xml += "<symbol> { </symbol>\n"
                self.tokens.advance()

                # Label for NOT marker
                self.vm_code.write_label(neg_label)

                self.compileStatements()

                # Check for }
                assert type(self.tokens.current_token) == SymbolToken
                assert self.tokens.current_token.symbol == Symbols.RIGHT_CURLY_BRACKET
                self.xml += "<symbol> } </symbol>\n"
                self.tokens.advance()

        # END label (only present if there is an else), otherwise use the NOT marker
        self.vm_code.write_label( (end_label if has_else else neg_label) )
        self.xml += '</ifStatement>\n'
        return
    
    def compileWhileStatement(self):
        self.xml += '<whileStatement>\n'

        # Check for WHILE keyword
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.WHILE
        self.xml += "<keyword> while </keyword>\n"
        self.tokens.advance()

        # Place label here ?
        top_label = self.get_new_label()
        exit_label = self.get_new_label()

        self.vm_code.write_label(top_label)

        # Check for (
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_BRACKET
        self.xml += "<symbol> ( </symbol>\n"
        self.tokens.advance()

        self.compileExpression()

        # Put the condition here. Result should already be on the top of the stack
        self.vm_code.write_arithmetic(COMMAND.NOT)
        self.vm_code.write_if(exit_label)
        # ? Because NOT(GT) == LT OR EQ does this change the bounds ?

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

        # Jump to top
        self.vm_code.write_goto(top_label)

        # Place exit label here ?
        self.vm_code.write_label(exit_label)

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
        # throw item at the top of the stack from subroutine call as not saved anywhere
        self.vm_code.write_pop(SEGMENT.TEMP, 0)
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
                # if not returning anything, push constant 0
                self.vm_code.write_push(SEGMENT.CONST, 0)
                self.tokens.advance()
                self.vm_code.write_return()
                return
            
        self.compileExpression()

        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.SEMICOLON
        self.xml += "<symbol> ; </symbol>\n"
        # TODO Push this value onto the stack
        # ? Does compileExpression already do this?
        self.tokens.advance()
        self.vm_code.write_return()

        self.xml += '</returnStatement>\n'
        return
    
    
    def compileExpression(self):
        self.xml += '<expression>\n'

        self.compileTerm()
        symbols = []

        while True:
            if type(self.tokens.current_token ) == SymbolToken:
                if self.tokens.current_token.symbol in [Symbols.PLUS, Symbols.MINUS, Symbols.ASTERISK, Symbols.FORWARDS_SLASH, \
                                                        Symbols.AMPERSAND, Symbols.PIPE, \
                                                        Symbols.LESS_THAN, Symbols.GREATER_THAN, Symbols.EQUALS]:
                    self.xml += f"<symbol> {SymbolsLUT[self.tokens.current_token.symbol]} </symbol>\n"
                    symbols.append(self.tokens.current_token.symbol)
                    self.tokens.advance()

                    self.compileTerm()
                else:
                    break
            else:
                break
        
        symbols.reverse()
        for operation in symbols:
            if operation == Symbols.ASTERISK:
                # TODO Check these labels are correct, and also that it works in the first place.
                self.vm_code.write_call("Math.multiply", 2)
            elif operation == Symbols.FORWARDS_SLASH:
                self.vm_code.write_call("Math.divide", 2)
            elif operation == Symbols.MINUS:
                self.vm_code.write_arithmetic(COMMAND.NEG)
                self.vm_code.write_arithmetic(COMMAND.ADD)
            else:
                self.vm_code.write_arithmetic(operation.value)

        self.xml += '</expression>\n'
        return
    
    def compileTerm(self):
        self.xml += '<term>\n'
        
        # their own class:          integerConstant | stringConstant | keywordConstant |
        # start with identifier:    varName | varName '[' expression ']' | subroutineCall | 
        # start with symbol:        '(' expression ')' | unaryOp term

        if type(self.tokens.current_token) == IntegerValueToken:
            self.xml += f"<integerConstant> {str(self.tokens.current_token.integerValue)} </integerConstant>\n"
            self.vm_code.write_push(SEGMENT.CONST, self.tokens.current_token.integerValue)
            self.tokens.advance()

        elif type(self.tokens.current_token) == StringValueToken:
            self.xml += f"<stringConstant> {str(self.tokens.current_token.stringValue)} </stringConstant>\n"
            # TODO Creates new string object with length
            # TODO Adds each character
            self.compileString(self.tokens.current_token.stringValue)
            self.tokens.advance()

        elif type(self.tokens.current_token) == KeywordToken:
            assert self.tokens.current_token.keyword in [Keywords.TRUE, Keywords.FALSE, Keywords.NULL, Keywords.THIS]
            self.xml += f"<keyword> {self.tokens.current_token.keyword.name.lower()} </keyword>\n"
            if self.tokens.current_token.keyword == Keywords.TRUE:
                self.vm_code.write_push(SEGMENT.CONST, 1)
                self.vm_code.write_arithmetic(COMMAND.NEG)
            elif self.tokens.current_token.keyword == Keywords.FALSE:
                self.vm_code.write_push(SEGMENT.CONST, 0)
            elif self.tokens.current_token.keyword == Keywords.NULL:
                self.vm_code.write_push(SEGMENT.CONST, 0)
            elif self.tokens.current_token.keyword == Keywords.THIS:
                print(self.subroutine_name)
                self.vm_code.write_push(SEGMENT.POINTER, 0)
            self.tokens.advance()

        elif type(self.tokens.current_token) == IdentifierToken:
            # * start with identifier:    varName | varName '[' expression ']' | subroutineCall
            # varname:                      single identifier token
            # varName '[' expression ']':   identifier then symbol '[' then ...
            # subroutineCall:               identifier then symbol '(' then ...

            if type(self.tokens.look_ahead()) == SymbolToken:
                if self.tokens.look_ahead().symbol == Symbols.LEFT_HARD_BRACKET:
                    # varName '[' expression ']':   identifier then symbol '[' then ...
                    self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
                    self.vm_code.write_push(
                        self.symbol_table.kind_of(self.tokens.current_token.identifier).value,
                        self.symbol_table.index_of(self.tokens.current_token.identifier)
                    )
                    self.tokens.advance()

                    self.xml += "<symbol> [ </symbol>\n"
                    self.tokens.advance()

                    self.compileExpression()

                    self.vm_code.write_arithmetic(COMMAND.ADD)
                    self.vm_code.write_pop(SEGMENT.POINTER, 1)
                    self.vm_code.write_push(SEGMENT.THAT, 0)

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
                    self.vm_code.write_push(
                        self.symbol_table.kind_of(self.tokens.current_token.identifier).value,
                        self.symbol_table.index_of(self.tokens.current_token.identifier)
                    )
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

                operation = self.tokens.current_token.symbol
                self.xml += f"<symbol> {SymbolsLUT[self.tokens.current_token.symbol]} </symbol>\n"
                self.tokens.advance()

                # TODO Push token then do operation

                self.compileTerm()

                if operation == Symbols.MINUS:
                    self.vm_code.write_arithmetic(COMMAND.NEG)
                elif operation == Symbols.TILDA:
                    self.vm_code.write_arithmetic(COMMAND.NOT)

        self.xml += '</term>\n'
        return
    
    def compileSubroutineCall(self):
        #self.xml += '<subroutineCall>\n'

        assert type(self.tokens.current_token) == IdentifierToken
        self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
        label = self.tokens.current_token.identifier
        print(self.tokens.tokens[self.tokens.current_index-2: self.tokens.current_index + 3])
        self.tokens.advance()

        # Check for ( or .
        n_args = 0
        assert type(self.tokens.current_token) == SymbolToken
        if self.tokens.current_token.symbol == Symbols.LEFT_BRACKET:
            # Check for (
            self.xml += "<symbol> ( </symbol>\n"
            self.tokens.advance()

            self.vm_code.write_push(SEGMENT.POINTER, 0)
            label = self.classname + "." + label
            n_args += 1

            n_args += self.compileExpressionList()

            # Check for )
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
            self.xml += "<symbol> ) </symbol>\n"
            self.tokens.advance()
        else:
            assert self.tokens.current_token.symbol == Symbols.PERIOD
            self.xml += "<symbol> . </symbol>\n"
            self.tokens.advance()

            # label is currently name of instance of the class.
            name = label
            if self.symbol_table.exists(name):
                label = self.symbol_table.type_of(name)
                self.vm_code.write_push(
                    self.symbol_table.kind_of(name).value,
                    self.symbol_table.index_of(name)
                )
                n_args += 1

            assert type(self.tokens.current_token) == IdentifierToken
            self.xml += f"<identifier> {self.tokens.current_token.identifier} </identifier>\n"
            label += '.' + self.tokens.current_token.identifier
            self.tokens.advance()

            # Check for (
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol == Symbols.LEFT_BRACKET
            self.xml += "<symbol> ( </symbol>\n"
            self.tokens.advance()

            n_args += self.compileExpressionList()

            # Check for )
            assert type(self.tokens.current_token) == SymbolToken
            assert self.tokens.current_token.symbol == Symbols.RIGHT_BRACKET
            self.xml += "<symbol> ) </symbol>\n"
            self.tokens.advance()

        print("label written:", label)
        self.vm_code.write_call(label, n_args)

        #self.xml += '</subroutineCall>\n'
        return

    def compileExpressionList(self) -> int:
        self.xml += '<expressionList>\n'
        count = 0

        while True:
            if type(self.tokens.current_token) in [IntegerValueToken, StringValueToken, IdentifierToken]:
                self.compileExpression()
                count += 1

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
                    count += 1

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
                    count += 1

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
        # return number of arguments
        return count

    def compileString(self, string: str):
        # TODO String create and push to stack
        self.vm_code.write_push(SEGMENT.CONST, len(string))
        self.vm_code.write_call("String.new", 1)
        for char in string:
            self.vm_code.write_push(SEGMENT.CONST, ord(char))
            self.vm_code.write_call("String.appendChar", 2)