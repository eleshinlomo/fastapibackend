from fastapi import HTTPException
import requests

# Get User Profile
async def login_checker():
    BASE_URL = 'http://localhost:8000/api/loginchecker/'
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = await requests.get(BASE_URL, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))