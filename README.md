Set-Content -Path README.md -Value @"
<div align="center">

<img src="docs/banner.png" alt="CAN-Guard" width="100%">

<br>

[![CI](https://github.com/Lohit-18/can-guard/actions/workflows/ci.yml/badge.svg)](https://github.com/Lohit-18/can-guard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-1c6e46.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%20%E2%80%93%203.13-a87c00.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15%2B-a87c00.svg)](https://www.tensorflow.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-a87c00.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/tests-59%20passing-1c6e46.svg)](tests/)
[![Reproducible](https://img.shields.io/badge/results-bit--for--bit%20reproducible-1c6e46.svg)](#reproducibility)

**A modern car is fifty to a hundred computers sharing one broadcast wire with no authentication.**  
**Anything that can transmit can claim to be the brake controller. CAN-Guard notices when something does.**

[Results](#results) · [How it works](#how-it-works) · [Quick start](#quick-start) · [Limitations](#limitations-the-part-worth-reading) · [Licence](#licence)

</div>

---

## What this is

CAN-Guard is an intrusion detection system for the Controller Area Network bus inside a vehicle. It watches the traffic, learns what a healthy bus looks like while the car is driven normally, and raises an alarm when the messages stop agreeing with each other or with physics.

It detects five families of attack — unauthorized throttle commands, forged brake signals, denial-of-service floods, fuzzing sweeps and replayed recordings — under **two threat models**, including the stealthy one where the attacker silences the real ECU and transmits in its place with perfect timing.

The whole thing runs offline on a laptop in about two minutes. There is no cloud service, no GPU, no account, and no dataset to buy: a physics-based vehicle and bus simulator generates the traffic, so every result here reproduces from a clean checkout.

```bash
pip install -r requirements.txt
python run_all.py