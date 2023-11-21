from enum import Enum
from typing import Union, Tuple, Iterator, List, Any, Iterable, Dict
import re

# ! PUT INTO UTIL CLASS
class SmartIter:
    def __init__(self, iter: Iterable):
        self.values = tuple(iter)
        self.counter = 0
    def __next__(self):
        if self.counter == len(self.values):
            raise StopIteration()
        self.counter += 1
        return self.values[self.counter-1]
    def look_ahead(self, num):
        if self.counter + num >= len(self.values): return ' '
        else: return self.values[self.counter-1 + num]
    def reverse(self, num):
        self.counter -= num

def find_first(string: str, chars: List[str]):
    lowest = None
    for char in (chars):
        try:
            index = string.index(char)
        except ValueError:
            continue
        if lowest == None:
            lowest = index
        else:
            lowest = min(lowest, index)
    return lowest
def find_last(string: str, chars: List[str]):
    highest = None
    for char in (chars):
        try:
            index = string.rindex(char)
        except ValueError:
            continue
        if highest == None:
            highest = index
        else:
            highest = max(highest, index)
    return highest
        




class SyntaxTokenType(Enum):
    NONE = 0
    IDENIFIER = 1
    SYMBOL = 2
    STRING = 3
    REGEX_STRING = 4
class SyntaxToken:
    token_type: SyntaxTokenType = SyntaxTokenType.NONE
    value: str = ''
    def __repr__(self):
        out = self.token_type.name
        out += ':' + self.value
        return out

def check_for_identifier(rule, ruleSet, scope):
    if scope > 1:
        return rule, scope
    if type(rule) == IdentifierRule:
        if rule.rule in ruleSet.terminals_dict.keys():
            rule = ruleSet.terminals_dict[rule.rule]
            rule, _ = check_for_identifier(rule, ruleSet, scope+1)
        elif rule.rule in ruleSet.non_terminals_dict.keys():
            rule = ruleSet.non_terminals_dict[rule.rule].rule
            rule, _ = check_for_identifier(rule, ruleSet, scope+1)
        else:
            assert False, "IDEK Anymore"
    return rule, scope + 2

class Terminal:
    pass
class RegexTerminal(Terminal):
    def __init__(self, identifier: str, regex: str) -> None:
        self.identifier: str = identifier
        self.expression: str = regex
    def __repr__(self):
        return f"Terminal {self.identifier} REGEX"
    def check_valid(self, query: str, ruleSet=None) -> bool:
        start_re = find_first(self.expression, '[(')
        end_re = find_last(self.expression, '])+*')
        length = len(query)

        if length <= start_re:
            return query == self.expression[:length]
        else:
            return query[:start_re] == self.expression[:start_re] and \
                (re.fullmatch(self.expression[start_re:end_re+1], query[start_re:]) or \
                 re.fullmatch(self.expression[start_re:], query[start_re:])) 
        
    def is_valid(self, query: str, ruleSet, scope=None) -> bool:
        if type(query) == str:
            return re.fullmatch(self.expression, token.value), query, ruleSet    
        try:
            token: TerminalToken = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        return re.fullmatch(self.expression, token.value), query, ruleSet
    def is_possible(self, query: str, ruleSet, scope=None) -> bool:
        if type(query) == str:
            return self.check_valid(query, ruleSet), query, ruleSet
        try:
            token: TerminalToken = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        return self.check_valid(token.value, ruleSet), query, ruleSet
        
class LiteralTerminal(Terminal):
    def __init__(self, identifier: str, literals: Tuple[str]):
        self.identifier: str = identifier
        self.literals = tuple(literals)
    def __repr__(self):
        return f"Terminal {self.identifier} LITERAL"
    def check_valid(self, query: str) -> bool:
        if query in self.literals: return True
        for literal in self.literals:
            if len(query) > len(literal): continue
            if query == literal[:len(query)]:
                return True
        return False
    
    def is_valid(self, query: str, ruleSet, scope=None) -> bool:
        if type(query) == str:
            return (query in self.literals), query, ruleSet    
        
        try:
            token: TerminalToken = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        return (token.value in self.literals), query, ruleSet
    def is_possible(self, query: str, ruleSet, scope=None) -> bool:
        if type(query) == str:
            return self.check_valid(query), query, ruleSet
        try:
            token: TerminalToken = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        return self.check_valid(token.value), query, ruleSet


