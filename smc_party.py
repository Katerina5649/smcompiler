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
        
        #self.participants.remove(client_id)
        self.secrets_idx = protocol_spec.expr.secrets_idx
        self.self_secrets = []



    def run(self) -> int:
        """
        The method the client use to do the SMC.
        """
        self.tasks = self.protocol_spec.expr.command_list
        self.tasks.sort(key=lambda x: x[0])
        self.constants = self.protocol_spec.expr.constants
        
        #self.secrets_id = [x.id.decode('utf-8') for x in self.value_dict.keys()]
        
        for x in self.value_dict.keys():
            value = self.value_dict[x]
            secret_idx = x.id.decode('utf-8')
            self.self_secrets += [secret_idx]
            additive_secret = share_secret(value, len(self.participants))
            #print(f' As {additive_secret} by {self.client_id} for {value}')
            for i, client in enumerate(self.participants):
                self.comm.send_private_message(client, secret_idx, str(additive_secret[i].value))
                #print(f'Sent {additive_secret[i].value} to {client}')
                
        
        self.additive_secrets_dict = self.constants
        for secret_id in self.secrets_idx:
            
            mess = self.comm.retrieve_private_message(secret_id)
            value = mess.decode('utf-8')
            #print(f'Recieved {mess} by {self.client_id} for {secret_id}')
            self.additive_secrets_dict[secret_id] = Share(value, self.additive_secret_idx)
            #print(self.additive_secrets_dict) 
                
        time.sleep(2)       
        for command in self.tasks:
            #print(command)
            #print(command)
            #print(self.additive_secrets_dict)
            priority, operator, (left_id, left_priority), (right_id, right_priority), new_id = command
            new_id = new_id.decode('utf-8')
            left = self.additive_secrets_dict[left_id]
            right = self.additive_secrets_dict[right_id]
            self.additive_secrets_dict[new_id] = self.process_command(priority, operator, left, right)
            
        
        print(f'Final result for {self.client_id} is {self.additive_secrets_dict[new_id]}')
        self.comm.publish_message('final_result', str(self.additive_secrets_dict[new_id].value))
        
        result = 0
        for i, client in enumerate(self.participants):
            mess = self.comm.retrieve_public_message(client, 'final_result')
            result += int(mess)
        print(f'DEBUG {self.client_id} result is {result}')
        return result 
        #self.comm.publish_message('secters_id', message)
        #print(self.client_id + ' ' + message)
        #time.sleep(3)
       
        #secrets_dict = {}
        # from every client recieve their constant
        #for client in self.participants:
        #    keys = self.comm.retrieve_public_message(client, 'secters_id').decode("utf-8").split(' ')[:-1]
        #    for key in keys:
        #        secrets_dict[key] = client
        
        #print(secrets_dict)
        # send additive secret to everyone
        #for key in self.value_dict.keys():
        #    additive_secret = share_secret(self.value_dict[key], len(self.participants))
        #    for i, client_id in enumerate(self.participants):
        #        print(client_id)
        #        self.comm.send_private_message(client_id, key.id, str(additive_secret[i]) + ' ' + str(i))
        
        #time.sleep(3)
        
        #additive_secrets_dict = {}
        #for secret in secrets_dict.keys():
        #    additive_secrets_dict[secret] = self.comm.retrieve_private_message()
        
         
        
                
       
            
            

        #raise NotImplementedError("You need to implement this method.")
        


    # Suggestion: To process expressions, make use of the *visitor pattern* like so:
    def process_command(
            self,
            priority,
            operator,
            left,
            right          
        ) -> Share:
        if type(left) == type(2):
            left = Share(left, -1)
        if type(right) == type(2):
            right = Share(right, -1)  
            
        print(f'Type debug {type(left)} and {type(right)}')  
        if operator == '+':
            return  right + left 
        if operator == '-':
            return  right - left 
             
        #    if 
        # if expr is an addition operation:
        #     ...

        # if expr is a multiplication operation:
        #     ...

        # if expr is a secret:
        #     ...

        # if expr is a scalar:
        #     ...
        #
        # Call specialized methods for each expression type, and have these specialized
        # methods in turn call `process_expression` on their sub-expressions to process
        # further.
        #pass

    # Feel free to add as many methods as you want.
