
class Discovery(object):
    """Discovery defines the OIDC discovery params"""
    def __init__(self, url):
        self.msg = {"command": "discovery",
                    "params": {
                        "discovery_url": url
                        }
                    }
