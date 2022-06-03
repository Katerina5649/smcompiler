"""
Integration tests that verify different aspects of the protocol.
You can *add* new tests here, but it is best to  add them to a new test file.

ALL EXISTING TESTS IN THIS SUITE SHOULD PASS WITHOUT ANY MODIFICATION TO THEM.
"""

import time
from multiprocessing import Process, Queue

import pytest

from expression import Scalar, Secret
from protocol import ProtocolSpec
from server import run

from smc_party import SMCParty


def smc_client(client_id, prot, value_dict, queue):
    cli = SMCParty(
        client_id,
        "localhost",
        5000,
        protocol_spec=prot,
        value_dict=value_dict
    )
    res = cli.run()
    queue.put(res)
    print(f"{client_id} has finished!")


def smc_server(args):
    run("localhost", 5000, args)


def run_processes(server_args, *client_args):
    queue = Queue()

    server = Process(target=smc_server, args=(server_args,))
    clients = [Process(target=smc_client, args=(*args, queue)) for args in client_args]

    server.start()    #<--------!
    time.sleep(3)
    for client in clients:
        client.start()

    results = list()
    for client in clients:
        client.join()

    for client in clients:
        results.append(queue.get())

    server.terminate()
    server.join()

    # To "ensure" the workers are dead.
    time.sleep(2)

    print("Server stopped.")

    return results


def suite(parties, expr, expected):
    participants = list(parties.keys())

    prot = ProtocolSpec(expr=expr, participant_ids=participants)
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]

    results = run_processes(participants, *clients)

    for result in results:
        assert result == expected


def test_suite_add(n):
    parties = {}
    expr = None
    
    for i in range(n):
        secret = Secret()
        if expr is None:
            expr = secret
        else:
            expr += secret
            
        parties['A' + str(i)] = {secret : 1}
        
    expected = n
    suite(parties, expr, expected)
    print('Test passed')
    

def test_suite_mult(n):
    parties = {}
    expr = None
    
    for i in range(n):
        secret = Secret()
        if expr is None:
            expr = secret
        else:
            expr *= secret
            
        parties['A' + str(i)] = {secret : 2}
        
    expected = 2**n
    suite(parties, expr, expected)
    print('Test passed')
    
import seaborn as sns
sns.set_style("darkgrid")
import pylab as plb
import matplotlib.pyplot as plt
plb.rcParams['font.size'] = 14


if __name__ == "__main__":
    add_time_logs = []
    mult_time_logs = []
    n = 80
    start = time.time()
    test_suite_mult(n)
    end = time.time() - start
    print(f'\n \n {n} {end}')
    
    
    
    
    
    