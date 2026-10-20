import hashlib
import hmac
from typing import Any

import httpx

from .config import settings


def verify_wechat_signature(timestamp: str, nonce: str, signature: str) -> bool:
    if not settings.wechat_token:
        return False

    raw = "".join(sorted([settings.wechat_token, timestamp, nonce]))
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()
    return hmac.compare_digest(digest, signature)


async def get_access_token() -> str:
    if not settings.wechat_corp_id or not settings.wechat_secret:
        raise ValueError("WECHAT_CORP_ID 和 WECHAT_SECRET 未配置")

    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {"corpid": settings.wechat_corp_id, "corpsecret": settings.wechat_secret}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("errcode") not in (0, None):
            raise ValueError(f"获取 access_token 失败: {data}")
        return data["access_token"]


async def send_text_message(to_user: str, content: str) -> dict[str, Any]:
    if not settings.wechat_agent_id:
        return {"ok": False, "message": "WECHAT_AGENT_ID 未配置"}

    token = await get_access_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
    payload = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": int(settings.wechat_agent_id),
        "text": {"content": content},
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()


def extract_message_data(payload: dict) -> tuple[str, str, str]:
    msg_type = payload.get("msgtype") or payload.get("MsgType") or "text"

    content = ""
    if isinstance(payload.get("text"), dict):
        content = payload.get("text", {}).get("content", "")
    elif "Content" in payload:
        content = payload.get("Content", "")
    elif "content" in payload:
        content = payload.get("content", "")

    from_user = (
        payload.get("fromusername")
        or payload.get("fromUserName")
        or payload.get("FromUserName")
        or payload.get("sender")
        or "unknown"
    )

    return msg_type, content, from_user
