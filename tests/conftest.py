import types
import sys
from dataclasses import dataclass, field


@dataclass
class DummyApiClient:
    responses: dict = field(default_factory=dict)
    calls: list = field(default_factory=list)

    @classmethod
    def from_env(cls, env):
        return env["client"]

    def get(self, path):
        self.calls.append(("get", path))
        return self.responses.get(path)

    def post(self, path, payload=None, headers=None):
        self.calls.append(("post", path, payload, headers))
        return self.responses.get(path, {})

    def put(self, path, payload=None):
        self.calls.append(("put", path, payload))
        return self.responses.get(path, {})


module = types.ModuleType("bibind_core")
module.ApiClient = DummyApiClient
sys.modules.setdefault("bibind_core", module)
