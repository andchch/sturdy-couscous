from fastapi import HTTPException, status

privacy_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail='Privacy error')
