---
name: genpark-personal-agent-cardiac-ventricular-late-potentials-saecg-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for calculating Signal-Averaged ECG (SAECG) Ventricular Late Potentials (VLPs), RMS40, and arrhythmogenic substrate screening.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Cardiac Ventricular Late Potentials (SAECG) Skill

A sovereign personal agent capability for evaluating high-resolution Signal-Averaged Electrocardiogram (SAECG) signals, microvolt-level terminal fragmented conduction, Ventricular Late Potentials (VLPs), and re-entrant ventricular arrhythmia substrate risk.

## Core Capabilities
- **Simson 40 Hz Tri-Criteria Analysis**: Evaluates filtered QRS duration ($fQRS < 114\text{ ms}$), terminal 40 ms root mean square voltage ($RMS_{40} > 20\text{ }\mu\text{V}$), and terminal low-amplitude duration ($LAS_{40} < 38\text{ ms}$).
- **Ventricular Late Potential (VLP) Stratification**: Detects delayed fragmented depolarization in border zones of myocardial fibrosis when $\ge 2$ criteria fail.
- **Myocardial Electrical Stability Scoring**: Formulates overall intraventricular synchrony and sudden cardiac death substrate screening.
- **Cardiovascular Strain Protection**: Recommends autonomic down-regulation, avoidance of high-stimulant pre-workouts, and restorative recovery intervals.

## Fast Invocation
```python
from client import CardiacVentricularLatePotentialsClient

client = CardiacVentricularLatePotentialsClient()
res = client.evaluate_saecg(
    filtered_qrs_duration_ms=98.5,
    rms_40_uv=38.2,
    las_40_ms=24.0
)
print("VLP Positive:", res["vlp_positive"])
print("Synchrony Score:", res["myocardial_synchrony_score"], "/ 100")
```
