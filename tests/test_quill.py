"""Chat's tests: the real record store, its spaces and gate, on this machine.

Chat has no code: everything it does is declared in quill.toml and done by
the core's spaces. These hold what the manifest promises.
"""

import pytest

from cloudmorrow.quill.testing import Harness


@pytest.fixture()
def q():
    with Harness(".") as harness:
        yield harness


def test_general_is_there_for_everybody(q):
    general = [c for c in q.list("channel") if c["name"] == "general"]
    assert general and general[0]["kind"] == "public"
    assert [c["name"] for c in q.as_user("sam").list("channel")] == ["general"]


def test_what_is_said_in_general_everybody_reads(q):
    general = next(c for c in q.list("channel") if c["name"] == "general")
    q.seed("message", channel=general.id, body="morning all")
    said = q.as_user("sam").list("message", channel=general.id)
    assert [m["body"] for m in said] == ["morning all"]
