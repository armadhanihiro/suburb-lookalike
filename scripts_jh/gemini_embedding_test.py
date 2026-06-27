import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# 1. Test text embedding
def test_text_embedding():
    try:
        result = genai.embed_content(
            model='models/text-embedding-004',  # recommended model[citation:4][citation:9]
            content='What is the meaning of life?'
        )
        embedding = result['embedding']
        print(f"✅ test successful: {len(embedding)}")
        print(f"vector top 5: {embedding[:5]}")
    except Exception as e:
        print(f"❌ test fails: {e}")

# 2. Test suburb profile embedding
def test_suburb_profile_embedding():
    # load df first generated profile profile_text for each suburb, then embed it using genai.embed_content
    # 这里先用一个占位符文本演示
    sample_text = "Surry Hills（New South Wales），high percentage of professionals, is 45.2%, and the percentage of families with children is 32.1%."
    try:
        result = genai.embed_content(
            model='models/text-embedding-004',
            content=sample_text
        )
        embedding = result['embedding']
        print(f"✅ suburb profile embedding successful: {len(embedding)}")
    except Exception as e:
        print(f"❌ embedding fails: {e}")

if __name__ == "__main__":
    test_text_embedding()
    test_suburb_profile_embedding()