from a2_cli.config import EdgeGridConfig
import argparse
import mock
import pytest


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(command="reset", propertyId=12345, debug=True, edgerc="./tests/edgerc-sample", section=None))
def test_config(mock_args):
    config = EdgeGridConfig({"verbose": False}, "a2p-reset")
    assert config
    assert config.command == "reset"
    assert config.propertyId == 12345
    # verify that edgerc config is read properly
    assert config.host == "akab-rabdom-12345.luna.akamaiapis.net"


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(command="reset", propertyId=None, debug=True, edgerc="edgerc-sample", section=None))
def test_missing_arlid(mock_args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        config = EdgeGridConfig({"verbose": False}, "a2p-reset")
        assert pytest_wrapped_e.type == SystemExit


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(command=None, propertyId=None, debug=True, edgerc="edgerc-sample", section=None))
def test_missing_reset_command(mock_args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        config = EdgeGridConfig({"verbose": False}, "a2p-reset")
        assert pytest_wrapped_e.type == SystemExit
