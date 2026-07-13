import urllib.parse
import requests
import streamlit as st

import os

def load_env():
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")
load_env()

REDIRECT_URI = "https://bispado.sandlj.com.br/"

AUTHORIZED_EMAILS = [
    "sandra.nakata092@gmail.com",
    "leonardogmendoza@gmail.com" 
]

def get_google_auth_url():
    load_env()
    client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    if not client_id:
        return "#error-missing-client-id"
        
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    return f"{auth_url}?{urllib.parse.urlencode(params)}"

def get_google_user_info(code):
    load_env()
    client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    res = requests.post(token_url, data=data)
    if res.status_code == 200:
        access_token = res.json().get("access_token")
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_res = requests.get(user_info_url, headers=headers)
        if user_info_res.status_code == 200:
            return user_info_res.json()
    return None
