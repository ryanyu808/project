Download Procedures:
1. Cloned the `dataset_neiss-sports-injuries` repository to my computer.
2. Used the `data` folder inside the dataset repository.
3. Opened the CPSC NEISS query and download page in a browser.
4. Downloaded the 2023, 2024, and 2025 annual NEISS Excel files.
5. Downloaded the optional 2025 TSV file.
6. Moved the downloaded files into the repository's `data` folder.
7. Opened each Excel workbook to verify that it downloaded successfully.

Downloaded files, size, and format
- neiss2023.xlsx - 42.5 MB - opened successfully in Excel
- neiss2024.xlsx - 47.4 MB - opened successfully in Excel
- neiss2025.xlsx - 54.0 MB - opened successfully in Excel
- neiss2025.tsv - 85.9 MB - downloaded successfully

Problems/Blockers:
The three Excel files opened successfully with no issues. I attempted to verify the 2025 TSV using pandas, but Python was not available through my PowerShell environment. No additional software was installed because installation is not required at this stage.

Relevant technical questions:
- Flat files seem like a good option to investigate because the NEISS data is mostly read-only and the downloaded files are reasonable in size. PostgreSQL could become useful if we need to run repeated queries or have multiple people accessing the same data. Before deciding, we should test how easily and quickly the full dataset can be loaded and analyzed from flat files. 

Course tools that might help:
PostgreSQL: Could help organize and query the data if working directly with flat files become inefficient of if we need repeated queries.
Supabase: Could be useful if the team needs a shared PostgreSQL database that everyone can access, especially if we eventually deploy an application.
Hugging Face Spaces: Could be useful if we build a Streamlit app and want to make it accessible online. 

Next steps:
1. Test whether the full 3 year dataset loads and runs efficiently using flat files.
2. Determine whether the project will need shared access or repeated queries that would make PostgreSQL/Supabase useful.
3. Consider whether Streamlit would be useful if the final project needs an interactive interface for the target audience.