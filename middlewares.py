from fastapi import HTTPException, Header
from fastapi import status


def get_user_id(x_gapo_user_id=Header(None)) -> str:
    """Only accept api-call with valid header"""
    try:
        if not x_gapo_user_id:
            detail = "Missing UserID, Access denied"
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
        return x_gapo_user_id
    except ValueError as err:
        detail = "Missing UserID, Access denied"
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail) from err
