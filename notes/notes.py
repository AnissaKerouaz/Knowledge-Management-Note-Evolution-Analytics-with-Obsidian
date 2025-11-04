from pathlib import Path
import yaml
import re
from datetime import datetime

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
        yaml_data = yaml.safe_load(yaml_parts.group(1)) or {}

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
            "created", datetime.fromtimestamp(path.stat().st_ctime).isformat()),
        "modified": datetime.fromtimestamp(path.stat().st_mtime).isformat(),
        "tags": yaml_data.get("tags", []),
        "backlinks": backlinks,
        "content": content.strip(),

    }
