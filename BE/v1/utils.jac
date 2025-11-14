import from datetime { datetime }
import from pathlib { Path }
import os;
import shutil;

def get_current_datetime() -> str {
    return str(datetime.now());
}

def create_temp_dir(repo_name: str) -> str {
    temp_dir = "/tmp/codebase_genius/" + repo_name;
    Path(temp_dir).mkdir(parents=True, exist_ok=True);
    return temp_dir;
}

def cleanup_temp_dir(path: str) {
    if os.path.exists(path) {
        shutil.rmtree(path);
    }
}

def is_valid_github_url(url: str) -> bool {
    return "github.com" in url and ("https://github.com/" in url or "http://github.com/" in url);
}