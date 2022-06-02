"""
Trusted parameters generator.

MODIFY THIS FILE.
"""

import collections
from typing import (
    Dict,
    Set,
    Tuple,
)
import numpy as np
from communication import Communication
from secret_sharing import(
    share_secret,
    Share,
)

# Feel free to add as many imports as you want.


class TrustedParamGenerator:
    """
    A trusted third party that generates random values for the Beaver triplet multiplication scheme.
    """

    def __init__(self):
        self.participant_ids = []
        self.dictionary_a = {}
        self.dictionary_b = {}
        self.dictionary_c = {}

    def generate_a_b_c(self):
        a, b = np.random.randint(low = 0,high = 1000,  size=2)
        c = a*b

        a_additive = np.random.randint(low = 0,high = 1000,  size=len(self.participant_ids))
        a_additive[0] = a - sum(a_additive[1:])
        b_additive = np.random.randint(low = 0,high = 1000,  size=len(self.participant_ids))
        b_additive[0] = b - sum(b_additive[1:])
        c_additive = np.random.randint(low = 0,high = 1000,  size=len(self.participant_ids))
        c_additive[0] = c - sum(c_additive[1:])
        
        return a_additive, b_additive, c_additive
    
    
    def add_participant(self, participant_id: str) -> None:
        """
        Add a participant.
        """
        self.participant_ids.append(participant_id)
       

    def retrieve_share(self, client_id: str, op_id: str) -> Tuple[Share, Share, Share]:
        """
        Retrieve a triplet of shares for a given client_id.
       
        """
        if op_id not in self.dictionary_a.keys():
            a, b, c = self.generate_a_b_c()
            self.dictionary_a[op_id] = a
            self.dictionary_b[op_id] = b
            self.dictionary_c[op_id] = c
            
        i = self.participant_ids.index(client_id)
        #return (self.a_additive[i], self.b_additive[i], self.c_additive[i])
        return (Share(self.dictionary_a[op_id][i], i), Share(self.dictionary_b[op_id][i], i), Share(self.dictionary_c[op_id][i], i))
        
        
        
        
        

    # Feel free to add as many methods as you want.
