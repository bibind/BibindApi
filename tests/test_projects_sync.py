from time import perf_counter

from bibind_core import ApiClient


class Project:
    def __init__(self, name, tenant, gitlab_id):
        self.name = name
        self.tenant_id = tenant
        self.gitlab_project_id = gitlab_id
        self.tasks = []


def sync_gitlab(env, project):
    client = ApiClient.from_env(env)
    issues = client.get(f"/gitlab/projects/{project.gitlab_project_id}/issues") or []
    for issue in issues:
        project.tasks.append(issue["title"])
    return project.tasks


def test_sync_multi_tenant_and_performance():
    project_a = Project("A", "t1", 1)
    project_b = Project("B", "t2", 2)

    client_a = ApiClient({
        "/gitlab/projects/1/issues": [{"id": 1, "title": "A1"}]
    }, [])
    client_b = ApiClient({
        "/gitlab/projects/2/issues": [{"id": 2, "title": "B1"}]
    }, [])

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
