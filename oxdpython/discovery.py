
class Discovery(object):
    """Discovery defines the OIDC discovery params"""
    def __init__(self, base_url):
        discovery_url = "{0}/.well-known/openid-configuration".format(
            base_url)
        self.msg = {"command": "discovery",
                    "params": {
                        "discovery_url": discovery_url
                        }
                    }
