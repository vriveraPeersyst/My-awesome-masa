
import re
import unicodedata
from src.agent.data.team_mappings import TEAM_NAME_MAPPINGS

def normalize_text(text):
    # Remove accents and convert to lowercase
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text.lower()

def extract_team_names(question, history):
    question_normalized = normalize_text(question)
    history_normalized = normalize_text(history)
    combined_text = question_normalized + " " + history_normalized
    mentioned_teams = set()

    for folder_name, name_variations in TEAM_NAME_MAPPINGS.items():
        for name in name_variations:
            name_normalized = normalize_text(name)
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(name_normalized) + r'\b'
            if re.search(pattern, combined_text):
                mentioned_teams.add(folder_name)
                break  # Stop checking other variations for this team

    return list(mentioned_teams)
