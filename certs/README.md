# Koi Root CA

`tstc_koi_ca.pem`: `tstc` tenant'ının Koi Root CA sertifikası (AES konsolu → **Settings → Deployment → Network Routing → Establish network trust → Download CA**).

`aes-workshop-setup.ps1`, `-KoiRootCaFile` parametresi verilmezse bu klasördeki ilk `.pem`, `.cer` ya da `.crt` dosyasını makinenin **Trusted Root Certification Authorities** deposuna ekler. Tenant değişirse bu dosyayı yenisiyle değiştirin.

- Subject: `CN=Koi Root CA, O=KoiSecurity, OU=tstc`
- Thumbprint (SHA-1): `758A887D7DCA2EA140C561B913DA5DFB0027EA5C`
- Geçerlilik sonu: 16 Haziran 2036
