"""
Implementation of an SMC client.

MODIFY THIS FILE.
"""
# You might want to import more classes if needed.

import collections
import json
from typing import (
    Dict,
    Set,
    Tuple,
    Union
)
import importlib
import time
import json
from communication import Communication
from expression import (
    Expression,
    Secret
)
from protocol import ProtocolSpec
import secret_sharing
from secret_sharing import(
    reconstruct_secret,
    share_secret,
    Share,
)

# Feel free to add as many imports as you want.


class SMCParty:
    """
    A client that executes an SMC protocol to collectively compute a value of an expression together
    with other clients.

    Attributes:
        client_id: Identifier of this client
        server_host: hostname of the server
        server_port: port of the server
        protocol_spec (ProtocolSpec): Protocol specification
        value_dict (dict): Dictionary assigning values to secrets belonging to this client.
    """

    def __init__(
            self,
            client_id: str,
            server_host: str,
            server_port: int,
            protocol_spec: ProtocolSpec,
            value_dict: Dict[Secret, int]
        ):
        self.comm = Communication(server_host, server_port, client_id)

        self.client_id = client_id
        self.protocol_spec = protocol_spec
        self.value_dict = value_dict
        self.participants = sorted(protocol_spec.participant_ids.copy())
        self.additive_secret_idx = self.participants.index(self.client_id)
        # who will add constants
        self.first_member = min(self.participants)
        
        self.secrets_idx = protocol_spec.expr.secrets_idx
        self.self_secrets = []




    def run(self) -> int:
        """
        The method the client use to do the SMC.
        """
        self.tasks = self.protocol_spec.expr.command_list
        #self commands by priority
        self.tasks.sort(key=lambda x: x[0])
        self.constants = self.protocol_spec.expr.constants
        

        
        for x in self.value_dict.keys():
            value = self.value_dict[x]
            secret_idx = x.id.decode('utf-8')
            self.self_secrets += [secret_idx]
            additive_secret = share_secret(value, len(self.participants))
            for i, client in enumerate(self.participants):
                self.comm.send_private_message(client, secret_idx, str(additive_secret[i].value))
                
        
        self.additive_secrets_dict = self.constants
        for secret_id in self.secrets_idx:
            
            mess = self.comm.retrieve_private_message(secret_id)
            value = mess.decode('utf-8')
            self.additive_secrets_dict[secret_id] = Share(value, self.additive_secret_idx)
                      
        for command in self.tasks:
            priority, operator, (left_id, left_priority), (right_id, right_priority), new_id = command
            new_id = new_id.decode('utf-8')
            left = self.additive_secrets_dict[left_id]
            right = self.additive_secrets_dict[right_id]
            self.additive_secrets_dict[new_id] = self.process_command(priority, operator, left, right, new_id)
            
        
        self.comm.publish_message('final_result', str(self.additive_secrets_dict[new_id].value))
        
        result = 0
        for i, client in enumerate(self.participants):
            mess = self.comm.retrieve_public_message(client, 'final_result')
            result += int(mess)
        return result 
    

    def process_command(
            self,
            priority,
            operator,
            left,
            right,
            new_id
        ) -> Share:
        if type(left) == type(2): 
            left = Share(left, -1)
        if type(right) == type(2):
            right = Share(right, -1)  
            
        if operator == '+':
            return  right + left 
        if operator == '-':
            return  right - left 
        if operator == '*':
            if right.idx == -1 or left.idx == -1:
                return  right * left 
            a, b, c = self.comm.retrieve_beaver_triplet_shares(new_id)
            for i, client in enumerate(self.participants):
                mess = f'{left.value - a} {right.value - b}'
            
                self.comm.publish_message(new_id, str(mess))

            x_a, y_b = 0, 0
            for i, client in enumerate(self.participants):
                mess = self.comm.retrieve_public_message(client, new_id).decode("utf-8")
                mess = mess.split(' ')
                x_a += int(mess[0])
                y_b += int(mess[1])

            add = -x_a*y_b if self.additive_secret_idx == 0 else 0
            return Share(c + left.value*y_b + right.value*x_a + add, self.additive_secret_idx )
                

