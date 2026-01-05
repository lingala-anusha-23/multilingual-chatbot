from translatepy import Translator

# Test translation
translator = Translator()
try:
    result = translator.translate("Hello, how are you?", "fr")
    print("Translation successful:", result)
except Exception as e:
    print("Translation error:", e)