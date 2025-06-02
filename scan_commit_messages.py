import pandas as pd
import re

# Define patterns for sensitive info
PATTERNS = {
    "Email address": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "IP address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    "API key (generic)": r'(?i)\b(api|secret|token|key)[\s:=]+[a-zA-Z0-9\-_=]{10,}',
    "AWS key": r'AKIA[0-9A-Z]{16}',
    "Private key block": r'-----BEGIN (RSA|DSA|EC|PGP) PRIVATE KEY-----',
    "Path with usernames": r'/Users/[a-zA-Z0-9_.-]+|C:\\\\Users\\\\[a-zA-Z0-9_.-]+',
    "Phone number": r'\+?\d[\d\s().-]{7,}\d'
}

def scan_messages(file_path):
    df = pd.read_csv(file_path)

    findings = {key: [] for key in PATTERNS}

    for idx, msg in enumerate(df['message']):
        for label, pattern in PATTERNS.items():
            if re.search(pattern, msg):
                findings[label].append((idx, msg.strip()))

    print("🔍 Scan Results:")
    for category, matches in findings.items():
        if matches:
            print(f"\n--- {category} ---")
            for i, msg in matches:
                print(f"[Row {i}] {msg}")

if __name__ == "__main__":
    scan_messages("./commit_messages.csv")
