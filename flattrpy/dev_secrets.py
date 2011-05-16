
FLATTR_API_KEY = "<testing>"
FLATTR_API_SECRET = "<testing>"
DJANGO_SECRET_KEY = '244ce28557ba6b4c1196dcbfa24113a63ba60883'


if __name__ == "__main__":
    import hmac
    import hashlib    
    import getpass
    print "Regenerating live secrets file"
    pwd = getpass.getpass("Password: ")
    check_pwd = 'ad269e258fa2f0c90429d13db8adb004b92c4c88'
    assert hmac.HMAC(pwd,"testing",hashlib.sha1).hexdigest() == check_pwd
    #  Build an encryption trans table based on each byte's
    #  relative order in the sha1 stream of the key.
    found = []
    remaining = set(chr(x) for x in xrange(256))
    key = pwd
    while remaining:
        key = hashlib.sha1(key).digest()
        for c in key:
            if c in remaining:
                found.append(c)
                remaining.remove(c)
    etrans = "".join(found)
    def encrypt(s):
        return s.translate(etrans)
    #  Now reverse it into a decryption trans table.
    found = []
    for c in xrange(256):
        found.append(chr(etrans.index(chr(c))))
    dtrans = "".join(found)
    def decrypt(s):
        return s.translate(dtrans)
    #  Write out the encrypted secrets
    import os
    live_file = os.path.join(os.path.dirname(__file__),"live_secrets.py")
    with open(live_file,"w") as f:
        f.write("DJANGO_SECRET_KEY = '%s'\n" % (decrypt('W[D\xa8brs-S\xf67W\x83\x14\x8e\x91\x8b\x1e\xa7\x81\x1e\xd9\xae\x96\x06\x0f\x8b\xae\xa2V\x83\xc3bP\xc8~n\xf6\x96\xd9\x91D\xc3\xcb\xe8\x99\xcb\xbb\xa2\x99'),))
        f.write("FLATTR_API_KEY = '%s'\n" % (decrypt("2n]}\x06\xceV\x81\x08[6+\x196\x83\xbb]\xa2\xf6\xe4{+P\xe8\x0f\xc4\x9e}V\xaeA\xbb\xc3{\xd8\xbbr]P\x81D\x83n\xd8\xfb\xf7S\x86\x19-X'\x86n\x08\x14+\xa6lsR\xe8\x12A"),))
        f.write("FLATTR_API_SECRET = '%s'\n" % (decrypt("\xbb\xcd2qq\x14;\x86'R;\x14\x8e\x97\xd8}5\x97\x8e\xe8\xb8\x86\xcdAA\x14+\x8b\xcd'\xf6\x122;\x14\xe8\xb8;\x8e\x11\xe8I\x11V\x05\xae\x11-\xce\xa766\x14\x12\xa6A5\x08\xaeX\xbb\xa6D\xae"),))

