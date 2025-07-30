"""Wrapper around the Flyte SDK."""

from flytekit import task, workflow


def dummy_task() -> str:
    return "ok"


@workflow
def dummy_workflow() -> str:
    return dummy_task()
