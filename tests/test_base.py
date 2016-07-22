from random import shuffle

from py_search.base import FIFOQueue
from py_search.base import LIFOQueue
from py_search.base import PriorityQueue

def test_fifo_queue():
    """
    Ensure that elements are added and removed in a first in
    first out order.
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    fifo = FIFOQueue()
    for e in random_elements:
        fifo.push(e)
    output = []
    while len(fifo) > 0:
        output.append(fifo.pop())

    assert output == random_elements

def test_lifo_queue():
    """
    Ensure that all elements are added and removed in a last in
    first out order.
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    lifo = LIFOQueue()
    for e in random_elements:
        lifo.push(e)
    output = []
    while len(lifo) > 0:
        output.append(lifo.pop())

    random_elements.reverse()
    assert output == random_elements

def test_priority_queue():
    """
    Ensure the priority set is sorting elements correctly.
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    pq = PriorityQueue(node_value=lambda x: x)
    for e in random_elements:
        pq.push(e)
    output = []
    while len(pq) > 0:
        output.append(pq.pop())

    random_elements.sort()
    assert output == random_elements

def test_priority_queue_max_length():
    """
    Ensure the priority queue is enforcing a max length
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    pq = PriorityQueue(node_value=lambda x: x, max_length=3)
    for e in random_elements:
        pq.push(e)
    output = []
    while len(pq) > 0:
        output.append(pq.pop())

    random_elements.sort()
    assert output == random_elements[:3]

def test_priority_queue_cost_limit():
    """
    Ensure the priority queue is enforcing a cost limit
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    pq = PriorityQueue(node_value=lambda x: x, cost_limit=3)
    for e in random_elements:
        pq.push(e)
    output = []
    while len(pq) > 0:
        output.append(pq.pop())

    random_elements.sort()
    assert output == random_elements[:4]
