import numpy as np

import pop2net as p2n
import pop2net.utils as utils


def test_group_it_1():
    input_output = [
        (-1000, np.nan),
        (-1, np.nan),
        (0, 0),
        (3, 0),
        (7, 0),
        (10, 10),
        (15, 10),
        (96, 90),
        (100, 100),
        (150, 100),
        (10000, 100),
    ]

    for input, output in input_output:
        assert (
            utils.group_it(
                value=input,
                start=0,
                step=10,
                n_steps=11,
                return_value="lower_bound",
                summarize_highest=True,
            )
            is output
        )


def test_group_it_2():
    input_output = [
        (-1000, np.nan),
        (-1, np.nan),
        (0, 0),
        (3, 0),
        (7, 0),
        (10, 10),
        (15, 10),
        (96, 90),
        (100, 100),
        (150, np.nan),
        (10000, np.nan),
    ]

    for input, output in input_output:
        assert (
            utils.group_it(
                value=input,
                start=0,
                step=10,
                n_steps=11,
                return_value="lower_bound",
                summarize_highest=False,
            )
            is output
        )


def test_group_it_3():
    input_output = [
        (-1000, np.nan),
        (-1, np.nan),
        (0, 0),
        (3, 0),
        (7, 0),
        (10, 1),
        (15, 1),
        (96, 9),
        (100, 10),
        (150, 10),
        (10000, 10),
    ]

    for input, output in input_output:
        assert (
            utils.group_it(
                value=input,
                start=0,
                step=10,
                n_steps=11,
                return_value="index",
                summarize_highest=True,
            )
            is output
        )


def test_group_it_4():
    input_output = [
        (0, (0, 10)),
        (3, (0, 10)),
        (7, (0, 10)),
        (10, (10, 20)),
        (15, (10, 20)),
        (96, (90, 100)),
        (100, (100, 110)),
        (150, (100, 110)),
        (10000, (100, 110)),
    ]

    for input, output in input_output:
        assert (
            utils.group_it(
                value=input,
                start=0,
                step=10,
                n_steps=11,
                return_value="range",
                summarize_highest=True,
            )
            == output
        )


def test_to_list():
    assert utils._to_list(3) == [3]
    assert utils._to_list([3]) == [3]
    assert utils._to_list(None) == [None]
    assert utils._to_list([]) == []


def test_get_cls_as_str():
    class MyLocation(p2n.MagicLocation):
        pass

    assert utils._get_cls_as_str(MyLocation) == "MyLocation"
    assert utils._get_cls_as_str(p2n.Agent) == "Agent"


def test_join_positions():
    assert utils._join_positions(pos1="a", pos2="b") == "a-b"
    assert utils._join_positions(pos1="b", pos2="a") == "a-b"
    assert utils._join_positions(pos1=0, pos2=1) == "0-1"
    assert utils._join_positions(pos1=1, pos2=0) == "0-1"
