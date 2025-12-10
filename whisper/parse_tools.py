import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class WhisperRequest:
    target: str
    target_id: Optional[int]
    target_username: Optional[str]
    message: str

def parse_whisper_query(query: str) -> Optional[WhisperRequest]:
    args = query.strip().split()
    
    if len(args) < 2:
        return None

    raw_target = args[-1]
    message = " ".join(args[:-1])

    if len(message) > 200:
        return None

    target_id: Optional[int] = None
    target_username: Optional[str] = None
    display_target: str = raw_target

    if raw_target.isdigit():
        if len(raw_target) > 12:
            return None
        target_id = int(raw_target)
        
    elif raw_target.startswith("@"):
        username = raw_target[1:]
        length = len(username)
        if not (4 <= length <= 32) and not username.isdigit():
            return None
            
        if username.isdigit():
             target_id = int(username)
        else:
            target_username = username
            display_target = username
    else:
        return None

    return WhisperRequest(
        target=display_target.replace("@", ""), 
        target_id=target_id, 
        target_username=target_username, 
        message=message
    )

def validate_target(text: str) -> Optional[str]:
    if not text:
        return None
        
    text = text.strip()

    if text.isdigit():
        if 4 <= len(text) < 20:
            return text

    else:
        clean_text = text[1:] if text.startswith("@") else text
        
        if re.fullmatch(r"^[a-zA-Z0-9_]{4,32}$", clean_text):
            return clean_text
            
    return None