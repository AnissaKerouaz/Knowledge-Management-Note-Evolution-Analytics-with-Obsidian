from pathlib import Path
import yaml
import re
from datetime import datetime

def safe_yaml_load(yaml_text):
    """Clean YAML quirks (like unquoted ? and :) before loading."""
    def quote_if_needed(match):
        # Match content inside [ ... ] and split by commas
        items = match.group(1).split(',')
        quoted_items = []
        for item in items:
            item = item.strip()
            if any(c in item for c in [':', '?', ',', '[', ']']):
                item = f'"{item}"'
            quoted_items.append(item)
        return f"[{', '.join(quoted_items)}]"
    
    # Fix inline lists that might have unquoted special chars
    cleaned = re.sub(r'\[(.*?)\]', quote_if_needed, yaml_text)
    return yaml.safe_load(cleaned)

def parse_markdown(path: Path):
    '''reads an md file and extracts:
    - yaml frontmatter, backlinks, body text of the note'''
    #reading the file content as text
    text = path.read_text(encoding= "utf-8")
    #regex to find yaml frontmatter(between --- and ---)
    yaml_parts = re.match(r"---(.*?)---", text, re.DOTALL)
    yaml_data={}
    #if yaml exists, load it into a python dictionary
    if yaml_parts:
        yaml_data = safe_yaml_load(yaml_parts.group(1)) or {}


    #remove yaml part to isolate the main content
    content = re.sub(r"---(.*?)---", "", text, count = 1)
    #find all backlinks(text inside [[]])
    backlinks = re.findall(r"\[\[(.*?)\]\]", content)
    #build a dictionary with all extracted infos
    return{
        #filenames without .md extension
        "id": path.stem,
        #use yaml title or fallback
        "title": yaml_data.get("title", path.stem), 
        "created": yaml_data.get(
            "created", datetime.fromtimestamp(path.stat().st_ctime).isoformat()),
        "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
        "tags": yaml_data.get("tags", []),
        "backlinks": backlinks,
        "content": content.strip(),

    }
