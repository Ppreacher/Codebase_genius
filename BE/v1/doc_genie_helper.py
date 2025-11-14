# doc_genie_helper.py

import os
from pathlib import Path

def generate_markdown_documentation(repo_name, repo_url, readme_summary, ccg, entry_points) -> str:
    """
    Generates a complete markdown documentation from the analyzed components.
    """
    print(f"Helper: Generating markdown for {repo_name}")
    
    # --- This is where you build your markdown string ---
    # (This is just a simple example; you must build this out)
    
    md = []
    md.append(f"# 📚 Documentation for {repo_name}")
    md.append(f"**Repository:** [{repo_url}]({repo_url})\n")
    
    md.append("## 📌 Project Overview")
    md.append(readme_summary + "\n")

    md.append("## 🚀 Entry Points")
    if entry_points:
        for point in entry_points:
            md.append(f"* `{point}`")
    else:
        md.append("No common entry points (like main.py or app.py) found.\n")

    md.append("## 📊 Code Analysis")
    md.append(f"* **Total Files Analyzed:** {ccg.get('total_files', 0)}")
    md.append(f"* **Total Functions Found:** {ccg.get('total_functions', 0)}")
    md.append(f"* **Total Classes Found:** {ccg.get('total_classes', 0)}\n")

    md.append("## 📁 File Details")
    for file_path, info in ccg.get('files', {}).items():
        md.append(f"### `{file_path}`")
        if info.get('classes'):
            md.append("**Classes:**")
            for c in info['classes']:
                md.append(f"* `{c['name']}` (lines {c['start_line']}-{c['end_line']})")
        
        if info.get('functions'):
            md.append("**Functions:**")
            for f in info['functions']:
                md.append(f"* `{f['name']}` (lines {f['start_line']}-{f['end_line']})")
        md.append("\n")

    return "\n".join(md)


def save_documentation(repo_name: str, markdown_content: str) -> str:
    """
    Saves the generated markdown to a local file.
    """
    output_dir = Path(f"./outputs/{repo_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "docs.md"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Helper: Documentation saved to {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"Helper: Error saving file: {e}")
        return ""