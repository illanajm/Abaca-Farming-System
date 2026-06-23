import pandas as pd


def generate_analysis_engine(
        filtered_farmers,
        filtered_farms,
        filtered_pests,
        correlation=None
):

    interpretation = []
    insights = []
    recommendations = []


    # =========================
    # DATA VALIDATION
    # =========================

    if filtered_farms.empty:

        return {
            "interpretation": [
                "No farm records available for statistical interpretation."
            ],

            "insights": [
                "The selected filters do not contain farm production data."
            ],

            "recommendations": [
                "Register farm information before performing productivity analysis."
            ]
        }



    # =========================
    # BASIC STATISTICS
    # =========================

    avg_yield = filtered_farms["Yield"].mean()
    yield_std = filtered_farms["Yield"].std()

    avg_area = filtered_farms["Farm Area"].mean()


    # =========================
    # INTERPRETATION ENGINE
    # =========================


    if len(filtered_farms) < 3:

        interpretation.append(
            "The dataset contains limited farm records. Statistical conclusions should be interpreted cautiously."
        )

    else:

        cv = (yield_std / avg_yield) * 100


        if cv < 15:
            interpretation.append(
                "Yield production shows high consistency among farms."
            )

        elif cv < 30:
            interpretation.append(
                "Yield production shows moderate variation among farms."
            )

        else:
            interpretation.append(
                "Yield production varies significantly, indicating differences in farm management practices."
            )



    # =========================
    # FARM AREA RELATIONSHIP
    # =========================


    if correlation is not None and len(filtered_farms) >= 3:


        if correlation >= 0.6:

            insights.append(
                "Farm size has a strong positive association with yield based on available records."
            )

        elif correlation >= 0.3:

            insights.append(
                "Farm size shows a moderate relationship with yield."
            )

        else:

            insights.append(
                "Farm size alone does not strongly explain yield differences."
            )


    else:

        insights.append(
            "There is insufficient farm data to establish a reliable relationship between farm size and yield."
        )



    # =========================
    # PEST ANALYSIS
    # =========================


    if not filtered_pests.empty:

        pest = filtered_pests["Pest Type"].mode()[0]

        insights.append(
            f"{pest} is the most frequently recorded pest issue."
        )


        recommendations.append(
            f"Prioritize monitoring and preventive control measures for {pest}."
        )


    else:

        insights.append(
            "No pest incidence was recorded in the selected dataset."
        )



    # =========================
    # PRODUCTIVITY RECOMMENDATION
    # =========================


    if yield_std > avg_yield * .3:

        recommendations.append(
            "Standardize cultivation practices to reduce yield variation among farms."
        )

    else:

        recommendations.append(
            "Maintain current farming practices since yield performance is relatively stable."
        )



    if avg_area > 0:

        recommendations.append(
            "Consider improving farm inputs, soil management, and cultivation methods to maximize productivity."
        )



    return {


        "interpretation": interpretation,

        "insights": insights,

        "recommendations": recommendations

    }