# Secure Cloud Data Protection System

## Project Overview
The Secure Cloud Data Protection System is a Python-based application designed to protect sensitive user information through encryption and controlled access.

## Main Objectives
- Protect sensitive data using AES-256-GCM encryption.
- Reduce SQL Injection risks using parameterized SQL queries.
- Restrict data retrieval using capability-based access control.
- Maintain security activity logs.
- Allow authorized users to retrieve and decrypt stored information.

## Technologies Used
- Python
- Streamlit
- SQLite
- Cryptography
- AES-256-GCM Encryption

## Key Features
1. Secure User Registration
2. Data Encryption
3. SQLite Database Storage
4. Capability Code Generation
5. Authorized Data Retrieval
6. Data Decryption
7. Security Dashboard
8. Activity Logs

## Project Files
- app.py – Main Streamlit application
- database.py – Database operations
- security.py – Encryption and decryption
- access_control.py – Capability-based access control
- requirements.txt – Project dependencies

## How to Run
1. Install the dependencies:

   pip install -r requirements.txt

2. Start the application:

   python -m streamlit run app.py

## Project Status
Core features implemented and tested locally.

## Disclaimer
This is an educational prototype. Additional security controls and cloud deployment are required before production use.