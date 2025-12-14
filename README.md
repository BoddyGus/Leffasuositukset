# Movie Recommendations
Movie Recommendations is a web application where users can share movie tips and rate movies added by others.
The application is implemented in Python using the Flask library, and data is stored in an SQLite database.

## Features

- A user can create an account and log in to the application.
- A user can add new movies to the application (title, genre, description, year).
- A user can edit and delete the movies they have added.
- A user can see all movies added to the application, both their own and those added by other users.
- A user can search for movies with a keyword (for example based on the movie title or genre).
- On the user page, statistics are shown such as how many movies the user has added and a list of the movies they have added.
- A user can assign one or more categories to a movie (e.g. action, comedy, drama, horror).
- A user can add reviews (a comment and a rating) to their own and others’ movies.
- For each movie, all related reviews and the average rating are shown.

## Data Entities

- **Movie**
  The main data entity, containing the basic information of a movie (title, genre, description, year).

- **Review**
  A secondary data entity, containing the comment and rating given by a user for a specific movie.

## Technical Details

- The application is implemented in Python using the Flask library.
- The database is SQLite.
- The application uses raw SQL commands to interact with the database.
- The user interface consists of HTML pages and custom CSS.
- The application does not use JavaScript.
- Version control is handled with Git, and the code is published on GitHub.

## Installation

Install the `flask`-library:

```
$ pip install flask
```

Create the database tables and insert initial data:

```
$ sqlite3 database.db < schema.sql
```

You can start the application with:

```
$ flask run
```

## Large Dataset Testing and Pagination

For testing the application with a larger amount of data, you can:

1. Recreate the database:

  ```
  $ sqlite3 database.db < schema.sql
  ```

2. Generate a large test dataset using the provided `seed.py` script. The default values create roughly 200 users, 5000 movies and 20000 reviews:

  ```
  $ python seed.py
  ```

  You can edit the default numbers in `seed.py` if you want to test with smaller or larger datasets.

The front page uses server-side pagination (6 movies per page) when listing movies. The search field and page number (`page` parameter in the URL) can be used together, so you can test how searching and paging behave with large datasets.

With the default seed values (about 200 users, 5000 movies and 20000 reviews), the performance was measured using `time` and `curl` while the application was running. Loading the front page with different page numbers (`/?page=1`, `/?page=5`, `/?page=10`) took around 0.012 seconds per request. Searching with a common keyword and paging through the results (`/?q=action&page=1` and `/?q=action&page=3`) took about 0.059 seconds and 0.022 seconds respectively. These results indicate that server-side pagination keeps response times low even with a relatively large amount of data.

## Code Style Checks

Pylint was run for all Python files in the project with the command `pylint .`. The final overall score was **8.03/10**. Most of the remaining warnings relate to missing docstrings, long or branch-heavy functions and some duplicate code. These parts were left as they are at the end of the project to avoid introducing new bugs into otherwise working and tested functionality.
