import json
import random
import uuid

def generate_synthetic_data(num_samples=1000):
    dataset = []
    
    protocols = ["SMTP", "IMAP", "POP3"]
    tls_versions = ["TLS 1.3", "TLS 1.2", "TLS 1.1", "TLS 1.0", "SSLv3"]
    ciphers = [
        "TLS_AES_256_GCM_SHA384",
        "TLS_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_RSA_WITH_AES_128_CBC_SHA",
        "TLS_RSA_WITH_RC4_128_SHA",
        "TLS_RSA_WITH_3DES_EDE_CBC_SHA"
    ]
    
    for _ in range(num_samples):
        # Determine basic properties based on "scenario" weights
        scenario_rand = random.random()
        
        if scenario_rand < 0.6:  # 60% Secure
            tls = random.choice(["TLS 1.2", "TLS 1.3"])
            cipher = random.choice(ciphers[:4])
            starttls_success = True
            expired_cert = False
            self_signed = False
            risk_label = "LOW"
            anomaly = False
        elif scenario_rand < 0.8: # 20% Moderate Risk
            tls = "TLS 1.2"
            cipher = random.choice(["TLS_RSA_WITH_AES_128_CBC_SHA"])
            starttls_success = True
            expired_cert = random.choice([True, False])
            self_signed = False
            risk_label = "MEDIUM"
            anomaly = False
        elif scenario_rand < 0.95: # 15% High Risk
            tls = random.choice(["TLS 1.1", "TLS 1.0"])
            cipher = random.choice(ciphers[4:])
            starttls_success = random.choice([True, False])
            expired_cert = True
            self_signed = True
            risk_label = "HIGH"
            anomaly = random.choice([True, False])
        else: # 5% Critical Risk / Anomalous
            tls = "SSLv3"
            cipher = "TLS_RSA_WITH_RC4_128_SHA"
            starttls_success = False
            expired_cert = True
            self_signed = True
            risk_label = "CRITICAL"
            anomaly = True

        session = {
            "session_id": str(uuid.uuid4()),
            "protocol": random.choice(protocols),
            "tls_version": tls,
            "cipher_suite": cipher,
            "forward_secrecy": "ECDHE" in cipher or "DHE" in cipher,
            "starttls_success": starttls_success,
            "certificate_expired": expired_cert,
            "certificate_self_signed": self_signed,
            "duration": random.uniform(0.1, 10.0),
            "packet_count": random.randint(10, 500),
            "risk_label": risk_label,
            "is_anomaly": anomaly
        }
        dataset.append(session)
        
    return dataset

if __name__ == "__main__":
    import os
    data = generate_synthetic_data(1000)
    
    # Ensure directory exists
    os.makedirs("data/features", exist_ok=True)
    
    with open("data/features/synthetic_dataset.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Generated 1000 synthetic samples.")
