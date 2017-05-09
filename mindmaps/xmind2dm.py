# xmind2dm.py
import sys
import zipfile
from lxml import etree

def main(xmindfile):
    xmzip = zipfile.ZipFile(xmindfile, mode="r")
    xmzip.extract('content.xml')
    
    f = open('test.xml')
    xml = f.read()
    f.close()

    tree = etree.parse('test.xml')
    root = tree.getroot()
    print(root)
    elem = root.xpath("sheet/topic/children/topics/topic/children/topics/topic")
    print(elem)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        xmindfile = sys.argv[1]
    else:
        print('\n\n Please provide a XMind mindmap file to process. \n\n')
        exit()
        
    main(xmindfile)


