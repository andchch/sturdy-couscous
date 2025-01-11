from fastapi import HTTPException, status


user_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User already exists'
)

user_not_exists_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User does not exist'
)

self_follow_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, 
     detail='Self follow')

not_followed_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, 
     detail='Not followed')

already_followed_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
     detail='Already followed')

busy_username_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
     detail='Username is taken')
