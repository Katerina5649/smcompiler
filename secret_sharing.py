"""
Secret sharing scheme.
"""

from typing import List
import numpy as np

class Share:
    """
    A secret share in a finite field.
    """

    def __init__(self, value, idx,  *args, **kwargs):
        self.value = int(value)
        self.idx = idx
        # Adapt constructor arguments as you wish
        #raise NotImplementedError("You need to implement this method.")

    def __repr__(self):
        # Helps with debugging.
        return 'Share(' + str(self.value) + ')'
        #raise NotImplementedError("You need to implement this method.")

    def __add__(self, other):
        if self.idx == -1 and other.idx == -1:
            return Share(self.value + other.value, -1)
        if self.idx == -1:
            return Share(self.value + other.value, other.idx) if other.idx == 0 else Share(other.value, other.idx)
        if other.idx == -1:
            return Share(self.value + other.value, self.idx) if self.idx == 0 else Share(self.value, self.idx)
        return Share(self.value + other.value, self.idx)
       
        
        #raise NotImplementedError("You need to implement this method.")

    def __sub__(self, other):
        
        if self.idx == -1 and other.idx == -1:
            return Share(self.value - other.value, -1)
        if self.idx == -1:
            return Share(self.value - other.value, other.idx) if other.idx == 0 else Share(other.value, other.idx)
        if other.idx == -1:
            return Share(self.value - other.value, self.idx) if self.idx == 0 else Share(self.value, self.idx)
        return Share(self.value - other.value, self.idx)

        raise NotImplementedError("You need to implement this method.")

    def __mul__(self, other):
        if self.idx == -1 or other.idx == -1:
            return Share(self.value * other.value, max(self.idx, other.idx))
        raise NotImplementedError("You need to implement this method.")


def share_secret(secret: int, num_shares: int) -> List[Share]:
    """Generate secret shares."""
    additive_secret = np.random.randint(low = -100,high = 100,  size=num_shares)
    additive_secret[0] = secret - sum(additive_secret[1:])
    
    
    return [Share(additive_secret[i], i) for i in range(num_shares)]
    
    #raise NotImplementedError("You need to implement this method.")


def reconstruct_secret(shares: List[Share]) -> int:
    """Reconstruct the secret from shares."""
    return sum(shares)
    #raise NotImplementedError("You need to implement this method.")


# Feel free to add as many methods as you want.
