from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import datetime


class MockCA:
    def __init__(self, country="PK", organization="CS Department", common_name="Example CA Root"):
        self.country = country
        self.organization = organization
        self.common_name = common_name

        # root key + cert
        self.ca_private_key = None
        self.ca_certificate = None

        # serial -> metadata
        self.issued_certs = {}
        self.revoked_serials = set()

    def create_root_ca(self):
        print("Generating Root CA key pair...")

        self.ca_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.organization),
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name),
        ])

        print("Building self-signed Root CA certificate...")
        self.ca_certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(self.ca_private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True,
            )
            .sign(private_key=self.ca_private_key, algorithm=hashes.SHA256(), backend=default_backend())
        )

        print("Root CA certificate created.\n")

    def issue_certificate(self, common_name, organization, validity_days=365):
        if self.ca_certificate is None or self.ca_private_key is None:
            raise ValueError("Root CA not initialized")

        print(f"Issuing certificate for: {common_name}")

        subject_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        issuer = self.ca_certificate.subject
        serial_number = x509.random_serial_number()
        not_before = datetime.datetime.utcnow()
        not_after = not_before + datetime.timedelta(days=validity_days)

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(subject_private_key.public_key())
            .serial_number(serial_number)
            .not_valid_before(not_before)
            .not_valid_after(not_after)
            .add_extension(
                x509.BasicConstraints(ca=False, path_length=None),
                critical=True,
            )
        )

        certificate = cert.sign(
            private_key=self.ca_private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )

        self.issued_certs[serial_number] = {
            "certificate": certificate,
            "subject": certificate.subject,
            "issuer": certificate.issuer,
            "not_before": not_before,
            "not_after": not_after,
        }

        print(f"Certificate issued. Serial: {serial_number}\n")
        return subject_private_key, certificate

    def verify_certificate(self, certificate):
        print(f"Verifying certificate serial: {certificate.serial_number}")

        if certificate.serial_number in self.revoked_serials:
            print(" -> Certificate is revoked")
            return False

        now = datetime.datetime.utcnow()
        if not (certificate.not_valid_before <= now <= certificate.not_valid_after):
            print(" -> Certificate is expired or not yet valid")
            return False

        ca_public_key = self.ca_certificate.public_key()
        try:
            ca_public_key.verify(
                certificate.signature,
                certificate.tbs_certificate_bytes,
                padding.PKCS1v15(),
                certificate.signature_hash_algorithm,
            )
            print(" -> Signature is valid")
            return True
        except Exception as e:
            print(f" -> Signature verification failed: {e}")
            return False

    def revoke_certificate(self, serial_number):
        print(f"Revoking certificate serial: {serial_number}")
        self.revoked_serials.add(serial_number)

    def build_crl(self):
        if self.ca_certificate is None or self.ca_private_key is None:
            raise ValueError("Root CA not initialized")

        print("Building CRL...")
        builder = (
            x509.CertificateRevocationListBuilder()
            .issuer_name(self.ca_certificate.subject)
            .last_update(datetime.datetime.utcnow())
            .next_update(datetime.datetime.utcnow() + datetime.timedelta(days=7))
        )

        for serial in self.revoked_serials:
            revoked_cert = (
                x509.RevokedCertificateBuilder()
                .serial_number(serial)
                .revocation_date(datetime.datetime.utcnow())
                .add_extension(
                    x509.CRLReason(x509.ReasonFlags.key_compromise),
                    critical=False,
                )
                .build(default_backend())
            )
            builder = builder.add_revoked_certificate(revoked_cert)

        crl = builder.sign(
            private_key=self.ca_private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )

        print(f"CRL built. Revoked certificates: {len(self.revoked_serials)}")
        return crl

    @staticmethod
    def validate_chain(leaf_cert, issuer_cert, root_cert):
        def _verify(child, parent):
            pk = parent.public_key()
            try:
                pk.verify(
                    child.signature,
                    child.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    child.signature_hash_algorithm,
                )
                return True
            except Exception:
                return False

        if not _verify(leaf_cert, issuer_cert):
            return False
        if not _verify(issuer_cert, root_cert):
            return False
        return _verify(root_cert, root_cert)


if __name__ == "__main__":
    ca = MockCA()

    ca.create_root_ca()

    alice_priv, alice_cert = ca.issue_certificate(
        common_name="Alice",
        organization="Student Org",
        validity_days=365
    )

    print("Verifying Alice's certificate BEFORE revocation:")
    ca.verify_certificate(alice_cert)
    print()

    ca.revoke_certificate(alice_cert.serial_number)
    crl = ca.build_crl()

    with open("mock_ca_crl.pem", "wb") as f:
        f.write(crl.public_bytes(serialization.Encoding.PEM))

    print("\nVerifying Alice's certificate AFTER revocation:")
    ca.verify_certificate(alice_cert)
