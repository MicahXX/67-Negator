import re

BANNED_EMOJIS = {"🤰", "🫃", "🫄", "6️⃣", "7️⃣"}
CUSTOM_EMOJI_PATTERN = re.compile(r"<a?:[\w-]+:\d+>")

def is_emoji_only_message(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    parts = text.split()
    return all(part.startswith("<:") or part.startswith("<a:") or is_unicode_emoji(part) for part in parts)

def is_unicode_emoji(s: str) -> bool:
    return s in BANNED_EMOJIS or any(ord(c) > 10000 for c in s)

def contains_banned_pattern(content: str) -> bool:
    if not content:
        return False

    lowered = content.lower().strip()

    content_without_custom = CUSTOM_EMOJI_PATTERN.sub("", lowered)

    if any(emoji in content_without_custom for emoji in BANNED_EMOJIS):
        return True

    if "http://" in content_without_custom or "https://" in content_without_custom or "@" in content_without_custom:
        return False

    separators = [" ", "-", "_", "/", "&", ".", "~", ","]
    normalized = content_without_custom
    for sep in separators:
        normalized = normalized.replace(sep, "")

    banned_patterns = ["67", "sixseven", "sixtyseven", "sixmyseven"]
    if any(b in normalized for b in banned_patterns):
        return True

    for sep in separators:
        if f"6{sep}7" in content_without_custom or f"six{sep}seven" in content_without_custom:
            return True

    return False
