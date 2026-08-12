from jga_uif.stitch.capsule import create_capsule
capsule = create_capsule(b"hello", "tx-1", "a", "b", "local", "nonce-12345678", 1)
print(capsule.capsule_id)
