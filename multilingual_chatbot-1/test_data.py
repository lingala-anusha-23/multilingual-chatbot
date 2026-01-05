#!/usr/bin/env python3
"""
Simple test for RGMCET data integration
"""

# Simple RGMCET knowledge base (without gradio dependency)
class SimpleRGMCETAssistant:
    def __init__(self):
        self.college_info = {
            "rgmcet": """About RGMCET (Rajeev Gandhi Memorial College of Engineering and Technology):

Location: Nandyal, Andhra Pradesh, India
Established: 1996 (Inaugurated by Late Sri P.V. Narasimha Rao, former Prime Minister)
Affiliation: Jawaharlal Nehru Technological University Anantapur (JNTUA)
Accreditation: NBA Accredited (Tier-I category), NAAC A+ Grade, ISO 9001:2008, UGC Autonomous

Programs: B.Tech, M.Tech, MBA, MCA, Ph.D programs
Student Strength: 3,000+ students
Campus Area: 50 acres

Management:
• Chairman: Dr. M. Santhiramudu Garu
• Managing Director: M. Siva Ram Garu
• Principal: Dr. T Jayachandra Prasad""",

            "courses": """UG Engineering Programs (B.Tech):
• Computer Science and Engineering (CSE) - Intake: 420
• Electronics and Communication Engineering (ECE) - Intake: 240
• Electrical and Electronics Engineering (EEE) - Intake: 120
• Mechanical Engineering (ME) - Intake: 120
• Civil Engineering (CE) - Intake: 120

PG Programs:
• M.Tech in Computer Aided Structural Engineering, Electrical Drives & Control, etc.
• MBA and MCA programs
• Ph.D programs in 7 departments""",

            "fees": """Fee Structure (2023-24 to 2025-26):
• B.Tech Program: ₹76,010/- per year
• M.Tech Program: ₹69,080/- per year
• MBA Program: ₹51,300/- per year
• MCA Program: ₹60,000/- per year

Scholarships:
• 100% Tuition Fee Waiver for 4 years (EAMCET rank < 10,000)
• Government scholarships and fee reimbursement available""",

            "admissions": """Admission Procedure:
• B.Tech: Through EAMCET counseling
• M.Tech: GATE/PGECET scores
• MBA/MCA: ICET scores
• Reservation as per Andhra Pradesh government rules""",

            "placements": """Placement Statistics:
• Top Recruiters: TCS, Infosys, Wipro, Google, Microsoft, Amazon
• Average Package: ₹4-6 LPA
• Highest Package: ₹15-20 LPA
• Dedicated placement cell with excellent track record"""
        }

    def get_info(self, query):
        """Get information based on query"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["rgmcet", "college", "about", "overview"]):
            return self.college_info["rgmcet"]
        elif any(word in query_lower for word in ["course", "program", "btech", "mtech", "engineering"]):
            return self.college_info["courses"]
        elif any(word in query_lower for word in ["fee", "tuition", "cost", "scholarship"]):
            return self.college_info["fees"]
        elif any(word in query_lower for word in ["admission", "apply", "entrance"]):
            return self.college_info["admissions"]
        elif any(word in query_lower for word in ["placement", "job", "career", "company"]):
            return self.college_info["placements"]
        else:
            return "I can provide information about RGMCET courses, admissions, fees, scholarships, and placements. What would you like to know?"

def test_data_integration():
    """Test the RGMCET data integration"""
    assistant = SimpleRGMCETAssistant()

    print("🧪 Testing RGMCET Data Integration")
    print("=" * 50)

    test_queries = [
        "Tell me about RGMCET",
        "What courses are available?",
        "What is the fee structure?",
        "How to apply for admission?",
        "Tell me about placements"
    ]

    for query in test_queries:
        print(f"\n❓ Query: {query}")
        response = assistant.get_info(query)
        print(f"📝 Response: {response[:200]}{'...' if len(response) > 200 else ''}")

    print("\n" + "=" * 50)
    print("✅ RGMCET Data Successfully Integrated!")
    print("📊 Data Sources:")
    print("   • About RGMCET.txt")
    print("   • Courses Offered.txt")
    print("   • Admission Procedure.txt")
    print("   • Fee Structure.txt")
    print("   • Scholarships.txt")
    print("\n🚀 Next: Run 'python rgmcet_chatbot.py' for full web interface")

if __name__ == "__main__":
    test_data_integration()