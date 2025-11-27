import os
import re
import time
import subprocess
import sys

INTERFACE = "wlan0"
THRESHOLD_NEAR = 40
THRESHOLD_PRESENT = 25
THRESHOLD_AWAY = 15
SAMPLING_RATE = 0.5
SMOOTHING_FACTOR = 0.7

def get_wireless_metrics(interface):
    metrics = {'signal': None, 'noise': None}
    
    # Method 1: Use `iw`
    try:
        output = subprocess.check_output(
            ["iw", "dev", interface, "link"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        sig_match = re.search(r"signal:\s*(-?\d+)\s*dBm", output)
        if sig_match:
            metrics['signal'] = int(sig_match.group(1))
    except Exception:
        pass

    if metrics['signal'] is None:
        try:
            with open("/proc/net/wireless", "r") as f:
                for line in f.readlines()[2:]:
                    if interface in line:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            # Convert to dBm from quality (heuristic)
                            metrics['signal'] = int(float(parts[3]))
                            metrics['noise'] = int(float(parts[4]))
                            break
        except Exception:
            pass

    if metrics['signal'] is None:
        try:
            output = subprocess.check_output(
                ["iwconfig", interface],
                stderr=subprocess.DEVNULL,
                text=True
            )
            sig_match = re.search(r"Signal level=(-?\d+) dBm", output)
            noise_match = re.search(r"Noise level=(-?\d+) dBm", output)
            if sig_match:
                metrics['signal'] = int(sig_match.group(1))
            if noise_match:
                metrics['noise'] = int(noise_match.group(1))
        except Exception:
            pass

    return metrics

def calculate_snr(metrics):
    if metrics['signal'] is not None and metrics['noise'] is not None:
        return metrics['signal'] - metrics['noise']
    elif metrics['signal'] is not None:
        # Assume default noise floor if missing (e.g., -90 dBm)
        return metrics['signal'] + 90
    else:
        return None

def estimate_distance(snr):
    if snr is None or snr <= 0:
        return None
    return round(1000 / (snr + 5), 1)

def main():
    if not os.path.exists(f"/sys/class/net/{INTERFACE}"):
        print(f"ERROR: Interface {INTERFACE} not found!", file=sys.stderr)
        os.system("ip -o link | awk '!/loopback/ {print $2}' | cut -d':' -f1")
        sys.exit(1)

    smoothed_snr = None
    print("Wi-Fi Proximity Detection using SNR")
    print("=" * 50)
    print(f"{'Time':<8} | {'Signal':>7} | {'Noise':>7} | {'SNR':>6} | {'Dist':>6} | {'Status':<25}")
    print("-" * 75)

    try:
        while True:
            timestamp = time.strftime("%H:%M:%S")
            metrics = get_wireless_metrics(INTERFACE)
            snr = calculate_snr(metrics)

            if snr is not None:
                if smoothed_snr is None:
                    smoothed_snr = snr
                else:
                    smoothed_snr = SMOOTHING_FACTOR * smoothed_snr + (1 - SMOOTHING_FACTOR) * snr

            distance = estimate_distance(smoothed_snr) if smoothed_snr is not None else None

            if snr is None:
                status = "NO SIGNAL / UNAVAILABLE"
            elif smoothed_snr < 26:
                status = "VERY CLOSE (<50 cm)"
            elif smoothed_snr < 33:
                status = "NORMAL RANGE (0.5-2 m)"
            elif smoothed_snr < 40:
                status = "MOVING AWAY (2-4 m)"
            else:
                status = "FAR AWAY (>4 m)"

            signal_str = f"{metrics['signal']} dBm" if metrics['signal'] is not None else "N/A"
            noise_str = f"{metrics['noise']} dBm" if metrics['noise'] is not None else "N/A"
            snr_str = f"{smoothed_snr:.1f} dB" if smoothed_snr is not None else "N/A"
            dist_str = f"{distance} cm" if distance is not None else "N/A"

            print(
                f"{timestamp:<8} | {signal_str:>7} | {noise_str:>7} | {snr_str:>6} | {dist_str:>6} | {status:<25}",
                end="\r"
            )
            sys.stdout.flush()
            time.sleep(SAMPLING_RATE)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
