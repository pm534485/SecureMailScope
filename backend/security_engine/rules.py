from typing import Dict, Any, List

class SecurityRulesEngine:
    def __init__(self):
        # We define a few baseline rules for Hackathon demonstration
        self.rules = [
            self.check_deprecated_tls,
            self.check_missing_starttls,
            self.check_weak_ciphers,
            self.check_expired_cert,
            self.check_self_signed_cert,
            self.check_forward_secrecy
        ]

    def evaluate_session(self, session: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        for rule in self.rules:
            finding = rule(session)
            if finding:
                findings.append(finding)
        return findings

    def check_deprecated_tls(self, session: Dict[str, Any]) -> Dict[str, Any]:
        tls_info = session.get("tls_info", {})
        version = tls_info.get("negotiated_version", "")
        # TLS 1.0 (0x0301) and TLS 1.1 (0x0302) are deprecated
        if version in ["0x0301", "0x0302", "0x0300", "SSLv3", "TLS 1.0", "TLS 1.1"]:
            return self._create_finding(
                "Deprecated TLS Version",
                "HIGH",
                f"Session negotiated deprecated {version}",
                "Outdated protocol vulnerabilities can be exploited.",
                "Upgrade to TLS 1.2 or TLS 1.3."
            )
        return None

    def check_missing_starttls(self, session: Dict[str, Any]) -> Dict[str, Any]:
        starttls = session.get("starttls_info", {})
        if starttls.get("requested") and not starttls.get("success"):
            return self._create_finding(
                "STARTTLS Failure",
                "HIGH",
                "STARTTLS was requested but negotiation failed or was rejected.",
                "Communication remains in plaintext.",
                "Verify server configuration for STARTTLS support."
            )
        
        # If it's a plaintext port (25, 143, 110) and no STARTTLS requested
        if session.get("dst_port") in ["25", "143", "110"] and not starttls.get("requested") and not session.get("tls_info"):
            return self._create_finding(
                "Plaintext Communication",
                "CRITICAL",
                "No encryption or STARTTLS requested on standard plaintext port.",
                "Credentials and emails are transmitted in plaintext.",
                "Enforce STARTTLS or use implicit TLS ports (465, 993, 995)."
            )
        return None

    def check_weak_ciphers(self, session: Dict[str, Any]) -> Dict[str, Any]:
        cipher = session.get("tls_info", {}).get("cipher_suite", "").lower()
        if not cipher:
            return None
        
        weak_patterns = ["rc4", "des", "md5", "null", "anon", "export"]
        for p in weak_patterns:
            if p in cipher:
                return self._create_finding(
                    "Weak Cipher Suite",
                    "HIGH",
                    f"Negotiated weak cipher: {cipher}",
                    "The cipher is known to have cryptographic weaknesses.",
                    "Disable weak ciphers and prioritize AES-GCM or ChaCha20."
                )
        return None

    def check_expired_cert(self, session: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder for certificate checking
        return None

    def check_self_signed_cert(self, session: Dict[str, Any]) -> Dict[str, Any]:
         # Placeholder for certificate checking
         return None

    def check_forward_secrecy(self, session: Dict[str, Any]) -> Dict[str, Any]:
        cipher = session.get("tls_info", {}).get("cipher_suite", "").upper()
        if not cipher:
            return None
        # Non-DHE/ECDHE suites generally lack forward secrecy
        if "RSA_WITH" in cipher and "DHE" not in cipher:
            return self._create_finding(
                "No Forward Secrecy",
                "MEDIUM",
                f"Cipher {cipher} lacks forward secrecy.",
                "If the private key is compromised, past sessions can be decrypted.",
                "Enable and prioritize ECDHE or DHE cipher suites."
            )
        return None

    def _create_finding(self, title, severity, evidence, impact, recommendation):
        return {
            "title": title,
            "severity": severity,
            "evidence": evidence,
            "impact": impact,
            "recommendation": recommendation
        }

def calculate_score(findings: List[Dict[str, Any]]) -> int:
    score = 100
    for finding in findings:
        sev = finding.get("severity", "")
        if sev == "CRITICAL":
            score -= 30
        elif sev == "HIGH":
            score -= 20
        elif sev == "MEDIUM":
            score -= 10
        elif sev == "LOW":
            score -= 5
    return max(0, score)
