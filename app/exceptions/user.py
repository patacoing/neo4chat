from fastapi import HTTPException, status

class UserAlreadyExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")