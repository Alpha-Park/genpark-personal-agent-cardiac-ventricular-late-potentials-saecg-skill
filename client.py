"""
Cardiac Ventricular Late Potentials (SAECG) & Myocardial Synchrony Engine.
Provides deterministic, zero-dependency modeling of Signal-Averaged Electrocardiogram (SAECG),
filtered QRS duration (ms), terminal 40ms RMS voltage (uV), low-amplitude signal duration (LAS40 ms), and arrhythmogenic substrate screening.
"""

from typing import Dict, Any, List, Optional


class CardiacVentricularLatePotentialsClient:
    """
    Deterministic client for calculating Signal-Averaged ECG (SAECG) Ventricular Late Potentials (VLPs).
    Assesses slow, fragmented epicardial/endocardial conduction, myocardial fibrotic borders,
    re-entrant ventricular arrhythmogenic substrate, and sudden cardiac death risk stratification.
    """

    def __init__(self):
        pass

    def evaluate_saecg(
        self,
        filtered_qrs_duration_ms: float,
        rms_40_uv: float,
        las_40_ms: float,
        high_pass_filter_hz: int = 40
    ) -> Dict[str, Any]:
        """
        Calculates Simson criteria positivity for Ventricular Late Potentials (VLPs).
        Normative values (at 40 Hz high-pass filter):
        - Filtered QRS duration (fQRS): < 114.0 ms (abnormal >= 114.0 ms)
        - Root Mean Square voltage of terminal 40ms (RMS40): > 20.0 uV (abnormal <= 20.0 uV)
        - Duration of terminal signals < 40 uV (LAS40): < 38.0 ms (abnormal >= 38.0 ms)
        - Positive VLP = >= 2 of 3 criteria met
        """
        if filtered_qrs_duration_ms <= 0 or rms_40_uv <= 0 or las_40_ms < 0:
            return {"error": "Filtered QRS duration, RMS40, and LAS40 must be non-negative (fQRS & RMS strictly positive)"}

        # 1. Evaluate Simson Criteria
        crit_fqrs_abnormal = filtered_qrs_duration_ms >= 114.0
        crit_rms40_abnormal = rms_40_uv <= 20.0
        crit_las40_abnormal = las_40_ms >= 38.0

        abnormal_criteria_count = sum([crit_fqrs_abnormal, crit_rms40_abnormal, crit_las40_abnormal])
        vlp_positive = abnormal_criteria_count >= 2

        # 2. Myocardial Depolarization Synchrony Score (0 - 100)
        score = 80.0
        if filtered_qrs_duration_ms <= 100.0:
            score += 10.0
        elif filtered_qrs_duration_ms <= 110.0:
            score += 5.0
        elif filtered_qrs_duration_ms >= 125.0:
            score -= 22.0
        elif filtered_qrs_duration_ms >= 114.0:
            score -= 12.0

        if rms_40_uv >= 35.0:
            score += 10.0
        elif rms_40_uv >= 22.0:
            score += 5.0
        elif rms_40_uv <= 12.0:
            score -= 25.0
        elif rms_40_uv <= 20.0:
            score -= 12.0

        if las_40_ms <= 28.0:
            score += 5.0
        elif las_40_ms >= 45.0:
            score -= 20.0
        elif las_40_ms >= 38.0:
            score -= 10.0

        synchrony_score = round(min(100.0, max(5.0, score)), 1)

        if synchrony_score >= 85.0 and abnormal_criteria_count == 0:
            tier = "OPTIMAL_VENTRICULAR_DEPOLARIZATION_SYNCHRONY"
            interp = f"Negative for Ventricular Late Potentials (fQRS {filtered_qrs_duration_ms} ms < 114 ms, RMS40 {rms_40_uv} uV > 20 uV, LAS40 {las_40_ms} ms < 38 ms); homogenous intraventricular conduction."
            guidance = "Superior myocardial electrical stability. Low substrate for re-entrant ventricular arrhythmias."
        elif vlp_positive:
            tier = "POSITIVE_VENTRICULAR_LATE_POTENTIALS"
            interp = f"Positive for Ventricular Late Potentials ({abnormal_criteria_count}/3 Simson criteria met); signifies fragmented, delayed microvascular conduction in fibrotic myocardial zones."
            guidance = "Arrhythmogenic slow-conduction substrate detected. Avoid intense sympato-mimetic stimulants and heavy unpaced anaerobic strain; recommend clinical cardiology review."
        else:
            tier = "BORDERLINE_SAECG_CONDUCTION_DELAY"
            interp = f"Isolated abnormal criterion (fQRS {filtered_qrs_duration_ms} ms, RMS40 {rms_40_uv} uV, LAS40 {las_40_ms} ms); minor terminal conduction delay."
            guidance = "Maintain electrolyte balance (potassium and magnesium); practice heart-rate variability restorative recovery."

        return {
            "high_pass_filter_hz": high_pass_filter_hz,
            "filtered_qrs_duration_ms": filtered_qrs_duration_ms,
            "rms_40_uv": rms_40_uv,
            "las_40_ms": las_40_ms,
            "abnormal_criteria_count": abnormal_criteria_count,
            "vlp_positive": vlp_positive,
            "myocardial_synchrony_score": synchrony_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }
