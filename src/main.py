from textnode import TextNode

print("Hello World")

def main():
    testNode = TextNode("Fifty", "bold", "www.test.com")
    testNode2 = TextNode("Fifty", "bold", "www.test.com")
    print(testNode == testNode2)

main()