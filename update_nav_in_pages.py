import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove inline jQuery load script
    content = re.sub(
        r'<script>\s*\\$\(function\(\)\{[^}]+\}\);\s*</script>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # Ensure header placeholder after <body>
    content = re.sub(
        r'(<body[^>]*>\s*)',
        r"\1<header id=\"header\"></header>\n    ",
        content,
        count=1
    )

    # Ensure footer placeholder before </body>
    content = re.sub(
        r'(</footer>)(\s*)(</body>)',
        r"\1\n    <footer id=\"footer\"></footer>\2\3",
        content,
        count=1
    )

    # Insert include-nav.js before Vendor Scripts comment
    content = content.replace(
        '<!-- Vendor Scripts -->',
        '<script src="/assets/js/include-nav.js"></script>\n    <!-- Vendor Scripts -->'
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")

def main():
    root_dir = 'MotzzWebsite-main'
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html') and file not in ('header.html', 'footer.html'):
                process_file(os.path.join(subdir, file))

if __name__ == "__main__":
    main()
