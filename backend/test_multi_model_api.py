import requests

base_url = "http://localhost:8000"

test_prompt = {
    "prompt": "Explain the theory of relativity in simple terms."
}

def test_endpoint(endpoint: str):
    try:
        response = requests.post(f"{base_url}/{endpoint}", json=test_prompt)
        print(f"--- {endpoint.upper()} Response ---")
        print(response.status_code)
        print(response.json())
        print("\n")
    except Exception as e:
        print(f"Error testing {endpoint}: {e}")

if __name__ == "__main__":
    # test_endpoint("gpt")
    # test_endpoint("gemini")
    test_endpoint("claude")
