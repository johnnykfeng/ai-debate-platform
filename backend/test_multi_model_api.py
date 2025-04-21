import asyncio
import aiohttp

base_url = "http://localhost:8000"

test_prompt = {
    "prompt": "Create a limerick about a cat."
}


async def test_endpoint(session, endpoint: str):
    try:
        async with session.post(f"{base_url}/{endpoint}", json=test_prompt) as response:
            result = await response.json()
            print(f"--- {endpoint.upper()} Response ---")
            print(response.status)
            print(result)
            print("\n")
    except Exception as e:
        print(f"Error testing {endpoint}: {e}")


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            test_endpoint(session, "gpt"),
            test_endpoint(session, "gemini"),
            test_endpoint(session, "claude")
        )

if __name__ == "__main__":
    asyncio.run(main())
