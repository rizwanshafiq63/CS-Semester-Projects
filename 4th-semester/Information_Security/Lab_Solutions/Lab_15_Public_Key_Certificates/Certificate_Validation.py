from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime

# Load certificate from file
with open("certificate.pem", "rb") as f:
    cert_data = f.read()
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())

print("=== Certificate Validation ===\n")

# 1. Extract and display subject information
print("Subject Information:")
for attribute in cert.subject:
    print(f"  {attribute.oid._name}: {attribute.value}")

# 2. Extract and display issuer information
print("\nIssuer Information:")
for attribute in cert.issuer:
    print(f"  {attribute.oid._name}: {attribute.value}")

# 3. Check validity period
current_time = datetime.datetime.utcnow()
print("\nValidity Period:")
print(f"  Not Before: {cert.not_valid_before}")
print(f"  Not After: {cert.not_valid_after}")
print(f"  Current Time: {current_time}")

# Validate time
if cert.not_valid_before <= current_time <= cert.not_valid_after:
    print("Certificate is currently valid")
else:
    print("Certificate is EXPIRED or not yet valid")

# 4. Display serial number
print(f"\nSerial Number: {cert.serial_number}")

# 5. Display signature algorithm
print(f"\nSignature Algorithm: {cert.signature_algorithm_oid._name}")

# 6. Extract extensions
print("\nCertificate Extensions:")
for extension in cert.extensions:
    print(f" - {extension.oid._name}")

    if extension.oid._name == "subjectAltName":
        print(f"     SANs: {extension.value}")
    elif extension.oid._name == "keyUsage":
        print(f"     Key Usage: {extension.value}")

# 7. Verify if self-signed
if cert.issuer == cert.subject:
    print("\nThis is a self-signed certificate")
else:
    print("\nThis certificate is signed by a CA")

print("\n=== Validation Complete ===")
