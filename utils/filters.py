import re

CUSTOM_EMOJI_PATTERN = re.compile(r"^<a?:[\w-]+:\d+>$")

UNICODE_EMOJI_PATTERN = re.compile(
    r"[\U0001F1E0-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\uFE0F\u200D]"
)

BANNED_EMOJIS = {"🤰", "🫃", "🫄", "6️⃣", "7️⃣"}


def is_emoji_only_message(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    parts = text.split()
    return all(
        CUSTOM_EMOJI_PATTERN.fullmatch(p) or UNICODE_EMOJI_PATTERN.fullmatch(p)
        for p in parts
    )


def contains_banned_pattern(content: str) -> bool:
    if not content:
        return False

    lowered = content.lower().strip()

    if any(emoji in content for emoji in BANNED_EMOJIS):
        return True

    if "http://" in lowered or "https://" in lowered or "@" in lowered:
        return False

    separators = [" ", "-", "_", "/", "&", ".", "~", ","]
    normalized = lowered
    for sep in separators:
        normalized = normalized.replace(sep, "")

    banned = ["67", "sixseven", "sixtyseven", "sixmyseven"]
    if any(b in normalized for b in banned):
        return True

    for sep in separators:
        if f"6{sep}7" in lowered or f"six{sep}seven" in lowered:
            return True

    return False