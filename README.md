<div align="center">

# CAN-Guard: ML Intrusion Detection for Automotive Networks 🚗⚡

[![CI](https://github.com/Lohit-18/can-guard/actions/workflows/ci.yml/badge.svg)](https://github.com/Lohit-18/can-guard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-1c6e46.svg)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![ML Stack](https://img.shields.io/badge/ML-PyTorch%20%7C%20Scikit--Learn-orange.svg)]()
[![Reproducible](https://img.shields.io/badge/results-bit--for--bit%20reproducible-1c6e46.svg)](#evaluation-metrics)

**A production-ready OT security layer designed to detect injection, masquerade, and zero-day anomalies across dual-CAN architectures using multidimensional physics and timing heuristics.**

</div>

---

## 1. Executive Summary

CAN-Guard is an offline, machine-learning-backed Intrusion Detection System (IDS) engineered for modern automotive networks. Because standard Controller Area Network (CAN) protocols (ISO 11898) lack native payload encryption or transmitter authentication, in-vehicle networks are highly susceptible to spoofing and denial-of-service (DoS) attacks.

This system intercepts raw CAN frames, extracts 88 domain-specific features across a sliding time window, and evaluates them against an ensemble of supervised and unsupervised machine learning models to accurately classify malicious bus activity in real time.

---

## 2. System Architecture

```mermaid
flowchart LR
    subgraph Vehicle Topology
        A[Engine Control Unit<br>HS-CAN: 0x100] --> Bus[CAN Bus Interface]
        B[Brake Control Unit<br>HS-CAN: 0x300] --> Bus
        C[Body Control Unit<br>MS-CAN: 0x200] --> Bus
    end

    subgraph CAN-Guard IDS Pipeline
        Bus --> D[Packet Sniffer & Decoder]
        D --> E{Feature Extraction Engine}
        E -->|Timing | F1[IAT & Clock Skew]
        E -->|Integrity| F2[Payload Entropy]
        E -->|Physics| F3[Cross-ECU Validation]
        
        F1 & F2 & F3 --> G((Ensemble ML Engine))
        G --> H1[Random Forest]
        G --> H2[MLP Neural Network]
        G --> H3[Isolation Forest]
    end

    G --> I{Threat Classifier}
    I -->|Anomaly Detected| J[Trigger Dashboard Alert]
    
    classDef sim fill:#0d1117,stroke:#3fb950,color:#c9d1d9
    classDef engine fill:#161b22,stroke:#58a6ff,color:#c9d1d9
    class A,B,C,Bus sim
    class D,E,F1,F2,F3,G,H1,H2,H3,I,J engine