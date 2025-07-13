# Vuln Patch Manager

## 🚨 Problem Statement

Organizations struggle to quickly identify and prioritize vulnerabilities across multiple assets. Manual patching is time-consuming and increases risk of cyber attacks.

---

## 💡 Our Solution

An AI-powered vulnerability patch management dashboard that:

- ✅ Allows scanning of IP-based assets (simulated for demo)
- ✅ Generates comprehensive, professional risk assessments and remediation suggestions using OpenAI
- ✅ Supports interactive AI-based Q&A on vulnerabilities
- ✅ Generates downloadable PDF reports
- ✅ User-friendly, clean web dashboard

---

## 🌟 Features

- IP-based scan simulation (mock data)
- High-priority vulnerability identification
- AI-generated detailed summaries (findings, risk assessment, service description, remediation, patch status)
- Interactive AI queries
- PDF report generation
- Clean Bootstrap UI

---

## 🛠️ Tech Stack

- Python (Flask)
- Bootstrap (frontend styling)
- OpenAI GPT-4o (LLM for analysis)
- Render (cloud deployment)

---

## 🚀 Demo

Live URL: [https://vuln-patch-manager.onrender.com](https://vuln-patch-manager.onrender.com)

---

## 💬 Usage

1. Enter IP addresses (any dummy IP for demo, e.g., `192.168.0.100`)
2. Click **Start Scan**
3. Generate summary and download PDF
4. Ask questions in the AI query box

---

## 📝 How to run locally

```bash
pip install -r requirements.txt
python app.py
