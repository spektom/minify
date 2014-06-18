minify
======

This script minifies all CSS and JS files placed under the given path, then it goes, and updates
all HTML files that reference them by replacing URL argument of format "v20140125-1013" with the
latest timestamp.


### Usage ###

To minify all CSS and JS files that reside in folder "static/" invoke the following command:

  `./minify.py static/`

By default, minify.py will look for JS and CSS files starting from the current directory (".").
