# covermaker

Script to create PDF file covers using a LaTeX template and Python from a JSON.

#### Dependencies

* **Python**: This project uses only the Python Standard Libary (tested on `Python >= 3.4`).
* **Others**: `covermaker.py` needs to have `pdflatex` installed. `pdflatex` is included in the [TeX Live](http://tug.org/texlive/) LaTeX distribution.

#### How does it works?

`cover_template.tex` plays as a template using **tokenized variables** like `$variable` which will be replaced by the data set in the JSON file.

*Tokenized variable in the LaTeX template:*

```tex
\textsc{\LARGE $university} % Name of your university/college
```

Thanks to Python's **Template strings** (see the [docs](https://docs.python.org/release/3.5.2/library/string.html#template-strings) and the [PEP 292](https://www.python.org/dev/peps/pep-0292/)) the scrip replaces the `$variable` with the dictionary (when JSON is loaded) value asigned to the `"variable"` dictionary key.

*JSON object example:*

```json
{
"university" : "Technische Univesität München",
"subject" : "Flugsystemdynamik 1",
"document" : "Lehrstuhls für Flugsystemdynamik (FSD)",
"title" : "Flight System Dynamics 1 notes",
"name" : "Pablo",
"surname" : "Rodríguez Robles",
"email" : "prodrr05@estudiantes.unileon.es",
"date" : "21. September 2016"
}
```

*Iterating over the JSON array to get each object:*

```python
for cover in data["covers"]:
      create(cover)
```

*Creating template and substituting:*

```python
# This code is inside the create() function
with open('cover_template.tex', 'r') as p:
        template = p.read()
t = Template(template)
doc = t.substitute(cover)
```

*The script creates the file `cover.tex` with the variables replaced:*
```tex
\textsc{\LARGE Technische Universität München} % Name of your university/college
```

Running a **subprocess** we call `pdflatex` and create the `cover.pdf` which is placed in the `output` directory.

*subprocess call() used to call `pdflatex`:*

```python
# This code is inside the create() function
subprocess.call(['pdflatex',                   # Using pdflatex
                 '-output-directory=./output',
                 './.temp/cover%d.tex' % n],   # cover.tex destination's path
                 stdout=open(os.devnull, 'wb') # Disables pdflalatex's text output
                )
```


