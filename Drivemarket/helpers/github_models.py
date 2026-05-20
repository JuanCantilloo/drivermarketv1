import os

import requests


DEFAULT_MODEL = "openai/gpt-4.1"
DEFAULT_ENDPOINT = "https://models.github.ai/inference/chat/completions"
API_VERSION = "2026-03-10"


def get_github_model():
    model = os.getenv("GITHUB_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    if "/" not in model:
        return f"openai/{model}"
    return model


def get_github_models_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
        "Content-Type": "application/json",
    }


def call_github_chat(messages, *, temperature=0.7, max_tokens=600, top_p=0.9, timeout=25):
    headers = get_github_models_headers()
    if not headers:
        return None, "unconfigured"

    payload = {
        "model": get_github_model(),
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }
    endpoint = os.getenv("GITHUB_MODELS_ENDPOINT", DEFAULT_ENDPOINT)
    response = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
    return response, None
