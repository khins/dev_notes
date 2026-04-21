## Setup

1. Create a virtual environment:
   `python3 -m venv .venv`

2. Activate it:
   `source .venv/bin/activate`

3. Install dependencies:
   `pip install -r requirements.txt`

4. Set up PostgreSQL and create the schema from `sql/schema.sql`

5. Create a local `.env` file from `.env.example` and fill in your DB credentials

6. Run the app:
   `python -m app.main`

The app loads environment variables from `.env` automatically.

## Database Notes

If your database was created before the `title` rename, run this once:

`ALTER TABLE notes RENAME COLUMN topic TO title;`

If your database was created before the `languages` table was added, run this:

```sql
CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO languages (name) VALUES
('Python'),
('JavaScript'),
('SQL');
```

If your database already has a `notes.language` text column and you want to normalize it to `language_id`, run this:

```sql
INSERT INTO languages (name)
SELECT DISTINCT language
FROM notes
WHERE language IS NOT NULL
ON CONFLICT (name) DO NOTHING;

ALTER TABLE notes ADD COLUMN language_id INT REFERENCES languages(id);

UPDATE notes n
SET language_id = l.id
FROM languages l
WHERE n.language = l.name;

ALTER TABLE notes DROP COLUMN language;
```

## VS Code

This project includes VS Code settings and a debugger launch config.

1. Open the repo folder in VS Code
2. Select the interpreter at `.venv/bin/python`
3. Make sure your `.env` file exists
4. Open the Run and Debug panel
5. Start `Debug Dev Notes CLI` or press `F5`

Recommended first breakpoints:
- `app/main.py`
- `app/menu.py`
- `app/models.py`
- `app/db.py`
