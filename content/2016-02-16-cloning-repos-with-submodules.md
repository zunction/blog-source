Title: Cloning repositories with submodules
Date: 2016-02-16
Tags: git, submodules
Slug: cloning-repos-with-submodules
Author: zhangsheng

The setup of this blog is done in such a way that the source files and settings are stored in a particular github repository and the output files (the files that let us see this website) are kept in another. However, when pelican is being run to generate the output files, they are stored in a folder called `output`. After playing around with the theme that I want for my blog, I messed up the internals which up till now I don't know what went wrong. Hence I deleted the local files of my whole blog content and cloned the version from my github repository which should be a working copy using the following command:

```
git clone https://github.com/zunction/blog-source
```
But after cloning, the output which is the submodule in the file `blog-source` contains nothing instead of the files that should be inside. It turns out you have to do some setup of the submodule after cloning a repository with a submodule (take note that this is done in the folder containing the submodule):
```
git submodule update --init
```
after which you can check that the output folder is being linked to the correct remote repository by using
```
git remote -v
```
This is such a lifesaver for someone like me who always tinkers with stuff and get into trouble.
