import socket

from nose.tools import assert_equal, assert_is_instance, assert_raises,\
    assert_false, assert_true

from oxdpython.messenger import Messenger


def test_messenger_constructor():
    # port assignment
    mes1 = Messenger()
    assert_equal(mes1.port, 8099)

    mes2 = Messenger(3000)
    assert_equal(mes2.port, 3000)

    # host assignment
    assert_equal(mes1.host, 'localhost')
    assert_equal(mes2.host, 'localhost')

    # socket family and type
    assert_is_instance(mes1.sock, socket.SocketType)
    assert_equal(mes1.sock.type, socket.SOCK_STREAM)
    assert_equal(mes1.sock.family, socket.AF_INET)

    assert_is_instance(mes2.sock, socket.SocketType)
    assert_equal(mes2.sock.type, socket.SOCK_STREAM)
    assert_equal(mes2.sock.family, socket.AF_INET)


def test_send():
    """Messenger.send sends message"""
    msgr = Messenger(8099)
    response = msgr.send({"command": "test"})
    assert response.status


def test_send_fail():
    """Messenger.send raises error for non connected port"""
    # should raise error when oxd server is not running
    msgr = Messenger(4000)
    with assert_raises(RuntimeError):
        msgr.send({'command': 'raise_error'})


def test_first_connection():
    """Messenger connects deffered until first send"""
    msgr = Messenger()
    assert_false(msgr.firstDone)
    msgr.send({})
    assert_true(msgr.firstDone)
