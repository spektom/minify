minify
======

This script minifies all recently changed CSS and JS files placed under the given path,
then it goes, and updates all HTML files that reference them by replacing URL argument
of format "v20140125-1013" with the latest timestamp.

The following Internet services are in use by this script:

 * [cssminifier.com](cssminifier.com)
 * [reducisaurus.appspot.com](reducisaurus.appspot.com)
 * [closure-compiler.appspot.com](closure-compiler.appspot.com)


### Usage ###

`minify.py <static files prefix>`

For example, to minify all CSS and JS files that reside in folder "static/"
invoke the following command:

  `./minify.py static/`


