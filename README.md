# 🛡️ ShadowWatch

### CCTV Tampering Detection and Evidence Integrity System

ShadowWatch is a cybersecurity-focused CCTV monitoring system designed to detect camera tampering and help preserve trustworthy evidence.

## 🚨 Problem

CCTV cameras can be physically tampered with, covered, disconnected, or disabled. During such incidents, important surveillance evidence may be lost or compromised.

ShadowWatch aims to address this problem by detecting suspicious tampering activity and maintaining the integrity of recorded evidence.

## 💡 Key Features

- 🎥 CCTV feed analysis
- 🚨 Tampering detection
- 🔐 SHA-256 based evidence integrity verification
- ⛓️ Blockchain-style evidence record
- 🗄️ SQLite-based incident history
- 📋 Incident logging
- ✅ Evidence modification verification
- 🖥️ Streamlit-based user interface

## 🏗️ System Architecture

```text
CCTV Video
    ↓
Tampering Detection
    ↓
Incident Detection
    ↓
Evidence Hashing (SHA-256)
    ↓
Blockchain-style Evidence Record
    ↓
Integrity Verification
    ↓
Incident Database

## 🛠️ Technologies Used

- Python
- Streamlit
- OpenCV
- SQLite
- SHA-256 Cryptographic Hashing
- JSON
- Blockchain-style Hash Chaining

## 📂 Project Structure

```text
ShadowWatch/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── backend/
│   ├── __init__.py
│   ├── create_tampered_video.py
│   ├── database.py
│   ├── evidence_blockchain.py
│   └── tamper_detector.py
│
├── database/
│
└── videos/
    ├── primary_cctv.mp4
    └── tampered_cctv.mp4

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/astha278007-beep/ShadowWatch.git
cd ShadowWatch

## 🔐 Evidence Integrity

When an incident is detected, the system can generate a cryptographic hash of the evidence.

SHA-256 is used to create a unique fingerprint for the recorded evidence.

If the evidence is modified, its hash changes, allowing the system to detect possible tampering.

The project also demonstrates a blockchain-style chain of evidence records using previous and current block hashes.

## 🎥 Current Demo

The current implementation demonstrates the concept using **pre-recorded CCTV video files**.

It includes normal and simulated tampered CCTV footage for demonstrating the detection and evidence-integrity workflow.

> **Note:** Real-time live CCTV monitoring and automatic backup-camera activation are intended future extensions of the system. The current version is a demonstration implementation using pre-recorded video.

## 🚀 Future Scope

- Real-time CCTV/IP camera integration
- RTSP camera stream support
- Automatic backup-camera activation
- Real-time security alerts
- Continuous evidence buffering
- Cloud-based evidence storage
- Multi-camera monitoring
- Advanced AI-based tampering detection
- Stronger blockchain-based evidence management

## 🎯 Objective

The long-term objective of ShadowWatch is to provide a secure and trustworthy surveillance monitoring system where tampering can be detected quickly and important evidence can be protected against unauthorized modification.

## 👩‍💻 Project

**ShadowWatch — CCTV Tampering Detection and Evidence Integrity System**

Developed as a cybersecurity and surveillance-security project.
