def test_deploy_charm(harness):
    harness.begin()
    harness.set_leader(True)
    assert harness.model.unit.status == ActiveStatus()