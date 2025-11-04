from pathlib import Path
import pandas as pd
import os
from dotenv import load_dotenv
from notes.notes import parse_markdown
#loading the variables from the .env file
load_dotenv()
#getting the vault path from the .env
vault_path = Path(os.getenv("vault_path"))

def main():
    if not vault_path.exists():
        raise FileNotFoundError(f"error in vault path: {vault_path}")
    notes = []
    #going through every markdown file in the vault
    for file in vault_path.rglob("*.md"):
        note_data= parse_markdown(file)
        notes.append(note_data)
    #converting notes to a dataframe
    df = pd.DataFrame(notes)
    #saving output as a csv
    df.to_csv("data/raw/extracted_notes.csv", index=False)
    print(f"{len(df)} notes have been saved")

if __name__ == "__main__":
    main()