class TerminalToken:
    rule_identifier: str
    value: str
    def __repr__(self):
        return f"{self.rule_identifier}:{self.value}"


class BaseRule:
    rule: Any
    def __init__(self, rule: Any):
        self.rule = rule
    def __repr__(self):
        return f"<{type(self).__name__}:{repr(self.rule)}>"
    def is_valid(self, query: TerminalToken, ruleSet) -> Tuple[bool, List[TerminalToken], Any]:
        return
    def is_possible(self, query: TerminalToken, ruleSet) -> Tuple[bool, List[TerminalToken], Any]:
        return
class IdentifierRule(BaseRule):
    # stores a string that is the name of either a terminal or non-terminal rule
    rule: str
    def is_valid(self, query: List[TerminalToken], ruleSet, scope=None) -> Tuple[bool, List[TerminalToken], Any]:
        # ? assert token.rule_identifier == self.rule ?
        ruleSet.terminals: List[Union[RegexTerminal, LiteralTerminal]]
        ruleSet.non_terminals: List[Union[IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule]]

        try:
            token = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        
        if token.rule_identifier in ruleSet.terminals_dict.keys():
            terminal: Union[RegexTerminal, LiteralTerminal] = ruleSet.terminals_dict[token.rule_identifier]

            return terminal.is_valid(token.value, ruleSet, scope), query, ruleSet
        
        else:
            assert token.rule_identifier in ruleSet.non_terminals_dict.keys(), "invalid identifier rule"
            non_terminal: Union[IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule] = \
                ruleSet.non_terminals[token.rule_identifier]
            
            return non_terminal.is_valid(token.value, ruleSet, scope), query, ruleSet
    def is_possible(self, query: TerminalToken, ruleSet, scope=None) -> Tuple[bool, List[TerminalToken], Any]:
        ruleSet.terminals: List[Union[RegexTerminal, LiteralTerminal]]
        ruleSet.non_terminals: List[Union[IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule]]

        try:
            token = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        
        if token.rule_identifier in ruleSet.terminals_dict.keys():
            terminal: Union[RegexTerminal, LiteralTerminal] = ruleSet.terminals_dict[token.rule_identifier]
            boolean, _, _ = terminal.is_possible(token.value, ruleSet, scope)
            return boolean, query, ruleSet
        
        else:
            assert token.rule_identifier in ruleSet.non_terminals_dict.keys(), "invalid identifier rule"
            non_terminal: Union[IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule] = \
                ruleSet.non_terminals[token.rule_identifier]
            boolean = non_terminal.is_possible(token.value, ruleSet, scope)
            return boolean, query, ruleSet
class LiteralRule(BaseRule):
    rule: str
    # stores a string which must be present in the code
    def is_valid(self, query: List[TerminalToken], ruleSet, scope=None) -> Tuple[bool, List[TerminalToken], Any]:
        # ? Check is a terminal from terminal rules. Should probably most likely work without for now
        # query.rule_identifier
        try:
            token = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        return self.rule == token.value, query, ruleSet
    def is_possible(self, query: TerminalToken, ruleSet, scope=None) -> Tuple[bool, List[TerminalToken], Any]:
        # always Checking single token so no difference beween valid and possible
        # ? Check is a terminal from terminal rules. Should probably most likely work without for now
        # query.rule_identifier
        try:
            token = query.pop(0)
        except IndexError:
            return False, query, ruleSet
        return self.rule == token.value, query, ruleSet
