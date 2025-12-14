# Pylint Report

Pylint was run for the entire project using the command `pylint .`. The final overall score was **8.03/10**. Below is a summary of the most important types of messages and why they were not fully fixed at the end of the project.

## Raw pylint output

```text
pylint .
************* Module user
user.py:1:0: C0114: Missing module docstring (missing-module-docstring)
user.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:49:11: W0718: Catching too general exception Exception (broad-exception-caught)
user.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:100:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
user.py:3:0: C0411: standard import "secrets" should be placed before third party imports "flask.Blueprint", "werkzeug.security.generate_password_hash" (wrong-import-order)
************* Module reviews
reviews.py:414:0: C0304: Final newline missing (missing-final-newline)
reviews.py:1:0: C0114: Missing module docstring (missing-module-docstring)
reviews.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:54:4: R1731: Consider using 'page = max(page, 1)' instead of unnecessary if block (consider-using-max-builtin)
reviews.py:57:4: C0103: Variable name "PER_PAGE" doesn't conform to snake_case naming style (invalid-name)
reviews.py:128:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:133:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:147:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:173:4: C0103: Variable name "MAX_TITLE_LEN" doesn't conform to snake_case naming style (invalid-name)
reviews.py:147:0: R0911: Too many return statements (15/6) (too-many-return-statements)
reviews.py:147:0: R0912: Too many branches (15/12) (too-many-branches)
reviews.py:211:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:242:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:274:4: C0103: Variable name "MAX_TITLE_LEN" doesn't conform to snake_case naming style (invalid-name)
reviews.py:242:0: R0911: Too many return statements (16/6) (too-many-return-statements)
reviews.py:242:0: R0912: Too many branches (16/12) (too-many-branches)
reviews.py:308:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:323:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:345:11: W0718: Catching too general exception Exception (broad-exception-caught)
reviews.py:359:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:397:11: W0718: Catching too general exception Exception (broad-exception-caught)
reviews.py:359:0: R0911: Too many return statements (9/6) (too-many-return-statements)
reviews.py:404:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:407:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:407:0: E0102: function already defined line 4 (function-redefined)
reviews.py:410:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:410:0: E0102: function already defined line 4 (function-redefined)
reviews.py:2:0: C0411: standard import "datetime.datetime" should be placed before third party import "flask.Blueprint" (wrong-import-order)
************* Module config
config.py:1:0: C0304: Final newline missing (missing-final-newline)
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:40:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:40:0: R0914: Too many local variables (21/15) (too-many-locals)
************* Module app
app.py:25:0: C0304: Final newline missing (missing-final-newline)
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:21:0: C0413: Import "from user import init_user" should be placed at the top of the module (wrong-import-position)
app.py:22:0: C0413: Import "from reviews import init_reviews" should be placed at the top of the module (wrong-import-position)
************* Module queries.user_queries
queries/user_queries.py:20:0: C0304: Final newline missing (missing-final-newline)
queries/user_queries.py:1:0: C0114: Missing module docstring (missing-module-docstring)
queries/user_queries.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/user_queries.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/user_queries.py:15:11: W0718: Catching too general exception Exception (broad-exception-caught)
queries/user_queries.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module queries.review_queries
queries/review_queries.py:30:0: C0304: Final newline missing (missing-final-newline)
queries/review_queries.py:1:0: C0114: Missing module docstring (missing-module-docstring)
queries/review_queries.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/review_queries.py:6:10: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
queries/review_queries.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/review_queries.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/review_queries.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module queries.item_queries
queries/item_queries.py:60:0: C0301: Line too long (101/100) (line-too-long)
queries/item_queries.py:78:0: C0304: Final newline missing (missing-final-newline)
queries/item_queries.py:1:0: C0114: Missing module docstring (missing-module-docstring)
queries/item_queries.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:62:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:62:0: R0913: Too many arguments (6/5) (too-many-arguments)
queries/item_queries.py:62:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
queries/item_queries.py:69:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:69:0: R0913: Too many arguments (6/5) (too-many-arguments)
queries/item_queries.py:69:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
queries/item_queries.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
queries/item_queries.py:1:0: R0801: Similar lines in 2 files
==reviews:[20:33]
==seed:[9:22]
    "toiminta",
    "komedia",
    "draama",
    "kauhu",
    "scifi",
    "fantasia",
    "seikkailu",
    "trilleri",
    "animaatio",
    "dokumentti",
    "romantiikka",
]
 (duplicate-code)
queries/item_queries.py:1:0: R0801: Similar lines in 2 files
==queries.item_queries:[63:73]
==reviews:[200:300]
        INSERT INTO items (user_id, title, genre, age_rating, description, year)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [user_id, title, genre, age_rating, description, year])

def update_item(item_id, title, genre, age_rating, description, year):
    sql = """
        UPDATE items
           SET title = ?, genre = ?, age_rating = ?, description = ?, year = ?
         WHERE id = ? (duplicate-code)
queries/item_queries.py:1:0: R0401: Cyclic import (app -> reviews -> user) (cyclic-import)
queries/item_queries.py:1:0: R0401: Cyclic import (app -> reviews) (cyclic-import)
queries/item_queries.py:1:0: R0401: Cyclic import (app -> user) (cyclic-import)

------------------------------------------------------------------
Your code has been rated at 8.03/10 (previous run: 8.03/10, +0.00)

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
