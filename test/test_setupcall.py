def test_setupcall():
    """
    Test the call of the setup function
    """
    import os
    import jupyter_openvscodeserver_proxy as jx

    os.environ["OPENVSCODESERVER_BIN"] = "openvscode-server"

    print("\nRunning test_setupcall...")
    print(jx.setup_openvscodeserver())
