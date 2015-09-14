class Register(object):
    """Register class defines the command to be passed to the oxD
    for a OIDC client registration
    """
    def __init__(self, metadata):
        self.msg = {'command': 'register_client',
                    'params': metadata
                    }
