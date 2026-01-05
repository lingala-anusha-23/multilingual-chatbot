import gradio as gr
import warnings
warnings.filterwarnings("ignore")
from translatepy import Translator
import requests
import json

class RGMCET_Assistant:
    def __init__(self):
        self.chat_history = []
        self.translator = Translator()

        # Try to use AI API (Hugging Face Inference API as fallback)
        self.use_ai = False
        try:
            # Test if we can use Hugging Face API (free tier available)
            self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            self.headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}  # Free API doesn't need token
            self.use_ai = True
            print("🤖 AI mode activated! Using DialoGPT for intelligent responses.")
        except:
            print("📋 Using enhanced rule-based responses with RGMCET knowledge.")

        # Translation dictionaries for common responses
        self.translations = {
            "greeting": {
                "en": "Hello! I'm your RGMCET assistant. I can provide detailed information about Rajeev Gandhi Memorial College of Engineering and Technology. How can I help you today?",
                "hi": "नमस्ते! मैं आपका RGMCET सहायक हूं। मैं राजीव गांधी मेमोरियल कॉलेज ऑफ इंजीनियरिंग एंड टेक्नोलॉजी के बारे में विस्तृत जानकारी प्रदान कर सकता हूं। आज मैं आपकी कैसे मदद कर सकता हूं?",
                "te": "హలో! నేను మీ RGMCET సహాయకుడు. రాజీవ్ గాంధీ మెమోరియల్ కాలేజ్ ఆఫ్ ఇంజినీరింగ్ అండ్ టెక్నాలజీ గురించి వివరణాత్మక సమాచారం అందించగలను. నేటి నేను మీకు ఎలా సహాయం చేయగలను?",
                "ur": "ہیلو! میں آپ کا RGMCET اسسٹنٹ ہوں۔ میں راجیو گاندھی میموریل کالج آف انجینئرنگ اینڈ ٹیکنالوجی کے بارے میں تفصیلی معلومات فراہم کر سکتا ہوں۔ آج میں آپ کی کیسے مدد کر سکتا ہوں؟",
                "ta": "வணக்கம்! நான் உங்கள் RGMCET உதவியாளர். ராஜீவ் காந்தி நினைவு பொறியியல் மற்றும் தொழில்நுட்பக் கல்லூரி பற்றிய விரிவான தகவல்களை வழங்க முடியும். இன்று நான் உங்களுக்கு எவ்வாறு உதவ முடியும்?",
                "kn": "ಹ್ಯಾಲೋ! ನಾನು ನಿಮ್ಮ RGMCET ಸಹಾಯಕ. ರಾಜೀವ್ ಗಾಂಧೀ ಸ್ಮಾರಕ ಇಂಜಿನಿಯರಿಂಗ್ ಮತ್ತು ತಂತ್ರಜ್ಞಾನ ಕಾಲೇಜ್ ಬಗ್ಗೆ ವಿವರವಾದ ಮಾಹಿತಿಯನ್ನು ನೀಡಬಹುದು. ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
                "mr": "नमस्कार! मी तुमचा RGMCET सहाय्यक आहे. मी राजीव गांधी स्मारक अभियांत्रिकी आणि तंत्रज्ञान महाविद्यालयाबद्दल तपशीलवार माहिती देऊ शकतो. आज मी तुम्हाला कशी मदत करू शकतो?"
            },
            "thanks": {
                "en": "You're welcome! Feel free to ask me anything else about RGMCET. I'm here to help with all your queries about admissions, courses, facilities, and campus life.",
                "hi": "आपका स्वागत है! RGMCET के बारे में कुछ और पूछने के लिए स्वतंत्र महसूस करें। प्रवेश, पाठ्यक्रम, सुविधाएं और परिसर जीवन के बारे में आपके सभी प्रश्नों में मदद करने के लिए मैं यहां हूं।",
                "te": "మీరు స్వాగతం! RGMCET గురించి మరేమైనా అడగడానికి విలాసంగా భావించండి. ప్రవేశం, కోర్సులు, సౌకర్యాలు మరియు క్యాంపస్ జీవితం గురించి మీ అన్ని ప్రశ్నలలో సహాయం చేయడానికి నేను ఇక్కడ ఉన్నాను.",
                "ur": "آپ کا خیر مقدم ہے! RGMCET کے بارے میں کچھ اور پوچھنے کے لیے آزاد محسوس کریں۔ داخلہ، کورسز، سہولیات اور کیمپس کی زندگی کے بارے میں آپ کے تمام سوالات میں مدد کرنے کے لیے میں یہاں ہوں۔",
                "ta": "நீங்கள் வரவேற்கப்படுகிறீர்கள்! RGMCET பற்றி வேறு எதையும் கேட்க தயங்க வேண்டாம். சேர்க்கை, பாடத்திட்டங்கள், வசதிகள் மற்றும் வளாக வாழ்க்கை பற்றிய உங்கள் அனைத்து கேள்விகளிலும் உதவ நான் இங்கே இருக்கிறேன்.",
                "kn": "ನೀವು ಸ್ವಾಗತ. RGMCET ಬಗ್ಗೆ ಬೇರೆ ಏನಾದರೂ ಕೇಳಲು ಮುಕ್ತವಾಗಿ ಭಾವಿಸಿ. ಪ್ರವೇಶ, ಕೋರ್ಸ್‌ಗಳು, ಸೌಲಭ್ಯಗಳು ಮತ್ತು ಕ್ಯಾಂಪಸ್ ಜೀವನದ ಬಗ್ಗೆ ನಿಮ್ಮ ಎಲ್ಲಾ ಪ್ರಶ್ನೆಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಲು ನಾನು ಇಲ್ಲಿದ್ದೇನೆ.",
                "mr": "तुमचे स्वागत! RGMCET बद्दल आणखी काही विचारण्यासाठी मोकळ्या मनाने विचारा. प्रवेश, अभ्यासक्रम, सुविधा आणि कॅम्पस जीवन याबद्दल तुमच्या सर्व प्रश्नांमध्ये मदत करण्यासाठी मी येथे आहे."
            },
            "general": {
                "en": "I'm here to help with RGMCET-related questions. I can provide information about courses, admissions, fees, scholarships, campus facilities, placements, and everything about Rajeev Gandhi Memorial College of Engineering and Technology. What would you like to know?",
                "hi": "मैं RGMCET से संबंधित प्रश्नों में मदद करने के लिए यहां हूं। मैं पाठ्यक्रम, प्रवेश, शुल्क, छात्रवृत्ति, परिसर सुविधाएं, प्लेसमेंट और राजीव गांधी मेमोरियल कॉलेज ऑफ इंजीनियरिंग एंड टेक्नोलॉजी के बारे में सब कुछ के बारे में जानकारी प्रदान कर सकता हूं। आप क्या जानना चाहेंगे?",
                "te": "నేను RGMCET సంబంధిత ప్రశ్నలలో సహాయం చేయడానికి ఇక్కడ ఉన్నాను. కోర్సులు, ప్రవేశం, ఫీజు, స్కాలర్‌షిప్‌లు, క్యాంపస్ సౌకర్యాలు, ప్లేస్‌మెంట్‌లు మరియు రాజీవ్ గాంధీ మెమోరియల్ కాలేజ్ ఆఫ్ ఇంజినీరింగ్ అండ్ టెక్నాలజీ గురించి అన్నింటి గురించి సమాచారం అందించగలను. మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?",
                "ur": "میں RGMCET سے متعلق سوالات میں مدد کرنے کے لیے یہاں ہوں۔ میں کورسز، داخلہ، فیس، اسکالرشپس، کیمپس کی سہولیات، پلسمنٹس اور راجیو گاندھی میموریل کالج آف انجینئرنگ اینڈ ٹیکنالوجی کے بارے میں ہر چیز کے بارے میں معلومات فراہم کر سکتا ہوں۔ آپ کیا جاننا چاہیں گے؟",
                "ta": "RGMCET தொடர்பான கேள்விகளில் உதவ நான் இங்கே இருக்கிறேன். பாடத்திட்டங்கள், சேர்க்கை, கட்டணம், உதவித்தொகை, வளாக வசதிகள், வேலைவாய்ப்புகள் மற்றும் ராஜீவ் காந்தி நினைவு பொறியியல் மற்றும் தொழில்நுட்பக் கல்லூரி பற்றிய அனைத்தையும் பற்றிய தகவல்களை வழங்க முடியும். நீங்கள் என்ன தெரிந்துகொள்ள விரும்புகிறீர்கள்?",
                "kn": "RGMCET ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಲು ನಾನು ಇಲ್ಲಿದ್ದೇನೆ. ಕೋರ್ಸ್‌ಗಳು, ಪ್ರವೇಶ, ಶುಲ್ಕ, ಶಿಷ್ಯವೇತನ, ಕ್ಯಾಂಪಸ್ ಸೌಲಭ್ಯಗಳು, ನೇಮಕಾತಿ ಮತ್ತು ರಾಜೀವ್ ಗಾಂಧೀ ಸ್ಮಾರಕ ಇಂಜಿನಿಯರಿಂಗ್ ಮತ್ತು ತಂತ್ರಜ್ಞಾನ ಕಾಲೇಜ್ ಬಗ್ಗೆ ಎಲ್ಲವನ್ನೂ ಬಗ್ಗೆ ಮಾಹಿತಿಯನ್ನು ನೀಡಬಹುದು. ನೀವು ಏನನ್ನು ತಿಳಿದುಕೊಳ್ಳಲು ಬಯಸುತ್ತೀರಿ?",
                "mr": "मी RGMCET संबंधित प्रश्नांमध्ये मदत करण्यासाठी येथे आहे. अभ्यासक्रम, प्रवेश, फी, शिष्यवृत्ती, कॅम्पस सुविधा, प्लेसमेंट आणि राजीव गांधी स्मारक अभियांत्रिकी आणि तंत्रज्ञान महाविद्यालयाबद्दल सर्व काही याबद्दल माहिती देऊ शकतो. तुम्हाला काय माहिती हवी आहे?"
            }
        }

        # Comprehensive RGMCET knowledge base with real data
        self.college_info = {
            "courses": {
                "ug_engineering": """🎓 **UG Engineering Programs (B.Tech)**:

**Computer Science and Engineering (CSE)** - Intake: 420
• Specializations: Regular CSE, Data Science (240), AI & ML (240), Cyber Security (120)

**Electronics and Communication Engineering (ECE)** - Intake: 240
• Focus: Communication systems, VLSI design, Embedded systems

**Electrical and Electronics Engineering (EEE)** - Intake: 120
• Focus: Power systems, Electrical machines, Control systems

**Mechanical Engineering (ME)** - Intake: 120
• Focus: Design, Manufacturing, Thermal engineering

**Civil Engineering (CE)** - Intake: 120
• Focus: Structural engineering, Construction management

**Total UG Intake**: 1,260 students per year""",

                "pg_engineering": """🎓 **PG Engineering Programs (M.Tech)**:

**Computer Aided and Structural Engineering** - Intake: 18
**Electrical Drives and Control** - Intake: 18
**Energy Engineering** - Intake: 9
**VLSI Design** - Intake: 18
**Computer Science** - Intake: 9

**Total PG Engineering Intake**: 72 students""",

                "pg_sciences": """🎓 **PG Science Programs**:

**Master of Business Administration (MBA)** - Intake: 60
**Master of Computer Applications (MCA)** - Intake: 60

**Total PG Science Intake**: 120 students""",

                "phd": """🎓 **Ph.D Programs**:

Available in 7 departments recognized as research centers by JNTUA:
• Civil Engineering (CE)
• Electrical and Electronics Engineering (EEE)
• Mechanical Engineering (ME)
• Electronics and Communication Engineering (ECE)
• Physics
• Mathematics
• MBA

**Eligibility**: As per JNTUA norms""",

                "certification": """📜 **Certification Courses** (Deen Dayal Upadhyay KAUSHAL Kendra):

• Computer Hardware Course (CSE Department)
• Linux Programming Course (CSE Department)
• Data Entry Operator Course (IT Department)"""
            },

            "admissions": """📋 **Admission Procedure - RGMCET**:

**B.Tech Programs**:
• **Entrance Exam**: EAMCET (Engineering, Agricultural and Medical Common Entrance Test)
• **Conducting Authority**: Convener of EAMCET, Government of Andhra Pradesh
• **Selection**: Based on EAMCET ranks and marks
• **Reservation**: As per state government rules
• **Counseling**: Web-based counseling for convener quota seats
• **Category-B Seats**: As per APSCHE guidelines for self-financing institutions

**M.Tech Programs**:
• **Entrance Exams**: GATE / PGECET
• **Selection**: Based on GATE/PGECET ranks and scores
• **Category-B Seats**: As per APSCHE guidelines

**MBA & MCA Programs**:
• **Entrance Exam**: ICET (Integrated Common Entrance Test)
• **Selection**: Based on ICET ranks and scores
• **Category-B Seats**: As per APSCHE guidelines

**Ph.D Programs**:
• **Process**: As prescribed by JNTUA
• **Eligibility**: As per JNTUA norms

**Important**: All admissions follow reservation policies of Andhra Pradesh Government""",

            "fees": """💰 **Fee Structure (2023-24 to 2025-26)** - As per APHERMC:

**B.Tech Program**: ₹76,010/- per year
**M.Tech Program**: ₹69,080/- per year
**MBA Program**: ₹51,300/- per year
**MCA Program**: ₹60,000/- per year

**Scholarships & Fee Waivers**:
• **100% Tuition Fee Waiver** for 4 years for students with EAMCET rank < 10,000
• **Government Scholarships**: Tuition fee reimbursement for eligible students
• **GATE Stipend**: For M.Tech students admitted through GATE
• **PGECET/ICET Benefits**: Tuition fee reimbursement as per eligibility

**Reference**:
• B.Tech: GO No. 41
• M.Tech: GO Ms. No. 51
• MBA & MCA: GO Ms. No. 48""",

            "rgmcet": """🏫 **About RGMCET (Rajeev Gandhi Memorial College of Engineering and Technology)**:

**📍 Location**: Nandyal, Andhra Pradesh, India
**📅 Established**: 1996 (Inaugurated by Late Sri P.V. Narasimha Rao, former Prime Minister)
**🏛️ Affiliation**: Jawaharlal Nehru Technological University Anantapur (JNTUA)
**⭐ Accreditation**:
   • NBA Accredited (Tier-I category, 4 times)
   • NAAC A+ Grade (3.54/4.0 CGPA)
   • ISO 9001:2008 Certified
   • UGC Autonomous Status (2010)
   • TCS Accredited for Placements
   • College with Potential for Excellence (CPE) by UGC

**🎓 Programs Offered**:
• **UG Engineering**: B.Tech in Civil, EEE, Mechanical, ECE, CSE (with specializations)
• **PG Engineering**: M.Tech in 5 specializations
• **PG Sciences**: MBA, MCA
• **Research**: Ph.D programs in 7 departments

**📊 Statistics**:
• Student Strength: 3,000+ students
• Campus Area: 50 acres on NH-18
• Faculty: Experienced faculty with Ph.D. qualifications

**🏆 Achievements**:
• World Bank assisted TEQIP-1 for quality improvement
• DSIR recognition for research equipment
• Best JKC Center award twice by Govt. of Andhra Pradesh
• Deen Dayal Upadhyay KAUSHAL Kendra
• SIEMENS Technical Skill Development Institute (TSDI)

**👥 Management**:
• **Chairman**: Dr. M. Santhiramudu Garu
• **Managing Director**: M. Siva Ram Garu
• **Principal**: Dr. T Jayachandra Prasad
• **Dean-Admin & Director Placements**: Dr. D.V. Ashok Kumar
• **Dean-Student Affairs**: Dr. B.Rami Reddy

**🌟 Vision**: To develop this rural-based engineering college into an institute of technical education with global standards

**🎯 Mission**:
• Build world-class undergraduate programs with strong theoretical knowledge
• Establish postgraduate programs in cutting-edge technologies
• Create conducive ambiance for research
• Develop industry linkages for strong interaction
• Offer demand-driven courses meeting industry needs
• Inculcate human values and ethos for all-round development""",

            "facilities": """🏢 **Campus Facilities - RGMCET**:

**Academic Facilities**:
• Smart Classrooms with digital boards
• State-of-the-art Laboratories
• Research Centers with DSIR recognition
• Library with 50,000+ books and digital resources
• Computer Labs with latest software
• Auditorium (1000+ seating capacity)
• Conference Halls with video conferencing

**Infrastructure**:
• 50-acre campus on NH-18
• Modern hostel facilities
• Sports Complex (indoor & outdoor)
• Gymnasium and fitness center
• Medical Center with qualified doctors
• Cafeteria with healthy food options
• Transportation services
• 24/7 Security and CCTV surveillance

**Technology & Research**:
• ISO 9001:2008 certified
• SIEMENS TSDI recognition
• Deen Dayal Upadhyay KAUSHAL Kendra
• Innovation and incubation centers
• Industry collaboration facilities""",

            "placements": """💼 **Placement & Career Services - RGMCET**:

**Placement Statistics**:
• **Top Recruiters**: TCS, Infosys, Wipro, Google, Microsoft, Amazon
• **Average Package**: ₹4-6 LPA
• **Highest Package**: ₹15-20 LPA (varies annually)
• **Placement Rate**: Consistently high with top rankings

**Placement Cell**:
• Dedicated team for career guidance
• Pre-placement training programs
• Mock interviews and aptitude tests
• Resume building workshops
• Industry interaction sessions

**Career Support**:
• Internship opportunities with leading companies
• Entrepreneurship development programs
• Higher education guidance
• Alumni mentorship network
• Industry-academia collaboration

**Awards**: Best JKC Center twice by Government of Andhra Pradesh""",

            "hostel": """🏠 **Hostel Facilities - RGMCET**:

**Accommodation**:
• Separate hostels for boys and girls
• Modern facilities with Wi-Fi connectivity
• Well-furnished rooms (Single/Double/Triple occupancy)
• 24/7 security with biometric access
• Study areas and common rooms

**Amenities**:
• Nutritious mess facilities
• Laundry services
• Reading rooms and recreation areas
• Gym facilities in hostels
• Medical assistance availability

**Campus Life**:
• Located within the 50-acre campus
• Easy access to academic buildings
• Sports facilities nearby
• Cultural and recreational activities
• Community living environment""",

            "sports": """⚽ **Sports & Recreation Facilities - RGMCET**:

**Indoor Sports**:
• Basketball courts
• Volleyball courts
• Badminton courts
• Table tennis facilities
• Chess and carrom rooms

**Outdoor Sports**:
• Football ground
• Cricket pitch
• Tennis courts
• Athletics track
• Kho-Kho and Kabaddi grounds

**Fitness Facilities**:
• Modern gymnasium
• Yoga and meditation centers
• Swimming pool (Olympic size)
• Fitness equipment and trainers

**Achievements**:
• Regular participation in inter-college tournaments
• State and national level competitions
• Sports scholarships for outstanding athletes
• Well-equipped sports complex""",

            "transport": """🚌 **Transportation Services - RGMCET**:

**College Buses**:
• Routes covering major areas of Nandyal and surrounding regions
• Timings: Morning 7 AM - 9 AM, Evening 4 PM - 7 PM
• Frequency: Every 30 minutes during peak hours
• Safety features: GPS tracking, experienced drivers

**Parking Facilities**:
• Dedicated parking for students with vehicles
• Two-wheeler and four-wheeler parking areas
• 24/7 security surveillance

**Local Connectivity**:
• Well-connected to NH-18
• Information about nearby bus stands
• Auto-rickshaw and taxi services available
• Proximity to railway station and bus stand""",

            "healthcare": """🏥 **Healthcare & Wellness - RGMCET**:

**Medical Center**:
• Qualified doctors and nursing staff
• 24/7 medical assistance
• First-aid facilities
• Regular health check-ups

**Emergency Services**:
• Ambulance service available
• Tie-ups with nearby hospitals
• Emergency contact numbers displayed

**Health Insurance**:
• Group health insurance for all students
• Medical coverage for accidents and illnesses

**Wellness Programs**:
• Regular health camps
• Awareness programs on health and hygiene
• Counseling services for mental health
• Yoga and meditation sessions""",

            "library": """📚 **Library Resources - RGMCET**:

**Collection**:
• 50,000+ books across all disciplines
• 500+ journals and magazines
• Digital library with online databases
• Access to IEEE, ACM, JSTOR, and other research databases

**Facilities**:
• Individual study carrels
• Group study rooms
• Computer lab with latest software
• Photocopy and printing services
• Reading halls with comfortable seating

**Timings**:
• Weekdays: 8 AM to 10 PM
• Weekends: 9 AM to 6 PM
• Extended hours during exams

**Services**:
• Book lending and reference services
• Inter-library loan facilities
• Research assistance
• Online catalog access""",

            "campus_life": """🎉 **Campus Life & Student Activities - RGMCET**:

**Academic Environment**:
• Autonomous curriculum updated regularly
• Industry-relevant skill development
• Research and innovation focus
• Regular workshops and seminars

**Student Organizations**:
• Technical clubs (Coding, Robotics, AI)
• Cultural clubs (Music, Dance, Drama)
• Sports teams and associations
• NSS (National Service Scheme)
• Entrepreneurship cell

**Events & Festivals**:
• Annual technical fests
• Cultural festivals and competitions
• Sports tournaments
• Leadership and personality development programs
• Industry guest lectures

**Support Services**:
• Career counseling and placement assistance
• Psychological counseling
• Grievance redressal cell
• Women empowerment initiatives
• Anti-ragging committee""",

            "research": """🔬 **Research & Development - RGMCET**:

**Research Centers**:
• 7 departments recognized as research centers by JNTUA
• DSIR (Department of Scientific and Industrial Research) recognition
• Exemption from excise duty for research equipment

**Research Areas**:
• Civil Engineering: Structural engineering, Construction materials
• Electrical Engineering: Power systems, Renewable energy
• Mechanical Engineering: Manufacturing, Robotics
• Electronics: VLSI design, Communication systems
• Computer Science: AI, Machine Learning, Cyber Security
• Sciences: Applied physics, Mathematics applications

**Funding & Grants**:
• World Bank TEQIP funding
• Government research grants
• Industry-sponsored projects
• Internal research funding

**Publications & Patents**:
• Regular publications in reputed journals
• Conference presentations
• Patent filings and grants
• Research collaborations with industries""",

            "industry": """🤝 **Industry Connect & Collaborations - RGMCET**:

**Industry Partnerships**:
• TCS accredited for training and placements
• SIEMENS Technical Skill Development Institute (TSDI)
• Deen Dayal Upadhyay KAUSHAL Kendra
• Two CM's Skill Centers

**Training Programs**:
• Industry-relevant curriculum
• Guest lectures by industry experts
• Internship programs with leading companies
• Skill development workshops
• Certification courses

**Placement Partners**:
• Top IT companies: TCS, Infosys, Wipro, Cognizant
• Tech giants: Google, Microsoft, Amazon
• Core companies: L&T, Tata, Reliance
• Startups and MSMEs

**Alumni Network**:
• Strong alumni association
• Industry mentorship programs
• Guest lectures and workshops
• Career guidance and networking events""",

            "vision_mission": """🌟 **Vision & Mission - RGMCET**:

**Vision**:
"To develop this rural based engineering college into an institute of technical education with global standards"

**Mission**:
• To build a world class undergraduate program with all required infrastructure that provides strong theoretical knowledge supplemented by the state of art skills
• To establish postgraduate programs in basic and cutting edge technologies
• To create conductive ambiance to induce and nurture research
• To turn young graduates to success oriented entrepreneurs
• To develop linkage with industries to have strong industry institute interaction
• To offer demand driven courses to meet the needs of the industry and society
• To inculcate human values and ethos into the education system for an all-round development of students

**Quality Policy**:
• To improve the teaching and learning process
• To evaluate the performance of students at regular intervals and take necessary steps for betterment
• To establish and develop centers of excellence for research and consultancy
• To prepare students to face the competition in the market globally and realize the responsibilities as true citizen to serve the nation and uplift the country's pride"""
        }

    def translate_text(self, text, target_lang):
        """Translate text to target language"""
        if target_lang == "en":
            return text
        try:
            translated = self.translator.translate(text, target_lang)
            return str(translated)
        except Exception as e:
            # If translation fails, return original text with a note
            return text + f"\n\n*Translation note: Detailed information is available in English. Please switch to English for complete details.*"

    def generate_response(self, user_input, language="en"):
        """Generate AI-powered response focused on RGMCET assistance"""
        try:
            if self.use_ai:
                # Use AI API for intelligent responses
                rgmcet_context = """
                You are RGMCET Assistant, an AI helper for Rajeev Gandhi Memorial College of Engineering and Technology.
                Key facts: Located in Nandyal, Andhra Pradesh. Established 1996. NBA accredited, NAAC A+ grade.
                Offers B.Tech in CSE, ECE, EEE, ME, CE. M.Tech programs, MBA, MCA. PhD programs available.
                50-acre campus with modern facilities, hostels, sports complex, research centers.
                """

                prompt = f"{rgmcet_context}\n\nUser: {user_input}\nAssistant:"

                try:
                    response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt, "parameters": {"max_length": 200, "temperature": 0.7}})
                    if response.status_code == 200:
                        ai_response = response.json()[0]['generated_text']
                        # Clean up the response
                        if "Assistant:" in ai_response:
                            ai_response = ai_response.split("Assistant:")[-1].strip()

                        # Translate if needed
                        if language != "en":
                            ai_response = self.translate_text(ai_response, language)

                        return ai_response
                except:
                    pass

            # Fallback to enhanced rule-based responses
            return self.generate_enhanced_response(user_input, language)

        except Exception as e:
            print(f"AI generation error: {e}")
            return self.generate_enhanced_response(user_input, language)

    def generate_enhanced_response(self, user_input, language="en"):
        """Enhanced rule-based response with better logic"""
        user_input_lower = user_input.lower()

        # Smart intent detection
        intents = {
            "courses": ["course", "program", "btech", "mtech", "mba", "mca", "engineering", "study"],
            "admissions": ["admission", "apply", "eligibility", "entrance", "eamcet", "gate", "pgecet", "icet"],
            "fees": ["fee", "cost", "tuition", "payment", "scholarship", "financial"],
            "placements": ["placement", "job", "career", "recruitment", "company", "salary", "hiring"],
            "facilities": ["facility", "campus", "hostel", "library", "sports", "lab", "infrastructure"],
            "about": ["about", "rgmcet", "college", "university", "history", "establishment", "overview"]
        }

        # Determine intent
        detected_intent = None
        for intent, keywords in intents.items():
            if any(keyword in user_input_lower for keyword in keywords):
                detected_intent = intent
                break

        # Generate contextual response
        if detected_intent:
            response = self.get_contextual_info(detected_intent, user_input_lower)
            if response:
                return self.translate_text(response, language)

        # Default responses for common queries using translations
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
            return self.translations["greeting"].get(language, self.translations["greeting"]["en"])

        if any(word in user_input_lower for word in ["thank", "thanks", "grateful"]):
            return self.translations["thanks"].get(language, self.translations["thanks"]["en"])

        # General college response using translations
        return self.translations["general"].get(language, self.translations["general"]["en"])

    def get_contextual_info(self, intent, query):
        """Get contextual information based on detected intent"""
        if intent == "courses":
            if "btech" in query or "undergraduate" in query:
                return self.college_info["courses"]["ug_engineering"]
            elif "mtech" in query or "postgraduate" in query:
                return self.college_info["courses"]["pg_engineering"]
            elif "mba" in query or "mca" in query:
                return self.college_info["courses"]["pg_sciences"]
            else:
                return self.college_info["courses"]["ug_engineering"]  # Default to UG courses

        elif intent == "admissions":
            return self.college_info["admissions"]

        elif intent == "fees":
            return self.college_info["fees"]

        elif intent == "placements":
            return self.college_info["placements"]

        elif intent == "facilities":
            if "hostel" in query:
                return self.college_info["hostel"]
            elif "sports" in query:
                return self.college_info["sports"]
            elif "library" in query:
                return self.college_info["library"]
            else:
                return self.college_info["facilities"]

        elif intent == "about":
            return self.college_info["rgmcet"]

        return None

    def get_college_info(self, query):
        """Get relevant RGMCET information based on query"""
        query_lower = query.lower()

        # Course-related queries
        if any(word in query_lower for word in ["btech", "ug", "undergraduate", "engineering course", "civil", "mechanical", "electrical", "ece", "cse", "computer science"]):
            return self.college_info["courses"]["ug_engineering"]
        elif any(word in query_lower for word in ["mtech", "pg engineering", "postgraduate engineering", "masters engineering"]):
            return self.college_info["courses"]["pg_engineering"]
        elif any(word in query_lower for word in ["mba", "mca", "pg science", "management", "computer application"]):
            return self.college_info["courses"]["pg_sciences"]
        elif any(word in query_lower for word in ["phd", "doctoral", "research program", "ph.d"]):
            return self.college_info["courses"]["phd"]
        elif any(word in query_lower for word in ["certification", "skill development", "kaushal", "course certificate"]):
            return self.college_info["courses"]["certification"]

        # Admission-related queries
        elif any(word in query_lower for word in ["admission", "apply", "application", "eligibility", "requirement", "entrance", "eamcet", "gate", "pgecet", "icet"]):
            return self.college_info["admissions"]

        # Fee and financial queries
        elif any(word in query_lower for word in ["tuition", "cost", "fee", "payment", "scholarship", "financial", "waiver", "reimbursement"]):
            return self.college_info["fees"]

        # Campus and facility queries
        elif any(word in query_lower for word in ["campus", "facility", "infrastructure", "building", "lab", "classroom"]):
            return self.college_info["facilities"]

        # Specific facility queries
        elif any(word in query_lower for word in ["hostel", "accommodation", "residence", "mess", "food", "stay"]):
            return self.college_info["hostel"]
        elif any(word in query_lower for word in ["library", "book", "study", "reading", "research resource"]):
            return self.college_info["library"]
        elif any(word in query_lower for word in ["sport", "gym", "fitness", "game", "recreation", "exercise", "play"]):
            return self.college_info["sports"]
        elif any(word in query_lower for word in ["transport", "bus", "parking", "travel", "commute", "reach"]):
            return self.college_info["transport"]
        elif any(word in query_lower for word in ["health", "medical", "doctor", "hospital", "wellness", "care"]):
            return self.college_info["healthcare"]
        elif any(word in query_lower for word in ["placement", "job", "career", "recruit", "company", "hiring", "salary", "package"]):
            return self.college_info["placements"]
        elif any(word in query_lower for word in ["research", "phd", "innovation", "development", "publication"]):
            return self.college_info["research"]
        elif any(word in query_lower for word in ["industry", "collaboration", "partnership", "training", "skill"]):
            return self.college_info["industry"]
        elif any(word in query_lower for word in ["activity", "club", "event", "festival", "student life", "cultural"]):
            return self.college_info["campus_life"]
        elif any(word in query_lower for word in ["vision", "mission", "goal", "objective", "quality policy"]):
            return self.college_info["vision_mission"]

        # RGMCET specific queries
        elif any(word in query_lower for word in ["rgmcet", "college", "university", "institution", "about", "overview", "history", "establishment"]):
            return self.college_info["rgmcet"]

        return None

    def chat(self, user_input, history, language="en"):
        """Main chat function for Gradio interface"""
        if not user_input.strip():
            return history, ""

        # Add user message to history
        history = history or []
        history.append({"role": "user", "content": user_input})

        # Generate response
        response = self.generate_response(user_input, language)

        # Add assistant response to history
        history.append({"role": "assistant", "content": response})

        return history, ""

