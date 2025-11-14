import os
import ast

def analyze_repository(repo_path):
    """Analyze all Python files in a repository using AST"""
    
    ccg = {
        "files": {},
        "total_functions": 0,
        "total_classes": 0,
        "total_files": 0
    }
    
    for root, dirs, files in os.walk(repo_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", ".venv", "venv", "node_modules", ".idea"]]
        
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    tree = ast.parse(code)
                    
                    file_info = {
                        "path": file_path,
                        "functions": [],
                        "classes": [],
                        "imports": []
                    }
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                file_info["imports"].append(f"import {alias.name}")
                        
                        elif isinstance(node, ast.ImportFrom):
                            module = node.module or ""
                            names = ", ".join([alias.name for alias in node.names])
                            file_info["imports"].append(f"from {module} import {names}")
                        
                        elif isinstance(node, ast.FunctionDef):
                            file_info["functions"].append({
                                "name": node.name,
                                "start_line": node.lineno,
                                "end_line": node.end_lineno or node.lineno
                            })
                        
                        elif isinstance(node, ast.ClassDef):
                            file_info["classes"].append({
                                "name": node.name,
                                "start_line": node.lineno,
                                "end_line": node.end_lineno or node.lineno
                            })
                    
                    ccg["files"][rel_path] = file_info
                    ccg["total_functions"] += len(file_info["functions"])
                    ccg["total_classes"] += len(file_info["classes"])
                    ccg["total_files"] += 1
                
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
                    ccg["files"][rel_path] = {
                        "path": file_path,
                        "functions": [],
                        "classes": [],
                        "imports": [],
                        "error": str(e)
                    }
    
    return ccg

def get_entry_points(ccg):
    """Identify entry point files"""
    entry_patterns = ["main.py", "app.py", "cli.py", "__main__.py", "run.py"]
    entry_points = []
    
    for file_path in ccg["files"].keys():
        file_name = os.path.basename(file_path)
        if file_name in entry_patterns:
            entry_points.append(file_path)
    
    return entry_points