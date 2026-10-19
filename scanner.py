import concurrent.futures
import os
import random
import time
import requests

# ==========================================
# MiTV Network - Pro M3U Scanner Engine
# Organization: MUSLIM ISLAM
# ==========================================

COMMON_PORTS = [80, 8080, 8000, 8880, 25461, 8443, 5000, 81]
IP_PREFIXES = [
    39,
    43,
    103,
    110,
    119,
    120,
    175,
    182,
    202,
    221,
    114,
    115,
    1,
    2,
    14,
    27,
    36,
]


def generate_random_ip():
  first = random.choice(IP_PREFIXES)
  second = random.randint(0, 255)
  third = random.randint(0, 255)
  fourth = random.randint(1, 254)
  return f"{first}.{second}.{third}.{fourth}"


def check_playlist(ip, port):
  url = f"http://{ip}:{port}/playlist.m3u"
  try:
    response = requests.get(url, timeout=2.5)
    if response.status_code == 200:
      content = response.text
      if "#EXTM3U" in content or "#EXTINF" in content:
        print(f"[+] VALID M3U FOUND: {url}")

        # Safe file write with deduplication
        filename = "found_playlists.txt"
        existing = []
        if os.path.exists(filename):
          with open(filename, "r", encoding="utf-8") as f:
            existing = f.read().splitlines()

        if url not in existing:
          with open(filename, "a", encoding="utf-8") as f:
            f.write(url + "\n")
          print(f"[SAVED] Added to {filename}")
        return True
  except requests.exceptions.RequestException:
    pass
  return False


def scan_worker(_):
  ip = generate_random_ip()
  for port in COMMON_PORTS:
    if check_playlist(ip, port):
      break


def main():
  print("=" * 60)
  print(" MiTV Network - Pro Level 24/7 M3U IP Scanner ")
  print(" Organization: MUSLIM ISLAM | Kasur, Punjab, Pakistan ")
  print("=" * 60)

  start_time = time.time()
  # Run for roughly 4 hours 45 minutes before safe exit to restart
  max_runtime_seconds = 17100

  with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
    while (time.time() - start_time) < max_runtime_seconds:
      futures = [executor.submit(scan_worker, i) for i in range(120)]
      concurrent.futures.wait(futures)

  print(
      "\n[INFO] Scan session completed safely. Preparing for automated workflow"
      " restart..."
  )


if __name__ == "__main__":
  main()
