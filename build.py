from pathlib import Path
import markdown
import yaml


CONTENT_DIR = Path("content/blog")
TEMPLATE_FILE = Path("templates/article.html")
OUTPUT_DIR = Path("blog")

BASE_URL = "https://itfinancialmanagementsoftware.com"


def read_post(file_path):
    raw = file_path.read_text(encoding="utf-8")

    if not raw.startswith("---"):
        raise ValueError(f"{file_path} does not contain front matter.")

    parts = raw.split("---", 2)

    metadata_text = parts[1]
    markdown_text = parts[2]

    metadata = yaml.safe_load(metadata_text)

    html_content = markdown.markdown(
        markdown_text,
        extensions=["extra", "sane_lists"]
    )

    return metadata, html_content


def build_post(file_path, template):
    metadata, html_content = read_post(file_path)

    title = metadata["title"]
    slug = metadata["slug"]
    post_date = str(metadata["date"])
    description = metadata["description"]
    category = metadata.get("category", "ITFM")

    output_html = template

    output_html = output_html.replace("{{title}}", title)
    output_html = output_html.replace("{{slug}}", slug)
    output_html = output_html.replace("{{date}}", post_date)
    output_html = output_html.replace("{{description}}", description)
    output_html = output_html.replace("{{category}}", category)
    output_html = output_html.replace("{{content}}", html_content)

    post_directory = OUTPUT_DIR / slug
    post_directory.mkdir(parents=True, exist_ok=True)

    output_file = post_directory / "index.html"

    output_file.write_text(
        output_html,
        encoding="utf-8"
    )

    print(f"Built: /blog/{slug}/")


def build_sitemap(posts):
    urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/blog/",
    ]

    for metadata in posts:
        slug = metadata["slug"]
        urls.append(f"{BASE_URL}/blog/{slug}/")

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']

    sitemap.append(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    )

    for url in urls:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{url}</loc>")
        sitemap.append("  </url>")

    sitemap.append("</urlset>")

    Path("sitemap.xml").write_text(
        "\n".join(sitemap),
        encoding="utf-8"
    )

    print("Built: /sitemap.xml")


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    template = TEMPLATE_FILE.read_text(
        encoding="utf-8"
    )

    post_files = list(
        CONTENT_DIR.glob("*.md")
    )

    print(f"Found {len(post_files)} posts.")

    all_posts = []

    for post_file in post_files:
        metadata, html_content = read_post(post_file)

        all_posts.append(metadata)

        build_post(post_file, template)

    build_sitemap(all_posts)

    print("Build complete.")


if __name__ == "__main__":
    main()