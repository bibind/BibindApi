"""High level project synchronisation tests.

This module exercises several pieces of functionality that rely on HTTP
interactions.  The :mod:`bibind_core.ApiClient` used in the tests is provided by
``tests.conftest`` and records calls in memory, allowing the tests to run very
quickly (<500 ms) without making any real network requests.
"""

from time import perf_counter

from bibind_core import ApiClient


class Project:
    """Minimal project representation used by the tests."""

    def __init__(self, name, tenant, gitlab_id):
        self.name = name
        self.tenant_id = tenant
        self.gitlab_project_id = gitlab_id
        self.tasks = []
        self.budget = None


def sync_gitlab(env, project):
    """Synchronise GitLab issues into ``project.tasks``."""

    client = ApiClient.from_env(env)
    issues = client.get(f"/gitlab/projects/{project.gitlab_project_id}/issues") or []
    for issue in issues:
        project.tasks.append(issue["title"])
    return project.tasks


# ---------------------------------------------------------------------------
# Budget and billing helpers


class BudgetLine:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount


class ProjectBudget:
    def __init__(self):
        self.line_ids = []
        self.spent_labor = 0
        self.spent_infra = 0
        self.spent_total = 0

    def compute(self):
        self.spent_labor = sum(l.amount for l in self.line_ids if l.type == "labor")
        self.spent_infra = sum(l.amount for l in self.line_ids if l.type == "infra")
        self.spent_total = self.spent_labor + self.spent_infra


def fetch_budget(env, project):
    """Fetch budget information for a project via the API."""

    client = ApiClient.from_env(env)
    data = client.get(f"/gitlab/projects/{project.gitlab_project_id}/budget") or []
    budget = ProjectBudget()
    budget.line_ids = [BudgetLine(**l) for l in data]
    budget.compute()
    project.budget = budget
    return budget


def create_invoice(env, project, amount):
    """Trigger invoice creation for ``project``."""

    client = ApiClient.from_env(env)
    resp = client.post(
        f"/gitlab/projects/{project.gitlab_project_id}/invoice",
        {"amount": amount},
    )
    return resp.get("status")


# ---------------------------------------------------------------------------
# AI studio helper


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


# ---------------------------------------------------------------------------
# Security helpers


class User:
    def __init__(self, tenant):
        self.tenant_id = tenant


def trigger_bootstrap(env, user):
    client = ApiClient.from_env(env)
    return client.post("/bootstrap", headers={"Tenant": user.tenant_id})


# ---------------------------------------------------------------------------
# Tests


def test_sync_multi_tenant_and_performance():
    project_a = Project("A", "t1", 1)
    project_b = Project("B", "t2", 2)

    client_a = ApiClient({"/gitlab/projects/1/issues": [{"id": 1, "title": "A1"}]}, [])
    client_b = ApiClient({"/gitlab/projects/2/issues": [{"id": 2, "title": "B1"}]}, [])

    env_a = {"client": client_a}
    env_b = {"client": client_b}

    start = perf_counter()
    tasks_a = sync_gitlab(env_a, project_a)
    tasks_b = sync_gitlab(env_b, project_b)
    elapsed = perf_counter() - start

    assert tasks_a == ["A1"]
    assert tasks_b == ["B1"]
    assert "B1" not in project_a.tasks
    assert "A1" not in project_b.tasks
    assert elapsed < 0.5


def test_budget_fetch_and_compute():
    project = Project("A", "t1", 1)
    client = ApiClient(
        {
            "/gitlab/projects/1/budget": [
                {"type": "labor", "amount": 100},
                {"type": "infra", "amount": 50},
            ]
        },
        [],
    )
    env = {"client": client}

    budget = fetch_budget(env, project)

    assert budget.spent_labor == 100
    assert budget.spent_infra == 50
    assert budget.spent_total == 150


def test_billing_invoice_creation():
    project = Project("A", "t1", 1)
    client = ApiClient({"/gitlab/projects/1/invoice": {"status": "created"}}, [])
    env = {"client": client}

    status = create_invoice(env, project, 200)

    assert status == "created"
    # verify payload sent to API
    assert client.calls[0][2] == {"amount": 200}


def test_ai_task_execution():
    client = ApiClient({"/ai": {"result": "ok"}}, [])
    env = {"client": client}
    task = AITask("demo")

    task.run(env)

    assert task.state == "done"
    assert task.result == "ok"
    assert client.calls[0][2] == {"task": "demo"}


def test_security_tenant_headers_isolated():
    client = ApiClient({"/bootstrap": {"status": "ok"}}, [])
    env = {"client": client}

    alice = User("t1")
    bob = User("t2")
    trigger_bootstrap(env, alice)
    trigger_bootstrap(env, bob)

    assert client.calls[0][3]["Tenant"] == "t1"
    assert client.calls[1][3]["Tenant"] == "t2"

