import re

import httpx

from .config import settings


def _fallback_rule_reply(message: str) -> str:
    text = (message or "").strip()
    lower = text.lower()

    if not text:
        return "您好，欢迎使用智能客服。"

    if re.search(r"(你好|hello|hi)", lower):
        return "您好！很高兴为您服务。"

    if re.search(r"(价格|报价|多少钱)", lower):
        return "请提供需求类型、数量和交付时间，我将为您给出参考报价。"

    if re.search(r"(售后|故障|问题|异常)", lower):
        return "我们已经记录您的问题，请描述故障现象和出现时间，我会尽快协助您。"

    if re.search(r"(退出|bye|拜拜)", lower):
        return "好的，再见，祝您生活愉快。"

    return "已收到您的消息，我们会尽快处理。"


async def generate_reply(message: str) -> str:
    if not settings.openai_api_key:
        return _fallback_rule_reply(message)

    prompt = (
        "你是企业微信客户服务助手，语气简洁、专业、友好。"
        "请用中文回复用户消息。不要输出无关内容。\n\n用户消息："
        f"{message}"
    )

    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": "你是企业微信客服助手，负责回答客户消息。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"].strip()
            return content if content else _fallback_rule_reply(message)
    except Exception:
        return _fallback_rule_reply(message)
