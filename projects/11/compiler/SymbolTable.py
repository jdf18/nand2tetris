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
        return
    
    def __repr__(self):
        return str(self.class_symbol_table) + '\n' + str(self.subroutine_symbol_table)
    
    def startSubroutine(self):
        # Starts a new subroutine scope (i.e., resets the subroutine’s symbol table).
        self.subroutine_symbol_table: Dict[str, Tuple[str, KIND, int]] = {}
        return
    
    def define(self, name: str, type: str, kind: KIND):
        # Defines a new identifier of a given name, type, and kind and assigns it a running index. 
        # STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.

        # A symbol name can not be a subroutine name or class name
        if kind in [KIND.STATIC, KIND.FIELD]:
            new_index = self.var_count(kind)
            self.class_symbol_table.update(
                {name: (type, kind, new_index)}
            )
        else:
            new_index = self.var_count(kind)
            self.subroutine_symbol_table.update(
                {name: (type, kind, new_index)}
            )
        return
    
    def var_count(self, kind: KIND) -> int:
        # Returns the number of variables of the given kind already defined in the current scope.
        i = 0
        if kind in [KIND.STATIC, KIND.FIELD]:
            for k, v in self.class_symbol_table.items():
                if v[1] == kind:
                    i += 1
            return i
        for k, v in self.subroutine_symbol_table.items():
            if v[1] == kind:
                i += 1
        return i

    def kind_of(self, name: str) -> KIND:
        # Returns the kind of the named identifier in the current scope. 
        # If the identifier is unknown in the current scope, returns NONE.
        if name in self.subroutine_symbol_table.keys():
            return self.subroutine_symbol_table[name][1]
        return self.class_symbol_table[name][1]
    def type_of(self, name: str) -> str:
        # Returns the type of the named identifier in the current scope.
        if name in self.subroutine_symbol_table.keys():
            return self.subroutine_symbol_table[name][0]
        return self.class_symbol_table[name][0]
    def index_of(self, name: str) -> int:
        # Returns the index assigned to the named identifier.
        if name in self.subroutine_symbol_table.keys():
            return self.subroutine_symbol_table[name][2]
        return self.class_symbol_table[name][2]