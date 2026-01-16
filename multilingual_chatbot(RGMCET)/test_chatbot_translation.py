import sys
sys.path.append('.')
from rgmcet_chatbot import RGMCET_Assistant

def test_translation():
    assistant = RGMCET_Assistant()

    # Test basic translation
    print("Testing translation functionality:")
    print("=" * 50)

    # Test greeting in different languages
    test_languages = ["en", "hi", "te", "ta", "ur", "mr", "kn"]

    for lang in test_languages:
        try:
            greeting = assistant.translations["greeting"].get(lang, assistant.translations["greeting"]["en"])
            print(f"{lang.upper()}: {greeting}")
        except Exception as e:
            print(f"Error with {lang}: {e}")

    print("\nTesting college info translation:")
    print("=" * 50)

    # Test translating college information
    sample_text = "Computer Science and Engineering (CSE) - Intake: 420"
    for lang in ["en", "hi", "te", "ta", "ur", "mr", "kn"]:
        try:
            translated = assistant.translate_text(sample_text, lang)
            print(f"{lang.upper()}: {translated[:100]}...")
        except Exception as e:
            print(f"Translation error for {lang}: {e}")

if __name__ == "__main__":
    test_translation()