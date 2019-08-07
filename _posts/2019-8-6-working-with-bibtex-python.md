---
layout: post
title: Working with BibTeX in Python - Biblib
---

During a PhD, one can read and store hundreds of papers. There is always a need to keep the papers well organized and kept, and also to have a way to easily transfer the citations of the papers to a manuscript.  I will not talk about which is the best way to store papers, as there are a few alternatives (I am a huge fan of Mendeley, despite the issues the desktop client has), but for citations, I think that BibTeX is the superior way in all aspects. As long as you are using LaTeX, of course, but come on, you should be using LaTeX anyway if you are in a scientific work. BibTeX is a nice way to format all the citations the same way, change how the citations are presented with a single line, and be more flexible.

Recently, I needed to do an analysis of a large bibliography of papers (>100 articles): I needed to look at the titles and abstracts of each paper and see if they coincide with a few selected keywords. Of course, I would not be doing that manually: I wanted a way to obtain automatically, for each paper, which keywords coincide. So, Python script! It is usually said that there is a Python package for everything. I still have not found myself in a situation where that sentence is false, but another different problem arises: there are too many Python packages that do exactly the same, and even have the same name! And this is what happened here. After a few searches, I found a post in Stack Overflow that recommended the library Biblib. But, when I searched for this library, I found two different packages:

1. [Biblib](https://github.com/aclements/biblib)

2. [Biblib](https://pypi.org/project/biblib/)

Which is the correct one? The answer is the first one, as it implements the actual BibTeX grammar and thus has complete compatibility, but my point is that, if you find it, and then you use pip (or any package manager) to install biblib thinking that you would get the first one, the package that will be installed is the second one, which is completely different from the first one!

Anyway, after installing and removing packages, I finally managed to install the package and code my small script. Biblib contains an elegant, easy to use library to deal with the BibTeX format in Python, read, write, and create entries. I will now comment a bit the code used.

First, how to load a .bib file. first, you need to open it with the standard Python library, and then use the Parser() function:

```py
import biblib.bib
bib_file = 'bibtex_collection.bib'
with open(bib_file, 'r') as fp:
    db = biblib.bib.Parser().parse(fp, log_fp=sys.stderr).get_entries()
```

The obtained object is an OrdreredDict(). You can iterate over it using values(), for example, or with a specific key (which will be the citation key). You can then access all the fields of the object, by name.

```py
for ent in db.values():
        key = ent.key
        abstract = ent['abstract']
```

It also includes some nice functions, like a function to print an entry in a nice, formatted way:

```py
print(ent.to_bib())
```

With this library, my problem was solved in a mere 10 minutes, without errors nor incomptabilities. Give it a try if you need to deal with BibTeX files in Python!

By the way, I keep updating the site with some funcionalities when I have some free time. I will put the changelog here, until I have a proper page to add it.

*Changelog:*
* Added commentaries to the blog pages.
* Added new icon to the site.


*To do soon:*
* Add keyword categories in each blog entry.
* Fix about me.
* Create a section of the changelog of the site.
* Create an archive of all the entries of the blog.
