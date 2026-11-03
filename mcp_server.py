"""
MCP Server for Cardiac Ventricular Late Potentials (SAECG) Skill.
Exposes JSON-RPC Model Context Protocol tools for evaluating Simson SAECG criteria, RMS40, and arrhythmogenic substrate scores.
"""

import sys
import json
from typing import Dict, Any
from client import CardiacVentricularLatePotentialsClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_saecg",
                "description": "Calculates Signal-Averaged ECG (SAECG) Ventricular Late Potentials (VLPs) Simson criteria, RMS40 (uV), LAS40 (ms), and myocardial synchrony score.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filtered_qrs_duration_ms": {
                            "type": "number",
                            "description": "Total filtered QRS duration fQRS in milliseconds (normative < 114.0 ms, e.g. 102.0 ms)."
                        },
                        "rms_40_uv": {
                            "type": "number",
                            "description": "Root Mean Square voltage of the terminal 40 ms in microvolts (normative > 20.0 uV, e.g. 32.5 uV)."
                        },
                        "las_40_ms": {
                            "type": "number",
                            "description": "Duration of terminal low-amplitude signals < 40 uV in milliseconds (normative < 38.0 ms, e.g. 26.0 ms)."
                        },
                        "high_pass_filter_hz": {
                            "type": "integer",
                            "description": "Bi-directional high-pass filter frequency in Hz (default: 40 Hz).",
                            "default": 40
                        }
                    },
                    "required": ["filtered_qrs_duration_ms", "rms_40_uv", "las_40_ms"]
                }
            }
        ]
    }


def handle_request(client: CardiacVentricularLatePotentialsClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_saecg":
            res = client.evaluate_saecg(
                filtered_qrs_duration_ms=float(args.get("filtered_qrs_duration_ms", 102.0)),
                rms_40_uv=float(args.get("rms_40_uv", 30.0)),
                las_40_ms=float(args.get("las_40_ms", 28.0)),
                high_pass_filter_hz=int(args.get("high_pass_filter_hz", 40))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {name}"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": f"Invalid Request: Unsupported method {method}"
            }
        }


def main():
    client = CardiacVentricularLatePotentialsClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error or exception: {str(e)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
