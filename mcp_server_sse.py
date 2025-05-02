from random import random

from mcp.server import FastMCP
from mcp.server.fastmcp import Context

from shared.mcp_base_server import IzzyMCP

settings = {"host": "127.0.0.1", "port": 3500}
mcp = IzzyMCP("Contoso Medical MCP Service", log_level="DEBUG", **settings)

@mcp.tool(description="Returns the Information from the Service about Contoso Medical")
def get_information(ctx: Context) -> str:
    """
    Returns detailed information about the services and leadership of Contoso Medical.
    """
    info = """
    Welcome to Contoso Medical — Your Partner in Health and Wellness

    About Us:
    Contoso Medical is a leading healthcare provider dedicated to delivering compassionate, innovative, and high-quality care. 
    With over 25 years of service, we support communities through a comprehensive network of hospitals, specialty clinics, 
    urgent care centers, and telehealth platforms.

    Our Services:
    ----------------------------
    1. Primary Care
       - Family medicine
       - Preventive health screenings
       - Chronic disease management

    2. Specialty Care
       - Cardiology
       - Oncology
       - Neurology
       - Endocrinology
       - Rheumatology

    3. Women's Health
       - OB/GYN services
       - Fertility treatments
       - Breast health

    4. Pediatric Care
       - Newborn care
       - Immunizations
       - Pediatric specialists

    5. Mental Health Services
       - Counseling and therapy
       - Psychiatric evaluations
       - Substance use recovery programs

    6. Surgical Services
       - Minimally invasive procedures
       - Outpatient and inpatient surgery
       - Robotic-assisted surgery

    7. Emergency & Urgent Care
       - 24/7 Emergency Rooms
       - Trauma response teams
       - Walk-in urgent care centers

    8. Virtual Care
       - Telehealth visits
       - Online symptom checker
       - Prescription refills and follow-ups

    9. Senior Care
       - Geriatric specialists
       - Assisted living coordination
       - In-home care services

    Leadership Team:
    ----------------------------
    - Dr. Rebecca Lin, Chief Executive Officer
      With over 20 years of leadership in hospital administration, Dr. Lin is committed to operational excellence and patient-first innovation.

    - James Thornton, Chief Operating Officer
      A former U.S. Army medic, James brings strategic discipline and healthcare logistics experience to streamline operations.

    - Dr. Nia Kapoor, Chief Medical Officer
      A triple-board-certified physician, Dr. Kapoor champions clinical excellence and medical ethics.

    - Sarah Fields, Chief Nursing Officer
      Sarah leads all nursing teams across Contoso Medical’s network, emphasizing holistic, empathetic care.

    - Carlos Ramirez, Chief Information Officer
      With a background in health IT and cybersecurity, Carlos leads digital transformation and data governance.

    - Linda Green, Chief Financial Officer
      Linda oversees financial planning, budget efficiency, and sustainable growth.

    Our Commitment:
    ----------------------------
    At Contoso Medical, we believe that health is a human right. We invest in patient education, research partnerships, 
    and community wellness programs to ensure every individual has access to world-class healthcare.

    Contact Us:
    Visit us online at www.contosomedical.com or call us at 1-800-CONTOSO.

    Thank you for choosing Contoso Medical — Where Compassion Meets Innovation.
    """


    return info


@mcp.tool(description="Retrieves the Current Temperature in Fahrenheit for Contoso Islands")
async def get_temperature(ctx: Context) -> float:
    await ctx.debug(ctx.session)
    print(ctx.request_context)
    return random() * 95

@mcp.tool(description="Calculates the Taxes for a specific amount")
async def calculate_taxes(amount: float, ctx: Context) -> float:
    return random() * amount


if __name__ == "__main__":
    mcp.run(transport='sse')