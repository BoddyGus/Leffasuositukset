# Pylint Report

Pylint was run for the entire project using the command `pylint .`. The final overall score was **8.03/10**. Below is a summary of the most important types of messages and why they were not fully fixed at the end of the project.

## Missing docstrings

Many messages are of the form:

- `C0114: Missing module docstring`
- `C0116: Missing function or method docstring`

These mean that modules and functions do not have docstring comments. For this small project, the code is already relatively short and readable, so I decided not to add docstrings everywhere at the end of the project. Adding docstrings would not change the behaviour of the application and could have taken time away from functional and security testing.

## Long or branch-heavy functions

Some functions trigger warnings like:

- `R0911: Too many return statements`
- `R0912: Too many branches`
- `R0914: Too many local variables`

These functions mainly handle form validation and input checking (for example when creating or editing movies and reviews). They are currently working and well tested. Refactoring them into many smaller functions at this stage might make the control flow harder to follow and could introduce new bugs, so I chose to leave them as they are.

## Duplicate code

Pylint reports a few `R0801: Similar lines in 2 files` warnings. These come from repeated patterns such as:

- The list of allowed genres.
- Very similar SQL for inserting and updating movies.

In this context, a bit of duplication keeps each function self-contained and easier to understand. Extracting all of this into shared helpers would make the code more abstract without a clear benefit for this size of project.

## Cyclic imports and import order

There are `R0401: Cyclic import` and `C0411/C0413: import order` warnings caused by the structure of the Flask application (the main app module, blueprints, and query helper modules importing each other). The application runs correctly in practice, and resolving all cyclic-import and import-order warnings would require a significant restructuring of the package layout. This was considered too risky and unnecessary for a working course project.

## Other minor style issues

Some smaller warnings remain, such as:

- Constant naming (for example `secret_key` not in upper case).
- A few missing final newlines at the end of files.
- "Unnecessary else after return" suggestions.

These are purely stylistic and do not affect correctness. I corrected some easy issues but intentionally did not chase every style warning in order to keep the focus on functionality, security (CSRF, password hashing, access control) and large-data performance.

Overall, the Pylint report shows that the project follows reasonably good style (score 8.03/10), and the remaining warnings are mainly about coding style and structure rather than actual bugs.
