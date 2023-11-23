from typing import List, Union
from enum import Enum

from JackTokeniser import Tokensiser, Keywords, Symbols, KeywordToken, SymbolToken, IdentifierToken, IntegerValueToken, StringValueToken

class TermStates(Enum):
    INTEGER_CONSTANT = 0
    STRING_CONSTANT = 1
    KEYWORD_CONSTANT = 2
    IDENTIFIER = 3
    IDENTIFIER_INDEX = 4
    SUBROUTINE_CALL = 5
    BRACKETS_EXPRESSION = 6
    UNARY_OPERATION = 7
    

def indent_string(string: str, indent: int):
    if string == None: return ''
    lines = string.split('\n')
    lines = map(lambda x : '\t'*indent + x + '\n', lines)
    return ''.join(lines)

class ClassObject:
    def __init__(self):
        self.name: str = None
        self.variable_declarations: List[ClassVariableDeclarationObject] = None
        self.subroutine_declaration: SubroutineDeclarationObject = None
    def toXML(self) -> str:
        out =   '<class>\n'
        out +=  '\t<keyword> class </keyword>\n'
        out += f'\t<identifier> {self.name} </identifier>\n'
        out +=  '\t<symbol> { </symbol>\n'
        if self.variable_declarations:
            out += indent_string((''.join([i.toXML() for i in self.variable_declarations])),1)
        if self.subroutine_declaration:
            out += indent_string(self.subroutine_declaration.toXML(),1)
        out +=  '\t<symbol> } </symbol>\n'
        out +=  '</class>'
        return out

class ClassVariableDeclarationObject:
    def __init__(self):
        self.is_static: bool = None
        self.is_type_keyword: bool = None
        self.type_keyword: Keywords = None
        self.type_identifier: str = None
        self.variable_names: List[str] = None
    def toXML(self) -> str:
        out =   '<classVarDec>\n'
        out += f'\t<keyword> {("static" if self.is_static else "field")} </keyword>\n'
        out += (
            f'\t<keyword> {self.type_keyword.name.lower()} </keyword>\n'
            if self.is_type_keyword else
            f'\t<identifier> {self.type_identifier} </identifier>\n'
        )
        out += f'\t<identifier> {self.variable_names[0]} </identifier>\n'
        
        if len(self.variable_names) >= 2:
            out += ''.join(map(lambda x : f'\t<symbol> , </symbol>\n\t<identifier> {x} </identifier>\n', self.variable_names[1:]))
        out += '\t<symbol> ; </symbol>\n'
        out += '</classVarDec>\n'
        return out
    def __int__(self) -> int:
        return 2 + (2 * len(self.variable_names))

class SubroutineDeclarationObject:
    def __init__(self):
        self.subroutine_type: Keywords = None
        self.is_return_type_void: bool = None
        self.is_return_type_keyword: bool = None
        self.return_type_keyword: Keywords = None
        self.return_type_identifier: str = None
        self.subroutine_name: str = None
        self.parameter_list: ParameterListObject = None
        self.subroutine_body: SubroutineBodyObject = None
    def toXML(self) -> str:
        out =   '<subroutineDec>\n'
        out += f'\t<keyword> {self.subroutine_type.name.lower()} </keyword>\n'
        out += (
            '\t<keyword> void </keyword>\n'
            if self.is_return_type_void else
            (
                f'\t<keyword> {self.return_type_keyword.name.lower()} </keyword>\n'
                if self.is_return_type_keyword else
                f'\t<identifier> {self.return_type_identifier} </identifier>\n'
            )
        )
        out += f'\t<identifier> {self.subroutine_name} </identifier>\n'
        out += '\t<symbol> ( </symbol>\n'
        out += indent_string(self.parameter_list.toXML(), 1)
        out += '\t<symbol> ) </symbol>\n'
        out += indent_string(self.subroutine_body.toXML(), 1)

        return out

class ParameterListObject:
    def __init__(self):
        self.parameter_types: List[Union[Keywords,IdentifierToken]] = []
        self.parameter_names: List[str] = []
    def toXML(self) -> str:
        if len(self.parameter_types) == 0:
            return ''
        out = '<parameterList>\n'
        for parameter_type, parameter_name in zip(self.parameter_types, self.parameter_names):
            out += (
                f'\t<keyword> {parameter_type.name.lower()} <keyword>\n'
                if type(parameter_type) == Keywords else
                f'\t<identifier> {parameter_type.identifier} </identifier>\n'
            )
            out += f'\t<identifier> {self.parameter_name} </identifier>\n'
            out += '\t<symbol> , </symbol>\n'
        
        out = out[:-len('\t<symbol> , </symbol>\n')]
        out += '</parameterList>\n'
    
