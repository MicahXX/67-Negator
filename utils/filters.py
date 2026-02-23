import re

BANNED_EMOJIS = {"🤰", "🫃", "🫄", "6️⃣", "7️⃣"}
CUSTOM_EMOJI_PATTERN = re.compile(r"<a?:[\w-]+:\d+>")

LEET_MAP = str.maketrans({
    '1': 'i',  # s1xseven -> sixseven
    '3': 'e',  # s3ven -> seven
    '5': 's',  # 5ixtyseven -> sixtyseven
    '$': 's',  # $ixtyseven -> sixtyseven
    '|': 'l',
})


def is_emoji_only_message(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    parts = text.split()
    return all(part.startswith("<:") or part.startswith("<a:") or is_unicode_emoji(part) for part in parts)


def is_unicode_emoji(s: str) -> bool:
    return s in BANNED_EMOJIS or any(ord(c) > 10000 for c in s)


def contains_banned_pattern(content: str, ultimate_defense: bool = False) -> bool:
    if not content:
        return False

    lowered = content.lower().strip()
    content_without_custom = CUSTOM_EMOJI_PATTERN.sub("", lowered)

    if any(emoji in content_without_custom for emoji in BANNED_EMOJIS):
        return True

    if "http://" in content_without_custom or "https://" in content_without_custom or "@" in content_without_custom:
        return False

    separators = [" ", "-", "_", "/", "&", ".", "~", ",", "'", "*", "`", "(", ")", ":", ";", "!"]

    normalized = content_without_custom
    for sep in separators:
        normalized = normalized.replace(sep, "")

    if re.search(r'(?<!\d)67(?!\d)', normalized):
        return True

    leet_normalized = normalized.translate(LEET_MAP)

    word_patterns = [
        "six7",
        "6ix7",
        "sixseven",
        "sixtyseven",
        "sixmyseven",
        # Spanish: sesenta y siete
        "sesentaysiete",
        "sesentasiete",
        # French: soixante-sept
        "soixantesept",
        # German: siebenundsechzig
        "siebenundsechzig",
        # Italian: sessanta sette
        "sessantasette",
        # Portuguese: sessenta e sete
        "sessentaesete",
        "sessentasete",
    ]

    for pattern in word_patterns:
        if pattern in normalized or pattern in leet_normalized:
            return True

    # "6seven": regex guard so "16seventh" doesn't match.
    if re.search(r'(?<!\d)6seven', normalized) or re.search(r'(?<!\d)6seven', leet_normalized):
        return True

    # Separator-based checks on pre-stripped content.
    for sep in separators:
        if (f"6{sep}7" in content_without_custom or
                f"six{sep}seven" in content_without_custom or
                f"six{sep}7" in content_without_custom or
                f"6{sep}seven" in content_without_custom):
            return True
        # Other languages with an explicit separator between the two parts.
        if (f"sesenta{sep}siete" in content_without_custom or   # Spanish
                f"soixante{sep}sept" in content_without_custom or  # French
                f"sessanta{sep}sette" in content_without_custom or # Italian
                f"sessenta{sep}sete" in content_without_custom):   # Portuguese
            return True

    if ultimate_defense:
        if re.search(r'(?<!\d)6(?!\d)', normalized) or re.search(r'(?<!\d)7(?!\d)', normalized):
            return True

        leet_content = content_without_custom.translate(LEET_MAP)
        udm_word_patterns = [
            r'\bsix\b',         # English 6
            r'\bseven\b',       # English 7
            r'\bseis\b',        # Spanish / Portuguese 6
            r'\bsiete\b',       # Spanish 7
            r'\bsete\b',        # Portuguese 7
            r'\bsesenta\b',     # Spanish 60
            r'\bsessenta\b',    # Portuguese 60
            r'\bsoixante\b',    # French 60
            r'\bsept\b',        # French 7
            r'\bsechs\b',       # German 6
            r'\bsieben\b',      # German 7
            r'\bsechzig\b',     # German 60
            r'\bsei\b',         # Italian 6
            r'\bsette\b',       # Italian 7
            r'\bsessanta\b',    # Italian 60
        ]
        for pattern in udm_word_patterns:
            if re.search(pattern, content_without_custom) or re.search(pattern, leet_content):
                return True

    return False
