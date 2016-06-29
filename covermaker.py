from string import Template
import subprocess
import os


def create(cover, n, debug=False):
    """
    Takes a JSON object and replaces all the variables in the
    LaTeX template. Then it calls pdflatex via subprocess and
    creates the PDF conver from the .tex file.

    cover --> JSON object
    n ------> Used to name all the outputs
    debug --> Toogles the debug flags
    """

    # We replace '_' by '\_' because of LaTeX does not recognize
    # the underscore as a character.
    # [http://texblog.net/latex-archive/uncategorized/symbols/]
    #
    if '_' in cover['email']:
        cover['email'] = cover['email'].replace('_', '\_')

    doc_path = '.temp/cover%d.tex' % n
    if debug:
        print("Document created.")

    with open('cover_template.tex', 'r') as p:
        template = p.read()
    if debug:
        print("Template readed.")

    # See PEP 292:
    # [https://docs.python.org/release/3.5.2/
    # library/string.html#template-strings]
    #
    t = Template(template)
    doc = t.substitute(cover)
    if debug:
        print("Template filled.")

    with open(doc_path, 'w') as f:
        f.write(doc)
    if debug:
        print("Cover written.")

    subprocess.call(['pdflatex',
                     '-output-directory=./output',
                     './.temp/cover%d.tex' % n],
                     stdout=open(os.devnull, 'wb')
                    )
    if debug:
        print("Pdflatex called.")

    os.remove('./output/cover%d.log' % n)
    os.remove('./output/cover%d.out' % n)
    os.remove('./output/cover%d.aux' % n)
    if debug:
        print("Unnecessary files removed.")


if __name__ == '__main__':
    import json
    import os, shutil

    # Loads the JSON array, which contains the different
    # cover objects
    data = json.loads(open('covers.json').read())

    # Removing previus content in the directory output
    folder = 'output'

    # Since Python 3 raw_input() is named input()
    # [https://docs.python.org/3/library/functions.html#input]
    s = ''
    while s == '':
        s = input('\033[93m' + 'Warning: ' + '\033[0m' +
                  "Content in the 'output' folder will be removed.\n" +
                  "Type something to continue: ")

    # Removes all the files whitin the indicated directory
    # Taken from:
    # [http://stackoverflow.com/a/185941]
    #
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print("Removed '%s'" % the_file)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    # Pythonic way to count inside a for loop
    # [http://stackoverflow.com/a/3162287]
    #
    for i, cover in enumerate(data["covers"]):
        print("Calling pdflatex to create cover %d" % i)
        create(cover, data["covers"].index(cover), debug=False)
        print("Created cover %d" % i)
