from cryptography import x509
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime

# Step 1: Generate RSA key pair
print("Generating RSA key pair...")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Step 2: Create certificate subject and issuer (same for self-signed)
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"PK"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Punjab"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Rawalpindi"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"CS Department"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"student.example.edu.pk"),
])

# Step 3: Build the certificate
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()                         # Add public key to certificate
).serial_number(
    x509.random_serial_number()                      # Generate unique serial number
).not_valid_before(
    datetime.datetime.utcnow()                       # Certificate valid from now
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)  # Valid for 1 year
).add_extension(
    # Add Subject Alternative Names (SANs)
    x509.SubjectAlternativeName([
        x509.DNSName(u"student.example.edu.pk"),
        x509.DNSName(u"www.student.example.edu.pk"),
    ]),
    critical=False,
).add_extension(
    # Add Key Usage extension
    x509.KeyUsage(
        digital_signature=True,
        key_encipherment=True,
        content_commitment=False,
        data_encipherment=False,
        key_agreement=False,
        key_cert_sign=False,
        crl_sign=False,
        encipher_only=False,
        decipher_only=False,
    ),
    critical=True,
).sign(private_key, hashes.SHA256(), default_backend())  # Sign with SHA-256

# Step 4: Save private key to file
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"mypassword")
    ))

# Step 5: Save certificate to file
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Certificate created successfully!")
print(f"Serial Number: {cert.serial_number}")
print(f"Valid From: {cert.not_valid_before}")
print(f"Valid Until: {cert.not_valid_after}")
