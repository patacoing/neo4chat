class DatabaseNotConnectedException(Exception):
    def __init__(self) -> None:
        super().__init__("Database is not connected")