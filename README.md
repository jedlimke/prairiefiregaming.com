# Prairie Fire Gaming Website

Simple Jekyll site for Prairie Fire Gaming, hosted on GitHub Pages.

## Local Development

### Prerequisites

- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))

### Running Locally

1. **Build and start:**
   ```sh
   docker-compose up --build
   ```

2. **View the site:**
   ```
   http://localhost:4000
   ```

3. **Stop:**
   Press `Ctrl+C`

Changes to files are automatically detected and the site rebuilds.

## Deployment

Pushes to `master` branch automatically deploy to GitHub Pages via GitHub Actions.

## Content Structure

- **Pages**: Edit markdown files in root and `/about/`
- **Posts**: Add markdown files to `/_posts/` using format `YYYY-MM-DD-title.md`
- **Styles**: Modify SCSS files in `/_sass/`
- **Config**: Edit `_config.yml` for site settings
