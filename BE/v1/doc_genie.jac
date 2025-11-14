# doc_genie.jac

# Import the Python helper functions
import from doc_genie_helper { 
    generate_markdown_documentation, 
    save_documentation 
}
import os;

import from main { code_genius }

node DocGenie {
    has documentation: str = "";

    can generate_documentation with code_genius entry {
        print("✍️  DocGenie: Starting documentation generation...");

        # Get all data directly from the visitor (code_genius walker)
        repo_name = visitor.repo_name;
        repo_url = visitor.repo_url;
        readme_summary = visitor.readme_summary;
        ccg = visitor.ccg;
        entry_points = visitor.entry_points;

        # Check if we have the data we need
        if not ccg or not repo_name {
            print("❌ DocGenie: ERROR: No CCG or repo_name on visitor");
            report {"error": "DocGenie missing required data from visitor"};
            disengage;
        }
        
        print("   - Generating documentation for: " + repo_name);

        # Call the Python helper function
        markdown_doc = generate_markdown_documentation(
            repo_name=repo_name,
            repo_url=repo_url,
            readme_summary=readme_summary,
            ccg=ccg,
            entry_points=entry_points
        );

        # Save documentation on self and back on the walker
        self.documentation = markdown_doc;
        visitor.documentation = markdown_doc; 
        
        # Call the Python helper to save the file
        output_path = save_documentation(repo_name, markdown_doc);

        if output_path {
            print("✅ DocGenie: Documentation generated: " + output_path);
            report {
                "status": "documented", 
                "output_path": output_path, 
                "total_lines": len(markdown_doc.split("\n"))
            };
        } else {
            print("❌ DocGenie: Failed to save documentation.");
            report {"error": "Failed to save documentation file"};
        }
    }
}