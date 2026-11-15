# Vaibhav Rathore — Research Portfolio

Source for [vaibhavrathore1999.github.io](https://vaibhavrathore1999.github.io), my personal research and professional portfolio.

The site presents my work in domain generalization, open-world recognition, representation learning, multilingual AI, time-series modeling, and applied machine learning.

## Site sections

- **Home** — introduction, news, publications, blog, experience, education, and awards
- **Research** — research themes, ongoing work, and completed projects
- **Publications** — published and accepted papers, followed by ongoing research
- **Writing** — accessible articles about machine learning and computer vision
- **CV** — education, experience, publications, service, teaching, and skills

## Updating research

Publication and project metadata lives in [`_data/research.yml`](_data/research.yml). The homepage, Research page, Publications page, and web CV render from this shared source.

Career, education, publication, and recognition milestones live in [`_data/timeline.yml`](_data/timeline.yml).

Published or accepted work may include:

- Venue and publication status
- Public paper, code, project, slides, or poster links
- Authors and a short contribution summary

Ongoing research intentionally includes only:

- Title
- Authors
- A concise, public-safe summary

Do not add venue names, submission dates, review status, submission identifiers, reviewer correspondence, or private manuscript links to ongoing work.

## Local development

The site uses Jekyll and the Academic Pages theme.

```bash
bundle install
bundle exec jekyll serve --livereload
```

Open `http://localhost:4000` to preview the site. Before publishing, run:

```bash
bundle exec jekyll build
```

The download links serve the supplied `resume/Resume_Sep26.pdf`, configured by
`resume_url` in `_config.yml`. The web CV continues to use the site data.
The optional `scripts/build_cv.py` generator writes a separate `files/cv.pdf`;
it does not replace the supplied resume.

The public CV and publication lists intentionally exclude ongoing venues,
review status, submission identifiers, and private manuscript links. Add a
paper to `published` only when its accepted or published status is public;
keep work in `ongoing` until then.

## Repository structure

```text
_data/research.yml       Research and publication metadata
_data/timeline.yml       Career and academic milestones
_pages/                  Main site pages
_posts/                  Long-form posts
_sass/layout/_minimal.scss
                         Site-specific minimalist design
assets/css/main.scss     Stylesheet entry point
_config.yml              Jekyll and site configuration
```

## Publishing

Changes pushed to the `main` branch are deployed through GitHub Pages.

## Credits

Built with [Jekyll](https://jekyllrb.com/) and adapted from the [Academic Pages](https://academicpages.github.io/) template. Site content and custom design are maintained by Vaibhav Rathore.
