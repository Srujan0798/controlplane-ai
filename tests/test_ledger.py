from controlplane.ledger import EvidenceLedger
from controlplane.models import Principal

def test_hash_chain_links_entries():
    led = EvidenceLedger.begin(
        request_id="req-1",
        principal=Principal(id="u1", clearance=frozenset({"public"})),
        action_intent="demo",
        policy_version="matrix-v1",
    )
    h1 = led.append("note", {"n": 1})
    h2 = led.append("note", {"n": 2})
    assert h1 != h2
    assert led.verify_chain() is True

def test_tamper_breaks_chain():
    led = EvidenceLedger.begin(
        request_id="req-1",
        principal=Principal(id="u1", clearance=frozenset({"public"})),
        action_intent="demo",
        policy_version="matrix-v1",
    )
    led.append("note", {"n": 1})
    led._entries[0].payload["n"] = 99  # intentional tamper for test
    assert led.verify_chain() is False