class SubroutineBodyObject:
    def __init__(self):
        self.variable_declarations: List[VariableDeclarationObject] = []
        self.statements: StatementsObject = None
    def toXML(self) -> str:
        out =   '<subroutineBody>\n'
        out +=  '\t<symbol> { </symbol>\n'
        for varDec in self.variable_declarations:
            out += indent_string(varDec.toXML(), 1)
        out += indent_string(self.statements, 1)
        out +=  '\t<symbol> } </symbol>\n'
        out +=  '</subroutineBody>\n'
        return out
    
class VariableDeclarationObject:
    def __init__(self):
        self.is_type_keyword: bool = None
        self.type_keyword: Keywords = None
        self.type_identifier: str = None
        self.variable_names: List[str] = None
    def __int__(self):
        return 2 + 2*len(self.variable_names)
    def toXML(self) -> str:
        out =   '<varDec>\n'
        out +=  '\t<keyword> var </keyword>\n'
        out += (
            f'\t<keyword> {self.type_keyword.name.lower()} </keyword>\n'
            if self.is_type_keyword else
            f'\t<identifier> {self.type_identifier} </identifier>\n'
        )
        out += f'\t<identifier> {self.variable_names[0]} </identifier>\n'
        
        for name in self.variable_names[1:]:
            out +=  '\t<symbol> , </symbol>\n'
            out += f'\t<identifier> {name} </identifier>\n'
            
        out += '\t<symbol> ; </symbol>\n'
        out += '</varDec>\n'
        return out

class StatementsObject:
    def __init__(self):
        self.statements: STATEMENT_UNION = []

class LetStatementObject:
    def __init__(self):
        self.variable_name: str = None
        self.has_index: bool = None
        self.index_expression: ExpressionObject = None
        self.expression: ExpressionObject = None

class IfStatementObject:
    pass

class WhileStatementObject:
    pass

class DoStatementObject:
    pass

class ReturnStatementObject:
    pass

STATEMENT_UNION = Union[LetStatementObject, IfStatementObject, WhileStatementObject, DoStatementObject, ReturnStatementObject]

class ExpressionObject:
    def __init__(self):
        self.term: TermObject = None
        self.has_operation: bool = None
        self.operation: Symbols = None
        self.operation_term: TermObject = None

class TermObject:
    def __init__(self):
        self.term_state: TermStates = None


class ExpressionListObject:
    pass

