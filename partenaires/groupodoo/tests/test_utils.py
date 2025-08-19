import importlib.util
import pathlib

utils_path = pathlib.Path(__file__).resolve().parents[1] / "utils.py"
spec = importlib.util.spec_from_file_location("groupodoo_utils", utils_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)


def test_compute_hmac_consistency():
    secret = "secret"
    data = b"payload"
    sig1 = utils.compute_hmac(secret, data)
    sig2 = utils.compute_hmac(secret, data)
    assert sig1 == sig2
