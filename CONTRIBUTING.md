# Contributing Guidelines

Thank you for your interest in contributing to this project. Contributions are welcome, provided they follow the guidelines below.

## How to Contribute

1. **Fork the repository:** All work must be done in a fork. Do not commit directly to the main repository.
2. **Create a new branch:** Use descriptive branch naming conventions like `feature/<short-description>` or `bugfix/<short-description>`. Keep branch names limited to a single purpose.
3. **Make your changes:** Write clean, readable, and maintainable code. Follow the existing project structure and conventions. Avoid combining unrelated changes in one branch.
4. **Data and Environment Hygiene:** * Clear all Jupyter Notebook cell outputs before committing to prevent large Git diffs.
    * Do not commit large datasets or model binaries directly; use `.gitignore` or Data Version Control (DVC).
    * If you introduce new libraries, update `requirements.txt` or `environment.yml` accordingly.
5. **Add documentation where needed:** Add comments only when the intent is not clear. Update documentation if behavior, usage, or configuration changes.
6. **Commit your work:** Use clear and meaningful commit messages. Each commit should represent a logical unit of work. Avoid vague or generic commit messages.
7. **Submit a Pull Request:** Your Pull Request should clearly describe what was changed, why the change was necessary, and how the change was tested. Pull Requests missing this information may be delayed or rejected.

## Code Standards
* Follow the existing project structure
* Keep functions and classes modular and easy to read
* Avoid introducing unnecessary dependencies
* Remove unused code, imports, and variables
* Ensure all scripts and notebooks run without errors
* Do not commit commented-out code

## Testing Expectations
* Changes must not break existing functionality
* New features should include basic validation or tests where appropriate
* Notebooks must run end-to-end without manual intervention

## Reporting Issues
Please use the provided issue templates for bug reports and feature requests. Issues that do not follow the templates may be closed to keep discussions clear and actionable.
