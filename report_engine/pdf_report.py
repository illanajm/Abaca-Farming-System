from io import BytesIO
from datetime import datetime

import plotly.express as px

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet



def generate_pdf_report(
        analysis,
        filtered_farmers,
        filtered_farms,
        filtered_pests
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        title="Abaca Farming Analytics Report"
    )


    styles = getSampleStyleSheet()

    elements = []



    # =================================
    # COVER PAGE
    # =================================

    elements.append(
        Paragraph(
            "<b>ABACA FARMING MANAGEMENT SYSTEM</b>",
            styles["Title"]
        )
    )


    elements.append(
        Spacer(1,10)
    )


    elements.append(
        Paragraph(
            "📊 EXECUTIVE ANALYTICS REPORT",
            styles["Heading2"]
        )
    )


    elements.append(
        Spacer(1,10)
    )


    elements.append(
        Paragraph(
            f"Generated Date: {datetime.now().strftime('%B %d, %Y')}",
            styles["Normal"]
        )
    )


    elements.append(
        Spacer(1,20)
    )



    # =================================
    # EXECUTIVE SUMMARY
    # =================================


    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Heading2"]
        )
    )


    avg_yield = (
        round(filtered_farms["Yield"].mean(),2)
        if not filtered_farms.empty
        else 0
    )


    most_common_pest = (
        filtered_pests["Pest Type"].mode()[0]
        if not filtered_pests.empty
        else "N/A"
    )


    summary = f"""
    This report provides an analytical overview of abaca farming operations.

    <br/><br/>

    Total Farmers:
    <b>{len(filtered_farmers)}</b>

    <br/>

    Total Farms:
    <b>{len(filtered_farms)}</b>

    <br/>

    Average Yield:
    <b>{avg_yield}</b>

    <br/>

    Most Common Pest:
    <b>{most_common_pest}</b>

    <br/><br/>

    The analysis is generated using the Abaca Analytics Engine.
    """



    elements.append(
        Paragraph(
            summary,
            styles["BodyText"]
        )
    )


    elements.append(
        Spacer(1,20)
    )



    # =================================
    # KPI TABLE
    # =================================


    elements.append(
        Paragraph(
            "Key Performance Indicators",
            styles["Heading2"]
        )
    )


    kpi_table = Table(
        [
            ["Metric","Value"],

            [
                "Farmers",
                len(filtered_farmers)
            ],

            [
                "Farms",
                len(filtered_farms)
            ],

            [
                "Average Yield",
                avg_yield
            ],

            [
                "Pest Incidents",
                len(filtered_pests)
            ]
        ],
        colWidths=[250,250]
    )


    kpi_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.HexColor("#006622")
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),

            (
                "GRID",
                (0,0),
                (-1,-1),
                .5,
                colors.grey
            ),

            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            )
        ])
    )


    elements.append(kpi_table)


    elements.append(
        Spacer(1,20)
    )



    # =================================
    # DATA VISUALIZATION
    # =================================


    elements.append(
        Paragraph(
            "Data Visualization",
            styles["Heading2"]
        )
    )


    if not filtered_farms.empty:


        fig = px.scatter(
            filtered_farms,
            x="Farm Area",
            y="Yield",
            color="Soil Type",
            title="Farm Area vs Yield"
        )


        img = fig.to_image(
            format="png"
        )


        chart = Image(
            BytesIO(img),
            width=480,
            height=300
        )


        elements.append(chart)



    elements.append(
        Spacer(1,20)
    )



    # =================================
    # FARMER TABLE
    # =================================


    elements.append(
        Paragraph(
            "Farmer Demographics",
            styles["Heading2"]
        )
    )


    if not filtered_farmers.empty:


        farmer_table = Table(
            [
                filtered_farmers.columns.tolist()
            ]
            +
            filtered_farmers.astype(str)
            .values
            .tolist()
        )


        farmer_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.HexColor("#009933")
                ),

                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,0),
                    colors.white
                ),

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    .3,
                    colors.grey
                ),

                (
                    "FONTSIZE",
                    (0,0),
                    (-1,-1),
                    7
                )

            ])
        )


        elements.append(
            farmer_table
        )



    elements.append(
        Spacer(1,20)
    )



    # =================================
    # AI INTERPRETATION
    # =================================


    elements.append(
        Paragraph(
            "AI Interpretation",
            styles["Heading2"]
        )
    )


    for item in analysis["interpretation"]:


        elements.append(
            Paragraph(
                "• " + item,
                styles["BodyText"]
            )
        )



    elements.append(
        Spacer(1,20)
    )



    # =================================
    # AI INSIGHTS
    # =================================


    elements.append(
        Paragraph(
            "AI Generated Insights",
            styles["Heading2"]
        )
    )


    for item in analysis["insights"]:


        elements.append(
            Paragraph(
                "• " + item,
                styles["BodyText"]
            )
        )



    elements.append(
        Spacer(1,20)
    )



    # =================================
    # AI RECOMMENDATIONS
    # =================================


    elements.append(
        Paragraph(
            "AI Recommendations",
            styles["Heading2"]
        )
    )


    for item in analysis["recommendations"]:


        elements.append(
            Paragraph(
                "• " + item,
                styles["BodyText"]
            )
        )



    elements.append(
        Spacer(1,20)
    )



    elements.append(
        Paragraph(
            "Generated by Abaca Farming Management System © 2026",
            styles["Italic"]
        )
    )



    doc.build(elements)


    buffer.seek(0)


    return buffer