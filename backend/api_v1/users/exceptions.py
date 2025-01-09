from fastapi import HTTPException, status


user_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User already exists'
)

user_not_exists_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User does not exist'
)