# Cardiac Ventricular Late Potentials (SAECG) Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for non-invasive evaluation of Signal-Averaged ECG (SAECG) Ventricular Late Potentials (VLPs), terminal microvolt fragmentation, and arrhythmogenic substrate screening.

```mermaid
flowchart TD
    RawECG["High-Resolution Multilead Signal-Averaged ECG (>= 250 beats)"] --> BiFilter["Bi-Directional 40 Hz High-Pass Butterworth Filter"]
    BiFilter --> VectorMag["Vector Magnitude QRS Complex: X^2 + Y^2 + Z^2"]
    VectorMag --> SimsonMetrics["Simson Criteria: Filtered QRS (fQRS), RMS40 (uV), LAS40 (ms)"]
    SimsonMetrics --> VLP_Check["Late Potentials Gating (>= 2 of 3 Criteria Met)"]
    VLP_Check --> SynchronyScore["Myocardial Conduction Synchrony & Arrhythmic Risk Score"]
    SynchronyScore --> Agent["OpenClaw / Hermes Personal Agent Recovery Guarding"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Electrophysiology Standards**: Implements validated Simson 40 Hz high-pass criteria for ventricular late potentials.
- **Myocardial Electrical Stability**: Highly sensitive detection of slow, fragmented conduction predisposing to re-entrant ventricular tachyarrhythmias.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import CardiacVentricularLatePotentialsClient

client = CardiacVentricularLatePotentialsClient()
result = client.evaluate_saecg(
    filtered_qrs_duration_ms=98.5,
    rms_40_uv=38.2,
    las_40_ms=24.0
)
print("VLP Positive:", result["vlp_positive"])
print("Synchrony Score:", result["myocardial_synchrony_score"])
print("Classification:", result["classification"])
```

## License
Apache-2.0
