# Blog

## Importing a post from Joplin

1. In Joplin, select **one** note and choose
   **File → Export → MD - Markdown + Front Matter**. Export it into an empty folder.
2. Install the dependency (once):

   ```sh
   pip install python-frontmatter
   ```

3. Run the importer with the export folder:

   ```sh
   python website/blog/import_joplin.py /path/to/export-folder
   ```

   Add `--force` to overwrite an existing post with the same slug.

4. Review and commit the changes:

   ```sh
   git add website/blog
   git commit -m "add <name> post"
   ```

### What the script does

- Writes the note to `posts/<slug>.md`, with normalized front matter
  (`title`, `date`, `tags`, `slug`).
- Copies images from `_resources/` to `assets/<slug>/` and rewrites links
  to `/blog/assets/<slug>/...`.
- Adds or updates the entry in `posts.json`, sorted newest first.

### Front matter fields

| Field   | Source                                           | Fallback          |
|---------|--------------------------------------------------|-------------------|
| `title` | `title`                                          | note filename     |
| `slug`  | `slug`, otherwise derived from the title         | `post`            |
| `date`  | `date`, then `created`, then `updated`           | today             |
| `tags`  | `tags` (list or comma/space-separated string)    | none              |

Set a `slug` in the Joplin note if you want a stable URL independent of the title.

### Troubleshooting

- **"Multiple markdown files at the same depth"**: the export contains more
  than one note. Export a single note.
- **"Post already exists"**: re-run with `--force` to replace it.
