from fastapi import HTTPException, status

privacy_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail='Privacy error')
no_profile_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail='No data for this user')
