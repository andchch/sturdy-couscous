from fastapi import HTTPException, status


user_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User already exists'
)