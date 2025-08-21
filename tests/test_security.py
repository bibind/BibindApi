from bibind_core import ApiClient


class User:
    def __init__(self, tenant):
        self.tenant_id = tenant


def trigger_bootstrap(env, user):
    client = ApiClient.from_env(env)
    return client.post("/bootstrap", headers={"Tenant": user.tenant_id})


def test_tenant_headers_isolated():
    client = ApiClient({"/bootstrap": {"status": "ok"}}, [])
    env = {"client": client}
    alice = User("t1")
    bob = User("t2")
    trigger_bootstrap(env, alice)
    trigger_bootstrap(env, bob)
    assert client.calls[0][3]["Tenant"] == "t1"
    assert client.calls[1][3]["Tenant"] == "t2"
