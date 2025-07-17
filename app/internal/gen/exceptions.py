class MissingParameterError(Exception):
    def __init__(self, parameter: str) -> None:
        super().__init__(f"Missing parameter: {parameter}")
