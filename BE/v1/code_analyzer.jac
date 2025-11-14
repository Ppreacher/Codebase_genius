# code_analyzer.jac

# Import the Python functions from the .py file
import from code_analyzer_helper { 
    analyze_repository, 
    get_entry_points 
}
import os;

import from main { code_genius }

# Define the Agent (as a Jac Node)
node CodeAnalyzer {
    
    # This ability is called when the code_genius walker "visits"
    can analyze_code with code_genius entry {
        
        # Get the repo_path from the visitor (the code_genius walker)
        repo_path = visitor.repo_path;

        if not repo_path or not os.path.exists(repo_path) {
            print("❌ CodeAnalyzer: Invalid repo_path provided.");
            visitor.status = "failed";
            report {"error": "CodeAnalyzer received invalid repo_path"};
            disengage;
        }

        print("🔎 CodeAnalyzer: Analyzing repository at " + repo_path);
        
        # Call the imported Python function
        try {
            ccg = analyze_repository(repo_path);
            
            # Add this check to satisfy the linter and make the code safer
            if not ccg {
                print("❌ CodeAnalyzer: Analysis returned empty data.");
                raise Exception("Analysis failed to produce results");
            }

            entry_points = get_entry_points(ccg);

            # Save the results back onto the visitor (the code_genius walker)
            visitor.ccg = ccg;
            visitor.entry_points = entry_points;
            visitor.status = "analyzed";

            print("✅ CodeAnalyzer: Analysis complete.");
            print("   - Files: " + str(ccg["total_files"]));
            print("   - Functions: " + str(ccg["total_functions"]));
            print("   - Classes: " + str(ccg["total_classes"]));

            report {
                "status": "success", 
                "total_files": ccg["total_files"]
            };
        } 
        except Exception as e {
            print("❌ CodeAnalyzer: Analysis failed: " + str(e));
            visitor.status = "failed";
            report {"error": "Analysis failed: " + str(e)};
        }
    }
}