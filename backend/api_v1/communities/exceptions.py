from fastapi import HTTPException, status

community_exists = HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                 detail='Community with this name already exists')

community_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail='Community not found')

already_joined = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail='User is already a member of the community')

