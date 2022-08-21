class TvmBaseException(Exception):
    pass


class UnknownNetworkException(TvmBaseException):
    def __init__(self, name: str):
        super().__init__(f'Unknown network "{name}"')


class ClientRunLocalException(TvmBaseException):
    pass