class CompilationEngine:
    def __init__(self, tokeniser: Tokensiser):
        self.tokeniser = tokeniser
        self.tokens = self.tokeniser.tokensList
    def compileClass(self, offset: int = 0) -> ClassObject:
        self.tokens.advance()
        assert type(self.tokens.current_token) == KeywordToken
        assert self.tokens.current_token.keyword == Keywords.CLASS
        
        self.tokens.advance()
        assert type(self.tokens.current_token) == IdentifierToken
        class_name = self.tokens.current_token.identifier

        self.tokens.advance()
        assert type(self.tokens.current_token) == SymbolToken
        assert self.tokens.current_token.symbol == Symbols.LEFT_CURLY_BRACKET

        # Any classVariableDeclaration
        class_variable_declarations = []
        while True:
            token = self.tokens.look_ahead(1)
            if type(token) != KeywordToken:
                break
            elif not (token.keyword in [Keywords.STATIC, Keywords.FIELD]):
                break

            class_variable_declarations.append(self.compileClassVariableDeclaration())
            #self.tokens.advance(int(class_variable_declarations[-1]))
        
        # Any subroutineDeclaration
        class_subroutine_declaration = self.compileSubroutineDeclaration()

        class_object = ClassObject()
        class_object.name = class_name
        class_object.variable_declarations = class_variable_declarations
        class_object.subroutine_declaration = class_subroutine_declaration
        return class_object
    def compileClassVariableDeclaration(self, offset: int = 0):
        try:
            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == KeywordToken
            assert token.keyword in [Keywords.STATIC, Keywords.FIELD]
            is_static = bool(token.keyword == Keywords.STATIC)

            offset += 1
            token = self.tokens.look_ahead(offset)
            if type(token) == KeywordToken:
                assert token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
                type_is_keyword = True
                type_keyword = token.keyword
            else:
                assert type(token) == IdentifierToken
                type_is_keyword = False
                type_identifier = token.identifier
            
            # Collect variable names
            variable_names: List[str] = []
            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == IdentifierToken
            variable_names.append(token.identifier)
            while True:
                next_token = self.tokens.look_ahead(offset + 1)
                assert type(next_token) == SymbolToken
                if next_token.symbol == Symbols.SEMICOLON:
                    # end of statement
                    offset += 1
                    self.tokens.advance(n = offset)
                    break
                assert next_token.symbol == Symbols.COMMA
                
                offset += 2
                token = self.tokens.look_ahead(offset)
                assert type(token) == IdentifierToken
                variable_names.append(token.identifier)

            class_variable_declaration_object = ClassVariableDeclarationObject()
            class_variable_declaration_object.is_static = is_static
            class_variable_declaration_object.is_type_keyword = type_is_keyword
            if type_is_keyword:
                class_variable_declaration_object.type_keyword = type_keyword
            else:
                class_variable_declaration_object.type_identifier = type_identifier
            class_variable_declaration_object.variable_names = variable_names
            return class_variable_declaration_object
        except AssertionError:
            # Could not find any ClassVariableDeclarations
            return None
        except Exception as e:
            raise e
    def compileSubroutineDeclaration(self, offset: int = 0):
        try:
            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == KeywordToken
            assert token.keyword in (Keywords.CONSTRUCTOR, Keywords.FUNCTION, Keywords.METHOD)
            subroutine_type = token.keyword

            offset += 1
            token = self.tokens.look_ahead(offset)
            is_return_type_void = False
            is_return_type_keyword = False
            return_type_keyword = None
            return_type_identifier = None
            if type(token) == KeywordToken:
                if token.keyword == Keywords.VOID:
                    is_return_type_void = True
                else:
                    assert token.keyword in (Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN)
                    is_return_type_keyword = True
                    return_type_keyword = token.keyword
            else:
                assert type(token) == IdentifierToken
                return_type_identifier = token.identifier

            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == IdentifierToken
            subroutine_name = token.identifier

            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == SymbolToken
            assert token.symbol == Symbols.LEFT_BRACKET

            parameter_list = self.compileParameterList(offset=offset)

            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == SymbolToken
            assert token.symbol == Symbols.RIGHT_BRACKET

            subroutine_body = self.compileSubroutineBody(offset)

            subroutine_declaration_object = SubroutineDeclarationObject()
            subroutine_declaration_object.subroutine_type = subroutine_type
            subroutine_declaration_object.is_return_type_void = is_return_type_void
            subroutine_declaration_object.is_return_type_keyword = is_return_type_keyword
            subroutine_declaration_object.return_type_keyword = return_type_keyword
            subroutine_declaration_object.return_type_identifier = return_type_identifier
            subroutine_declaration_object.subroutine_name = subroutine_name
            subroutine_declaration_object.parameter_list = parameter_list
            subroutine_declaration_object.subroutine_body = subroutine_body
            return subroutine_declaration_object

        except AssertionError:
            # Could not find any subroutine declatations
            return None
        except Exception as e:
            raise e
    def compileParameterList(self, offset: int = 0):
        try:
            parameter_types = []
            parameter_names = []

            offset += 1
            token = self.tokens.look_ahead(offset)
            if type(token) == KeywordToken:
                assert token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
                parameter_types.append(token.keyword)
            else:
                assert type(token) == IdentifierToken
                parameter_types.append(IdentifierToken)
            
            while True:
                offset += 1
                token = self.tokens.look_ahead(offset)

                # If token is not a comma, then stop loop
                if type(token) != SymbolToken:
                    break
                elif token.symbol != Symbols.COMMA:
                    break

                offset += 1
                token = self.tokens.look_ahead(offset)
                if type(token) == KeywordToken:
                    assert token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]
                    parameter_types.append(token.keyword)
                else:
                    assert type(token) == IdentifierToken
                    parameter_types.append(IdentifierToken)
            
            parameter_list_object = ParameterListObject()
            parameter_list_object.parameter_types = parameter_types
            parameter_list_object.parameter_names = parameter_names
            return parameter_list_object

        except AssertionError:
            return ParameterListObject()
        except Exception as e:
            raise e
    def compileSubroutineBody(self, offset: int = 0):
        try:
            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == SymbolToken, "First token in subroutine body should be SYMBOL:{"
            assert token.symbol == Symbols.LEFT_CURLY_BRACKET, "First token in subroutine body should be SYMBOL:{"

            # compile any variable declarations
            variable_declarations = []
            while True:
                token = self.tokens.look_ahead(offset + 1)
                if type(token) != KeywordToken:
                    break
                elif token.keyword != Keywords.VAR:
                    break
                
                variable_declarations.append(self.compileVariableDeclaration(offset))
                offset += int(variable_declarations[-1])

            self.tokens.advance(n = offset)
            offset = 0

            statements = self.compileStatements(offset)

            subroutine_body_object = SubroutineBodyObject()
            subroutine_body_object.variable_declarations = variable_declarations
            subroutine_body_object.statements = statements
            return subroutine_body_object
        except AssertionError as e:
            print('error subroutine body', e.args)
            raise e
        except Exception as e:
            raise e
    def compileVariableDeclaration(self, offset: int = 0):
        try:
            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == KeywordToken, "First token in variable declaration should be keyword:VAR"
            assert token.keyword == Keywords.VAR, "First token in variable declaration should be keyword:VAR"

            offset += 1
            token = self.tokens.look_ahead(offset)
            type_keyword = None
            type_identifier = None
            if type(token) == KeywordToken:
                assert token.keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN], "Type token if keyword should be INT, CHAR or BOOLEAN"
                type_is_keyword = True
                type_keyword = token.keyword
            else:
                assert type(token) == IdentifierToken, "Type token if not keyword, should be identifier"
                type_is_keyword = False
                type_identifier = token.identifier
            
            # Collect variable names
            variable_names: List[str] = []
            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == IdentifierToken, "Token should be identifier for variable"
            variable_names.append(token.identifier)
            while True:
                next_token = self.tokens.look_ahead(offset + 1)
                assert type(next_token) == SymbolToken, "Token should be symbol"
                if next_token.symbol == Symbols.SEMICOLON:
                    # end of statement
                    offset += 1
                    #self.tokens.advance(n = offset)
                    break
                assert next_token.symbol == Symbols.COMMA, "Token should be comma if not semicolon"
                
                offset += 2
                token = self.tokens.look_ahead(offset)
                assert type(token) == IdentifierToken, "Token should be extra identifier for variable"
                variable_names.append(token.identifier)

            variable_declaration_object = VariableDeclarationObject()
            variable_declaration_object.is_type_keyword = type_is_keyword
            variable_declaration_object.type_keyword = type_keyword
            variable_declaration_object.type_identifier = type_identifier
            variable_declaration_object.variable_names = variable_names
            return variable_declaration_object
        except AssertionError as e:
            raise e
        except Exception as e:
            raise e
    def compileStatements(self, offset: int = 0):
        try:
            statements: List[STATEMENT_UNION] = []

            token = self.tokens.look_ahead(offset + 1)
            assert type(token) == KeywordToken, "Statements: first token should be keyword"
            print(token.keyword.name)

            if token.keyword == Keywords.LET:
                statements.append(self.compileLetStatement(offset))
            elif token.keyword == Keywords.IF:
                statements.append(self.compileIfStatement(offset))
            elif token.keyword == Keywords.WHILE:
                statements.append(self.compileWhileStatement(offset))
            elif token.keyword == Keywords.DO:
                statements.append(self.compileDoStatement(offset))
            elif token.keyword == Keywords.RETURN:
                statements.append(self.compileReturnStatement(offset))

        except AssertionError as e:
            raise e
        except Exception as e:
            raise e
    def compileLetStatement(self, offset: int = 0):
        self.tokens.debug(10, offset)

        offset += 1
        token = self.tokens.look_ahead(offset)
        assert type(token) == KeywordToken, "Let statement: First token should be keyword:LET"
        assert token.keyword == Keywords.LET, "Let statement: First token should be keyword:LET"

        offset += 1
        token = self.tokens.look_ahead(offset)
        assert type(token) == IdentifierToken, "Let statement: Second token should be identifier"
        variable_name = token.identifier

        has_index_expression = False
        index_expression = None
        token = self.tokens.look_ahead(offset + 1)
        assert type(token) == SymbolToken, "Let statement: Third token should be SYMBOL:[ OR SYMBOL:="
        
        if token.symbol == Symbols.LEFT_HARD_BRACKET:
            # list indexing
            offset += 2
            has_index_expression = True
            index_expression = self.compileExpression(offset)

            offset += 1
            token = self.tokens.look_ahead(offset)
            assert type(token) == SymbolToken, "Let statement: token should be SYMBOL:]"
            assert token.symbol == Symbols.RIGHT_HARD_BRACKET, "Let statement: token should be SYMBOL:]"
        
        offset += 1
        token = self.tokens.look_ahead(offset)
        assert type(token) == SymbolToken, "Let statement: token should be SYMBOL:="
        assert token.symbol == Symbols.EQUALS, "Let statement: token should be SYMBOL:="

        offset += 1
        main_expression = self.compileExpression(offset)

        offset += 1
        token = self.tokens.look_ahead(offset)
        assert type(token) == SymbolToken, "Let statement: token should be SYMBOL:;"
        assert token.symbol == Symbols.SEMICOLON, "Let statement: token should be SYMBOL:;"

        let_statement_object = LetStatementObject()
        let_statement_object.variable_name = variable_name
        let_statement_object.has_index = has_index_expression
        let_statement_object.index_expression = index_expression
        let_statement_object.expression = main_expression
        return let_statement_object
        
    def compileIfStatement(self, offset: int = 0):
        pass
    def compileWhileStatement(self, offset: int = 0):
        pass
    def compileDoStatement(self, offset: int = 0):
        pass
    def compileReturnStatement(self, offset: int = 0):
        pass
    def compileExpression(self, offset: int = 0):
        try:
            self.tokens.debug(10, offset)
            offset += 1
            term = self.compileTerm(offset)

            token = self.tokens.look_ahead(offset + 1)
            has_operation = False
            operation = None
            operation_term = None
            if type(token) != SymbolToken:
                pass
            elif not (token.symbol in [Symbols.PLUS, Symbols.MINUS, Symbols.ASTERISK, Symbols.FORWARDS_SLASH, Symbols.AMPERSAND, Symbols.PIPE, Symbols.GREATER_THAN, Symbols.LESS_THAN, Symbols.EQUALS]):
                pass
            else:
                has_operation = True
                operation = token.symbol
                offset += 2
                operation_term = self.compileTerm(offset)

            expression_object = ExpressionObject()
            expression_object.term = term
            expression_object.has_operation = has_operation
            expression_object.operation = operation
            expression_object.operation_term = operation_term
            return expression_object

        except AssertionError as e:
            print('error expression', e.args)
            raise e
        except Exception as e:
            raise e
    def compileTerm(self, offset: int = 0):
        offset += 1
        token = self.tokens.look_ahead(offset)
        print("compiling term", token)
        if type(token) == IntegerValueToken:
            term_state = TermStates.INTEGER_CONSTANT
        elif type(token) == StringValueToken:
            term_state = TermStates.STRING_CONSTANT
        elif type(token) == KeywordToken:
            assert token.keyword in [Keywords.TRUE, Keywords.FALSE, Keywords.NULL, Keywords.THIS], f"Invalid keyword, {token.keyword.name}"
            term_state = TermStates.KEYWORD_CONSTANT
        elif type(token) == IdentifierToken:
            # TODO check if has index
            # TODO check if subroutine call

            token_test = self.tokens.look_ahead(offset + 1)
            if type(token_test) != SymbolToken:
                term_state = TermStates.IDENTIFIER
            elif token_test.symbol == Symbols.PERIOD:
                term_state = TermStates.SUBROUTINE_CALL
                
                offset += 2
                token = self.tokens.look_ahead(offset)
                assert type(token) == IdentifierToken
                offset += 1
                token = self.tokens.look_ahead(offset)
                assert type(token) == SymbolToken
                assert token.symbol == Symbols.LEFT_BRACKET
                offset += 1
                self.compileExpressionList(offset)
                offset += 0 # TODO setup offset after compilation
                token = self.tokens.look_ahead(offset)
                assert type(token) == SymbolToken
                assert token.symbol == Symbols.RIGHT_BRACKET
            elif token_test.symbol == Symbols.LEFT_HARD_BRACKET:
                term_state = TermStates.IDENTIFIER_INDEX
                # TODO add offset
            else:
                term_state = TermStates.IDENTIFIER
            
        elif type(token) == SymbolToken:
            if token.symbol == Symbols.LEFT_BRACKET:
                term_state = TermStates.BRACKETS_EXPRESSION
            else:
                assert token.symbol in [Symbols.MINUS, Symbols.TILDA]
                term_state = TermStates.UNARY_OPERATION

        term_object = TermObject()
        term_object.term_state = term_state
        return term_object
    def compileExpressionList(self, offset: int = 0):
        pass
    # Rules without compile methods:
    # type, className, subroutineName, variableName, statement, subroutineCall