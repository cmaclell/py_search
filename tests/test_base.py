from random import shuffle

from py_search.base import FIFOQueue
from py_search.base import LIFOQueue
from py_search.base import PriorityQueue
from py_search.base import Fringe
from py_search.base import Problem
from py_search.base import AnnotatedProblem
from py_search.base import Node


def test_problem():
    """
    Tests to make sure exceptions are raised.
    """
    p = Problem(None)

    try:
        p.predecessors(p.initial)
        assert False
    except NotImplementedError:
        pass

    try:
        p.successors(p.initial)
        assert False
    except NotImplementedError:
        pass

    try:
        p.random_node()
        assert False
    except NotImplementedError:
        pass

    # test to make sure the goal test falls back on the goal specified during
    # problem construction. In this case None == None - CM
    assert p.goal_test(p.initial)

    ap = AnnotatedProblem(p)

    # Should fall back on problem, which will raise an exception.
    try:
        ap.random_node()
        assert False
    except NotImplementedError:
        pass


def test_fringe():

    f = Fringe()

    try:
        f.push(1)
        assert False
    except NotImplementedError:
        pass

    try:
        f.pop()
        assert False
    except NotImplementedError:
        pass

    try:
        len(f)
        assert False
    except NotImplementedError:
        pass

    try:
        list(f)
        assert False
    except NotImplementedError:
        pass


def test_node():
    node1 = Node(1, node_cost=1)
    node2 = Node(2, node_cost=2)

    assert node1 < node2
    assert node1 != node2

    assert repr(node1) == "Node(%s)" % repr(1)
    assert repr(node1) != repr(node2)


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

    fifo.push(1)
    fifo.push(1)
    fifo.push(1)
    assert len(fifo) == 3

    fifo.remove(1)
    assert len(fifo) == 0

    fifo = FIFOQueue()
    fifo.push(0)
    fifo.push(1)
    fifo.push(2)
    assert list(fifo) == [0, 1, 2]

    fifo.remove(2)
    assert fifo.pop() == 0
    assert fifo.pop() == 1


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

    rev_random = [e for e in lifo]
    assert [e for e in reversed(random_elements)] == rev_random

    output = []
    while len(lifo) > 0:
        output.append(lifo.pop())

    random_elements.reverse()
    assert output == random_elements

    lifo = LIFOQueue()
    lifo.push(0)
    lifo.push(1)
    lifo.push(2)
    assert list(lifo) == [2, 1, 0]

    assert lifo.pop() == 2
    assert lifo.pop() == 1
    assert lifo.pop() == 0


def test_priority_queue():
    """
    Ensure the priority set is sorting elements correctly.
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    pq = PriorityQueue()
    for e in random_elements:
        pq.push(e)

    random_elements.sort()

    assert [e for e in pq] == random_elements
    assert pq.peek() == random_elements[0]

    output = []
    while len(pq) > 0:
        output.append(pq.pop())
    assert output == random_elements

    for e in random_elements:
        pq.push(e)
    assert len(pq) == 10

    pq.update_cost_limit(5)
    assert len(pq) == 6

    output = []
    while len(pq) > 0:
        output.append(pq.pop())
    assert output == random_elements[:6]

    pq = PriorityQueue(node_value=lambda x: x, max_length=3)
    pq.push(6)
    pq.push(0)
    pq.push(2)
    pq.push(6)
    pq.push(7)

    assert len(pq) == 3
    assert list(pq) == [0, 2, 6]

    pq.update_cost_limit(5)

    assert len(pq) == 2
    assert pq.peek() == 0
    assert pq.peek_value() == 0
    assert pq.pop() == 0
    assert pq.peek() == 2
    assert pq.peek_value() == 2
    assert pq.pop() == 2
    assert len(pq) == 0


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
