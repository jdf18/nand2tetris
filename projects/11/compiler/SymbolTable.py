from enum import Enum
from typing import Dict, Tuple

class KIND(Enum):
    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3

class SymbolTable:
    def __init__(self):
        # Creates a new empty symbol table
        self.class_symbol_table: Dict[str, Tuple[str, KIND, int]] = {}
        self.subroutine_symbol_table: Dict[str, Tuple[str, KIND, int]] = None
        pass
    def startSubroutine(self):
        # Starts a new subroutine scope (i.e., resets the subroutine’s symbol table).
        self.subroutine_symbol_table: Dict[str, Tuple[str, KIND, int]] = {}
        pass
    def define(self, name: str, type: str, kind: KIND):
        # Defines a new identifier of a given name, type, and kind and assigns it a running index. 
        # STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.

        # A symbol name can not be a subroutine name or class name
        pass
    def var_count(self, kind: KIND) -> int:
        # Returns the number of variables of the given kind already defined in the current scope.
        pass
    def kind_of(self, name: str) -> KIND:
        # Returns the kind of the named identifier in the current scope. 
        # If the identifier is unknown in the current scope, returns NONE.
        pass
    def type_of(self, name: str) -> str:
        # Returns the type of the named identifier in the current scope.
        pass
    def index_of(self, name: str) -> int:
        # Returns the index assigned to the named identifier.
        pass