"""
Example Usage: Cardiac Ventricular Late Potentials (SAECG) & Myocardial Synchrony.
Demonstrates zero-dependency calculation of SAECG Simson criteria, RMS40, and arrhythmogenic substrate scoring.
"""

from client import CardiacVentricularLatePotentialsClient


def main():
    client = CardiacVentricularLatePotentialsClient()
    print("=== Cardiac Ventricular Late Potentials (SAECG) Demo ===")

    # Test Case 1: Healthy homogenous intraventricular conduction (VLP Negative)
    res1 = client.evaluate_saecg(
        filtered_qrs_duration_ms=98.5,
        rms_40_uv=38.2,
        las_40_ms=24.0,
        high_pass_filter_hz=40
    )
    print("\nTest Case 1: Normal SAECG (VLP Negative)")
    print(f"  Filtered QRS (fQRS): {res1['filtered_qrs_duration_ms']} ms | RMS40: {res1['rms_40_uv']} uV | LAS40: {res1['las_40_ms']} ms")
    print(f"  Abnormal Criteria Count: {res1['abnormal_criteria_count']} / 3 | VLP Positive: {res1['vlp_positive']}")
    print(f"  Myocardial Synchrony Score: {res1['myocardial_synchrony_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Physiological Interpretation: {res1['physiological_interpretation']}")
    print(f"  Actionable Guidance: {res1['actionable_guidance']}")

    # Test Case 2: Positive Ventricular Late Potentials (Arrhythmogenic slow conduction substrate)
    res2 = client.evaluate_saecg(
        filtered_qrs_duration_ms=124.0,
        rms_40_uv=14.5,
        las_40_ms=44.0,
        high_pass_filter_hz=40
    )
    print("\nTest Case 2: Positive Ventricular Late Potentials Pattern")
    print(f"  fQRS: {res2['filtered_qrs_duration_ms']} ms | RMS40: {res2['rms_40_uv']} uV | LAS40: {res2['las_40_ms']} ms")
    print(f"  Abnormal Criteria Count: {res2['abnormal_criteria_count']} / 3 | VLP Positive: {res2['vlp_positive']}")
    print(f"  Myocardial Synchrony Score: {res2['myocardial_synchrony_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Actionable Guidance: {res2['actionable_guidance']}")


if __name__ == "__main__":
    main()
