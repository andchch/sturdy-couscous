from fastapi import HTTPException, status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

invalid_login_pass =  HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect email or password',
    headers={'WWW-Authenticate': 'Bearer'},
)

revoke_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token has been revoked',
    headers={'WWW-Authenticate': 'Bearer'},
)

role_forbidden = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='You do not have the necessary permissions',
)

auth_failed = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Authorization failed'
)
