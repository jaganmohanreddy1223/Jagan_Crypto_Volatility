import pyodbc
import streamlit as st
import hashlib

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=crypto_risk_db;"
        "Trusted_Connection=yes;"
    )
    return conn

def register_user(username, email, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customer_new (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, hashed_pw)
    )
    conn.commit()
    conn.close()

import hashlib
from db_connection import get_connection

def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()

def login_user(username_or_email, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_pwd = hash_password(password)

    query = """
    SELECT 1 FROM customer_new
    WHERE (username = ? OR email=?) AND password_hash = ?
    """

    cursor.execute(query, (username_or_email.strip(),username_or_email.strip(), hashed_pwd))
    user = cursor.fetchone()

    conn.close()
    return user is not None

