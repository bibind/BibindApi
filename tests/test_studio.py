from bibind_core import ApiClient


class AITask:
    def __init__(self, name):
        self.name = name
        self.state = "draft"
        self.result = None

    def run(self, env):
        client = ApiClient.from_env(env)
        resp = client.post("/ai", {"task": self.name})
        self.state = "done"
        self.result = resp.get("result")


def test_ai_task():
    client = ApiClient({"/ai": {"result": "ok"}}, [])
    env = {"client": client}
    task = AITask("demo")
    task.run(env)
    assert task.state == "done"
    assert task.result == "ok"
