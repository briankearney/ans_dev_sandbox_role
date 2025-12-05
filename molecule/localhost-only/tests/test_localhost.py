def test_connection_localhost(host):
    # Testinfra host for delegated driver represents local
    assert host.check_output('uname -n'), "Should be able to run commands on localhost"
