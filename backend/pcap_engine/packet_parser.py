import pyshark
import logging
from typing import Dict, Any, List
from security_engine.rules import SecurityRulesEngine, calculate_score
from ml.inference import MLInferenceEngine

logger = logging.getLogger(__name__)

class PcapParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.sessions: Dict[str, Any] = {}
        self.stats = {
            "total_packets": 0,
            "tcp_packets": 0,
            "smtp_sessions": 0,
            "imap_sessions": 0,
            "pop3_sessions": 0,
            "tls_sessions": 0,
        }
        self.rules_engine = SecurityRulesEngine()
        self.ml_engine = MLInferenceEngine()

    def _get_stream_key(self, packet) -> str:
        # PyShark provides a tcp.stream index which uniquely identifies a TCP stream in the PCAP
        try:
            return packet.tcp.stream
        except AttributeError:
            return None

    def analyze(self) -> Dict[str, Any]:
        try:
            # We filter for TCP to avoid processing irrelevant UDP/ICMP packets
            cap = pyshark.FileCapture(self.filepath, display_filter="tcp", keep_packets=False)
            
            for packet in cap:
                self.stats["total_packets"] += 1
                self.stats["tcp_packets"] += 1
                
                stream_id = self._get_stream_key(packet)
                if stream_id is None:
                    continue

                if stream_id not in self.sessions:
                    self.sessions[stream_id] = {
                        "session_id": stream_id,
                        "src_ip": packet.ip.src if hasattr(packet, 'ip') else (packet.ipv6.src if hasattr(packet, 'ipv6') else None),
                        "src_port": packet.tcp.srcport,
                        "dst_ip": packet.ip.dst if hasattr(packet, 'ip') else (packet.ipv6.dst if hasattr(packet, 'ipv6') else None),
                        "dst_port": packet.tcp.dstport,
                        "start_time": float(packet.sniff_timestamp),
                        "end_time": float(packet.sniff_timestamp),
                        "packet_count": 0,
                        "bytes_transferred": 0,
                        "protocols": set(),
                        "tls_info": {},
                        "starttls_info": {
                            "supported": False,
                            "requested": False,
                            "success": False,
                            "failure": False
                        }
                    }

                session = self.sessions[stream_id]
                session["packet_count"] += 1
                session["bytes_transferred"] += int(packet.length)
                session["end_time"] = float(packet.sniff_timestamp)
                
                # Protocol Detection via PyShark layers
                layer_names = [layer.layer_name for layer in packet.layers]
                for layer in layer_names:
                    session["protocols"].add(layer)
                
                self._extract_tls_info(packet, session)
                self._extract_starttls_info(packet, session)

            cap.close()

            # Clean up sets for JSON serialization
            for s in self.sessions.values():
                s["protocols"] = list(s["protocols"])
                s["duration"] = s["end_time"] - s["start_time"]
                
                # High level protocol classification
                if "smtp" in s["protocols"]:
                    self.stats["smtp_sessions"] += 1
                    s["primary_protocol"] = "SMTP"
                elif "imap" in s["protocols"]:
                    self.stats["imap_sessions"] += 1
                    s["primary_protocol"] = "IMAP"
                elif "pop" in s["protocols"]:
                    self.stats["pop3_sessions"] += 1
                    s["primary_protocol"] = "POP3"
                else:
                    s["primary_protocol"] = "UNKNOWN"

                if "tls" in s["protocols"]:
                    self.stats["tls_sessions"] += 1

                # Apply Security Rules
                s["findings"] = self.rules_engine.evaluate_session(s)
                s["rule_score"] = calculate_score(s["findings"])
                
                # Apply ML Inference
                ml_result = self.ml_engine.predict_risk(s)
                s["ml_risk"] = ml_result.get("predicted_risk")
                s["ml_confidence"] = ml_result.get("confidence")
                
                # Risk Fusion (Basic implementation)
                s["overall_score"] = s["rule_score"]
                if s["ml_risk"] == "CRITICAL":
                    s["overall_score"] = max(0, s["overall_score"] - 20)
                elif s["ml_risk"] == "HIGH":
                    s["overall_score"] = max(0, s["overall_score"] - 10)

            return {
                "stats": self.stats,
                "sessions": list(self.sessions.values())
            }

        except Exception as e:
            logger.error(f"Error parsing PCAP: {e}")
            raise

    def _extract_tls_info(self, packet, session):
        if not hasattr(packet, 'tls'):
            return
        
        # Check if it's a handshake
        if hasattr(packet.tls, 'handshake_type'):
            # 1 is ClientHello, 2 is ServerHello
            if packet.tls.handshake_type == '1':
                session["tls_info"]["client_hello_seen"] = True
                if hasattr(packet.tls, 'handshake_version'):
                    session["tls_info"]["client_version"] = packet.tls.handshake_version
            elif packet.tls.handshake_type == '2':
                session["tls_info"]["server_hello_seen"] = True
                if hasattr(packet.tls, 'handshake_version'):
                    session["tls_info"]["negotiated_version"] = packet.tls.handshake_version
                if hasattr(packet.tls, 'handshake_ciphersuite'):
                    session["tls_info"]["cipher_suite"] = packet.tls.handshake_ciphersuite
            
            # Certificate Extraction
            if packet.tls.handshake_type == '11': # Certificate
                session["tls_info"]["certificate_seen"] = True
                # Extract cert details if available in PyShark

    def _extract_starttls_info(self, packet, session):
        # SMTP
        if hasattr(packet, 'smtp'):
            if hasattr(packet.smtp, 'req_command') and packet.smtp.req_command.upper() == 'STARTTLS':
                session["starttls_info"]["requested"] = True
            if hasattr(packet.smtp, 'rsp_parameter') and '220' in packet.smtp.rsp_parameter and session["starttls_info"]["requested"]:
                 session["starttls_info"]["success"] = True

        # IMAP
        if hasattr(packet, 'imap'):
            if hasattr(packet.imap, 'request') and 'STARTTLS' in packet.imap.request:
                session["starttls_info"]["requested"] = True
            if hasattr(packet.imap, 'response') and 'OK' in packet.imap.response and 'STARTTLS' in packet.imap.response:
                session["starttls_info"]["success"] = True
                
        # POP3
        if hasattr(packet, 'pop'):
            if hasattr(packet.pop, 'request') and 'STLS' in packet.pop.request:
                session["starttls_info"]["requested"] = True
            if hasattr(packet.pop, 'response') and '+OK' in packet.pop.response and session["starttls_info"]["requested"]:
                session["starttls_info"]["success"] = True
