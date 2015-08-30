from oxdpython.messenger import Messenger


def test_send():
    """test send method of Messenger"""
    msgr = Messenger(8099)
    response = msgr.send({"command": "test"})
    assert 'status' in response.keys()
