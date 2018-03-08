""" Looter, a python package aiming at avoiding unnecessary repetition in
making common crawlers.
Author: alphardex  QQ:2582347430
If any suggestion, please contact me. Thank you for cooperation!

Usage:
  looter genspider <name> <tmpl>
  looter shell [<url>]
  looter (-h | --help | --version)

Options:
  -h --help        Show this screen.
  --version        Show version.
"""
import code
from .looter import *
from docopt import docopt

banner = f"""
Available objects:
    url          The url of the site you crawled.
    res          The response of the site.
    tree         The source tree, can be parsed by xpath and cssselect.

Available functions:
    fetch        Get the element tree of an HTML page.
    view         View the page in your browser. (test rendering)
    save_imgs    Download images from links.
    alexa_rank   Get the reach and popularity of a site in alexa.

For more info, plz refer to tutorial:
    [cssselect]: http://www.runoob.com/cssref/css-selectors.html
    [xpath]: http://www.runoob.com/xpath/xpath-syntax.html
"""

def main():
    """
    Commandline for looter!
    """
    argv = docopt(__doc__, version='1.41')
    if argv['genspider']:
        template = argv['<tmpl>']
        name = argv['<name>']
        if template not in ['data', 'image']:
            exit('Plz provide a template (data or image)')
        package_path = os.path.dirname(__file__)
        with open(f'{package_path}\\templates\\{template}.tmpl', 'r') as i, open(f'{name}.py', 'w') as o:
            o.write(i.read())

    if argv['shell']:
        if not argv['<url>']:
            url = input('Which site do u want to crawl?\nurl: ')
        else:
            url = argv['<url>']
        res = send_request(url)
        tree = etree.HTML(res.text)
        allvars = {**locals(), **globals()}
        code.interact(local=allvars, banner=banner)


if __name__ == '__main__':
    main()