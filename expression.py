"""
Tools for building arithmetic expressions to execute with SMC.

Example expression:
>>> alice_secret = Secret()
>>> bob_secret = Secret()
>>> expr = alice_secret * bob_secret * Scalar(2)

MODIFY THIS FILE.
"""

import numpy as np
import base64
import random
from typing import Optional


ID_BYTES = 4


def gen_id() -> bytes:
    id_bytes = bytearray(
        random.getrandbits(8) for _ in range(ID_BYTES)
    )
    return base64.b64encode(id_bytes)

class Expression:
    """
    Base class for an arithmetic expression.
    """

    def __init__(
            self,
            id: Optional[bytes] = None
        ):
        # If ID is not given, then generate one.
        if id is None:
            id = gen_id()
        self.id = id
        self.tree = None
        self.current_value = None
        self.number_of_parties = 0
        
        self.priority = 0
        self.command_list = []
        
    def create_command(self, symbol, new_expr):
        right_expr, left_expr = new_expr.tree.right, new_expr.tree.left
        expr_id, priority = new_expr.id, new_expr.priority
        command = [priority, (right_expr.id, right_expr.priority), (left_expr.id, left_expr.priority), expr_id]
        new_expr.command_list += [command]
        new_expr.command_list += right_expr.command_list
        new_expr.command_list += left_expr.command_list
        
    def add_to_tree(self, other, symbol):
        new_tree = Node(symbol)
        new_tree.left = self
        new_tree.right = other
        
        new_expr = Expression()
        new_expr.tree = new_tree
        #new_expr.value = self.value + other.value
        new_expr.number_of_parties = self.number_of_parties + other.number_of_parties
        new_expr.priority = max(new_tree.left.priority, new_tree.right.priority) + 1
        
        self.create_command(symbol, new_expr)
        return new_expr

    def __add__(self, other):
        symbol = '+'
        return self.add_to_tree(other, symbol)
        #raise NotImplementedError("You need to implement this method.")


    def __sub__(self, other):
        symbol = '-'
        return self.add_to_tree(other, symbol)
    
    def __mul__(self, other):
        symbol = '*'
        return self.add_to_tree(other, symbol)
    
    def __repr__(self):
        if self is None:
            return ''
        if self.tree.data == '*':
            return f"{repr(self.tree.left)} {self.tree.data} {self.tree.right}"
        return f"({repr(self.tree.left)} {self.tree.data} {self.tree.right})"
    
    def __hash__(self):
        return hash(self.id)


    # Feel free to add as many methods as you like.


class Scalar(Expression):
    """Term representing a scalar finite field value."""

    def __init__(
            self,
            value: int,
            id: Optional[bytes] = None
        ):
        super().__init__(id)
        self.value = value

        


    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.value)})"


    def __hash__(self):
        return


    # Feel free to add as many methods as you like.


class Secret(Expression):
    """Term representing a secret finite field value (variable)."""

    def __init__(
            self,
            value: Optional[int] = None,
            id: Optional[bytes] = None
        ):
        super().__init__(id)
        self.number_of_parties = 1
        self.value = value



    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.value if self.value is not None else ''})"
        )


    # Feel free to add as many methods as you like.

    
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data


# Feel free to add as many classes as you like.