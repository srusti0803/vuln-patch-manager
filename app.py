import json
from flask import Flask, jsonify, render_template, request, send_file
import nmap
from openai import OpenAI
from io import BytesIO
from xhtml2pdf import pisa
import os

app = Flask(__name__)
client = OpenAI()

def run_nmap_scan(target_ip="127.0.0.1"):
    # Instead of real nmap, return simulated data
    results = [
        {
            "cve_id": "CVE-2024-9999",
            "description": "Simulated open port 22 running ssh",
            "cvss_score": 9.0,
            "asset": target_ip,
            "asset_criticality": "High",
            "patched": False
        },
        {
            "cve_id": "CVE-2024-8888",
            "description": "Simulated open port 80 running http",
            "cvss_score": 7.5,
            "asset": target_ip,
            "asset_criticality": "Medium",
            "patched": False
        }
    ]
    return results

def prioritize_vuln(vuln):
    if vuln["cvss_score"] >= 8 or vuln["asset_criticality"] == "High":
        return "High"
    elif vuln["cvss_score"] >= 5:
        return "Medium"
    else:
        return "Low"

def load_vulns():
    with open("vulnerabilities.json") as f:
        vulns = json.load(f)
        for v in vulns:
            v["priority"] = prioritize_vuln(v)
        return vulns

def generate_summary(vulns):
    high_vulns = [v for v in vulns if v["priority"] == "High"]
    if not high_vulns:
        return "No high-priority vulnerabilities found."

    prompt = (
        "You are a security analyst. Analyze the following list of vulnerabilities and generate a detailed report with the following sections for each vulnerability:\n"
        "- Findings (detailed description and impact)\n"
        "- Risk Assessment (how severe it is and why)\n"
        "- Service Identification (describe the service and why it's risky)\n"
        "- Remediation Suggestions (step-by-step fixes)\n"
        "- Patch Status (recommend if patched or not)\n"
        "Format the response clearly and professionally, so it can directly go into a client report.\n\n"
    )

    for v in high_vulns:
        prompt += f"- CVE ID: {v['cve_id']}\nDescription: {v['description']}\nAsset: {v['asset']}\nPatched: {v['patched']}\nPriority: {v['priority']}\n\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route("/")
def index():
    vulns = load_vulns()
    return render_template("index.html", vulns=vulns)

@app.route("/scan", methods=["POST"])
def scan():
    ip_input = request.form.get("target_ips", "")
    ip_list = [ip.strip() for ip in ip_input.split(",") if ip.strip()]
    all_results = []

    for ip in ip_list:
        all_results.extend(run_nmap_scan(ip))

    with open("vulnerabilities.json", "w") as f:
        json.dump(all_results, f, indent=4)

    return jsonify({"message": f"Scan completed for: {', '.join(ip_list)}"})

@app.route("/summary")
def summary():
    vulns = load_vulns()
    report = generate_summary(vulns)
    return jsonify({"summary": report})

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.form.get("question", "")
    if not user_question:
        return jsonify({"answer": "No question provided."})

    vulns = load_vulns()

    prompt = (
        "Based on the following vulnerabilities, answer the user's question in detail.\n"
    )
    for v in vulns:
        prompt += f"- {v['cve_id']} ({v['description']}) on {v['asset']} (Priority: {v['priority']}).\n"
    prompt += f"\nUser question: {user_question}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"answer": response.choices[0].message.content})

@app.route("/generate_pdf")
def generate_pdf():
    vulns = load_vulns()
    summary_text = generate_summary(vulns)
    html = f"<h1>Vulnerability Report</h1><pre>{summary_text}</pre>"
    result = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=result)
    result.seek(0)
    return send_file(result, download_name="report.pdf", as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

