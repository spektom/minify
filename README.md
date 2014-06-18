minify
======

This script minifies all recently changed CSS and JS files placed under the given path,
then it goes, and updates all HTML files that reference them by replacing URL argument
of format "v20140125-1013" with the latest timestamp.

The following Internet services are used by this script:

	* cssminifier.com - Used for minifying CSS files.
	* closure-compiler.appspot.com - Used for minifying JS files.


### Usage ###

To minify all CSS and JS files that reside in folder "static/" invoke the following command:

  `./minify.py static/`

By default, minify.py will look for JS and CSS files starting from the current directory (".").

