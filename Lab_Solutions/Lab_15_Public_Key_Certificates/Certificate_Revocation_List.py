from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime

# Load CA’s private key (assuming we have one)
# For demo, we’ll generate a new CA key
ca_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Create CA name
ca_name = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"PK"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Example CA"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"Example CA Root"),
])

# Build CRL with revoked certificates
builder = x509.CertificateRevocationListBuilder()
builder = builder.issuer_name(ca_name)
builder = builder.last_update(datetime.datetime.utcnow())
builder = builder.next_update(datetime.datetime.utcnow() + datetime.timedelta(days=7))

# Add revoked certificates

# Certificate 1: Revoked due to key compromise
revoked_cert_1 = x509.RevokedCertificateBuilder().serial_number(
    12345  # Serial number of revoked certificate
).revocation_date(
    datetime.datetime.utcnow() - datetime.timedelta(days=2)
).add_extension(
    x509.CRLReason(x509.ReasonFlags.key_compromise),  # Revocation reason
    critical=False
).build(default_backend())

# Certificate 2: Revoked due to cessation of operation
revoked_cert_2 = x509.RevokedCertificateBuilder().serial_number(
    67890  # Another revoked certificate
).revocation_date(
    datetime.datetime.utcnow() - datetime.timedelta(days=5)
).add_extension(
    x509.CRLReason(x509.ReasonFlags.cessation_of_operation),
    critical=False
).build(default_backend())

# Add revoked certificates to CRL
builder = builder.add_revoked_certificate(revoked_cert_1)
builder = builder.add_revoked_certificate(revoked_cert_2)

# Sign the CRL
crl = builder.sign(
    private_key=ca_private_key,
    algorithm=hashes.SHA256(),
    backend=default_backend()
)

# Save CRL to file
with open("crl.pem", "wb") as f:
    f.write(crl.public_bytes(serialization.Encoding.PEM))

print("CRL created successfully!")
print(f"Issuer: {crl.issuer}")
print(f"Last Update: {crl.last_update}")
print(f"Next Update: {crl.next_update}")
print(f"Number of revoked certificates: {len(list(crl))}")


# Function to check if a certificate is revoked
def is_certificate_revoked(serial_number, crl_file="crl.pem"):
    """Check if a certificate serial number is in the CRL"""
    with open(crl_file, "rb") as f:
        crl_data = f.read()
        loaded_crl = x509.load_pem_x509_crl(crl_data, default_backend())

    for revoked_cert in loaded_crl:
        if revoked_cert.serial_number == serial_number:
            return True, revoked_cert.revocation_date
    return False, None


# Test the function
print("\n=== Testing Certificate Revocation Status ===")
test_serials = [12345, 67890, 99999]

for serial in test_serials:
    is_revoked, revocation_date = is_certificate_revoked(serial)
    if is_revoked:
        print(f"Certificate {serial}: REVOKED on {revocation_date}")
    else:
        print(f"Certificate {serial}: VALID (not revoked)")
