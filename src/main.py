from generatePage import generate_pages_recursive, static_to_public

def main():
    static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()

