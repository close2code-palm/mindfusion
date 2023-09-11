import json

import aiohttp


async def fetch_completion(prompt: str, request: str):
    messages = [
            {"role": "system", "content": f"{prompt}"},
            {"role": "user", "content": f"{request}"}
        ]
    endpoint = 'http://95.217.14.178:8080/candidates_openai/gpt'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
    }
    data = json.dumps(data)

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=data) as response:
            return await response.json()