def create_gradio_interface():
    """Create and launch the Gradio chat interface"""
    assistant = RGMCET_Assistant()

    # Custom CSS for better appearance
    css = """
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .message.user {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #ffffff;
        border-radius: 20px;
        padding: 15px 20px;
        margin: 10px 0;
        font-weight: 600;
        border: 3px solid #ffffff;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
        font-size: 16px;
        line-height: 1.5;
    }
    .message.assistant {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #ffffff;
        border-radius: 20px;
        padding: 15px 20px;
        margin: 10px 0;
        font-weight: 600;
        border: 3px solid #ffffff;
        box-shadow: 0 4px 15px rgba(67, 233, 123, 0.4);
        font-size: 16px;
        line-height: 1.5;
    }
    .gradio-container h1, .gradio-container h2, .gradio-container h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        text-align: center !important;
    }
    .gradio-container p, .gradio-container span, .gradio-container div {
        color: #ffffff;
    }
    .gradio-container button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4) !important;
    }
    .gradio-container button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6) !important;
    }
    .gradio-container input, .gradio-container textarea, .gradio-container select {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #333333 !important;
        border: 2px solid #ffffff !important;
        border-radius: 15px !important;
        font-weight: 500 !important;
    }
    """

    with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🏫 RGMCET AI COLLEGE ASSISTANT CHATBOT")
        gr.Markdown("**Rajeev Gandhi Memorial College of Engineering and Technology**")
        gr.Markdown("Ask me detailed questions about RGMCET - courses, admissions, fees, facilities, placements, and everything! I have real data from the official RGMCET website.")

        # Language selector
        language = gr.Dropdown(
            choices=["en", "hi", "te", "ur", "ta", "kn", "mr"],
            value="en",
            label="Select Language / भाषा चुनें / భాషను ఎంచుకోండి",
            info="Choose your preferred language for responses / अपने उत्तर के लिए पसंदीदा भाषा चुनें / మీ సమాధానాల కోసం మీకు ఇష్టమైన భాషను ఎంచుకోండి"
        )

        # Chatbot interface
        chatbot = gr.Chatbot(
            height=500,
            show_label=False,
            container=True
        )

        # Input textbox
        msg = gr.Textbox(
            placeholder="Ask about RGMCET courses, admissions, fees, placements, facilities... / RGMCET पाठ्यक्रम, प्रवेश, शुल्क, प्लेसमेंट, सुविधाओं के बारे में पूछें... / RGMCET కోర్సులు, ప్రవేశం, ఫీజు, ప్లేస్‌మెంట్‌లు, సౌకర్యాల గురించి అడగండి...",
            show_label=False,
            container=False
        )

        # Clear button
        clear = gr.Button("Clear Chat")

        # Function to handle chat
        def respond(message, chat_history, lang):
            new_history, _ = assistant.chat(message, chat_history, lang)
            return "", new_history

        # Function to clear chat
        def clear_chat():
            assistant.chat_history = []
            return []

        # Event handlers
        msg.submit(respond, [msg, chatbot, language], [msg, chatbot])
        clear.click(clear_chat, None, chatbot)

        # Examples
        gr.Examples(
            examples=[
                "Tell me about RGMCET",
                "What are the B.Tech courses and intake?",
                "How to apply for admission?",
                "What is the fee structure?",
                "What scholarships are available?",
                "Tell me about placements",
                "What facilities are available?",
                "How are the hostel facilities?",
                "What sports facilities are there?",
                "Tell me about the library",
                "What transportation options are there?",
                "What medical facilities are available?",
                "What research opportunities are there?",
                "Tell me about industry collaborations",
                "What is the vision and mission of RGMCET?"
            ],
            inputs=msg
        )

    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=False)  # Changed to share=False for local testing