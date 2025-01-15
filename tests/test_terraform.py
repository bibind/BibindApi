from api.playbook_runner import run_playbook


def test_run_playbook():
    result = run_playbook("ansible/playbooks/provision_server.yml")
    assert "PLAY RECAP" in result