# 🏫 RGMCET AI Assistant - Real Data Integration

A comprehensive AI-powered chatbot specifically designed for **Rajeev Gandhi Memorial College of Engineering and Technology (RGMCET)** using real data collected from the official RGMCET website.

## 🎯 What We Accomplished

✅ **Collected Real RGMCET Data** from official website:
- About RGMCET (History, Vision, Mission, Management)
- Courses Offered (UG/PG programs with intake numbers)
- Admission Procedure (Detailed admission processes)
- Fee Structure (2023-26 official fees)
- Scholarships (Fee waivers and financial aid)

✅ **Integrated Real Data** into AI Assistant:
- Replaced generic information with accurate RGMCET details
- Added comprehensive knowledge base covering all aspects
- Enhanced query matching for better responses

✅ **Created Advanced Features**:
- Detailed course information with intake numbers
- Accurate fee structure and scholarship details
- Complete admission procedures
- Facility information (hostel, library, sports, transport, healthcare)
- Placement statistics and company information
- Research and industry collaboration details

## 📁 Project Structure





```
multilingual_chatbot/
├── data/
│   ├── About RGMCET.txt          # Official college information
│   ├── Courses Offered.txt       # Program details with intake
│   ├── Admission Procedure.txt   # Admission guidelines
│   ├── Courses.xlsx              # Lists of courses available
│   └── Fee Structure.txt         # Official fee details
|   ├── RGMCET.txt                # Details of RGMCET IN text format
│   ├── RGMCET.txt.xlsx           # Basic details of college in Excel          
│   └──  Scholarships.txt         # Scholarships details           
├── rgmcet_chatbot.py             # Main chatbot application
├── test_data.py                  # Data integration test
├── test_rgmcet.py               # Comprehensive testing
└── README.md                     # This documentation
```

## 🚀 How to Run

### Quick Start
```bash
cd multilingual_chatbot
python rgmcet_chatbot.py
```

This launches a web interface where you can chat with the RGMCET AI Assistant.

### Test the Data Integration
```bash
python test_data.py
```

## 💡 What the Assistant Can Answer

### 🎓 **Courses & Programs**
- "What B.Tech courses are available?"
- "Tell me about M.Tech programs"
- "What MBA and MCA programs are offered?"
- "Tell me about Ph.D programs"
- "What certification courses are available?"

### 📋 **Admissions**
- "How to apply for admission?"
- "What entrance exams are required?"
- "What is the admission procedure?"

### 💰 **Fees & Scholarships**
- "What is the fee structure?"
- "How much is tuition fee?"
- "What scholarships are available?"
- "Is there fee waiver for good ranks?"

### 🏢 **Facilities**
- "What facilities are available?"
- "How are the hostel facilities?"
- "Tell me about the library"
- "What sports facilities are there?"
- "What transportation options are there?"
- "What medical facilities are available?"

### 💼 **Placements & Career**
- "How are the placements?"
- "What companies visit for recruitment?"
- "What is the average package?"

### 🔬 **Research & Industry**
- "What research opportunities are there?"
- "Tell me about industry collaborations"

### 🏛️ **About RGMCET**
- "Tell me about RGMCET"
- "What is the history of the college?"
- "Who are the management members?"
- "What accreditations does RGMCET have?"

## 🌟 Key Features

### 📊 **Real Data Integration**
- All information sourced from official RGMCET website
- Accurate fee structure (2023-26)
- Current course intake numbers
- Official admission procedures
- Real scholarship and placement data

### 🎯 **Smart Query Matching**
- Understands various ways to ask questions
- Provides detailed, relevant responses
- Covers all aspects of college life

### 🌍 **Multilingual Support**
- Language selector in web interface
- Supports 9 languages (English, Spanish, French, etc.)

### 💬 **Interactive Web Interface**
- Modern Gradio-based chat interface
- Example questions for quick start
- Clear chat history
- Mobile-friendly design

## 📈 **Data Accuracy**

**Source**: Official RGMCET Website
**Last Updated**: Based on 2023-24 to 2025-26 data
**Coverage**: Complete college information including:
- ✅ Establishment and history
- ✅ Management details
- ✅ Accreditation status
- ✅ Course offerings with intake
- ✅ Admission procedures
- ✅ Fee structure and scholarships
- ✅ Campus facilities
- ✅ Placement records
- ✅ Research activities
- ✅ Industry partnerships

## 🔧 **Technical Details**

- **Framework**: Python with Gradio
- **Data Structure**: Comprehensive knowledge base
- **Query Processing**: Keyword-based intelligent matching
- **Response Generation**: Pre-built detailed responses
- **Interface**: Web-based chat application

## 🎓 **Perfect For**

- **Prospective Students**: Get accurate information about courses, fees, admissions
- **Parents**: Understand college facilities, placements, and reputation
- **Current Students**: Quick access to college information and procedures
- **Researchers**: Information about research facilities and collaborations
- **Visitors**: Overview of RGMCET's offerings and achievements

## 🚀 **Future Enhancements**

- Integration with Llama models for AI-generated responses
- Voice input/output capabilities
- Mobile app version
- Real-time updates from RGMCET website
- Student portal integration

---

**🎉 Congratulations!** You now have a comprehensive RGMCET AI Assistant powered by real data from the official website. This chatbot provides accurate, detailed information about all aspects of RGMCET and serves as a valuable resource for students, parents, and anyone interested in the college.


**Ready to chat?** Run `python rgmcet_chatbot.py` and start exploring RGMCET! 🏫🤖

![Demo Video](https://github.com/user-attachments/assets/b2798e4f-0fae-4435-b8a0-5233449083e9)



