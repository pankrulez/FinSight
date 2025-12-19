import os
from pathlib import Path

def create_structure():
    # Define the folder structure
    dirs = [
        "data/raw",
        "data/processed",
        "data/vector_store",
        "models",
        "logs",
        "notebooks",
        "src/api",
        "src/agents",
        "src/data_engine",
        "src/ml_engine",
        "src/ui",
    ]
    
    # Create directories
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        # Create __init__.py in every src subdirectory to make them packages
        if d.startswith("src"):
            init_file = Path(d) / "__init__.py"
            init_file.touch()

    # Create root __init__.py
    Path("src/__init__.py").touch()
    
    print("✅ Project structure created successfully.")
    print("✅ __init__.py files created.")

if __name__ == "__main__":
    create_structure()