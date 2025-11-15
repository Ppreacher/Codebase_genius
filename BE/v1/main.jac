import from byllm.llm { Model }
import from dotenv { load_dotenv }
import from git { Repo }
import from pathlib { Path }
import os;
import shutil;
include utils;


# Initialize Groq AI model
glob llm = Model(
    model_name="groq/llama3-8b-8192",  # Using Groq's Llama 3
    verbose=False
);

# Session management nodes
node Memory {
    has data: dict = {};
}

node Session {
    has repo_url: str = "";
    has repo_name: str = "";
    has status: str = "initialized";
    has created_at: str = "";
    has file_tree: dict = {};
    has readme_summary: str = "";
    has documentation: str = "";
    has repo_path: str = "";
    has ccg: dict = {};
    has entry_points: list = [];
}

# RepoMapper Node
node RepoMapper {
    has repo_path: str = "";
    
    def clone_repository(url: str, target_path: str) -> dict {
        try {
            print("📥 Cloning from: " + url);
            Repo.clone_from(url, target_path);
            return {"success": True, "message": "Repository cloned successfully", "path": target_path};
        }
        except Exception as e {
            return {"success": False, "message": str(e)};
        }
    }
    
    def generate_file_tree(path: str) -> dict {
        ignore_dirs = [".git", "node_modules", "__pycache__", ".venv", "venv", ".env", "dist", "build", ".idea", ".vscode", ".pytest_cache"];
        ignore_files = [".DS_Store", ".gitignore", ".env"];
        
        tree = {"name": os.path.basename(path), "type": "directory", "children": []};
        
        try {
            items = os.listdir(path);
            for item in sorted(items) {
                if item in ignore_dirs or item in ignore_files {
                    continue;
                }
                item_path = os.path.join(path, item);
                if os.path.isdir(item_path) {
                    subtree = self.generate_file_tree(item_path);
                    tree["children"].append(subtree);
                }
                else {
                    tree["children"].append({"name": item, "type": "file"});
                }
            }
        }
        except Exception as e {
            print("Error generating file tree: " + str(e));
        }
        
        return tree;
    }
    
    def find_readme(path: str) -> str {
        readme_names = ["README.md", "README.MD", "readme.md", "README", "README.txt"];
        for name in readme_names {
            readme_path = os.path.join(path, name);
            if os.path.exists(readme_path) {
                return readme_path;
            }
        }
        return "";
    }
    
    def read_file_content(file_path: str) -> str {
        try {
            with open(file_path, 'r', encoding='utf-8') as f {
                return f.read();
            }
        }
        except Exception as e {
            return "Error reading file: " + str(e);
        }
    }
    
    def summarize_readme(readme_content: str) -> str by llm(
        incl_info=(self)
    );
    
    can map_repository with code_genius entry {
        repo_url = visitor.repo_url;
        repo_name = visitor.repo_name;
        
        print("🗺️ RepoMapper: Mapping repository: " + repo_url);
        
        # Use utils function (auto-clears cache!)
        temp_dir = create_temp_dir(repo_name);
        self.repo_path = temp_dir;
        visitor.repo_path = temp_dir;
        
        clone_result = self.clone_repository(repo_url, temp_dir);
        
        if not clone_result["success"] {
            visitor.status = "failed";
            print("❌ Clone failed: " + clone_result["message"]);
            report {"error": clone_result["message"]};
            disengage;
        }
        
        file_tree = self.generate_file_tree(temp_dir);
        visitor.file_tree = file_tree;
        
        readme_path = self.find_readme(temp_dir);
        if readme_path {
            readme_content = self.read_file_content(readme_path);
            
            # Check if AI is available
            if os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") {
            print("🤖 Using AI (" + llm.model_name + ") to summarize README...");
            readme_summary = self.summarize_readme(readme_content);
            }
            else {
                print("⚠️  No API key - using simple summary");
                if len(readme_content) > 1000 {
                    readme_summary = readme_content[:1000] + "\n\n... (truncated)";
                }
                else {
                    readme_summary = readme_content;
                }
            }
            
            visitor.readme_summary = readme_summary;
        }
        else {
            visitor.readme_summary = "No README file found.";
        }
        
        visitor.status = "mapped";
        
        print("✅ RepoMapper: Repository mapped successfully");
        
        report {
            "status": "success",
            "message": "Repository mapped successfully",
            "repo_path": temp_dir,
            "file_tree": file_tree,
            "readme_summary": visitor.readme_summary
        };
    }
}

