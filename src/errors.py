class ParseError(Exception):
    def __init__(self, message: str, line: int = None, col: int = None):
        loc = f" ({line}:{col})" if line is not None else ""
        super().__init__(message + loc)
        self.line = line
        self.col = col
