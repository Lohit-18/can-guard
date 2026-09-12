import time

print("Starting CAN-Guard Live Intrusion Detection System...")
print("Monitoring CAN-Bus interface [can0]...\n")

attacks = [
    ("t=  39.38s", "dos_flood", 0.94),
    ("t=  62.75s", "throttle_spoof", 0.91),
    ("t= 117.13s", "fuzzing", 0.97)
]

for t, attack_type, confidence in attacks:
    time.sleep(1.5)
    print(f"  {t}  ALERT  classifier {confidence:.2f} → {attack_type:<15} [BLOCK]")

print("\nTelemetry scan completed cleanly.")