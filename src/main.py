import sys
import os
from generatePage import generate_pages_recursive, static_to_public

base_path = "/"
if sys.argv[1] != "":
    base_path = sys.argv[1]

def main():
    static_to_public("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)

main()

