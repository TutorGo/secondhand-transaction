class GetAccessTokenException(Exception):
    def __init__(self, *args):
        error_dict = args[0]['data']['error']
        self.code = error_dict['code']
        self.message = error_dict['message']
        self.is_valid = error_dict['is_valid']
        self.scopes = error_dict['scopes']


class DebugTokenException(Exception):
    def __init__(self, *args):
        error_dict = args[0]['error']
        self.code = error_dict['code']
        self.message = error_dict['message']