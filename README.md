
# Privacy-Preserving Identity Hub Using Hybrid Cloud

## Overview

The Privacy-Preserving Identity Hub is a secure hybrid cloud-based identity management system designed to protect sensitive citizen information while enabling controlled access to digital services.

Traditional identity systems expose complete user information to every service provider, increasing privacy risks and the possibility of data leakage. This project introduces a privacy-preserving approach where only derived attributes are shared instead of full identity data.

The system separates identity storage and service verification into Private Cloud and Public Cloud environments to improve confidentiality, security, and controlled disclosure of information.

---

# Objectives

- Protect sensitive user identity data
- Minimize unnecessary identity disclosure
- Implement secure token-based authentication
- Separate trusted and untrusted environments using hybrid cloud
- Enforce policy-based access control
- Demonstrate privacy-preserving service authorization

---

# Key Features

- Hybrid Cloud Architecture
- Privacy-Preserving Identity Verification
- Derived Attribute Sharing
- DUID (Decentralized User Identifier)
- JWT-based Secure Authentication
- AES-256 Encryption
- RSA (RS256) Token Signing
- SHA-256 Metadata Hashing
- Device Binding Verification
- Policy-Based Access Control
- Real-Time Verification Flow Simulation
- Secure Login and Service Dashboard

---

# System Architecture

The system consists of the following components:

## 1. Frontend Dashboard
Provides a secure interface for:
- User Login
- Profile Registration
- Service Access Requests
- Real-time Verification Status

## 2. Private Cloud
Acts as the trusted zone responsible for:
- Identity storage
- Encryption
- Derived attribute generation
- Token issuance

## 3. Public Cloud
Acts as the service verification layer responsible for:
- JWT verification
- Policy validation
- Access decision generation

## 4. Policy Engine
Evaluates authorization policies based on derived attributes such as:
- isStudent
- isAdult
- isHealthEligible

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python Flask | Backend Framework |
| SQLite | Local Database |
| HTML/CSS/JavaScript | Frontend Development |
| JWT | Secure Token Authentication |
| AES-256 | Data Encryption |
| RSA (RS256) | Token Signing |
| SHA-256 | Metadata Hashing |
| bcrypt | Password Hashing |
| Render Cloud | Public Cloud Deployment |

---

# Security Mechanisms

## AES-256 Encryption
Sensitive user data such as:
- Name
- Date of Birth

are encrypted before storage in the private cloud.

---

## RSA (RS256) Digital Signature
JWT tokens are signed using RSA private keys to ensure:
- Integrity
- Authenticity
- Tamper protection

---

## SHA-256 Hashing
Used for:
- Device metadata hashing
- Identity consistency validation

---

## bcrypt Password Protection
User passwords are securely hashed before storage.

---

# Working Flow

## Step 1: User Registration
The user creates an account and submits identity details.

## Step 2: Identity Processing
The Private Cloud:
- Encrypts sensitive data
- Generates derived attributes
- Stores identity securely

## Step 3: Token Generation
A signed JWT token containing only derived claims is generated.

## Step 4: Public Cloud Verification
The Public Cloud:
- Verifies the token signature
- Validates device information
- Executes policy checks

## Step 5: Access Decision
The Policy Engine grants or denies service access based on user eligibility.

---

# Derived Attributes Used

| Derived Attribute | Purpose |
|---|---|
| isStudent | Education Service Access |
| isAdult | Welfare Service Access |
| isHealthEligible | Healthcare Service Access |

---

# Services Implemented

## Education Service
Accessible only for users classified as students.

## Healthcare Service
Accessible only for senior citizens meeting healthcare eligibility rules.

## Welfare Service
Accessible for adult users.

---

# Privacy Preservation Strategy

Instead of exposing:
- Full Name
- Complete DOB
- Raw Identity Information

the system shares only:
- Boolean eligibility claims
- Derived attributes

This minimizes unnecessary disclosure of personal information.

---

# Project Workflow

1. User logs into Identity Hub
2. Profile information is securely stored
3. Private Cloud generates encrypted claims
4. JWT token is issued
5. Token is transferred to Public Cloud
6. Public Cloud verifies token
7. Policy Engine validates eligibility
8. Access is granted or denied

---

# Folder Structure

```text
privacy-preserving-identity-hub/
│
├── backend/
│   ├── private_cloud/
│   ├── public_deploy/
│   ├── shared/
│   ├── tools/
│   └── run_backend.py
│
├── frontend/
│   ├── login.html
│   ├── profile.html
│   ├── dashboard.html
│   └── result.html
│
├── legacy_demo/
├── README.md
└── requirements.txt
````

# Installation and Setup

## Clone Repository

```bash
git clone https://github.com/sowmiyaramanathan04/privacy-preserving-identity-hub.git
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Private Cloud

```bash
python -m backend.private_cloud.identity_hub
```

---

## Run Backend Service

```bash
python backend/run_backend.py
```

---

## Open Frontend

Open:

```text
frontend/login.html
```

in browser.

---

# Experimental Results

The system successfully demonstrates:

* Privacy-preserving authentication
* Secure token verification
* Derived attribute-based access control
* Hybrid cloud identity separation
* Reduced identity disclosure

---

# Advantages

* Reduces privacy exposure
* Minimizes unnecessary identity sharing
* Secure authentication architecture
* Lightweight implementation
* Simple hybrid cloud simulation
* Flexible policy-based authorization

---

# Limitations

* Uses simulated hybrid cloud environment
* No multi-factor authentication
* Limited policy complexity
* No distributed cloud orchestration
* Local database storage

---

# Future Enhancements

* Zero-Knowledge Proof Integration
* Multi-Factor Authentication
* Real Cloud Deployment (AWS/Azure/GCP)
* Dynamic Context-Aware Policies
* Blockchain-based Identity Validation
* Key Rotation Mechanisms
* Advanced Risk-Based Authentication

---

# Conclusion

This project demonstrates a secure and privacy-focused identity management framework using hybrid cloud architecture. By sharing only derived attributes instead of complete identity information, the system reduces privacy risks while maintaining secure service access control.

The implementation successfully combines cryptographic techniques, token-based authentication, and policy-driven authorization to create a lightweight and practical privacy-preserving identity solution.

---

# Author

Sowmiya S R, Uday Vamsi V, Vignesh Adithya D
B.Tech Artificial Intelligence and Data Science


---

# License

This project is developed for academic and educational purposes.

```
```