sem RepoMapper.summarize_readme = """
Analyze the README content and provide a concise summary (3-5 sentences) covering:
1. What the project does (main purpose)
2. Key features or technologies used
3. Target users or use cases

Keep it brief but informative. Limit to 150 words maximum.
""";

# Main walker - orchestrates the workflow
walker code_genius {
    has repo_url: str = "";
    has session_id: str = "";
    has repo_name: str = "";
    has status: str = "initialized";
    has file_tree: dict = {};
    has readme_summary: str = "";
    has repo_path: str = "";
    has ccg: dict = {};
    has entry_points: list = [];
    has documentation: str = "";
    
    obj __specs__ {
        static has auth: bool = False;
    }
    
    can execute with `root entry {
        print("🚀 CodeGenius Orchestrator: Starting workflow for " + self.repo_url);
        
        if not self.repo_url or not is_valid_github_url(self.repo_url) {
            report {"error": "Invalid GitHub URL provided", "received": self.repo_url};
            disengage;
        }
        
        self.repo_name = self.repo_url.split("/")[-1].replace(".git", "");
        
        # Step 1: Map Repository
        print("📋 Step 1/3: Mapping repository structure...");
        repo_mapper_list = [root --> (`?RepoMapper)];
        if not repo_mapper_list {
            repo_mapper = root ++> RepoMapper();
        }
        else {
            repo_mapper = repo_mapper_list[0];
        }
        visit repo_mapper;
        
        if self.status == "failed" {
            report {"error": "Repository mapping failed"};
            disengage;
        }
        
        # Step 2: Analyze Code
        print("📋 Step 2/3: Analyzing code structure...");
        code_analyzer_list = [root --> (`?CodeAnalyzer)];
        if not code_analyzer_list {
            code_analyzer = root ++> CodeAnalyzer();
        }
        else {
            code_analyzer = code_analyzer_list[0];
        }
        visit code_analyzer;
        
        # Step 3: Generate Documentation
        print("📋 Step 3/3: Generating documentation...");
        doc_genie_list = [root --> (`?DocGenie)];
        if not doc_genie_list {
            doc_genie = root ++> DocGenie();
        }
        else {
            doc_genie = doc_genie_list[0];
        }
        visit doc_genie;
        
        print("🎉 CodeGenius Orchestrator: Workflow complete - Documentation generated!");
        
        report {
            "status": "success",
            "message": "Documentation generated successfully",
            "total_files": self.ccg["total_files"] if self.ccg else 0,
            "total_functions": self.ccg["total_functions"] if self.ccg else 0,
            "total_classes": self.ccg["total_classes"] if self.ccg else 0
        };
    }
}

# Session status walker
walker get_session_status {
    has session_id: str = "";
    
    obj __specs__ {
        static has auth: bool = False;
    }
    
    can execute with `root entry {
        if not self.session_id {
            report {"error": "No session_id provided"};
            disengage;
        }
        
        session = &(self.session_id);
        
        report {
            "session_id": jid(session),
            "repo_url": session.repo_url,
            "repo_name": session.repo_name,
            "status": session.status,
            "created_at": session.created_at,
            "readme_summary": session.readme_summary
        };
    }
}

include code_analyzer;
include doc_genie;

# Initialize on startup
with entry {
    load_dotenv();
}