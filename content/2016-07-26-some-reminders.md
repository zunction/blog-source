Title: Some reminders
Date: 2016-07-26 21:13
Tags: git, submodules
Slug: some-reminders
Author: zunction

Yet another reminder for myself on how to set up this blog.

Ran into lots of problems again and it took a couple of weeks and breaks away from it for me to eventually find the problem. Turns out that the problem was not with git; pelican was the culprit. Before I forget, let me just make the note here. In the `pelicanconf.py` and `publishconf.py` files that are created when you run `pelican-quickstart`, do not forget to set

```
DELETE_OUTPUT_DIRECTORY = False
OUTPUT_PATH = 'output/'
```

My pain came from blindly copying [iKevinY's](http://kevinyap.ca/) settings for his blog so as to obtain the minimalists [penumatic](https://github.com/iKevinY/pneumatic) theme. Another reminder least I forget again is that I have to
```
git add *
git commit -m 'commit message here'
git push origin master
```
to the output folder (repo) first before doing it for the blog-source. Dire consequences are to be expected if these reminders are not heeded by the future me.

![snowy](images/snowy)