class AnyRule(BaseRule):
    # Stores a rule that can be repeated 0 or more times
    rule: BaseRule
    def is_valid(self, query: List[TerminalToken], ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        self.rule, scope = check_for_identifier(self.rule, ruleSet, scope)

        is_valid, query, _ = self.rule.is_valid(query, ruleSet, scope)
        while is_valid:
            is_valid, query, _ = self.rule.is_valid(query, ruleSet, scope)
        return True, query, ruleSet
    def is_possible(self, query: TerminalToken, ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        # Always possible but need to take as many tokens out of query as possible
        self.rule, scope = check_for_identifier(self.rule, ruleSet, scope)

        while True:
            is_valid, query, _ = self.rule.is_valid(query, ruleSet, scope)
            if not is_valid:
                _, query, _ = self.rule.is_possible(query, ruleSet, scope)
                return True, query, ruleSet
class OptionalRule(BaseRule):
    # Stores a rule that is optional (0 or 1 times)
    rule: BaseRule
    def is_valid(self, query: List[TerminalToken], ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        self.rule, scope = check_for_identifier(self.rule, ruleSet, scope)

        is_valid, new_query, _ = self.rule.is_valid(query, ruleSet, scope)
        if is_valid:
            return True, new_query, ruleSet
        else:
            return True, query, ruleSet
    def is_possible(self, query: TerminalToken, ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        # Always possible but need to take as many tokens out of query as possible
        self.rule, scope = check_for_identifier(self.rule, ruleSet, scope)

        _, query, _ = self.rule.is_possible(query, ruleSet, scope)
        return True, query, ruleSet
class UnionRule(BaseRule):
    # Stores a list of rules where only one is present
    rule: List[BaseRule]
    def is_valid(self, query: List[TerminalToken], ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        scope += 1
        for i in range(len(self.rule)):
            self.rule[i], _ = check_for_identifier(self.rule[i], ruleSet, scope-1)

        for rule in self.rule:
            query: List[TerminalToken]
            is_valid: bool
            is_valid, new_query, _ = rule.is_valid(query, ruleSet, scope)
            if is_valid: return True, new_query, ruleSet
        return False, query, ruleSet
    def is_possible(self, query: TerminalToken, ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        scope += 1
        for i in range(len(self.rule)):
            self.rule[i], _ = check_for_identifier(self.rule[i], ruleSet, scope-1)

        for rule in self.rule:
            is_possible, new_query, _ = rule.is_possible(query, ruleSet, scope)
            if is_possible:
                return True, new_query, ruleSet
        return False, query, ruleSet
class SequenceRule(BaseRule):
    # stores a list of rules where each must be present
    rule: List[BaseRule]
    def is_valid(self, query: List[TerminalToken], ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        scope += 1
        for i in range(len(self.rule)):
            self.rule[i], _ = check_for_identifier(self.rule[i], ruleSet, scope-1)

        for rule in self.rule:
            query: List[TerminalToken]
            is_valid: bool
            is_valid, query, _ = rule.is_valid(query, ruleSet, scope)
            if not is_valid: return False, query, ruleSet
        return True, query, ruleSet
    def is_possible(self, query: TerminalToken, ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        scope += 1
        for i in range(len(self.rule)):
            self.rule[i], _ = check_for_identifier(self.rule[i], ruleSet, scope-1)

        possible = False
        for rule in self.rule:
            rule: BaseRule
            is_valid, new_query, _ = rule.is_valid(query, ruleSet, scope)
            if is_valid:
                possible = True
                query = new_query
                continue
            is_possible, new_query, _ = rule.is_possible(query, ruleSet, scope)
            if is_possible:
                return True, new_query, ruleSet
            else:
                return possible, query, ruleSet

class NonTerminal:
    def __init__(self, idenifier: str):
        self.identifier: str = idenifier
        self.rule: BaseRule = None
    def __repr__(self):
        return f"NONTERMINALRULE: {self.identifier}: {repr(self.rule)}"
    def is_valid(self, query: TerminalToken, ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        self.rule, scope = check_for_identifier(self.rule, ruleSet, scope)
        return self.rule.is_valid(query, ruleSet, scope)
    def is_possible(self, query: TerminalToken, ruleSet, scope) -> Tuple[bool, List[TerminalToken], Any]:
        self.rule, scope = check_for_identifier(self.rule, ruleSet, scope)
        return self.rule.is_possible(query, ruleSet, scope)
    

class RuleSet:
    terminals: List[Union[RegexTerminal,LiteralTerminal]]
    non_terminals: List[NonTerminal]
    def __init__(self, 
                 terminals: List[Union[RegexTerminal,LiteralTerminal]], 
                 non_terminals: List[NonTerminal]
                 ):
        self.terminals = terminals
        self.terminals_dict = {k.identifier : k for k in terminals}
        self.non_terminals = non_terminals
        self.non_terminals_dict = {k.identifier : k for k in non_terminals}


class TokeniserFactory:
    class MetaParser:
        def __init__(self, input: str):
            self.syntax: str = input
            self.tokens: List[SyntaxToken] = []
            self.terminals: List[Union[RegexTerminal,LiteralTerminal]] = []
            self.non_terminals: List[Union[IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule]] = []

        def tokenise(self):
            tokens = []

            i = iter(self.syntax)
            use_next_char = False
            next_char = ' '

            while True:
                if use_next_char:
                    char = next_char
                    use_next_char = False
                else:
                    try:
                        char: str = next(i)
                    except StopIteration:
                        break

                if char in '#|:;*?()':
                    # symbol

                    token = SyntaxToken()
                    token.token_type = SyntaxTokenType.SYMBOL
                    token.value = char
                    tokens.append(token)

                    continue
                    
                elif char.isalpha():
                    
                    if not char == 'r':
                        # identifier
                        value = ''
                        next_char = char

                        while next_char.isalpha():
                            value = value + next_char
                            next_char = next(i)

                        token = SyntaxToken()
                        token.token_type = SyntaxTokenType.IDENIFIER
                        token.value = value
                        tokens.append(token)

                        use_next_char = True
                        continue
            
                    else:
                        # identifier | regex
                        next_char = next(i)
                        if not next_char == "'":
                            # identifier
                            value = char

                            while next_char.isalpha():
                                value = value + next_char
                                next_char = next(i)

                            token = SyntaxToken()
                            token.token_type = SyntaxTokenType.IDENIFIER
                            token.value = value
                            tokens.append(token)

                            use_next_char = True
                            continue
                            
                        else: # next_char = "'"
                            # regex
                            value = ''

                            next_char = next(i)
                            while True:
                                if next_char == "'" and char != '\\':
                                    break
                                char = next_char

                                value = value + next_char
                                next_char = next(i)

                            token = SyntaxToken()
                            token.token_type = SyntaxTokenType.REGEX_STRING
                            token.value = value
                            tokens.append(token)

                            continue

                elif char == "'":
                    value = ''
                    next_char = next(i)
                    while True:
                        if next_char == "'" and char != '\\':
                            break
                        char = next_char

                        value = value + next_char
                        next_char = next(i)

                    token = SyntaxToken()
                    token.token_type = SyntaxTokenType.STRING
                    token.value = value
                    tokens.append(token)

                    continue

            self.tokens = tokens

                
        def parse(self):
            def parseTerminals(i: Iterator[SyntaxToken]) -> Tuple[SyntaxToken, Iterator[SyntaxToken], List[Union[RegexTerminal,LiteralTerminal]]]:
                terminals = []
                def parseTerminal(tokens: Tuple[SyntaxToken]) -> Terminal:
                    assert tokens[0].token_type == SyntaxTokenType.IDENIFIER, 'First token in a terminal rule should be an identifier'
                    terminal_identifier = tokens[0].value
                    assert tokens[1].token_type == SyntaxTokenType.SYMBOL and tokens[1].value == ':', "Second token in a terminal rule should be SYMBOL::"

                    assert tokens[-1].token_type == SyntaxTokenType.SYMBOL and tokens[-1].value == ';', "Terminal rule should end with SYMBOL:;"

                    if tokens[2].token_type == SyntaxTokenType.REGEX_STRING:
                        # REGEX TERMINAL
                        assert len(tokens) == 4, "Regex terminal rules should only contain 4 tokens"
                        terminal = RegexTerminal(terminal_identifier, tokens[2].value)
                        return terminal
                    
                    else:
                        assert tokens[2].token_type == SyntaxTokenType.STRING, "Third token in a literal terminal rule should be a literal"
                        # LITERAL TERMINAL
                        literals: List[str] = []
                        number_of_literals = ( len(tokens)-2 ) // 2
                        for i in range(number_of_literals):
                            is_last_literal = (i == number_of_literals - 1)
                            assert tokens[2+(i*2)].token_type == SyntaxTokenType.STRING, f"Token {2+(i*2)} should be a literal"
                            assert tokens[2+(i*2)+1].token_type == SyntaxTokenType.SYMBOL and tokens[2+(i*2)+1].value == ('|' if not is_last_literal else ';'), f"Token {2+(i*2)+1} should be SYMBOL:{('|' if not is_last_literal else ';')}"
                            literals.append(tokens[2+(i*2)].value)

                        terminal = LiteralTerminal(terminal_identifier, literals)
                        return terminal
                
                terminal_tokens = []
                current_token_set = []

                try:
                    token = next(i)
                except StopIteration:
                    return (token, terminal_tokens)
                
                while not (token.token_type == SyntaxTokenType.SYMBOL and token.value == '#'):
                    current_token_set.append(token)
                    if token.token_type == SyntaxTokenType.SYMBOL and token.value == ';':
                        # terminal rule declaration finished
                        terminal_tokens.append(current_token_set)
                        current_token_set = []

                    try:
                        token = next(i)
                    except StopIteration:
                        return (SyntaxToken(), terminal_tokens)
                    
                for token_set in terminal_tokens:
                    terminal = parseTerminal(token_set)
                    terminals.append(terminal)

                return token, i, terminals
            
            def parseNonTerminals(i: iter) -> Tuple[SyntaxToken, Iterator[SyntaxToken], List[Union[IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule]]]:
                non_terminals = []

                def parseNonTerminal(tokens: Tuple[SyntaxToken]) -> NonTerminal:
                    assert tokens[0].token_type == SyntaxTokenType.IDENIFIER, 'First token in a terminal rule should be an identifier'
                    identifier = tokens[0].value
                    assert tokens[1].token_type == SyntaxTokenType.SYMBOL and tokens[1].value == ':', f"Second token ({tokens[1]}) in a terminal rule should be SYMBOL::"

                    assert tokens[-1].token_type == SyntaxTokenType.SYMBOL and tokens[-1].value == ';', "Terminal rule should end with SYMBOL:;"

                    def parseGrouping(tokens: Tuple[SyntaxToken]) -> BaseRule:
                        collecting_bracket: int = 0
                        bracket_collection: List[SyntaxToken] = []

                        components: List[Union[BaseRule, SyntaxToken]] = []

                        for i, token in enumerate(tokens):
                        
                            if   token.token_type == SyntaxTokenType.SYMBOL and token.value == '(':
                                collecting_bracket += 1
                            elif token.token_type == SyntaxTokenType.SYMBOL and token.value == ')':
                                collecting_bracket -= 1
                                if collecting_bracket == 0:
                                    components.append(
                                        parseGrouping(bracket_collection)
                                    )
                            elif collecting_bracket > 0:
                                bracket_collection.append(token)

                            elif token.token_type == SyntaxTokenType.SYMBOL and token.value == '*':
                                components.append(token)
                            elif token.token_type == SyntaxTokenType.SYMBOL and token.value == '?':
                                components.append(token)
                            elif token.token_type == SyntaxTokenType.SYMBOL and token.value == '|':
                                components.append(token)
                            else:
                                if token.token_type == SyntaxTokenType.STRING:
                                    components.append(LiteralRule(token.value))
                                elif token.token_type == SyntaxTokenType.IDENIFIER:
                                    components.append(IdentifierRule(token.value))

                        final: List[BaseRule] = []
                        next_is_union = False
                        for i, token in enumerate(components):
                            if type(token) == SyntaxToken:
                                if token.value == '*':
                                    last = final.pop()
                                    final.append(
                                        AnyRule(last)
                                    )
                                elif token.value == '?':
                                    last = final.pop()
                                    final.append(
                                        OptionalRule(last)
                                    )
                                elif token.value == '|':
                                    if len(final) == 0:
                                        last = final.pop()
                                        final.append(
                                            UnionRule(list(last))
                                        )
                                    else:
                                        next_is_union = True
                                        if not type(final[-1]) == UnionRule:
                                            last: UnionRule = final.pop()
                                            final.append(
                                                UnionRule(list([last]))
                                            )

                            elif type(token) in [IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule, BaseRule]:
                                if next_is_union:
                                    last: UnionRule = final.pop()
                                    last.rule.append(token)
                                    final.append(last)
                                else:
                                    final.append(token)
                        # parse as normal
                        # when reach *?, put into rule itself
                        # when get to (, collect tokens until ), recall parseGrouping
                        if len(final) == 1:
                            return final[0]
                        else:
                            return SequenceRule(final)

                    non_terminal_rule = NonTerminal(identifier)
                    non_terminal_rule.rule = parseGrouping(tokens[2:-1])

                    return non_terminal_rule
                    

                non_terminal_tokens = []
                current_token_set = []

                try:
                    token = next(i)
                except StopIteration:
                    return (token, non_terminal_tokens)
                
                while not (token.token_type == SyntaxTokenType.SYMBOL and token.value == '#'):
                    current_token_set.append(token)
                    if token.token_type == SyntaxTokenType.SYMBOL and token.value == ';':
                        # non-terminal rule declaration finished
                        non_terminal_tokens.append(current_token_set)
                        current_token_set = []

                    try:
                        token = next(i)
                    except StopIteration:
                        break
                    
                for token_set in non_terminal_tokens:
                    non_terminal = parseNonTerminal(token_set)
                    non_terminals.append(non_terminal)

                return token, i, non_terminals

            i = iter(self.tokens)
            token = next(i)

            assert (token.token_type == SyntaxTokenType.SYMBOL) and (token.value == '#'), "Next token should be SYMBOL:#"
            token = next(i)
            assert (token.token_type == SyntaxTokenType.IDENIFIER) and (token.value.upper() in ['TERMINALS', 'NONTERMINALS']), "Token after SYMBOL:# should be IDENTIFIER:TERMINALS|NONTERMINALS"

            if token.value.upper() == 'TERMINALS':
                token, i, terminals = parseTerminals(i)
                self.terminals = terminals
            else:
                token, i, nonterminals = parseNonTerminals(i)
                self.non_terminals = nonterminals

            assert (token.token_type == SyntaxTokenType.SYMBOL) and (token.value == '#'), "Next token should be SYMBOL:#"
            token = next(i)
            assert (token.token_type == SyntaxTokenType.IDENIFIER) and (token.value.upper() in ['TERMINALS', 'NONTERMINALS']), "Token after SYMBOL:# should be IDENTIFIER:TERMINALS|NONTERMINALS"

            if token.value.upper() == 'TERMINALS':
                token, i, terminals = parseTerminals(i)
                self.terminals = terminals
            else:
                token, i, nonterminals = parseNonTerminals(i)
                self.non_terminals = nonterminals


            # Extend non-terminals to terminals (remove intermediate identifiers)
            #  create terminal subsets e.g. op, uop, kwconst
            #! expression infinte loop needs a soluition (self rule?)

            #! -h tags for rules that should be passed?

    class Tokeniser:
        def __init__(self):
            self.terminals: Tuple[Union[Terminal, RegexTerminal, LiteralTerminal]] = []
            self.tokens = None
        def set_terminal_rules(self, terminals: Tuple[Terminal]):
            self.terminals = tuple(terminals)
        def tokenise(self, code: str) -> Tuple[TerminalToken]:
            # ! WARNING If youre reading this, get ready to be confused. I dont know how but it works and im not touching it again
            code = SmartIter(code)
            tokens = []

            superposition: List[Union[Terminal, RegexTerminal, LiteralTerminal]] = []
            def collapse(current: str, superposition: List[Union[Terminal, RegexTerminal, LiteralTerminal]]):
                # removed = 0
                # for i in range(len(superposition)):
                #     if not superposition[i-removed].check_valid(current):
                #         superposition.pop(i-removed)
                #         removed += 1
                # ! This is temporaty as inefficient
                # ! Revert to above but need to figure out how to check if a REGEX string could still be valid if not initially
                # ? Maybe works now? will test in the future
                superposition = []
                for rule in self.terminals:
                    if rule.check_valid(current):
                        superposition.append(rule)
                return superposition
            
            current = ''
            superposition = list(self.terminals)
            matched = False
            
            while True:
                # get new chars
                # if want to go back as looked ahead earlier, do code.reverse(num)
                try:
                    char = next(code)
                except StopIteration:
                    break
                current += char

                # collapse the possible rules
                previous_superposition = superposition.copy()
                superposition = collapse(current, superposition)


                if matched and len(superposition) == 0:
                    # * Successful match
                    #   has been matched previous iter, now failed to match
                    # ? Always taking first rule in superpositions as that should be the order they are listed in the file
                    token = TerminalToken()
                    token.rule_identifier = previous_superposition[0].identifier
                    token.value = current[:-1]
                    tokens.append(token)

                    superposition = list(self.terminals)
                    matched = False
                    current = ''
                    code.reverse(1)
                    continue

                elif len(superposition) == 0:
                    # failed to match any rules and no superpositions
                    # ignore char and restart token search
                    superposition = list(self.terminals)
                    matched = False
                    current = ''
                    continue
                matched = bool(len(superposition) > 0)

            self.tokens = tokens
            return tokens
        
    class SyntaxAnalyser:
        def __init__(self):
            self.ast = None
        def set_rules(self, 
                      terminal_rules: List[Union[RegexTerminal,LiteralTerminal]], 
                      non_terminal_rules: List[NonTerminal]
                      ):
            self.rules = RuleSet(terminal_rules, non_terminal_rules)
        def generate(self):
            for statement in self.rules.non_terminals:
                name = statement.identifier
                rule = statement.rule

                print(name)
                input(rule)
                
                class_codegen = f'class _machine_generated_{name}Object:\n'
                i = 0
                indexes: List[str] = [] # lists properties of class
                def foo(rule, class_codegen, i: int):
                    indexes: List[str] = []
                    if type(rule) == SequenceRule:
                        for sub_rule in rule.rule:
                            if type(sub_rule) == IdentifierRule:
                                class_codegen += f'\t_{sub_rule.rule}_{i} = None\n'
                                indexes.append(sub_rule.rule)
                                i += 1
                            # elif type(sub_rule) == LiteralRule:
                            #     class_codegen += f'\t_{sub_rule.rule}_{i} = None\n'
                            #     indexes.append(sub_rule.rule)
                            #     i += 1
                            else:
                                code, ind = foo(sub_rule, '', i)
                                class_codegen += code
                                indexes.extend(ind)
                                i += len(ind)

                    elif type(rule) == UnionRule:
                        class_codegen += f'\t_union_{i} = None\n'
                        indexes.append(rule.rule)
                        i += 1

                    elif type(rule) == AnyRule:
                        if type(rule.rule) == IdentifierRule:
                            class_codegen += f'\t_{rule.rule.rule}_{i} = None\n' 
                        else:
                            class_codegen += f'\t_any_{i} = None\n'
                        indexes.append(rule.rule)
                        i += 1

                    elif type(rule) == OptionalRule:
                        class_codegen += f'\t_optional_{i} = None\n'
                        indexes.append(rule.rule)
                        i += 1

                    # elif type(rule) in [AnyRule, OptionalRule]:
                    #     # should be typed as array
                    #     sub_rule = rule.rule
                    #     if type(sub_rule) == IdentifierRule:
                    #         class_codegen += f'\t_{sub_rule.rule}_{i} = None\n'
                    #         indexes.append(sub_rule.rule)
                    #         i += 1
                    #     elif type(sub_rule) == LiteralRule:
                    #         class_codegen += f'\t_{sub_rule.rule}_{i} = None\n'
                    #         indexes.append(sub_rule.rule)
                    #         i += 1
                    #     else:
                    #         code, ind = foo(sub_rule, '', i)
                    #         class_codegen += code
                    #         indexes.extend(ind)
                    #         i += len(ind)

                    return class_codegen, indexes
                
                print(foo(rule, class_codegen, 0)[0])

                compile_codegen = f'def _machine_generated_compile{name}(query):'

                # def compileClass(tokens: Iterator) -> Tuple[Iterator, ClassObject]:
                #     classObj = classObject()

                #     assert next(tokens) == 'class'

                #     tokens, className = compileclassName(tokens)
                #     classObj.className = className

                #     assert next(tokens) =='{'

                #     tokens, CVD = classVariableDeclaration(tokens)
                #     classObj.CVD = [CVD]

        def analyse(self, tokens: List[TerminalToken]):
            (# * this is really dodgy code, hopefully wont need to interact with it ever again in my life
            # possible_rules: List[Union[RegexTerminal, LiteralTerminal, IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule]] = \
            #     [i for i in self.rules.non_terminals]

            # token_sublist: List[TerminalToken] = []

            # def collapse(
            #         query: List[TerminalToken],
            #         possible_rules: List[Union[RegexTerminal, LiteralTerminal, IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule]]
            #         ) -> List[Union[RegexTerminal, LiteralTerminal, IdentifierRule, LiteralRule, AnyRule, OptionalRule, UnionRule, SequenceRule]]:
            #     # is every possibility possible with the new query
            #     new_possibles = []
            #     for possibility in possible_rules:
            #         if possibility.is_possible(query, self.rules, 0):
            #             new_possibles.append(possibility)
            #     return new_possibles

            # while len(tokens) > 0:
            #     token_sublist.append(tokens.pop(0))

            #     possible_rules = collapse(token_sublist, possible_rules)
            #     print(token_sublist, possible_rules)
            #     input()


            # self.ast = possible_rules
            # return ast
            )
            
            #

            return

    def __init__(self, parse_data: str, code: str):
        self.meta_parser = self.MetaParser(parse_data)
        self.meta_parser.tokenise()
        self.meta_parser.parse()

        self.tokeniser = self.Tokeniser()
        self.tokeniser.set_terminal_rules(self.meta_parser.terminals)
        self.tokeniser.tokenise(code)

        self.analyser = self.SyntaxAnalyser()
        self.analyser.set_rules(self.meta_parser.terminals, self.meta_parser.non_terminals)
        self.analyser.analyse(self.tokeniser.tokens)
        
        # self.meta_parser.non_terminals
        
    

if __name__ == '__main__':
    with open('projects/10/compiler/Jack.parse') as file:
        contents = file.read()

    with open('projects/10/ArrayTest/Main.jack') as file:
        code = file.read()
    
    x = TokeniserFactory(contents, code)
    x.analyser.generate()