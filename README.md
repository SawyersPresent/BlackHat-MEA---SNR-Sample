# Wi‑Fi Proximity Detection & Machine Learning
# Black Hat MEA 2025 — Live Demonstration
# NOTE: EDUCATIONAL USE ONLY — Defensive research, awareness, and ethical demos.
# Do NOT use for unauthorized surveillance, espionage, or any illegal activity.

Overview
--------
This repository contains presentation materials, demonstration assets, and research notes for a Black Hat MEA 2025 live demonstration titled "Turning Wireless Signals into Proximity Intelligence."

The materials show how radio signal characteristics (e.g., SNR variations) can be used to infer physical proximity and how machine learning can improve contextual accuracy. The goal is to raise awareness about how seemingly benign wireless signals can be leveraged to create proximity‑aware behavior — and to encourage defensive mitigations and policy controls.

What this research demonstrates (high level)
--------------------------------------------
- How SNR and signal changes can correlate with physical proximity.
- How simple ML models can learn environmental baselines and improve classification of "VERY CLOSE", "CLOSE", and "NEAR" distance ranges.
- The risks that proximity‑based triggers pose for defensive tooling and sandbox evasion (conceptual, non‑actionable).
- Defensive countermeasures and monitoring techniques organizations can adopt.

Demo modes (presenter guidance)
------------------------------
- Simulated Demo: Use recorded or synthetic data to show the concept without interacting with live networks. 
- Live Demo (in-person, authorized environments only): If demonstrating with real radios, do so in a controlled, permissioned lab or stage environment. Obtain explicit written permission from facility owners and any participants. Prefer pre-recorded footage to reduce risk.

Safety, Legal, and Ethical Requirements
--------------------------------------
This research and its artifacts are strictly for:
- Security awareness training
- Defensive research
- Educational demonstrations conducted with explicit permission

Prohibited uses (examples)
- Unauthorized monitoring or tracking of people
- Targeted espionage, stalking, or privacy invasions
- Deploying code or tools against networks or devices without consent

If you do not have explicit permission for an environment, do not run live scans or interact with third‑party networks.

Technical summary (non‑actionable)
----------------------------------
- Core idea: monitor RF metadata (signal strength, SNR trends, stability) and map those features into proximity categories.
- ML enhancements: learn an environment baseline, compute deviations, and produce confidence scores for predictions so the system knows when to trust an inference.
- Emphasis: This repo focuses on research discussion, high‑level evaluation, and defensive recommendations — not on actionable offensive tooling.

Defensive recommendations (high level)
-------------------------------------
- Monitor for unusual Wi‑Fi scanning and netsh-like patterns at the endpoint.
- Implement application control and least privilege to restrict network scanning capabilities.
- Correlate physical access logs (badge entries, cameras) with suspicious network events.
- Conduct regular staff training on physical-cyber risk convergence.
- Use sandbox and analysis environments that do not expose host radio hardware unless expressly needed.
