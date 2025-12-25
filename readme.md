________________________________________
# d11-risk-console

**Human-centered risk reasoning console for D11-class heavy equipment.**  
Deterministic safety engine with ML advisory overlays that can only increase caution.  
All decisions are human-gated, auditable, replayable, and tamper-evident.

This project simulates and visualizes operational risk for heavy equipment using
synthetic telemetry. It is designed to demonstrate how autonomy-adjacent systems
can support operators *without* removing human authority.

---

## Core Principles

This system is built around a few non-negotiable rules:

- **Determinism first**  
  All authoritative risk is computed via explicit, inspectable logic.

- **ML is advisory only**  
  Machine learning can *never* trigger actions, approvals, proposals, or I/O.
  ML outputs are bounded overlays that may only increase caution.

- **Human-gated decisions**  
  Recommendations are surfaced, not executed. The operator is always the authority.

- **Auditability over cleverness**  
  Every meaningful event is hash-chained and exportable.

- **Failure-tolerant by design**  
  ML failures disable ML — the simulation continues safely.

---

## What This Is (and Is Not)

### ✅ This is:
- A risk reasoning console for heavy equipment operations
- A demonstration of human-centered autonomy architecture
- A deterministic safety core with ML reliability overlays
- A replayable, inspectable, ops-grade system

### ❌ This is not:
- An autonomous control system
- A black-box ML decision engine
- A production control stack
- A real telemetry or machine interface

All telemetry in this project is **synthetic**.

---

## Architecture Overview

The system is intentionally split into hard boundaries:

sim/ → Synthetic telemetry + deterministic replay
core/ → Deterministic risk math, invariants, proposals, audit
ml/ → ML advisory overlays (bounded, optional, integrity-checked)
ui/ → Streamlit UI (thin shell)
app/ → Application entrypoint

### Deterministic Core (`core/`)
- Computes rollover, slip, obstacle, and GNSS risks
- Produces a single authoritative `overall_risk`
- Classifies system state (STABLE → CRITICAL)
- Generates **deterministic-only** recommendations
- Enforces invariants (ML can never reduce risk)

### ML Advisory Layer (`ml/`)
- Computes:
  - anomaly score
  - out-of-distribution score
  - causal uncertainty
- Produces:
  - caution multipliers ≥ 1.0
  - per-sensor reliability estimates
- Is:
  - optional
  - bounded
  - cryptographically verified
- Can be disabled without stopping the system

### Audit Chain (`core/audit.py`)
- Append-only
- Hash-chained (tamper-evident)
- Covers:
  - control actions
  - ML flags
  - proposals
  - resets
- Exportable as CSV or JSON

### Replay & Determinism
- Telemetry is regenerated from:
  - seed
  - tick
  - sim config
- Allows side-by-side replay:
  - deterministic only
  - deterministic + ML overlay
- Makes ML influence measurable and reviewable

---

## Safety Guarantees (Enforced in Code)

The system explicitly enforces the following invariants:

- ML cannot reduce overall risk
- ML cannot reduce GNSS penalty weighting
- ML cannot generate proposals
- ML cannot execute actions
- Integrity failure disables ML immediately
- Reset requires a two-phase confirm
- History cannot be silently altered

Violations halt the simulation and are logged.

---

## Running the Console

### Requirements
- Python 3.10+
- Virtual environment recommended

### Install
```bash
pip install -r requirements.txt
Run
streamlit run app/app.py
You will see a live console with:
•	risk timeline
•	operator context
•	ML reliability overlays
•	human-gated recommendations
•	audit trail
________________________________________
ML Artifacts & Integrity
ML models are stored as artifacts with sidecar SHA-256 hashes.
At load time:
•	missing sidecar → ML disabled
•	hash mismatch → ML disabled
•	simulation continues safely
No retraining occurs automatically.
No silent fallback occurs.
________________________________________
Reset & Snapshots
Reset is intentionally slow and explicit:
1.	Arm reset
2.	Confirm reset within timeout
3.	Snapshot written to disk
4.	Session state cleared
Snapshots include:
•	session contract
•	telemetry history
•	proposals
•	audit log
•	active ML configuration
This supports post-incident review and reproducibility.
________________________________________
Intended Audience
This project is designed for:
•	infrastructure engineers
•	autonomy and robotics engineers
•	safety reviewers
•	operators and supervisors
•	systems architects
It is intentionally conservative, explicit, and boring in the right ways.
________________________________________
License & Use
This repository is provided for educational and architectural demonstration
purposes. It does not control real equipment.
Use it to study:
•	human-in-the-loop autonomy
•	deterministic safety design
•	ML reliability framing
•	audit-first system architecture
________________________________________
