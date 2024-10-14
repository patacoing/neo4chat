from fastapi import HTTPException


class WrongPasswordOrEmail(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Wrong password or email")