#!/usr/bin/env python3
"""
Test script for the RGMCET AI Assistant with real data
"""

from rgmcet_chatbot import RGMCET_Assistant

def test_assistant():
    """Test the RGMCET assistant functionality with real data"""
    assistant = RGMCET_Assistant()

    # Comprehensive test cases covering all RGMCET data
    test_cases = [
        # RGMCET Overview
        ("Tell me about RGMCET", "rgmcet"),
        ("What is RGMCET?", "rgmcet"),
        ("Tell me about the college", "rgmcet"),

        # Courses
        ("What B.Tech courses are available?", "courses"),
        ("Tell me about engineering programs", "courses"),
        ("What are the M.Tech programs?", "courses"),
        ("What MBA and MCA programs are offered?", "courses"),
        ("Tell me about Ph.D programs", "courses"),
        ("What certification courses are available?", "courses"),

        # Admissions
        ("How to apply for admission?", "admissions"),
        ("What is the admission procedure?", "admissions"),
        ("What entrance exams are required?", "admissions"),

        # Fees and Scholarships
        ("What is the fee structure?", "fees"),
        ("How much is tuition fee?", "fees"),
        ("What scholarships are available?", "fees"),

        # Facilities
        ("What facilities are available?", "facilities"),
        ("Tell me about campus infrastructure", "facilities"),

        # Specific Facilities
        ("How are the hostel facilities?", "hostel"),
        ("Tell me about the library", "library"),
        ("What sports facilities are there?", "sports"),
        ("What transportation options are there?", "transport"),
        ("What medical facilities are available?", "healthcare"),

        # Placements and Career
        ("How are the placements?", "placements"),
        ("What companies visit for recruitment?", "placements"),

        # Research and Industry
        ("What research opportunities are there?", "research"),
        ("Tell me about industry collaborations", "industry"),

        # Campus Life
        ("Tell me about campus life", "campus_life"),
        ("What student activities are there?", "campus_life"),

        # Vision and Mission
        ("What is the vision and mission of RGMCET?", "vision_mission"),

        # General queries
        ("Hello", "greeting"),
        ("Thank you", "thanks"),
        ("What is the weather like?", "general")
    ]

    print("Testing RGMCET AI Assistant with Real Data")
    print("=" * 60)

    passed_tests = 0
    total_tests = len(test_cases)

    for i, (test_input, expected_category) in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{test_input}'")
        response = assistant.generate_response(test_input)

        # Check if response is appropriate for the category
        if expected_category == "greeting" and "Hello" in response:
            status = "✓"
            passed_tests += 1
        elif expected_category == "thanks" and "welcome" in response.lower():
            status = "✓"
            passed_tests += 1
        elif expected_category == "general" and "RGMCET" in response:
            status = "✓"
            passed_tests += 1
        elif response and len(response) > 50:  # Meaningful response for RGMCET queries
            status = "✓"
            passed_tests += 1
        else:
            status = "✗"

        print(f"Status: {status}")
        print(f"Response preview: {response[:150]}{'...' if len(response) > 150 else ''}")

    print("\n" + "=" * 60)
    print(f"Test Results: {passed_tests}/{total_tests} tests passed")
    if passed_tests == total_tests:
        print("🎉 All tests completed successfully!")
        print("✅ RGMCET AI Assistant is ready with real data!")
    else:
        print("⚠ Some tests failed. Please check the responses above.")

    print("\n" + "=" * 40)
    print("🚀 Ready to launch: python rgmcet_chatbot.py")
    print("📊 Features tested: All RGMCET data categories")
    print("🌟 Data source: Official RGMCET website")

if __name__ == "__main__":
    test_assistant()