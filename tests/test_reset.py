import requests
import requests_mock
import pytest
from a2_cli.http_calls import reset
from collections import OrderedDict

def test_reset_success():
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.adapters = OrderedDict()
    session.mount('https', adapter)
    def custom_matcher_resp_ok(request):
        if request.path_url == '/adaptive-acceleration/v1/properties/12345/reset':
            resp = requests.Response()
            resp.status_code = 204
            return resp
        return None
    adapter.add_matcher(custom_matcher_resp_ok)
    assert reset(session, 'https://example.com/', 12345, False) == 0

def test_reset_forbidden():
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.adapters = OrderedDict()
    session.mount('https', adapter)
    def custom_matcher_forbidden(request):
        if request.path_url == '/adaptive-acceleration/v1/properties/98765/reset':
            resp = requests.Response()
            resp.status_code = 403
            resp.code = "forbidden"
            resp.error_type = "authorization failure"
            resp._content = b'{"title": "Forbidden."}'
            return resp
        return None
    adapter.add_matcher(custom_matcher_forbidden)
    # test that reset calls sys.exit
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        reset(session, 'https://example.com/', 98765, False)
        assert pytest_wrapped_e.type == SystemExit

def test_reset_404():
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.adapters = OrderedDict()
    session.mount('https', adapter)
    def custom_matcher_forbidden(request):
        if request.path_url == '/adaptive-acceleration/v1/properties/98765/reset':
            resp = requests.Response()
            resp.status_code = 404
            resp.code = "forbidden"
            resp.error_type = "resource not found"
            resp._content = b'{"title": "Resource not found."}'
            return resp
        return None
    adapter.add_matcher(custom_matcher_forbidden)
    # test that reset calls sys.exit
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        reset(session, 'https://example.com/', 98765, False)
        assert pytest_wrapped_e.type == SystemExit

def test_reset_server_error():
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.adapters = OrderedDict()
    session.mount('https', adapter)
    def custom_matcher_forbidden(request):
        if request.path_url == '/adaptive-acceleration/v1/properties/98765/reset':
            resp = requests.Response()
            resp.status_code = 500
            resp.code = "forbidden"
            resp.error_type = "internal error"
            resp._content = b'{"title": "Internal server error.", "errorString": "500: Internal sever error"}'
            return resp
        return None
    adapter.add_matcher(custom_matcher_forbidden)
    # test that reset calls sys.exit
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        reset(session, 'https://example.com/', 98765, False)
        assert pytest_wrapped_e.type == SystemExit
