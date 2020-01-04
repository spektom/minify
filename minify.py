#!/usr/bin/env python3

import datetime
import os.path
import re
import requests
import sys

HTML_EXT = (".py", ".html", ".js")


def minified_name(f):
    return re.sub("\.([^\.]*)$", ".min.\\1", f)


def write_minified_file(f, data):
    target = minified_name(f)
    with open(target, "w") as w:
        w.write(data)
    print("Written %s" % target)


# Minify CSS file
def css_minify(f):
    with open(f, "r") as c:
        content = c.read()
    try:
        print("Minifying CSS %s [using cssminifier.com]" % f)
        data = {"input": content}
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        r = requests.post("https://cssminifier.com/raw", data=data, timeout=3)
        write_minified_file(f, r.text)
    except:
        # Try another service:
        print("Minifying CSS %s [using cnvyr.io]" % f)
        r = requests.post(
            "http://srv.cnvyr.io/v1?min=css",
            files={"files0": content},
            timeout=3)
        write_minified_file(f, r.text.replace("/*** files0 ***/", "").strip())


# Compile JS file
def js_compile(f):
    with open(f, "r") as c:
        content = c.read()
    try:
        print("Compiling JS %s [using closure-compiler.appspot.com]" % f)
        data = {
            "js_code": content,
            "compilation_level": "SIMPLE_OPTIMIZATIONS",
            "output_format": "text",
            "output_info": "compiled_code",
        }
        r = requests.post(
            "https://closure-compiler.appspot.com/compile",
            data=data,
            timeout=3)
        write_minified_file(f, r.text)
    except:
        # Try another service:
        print("Minifying JS %s [using cnvyr.io]" % f)
        r = requests.post(
            "http://srv.cnvyr.io/v1?min=js",
            files={"files0": content},
            timeout=3)
        write_minified_file(f, r.text.replace("/*** files0 ***/", "").strip())


# Updates timestamps
def update_timestamps(m):
    cur_time = datetime.datetime.now().strftime("v%Y%m%d-%H%M")
    file_re = re.compile("(%s.*)v\d{8}\-\d{4}" % re.escape(m))

    for dname, dirs, files in os.walk("."):
        for fname in files:
            if fname.endswith(HTML_EXT):
                fpath = os.path.join(dname, fname)
                with open(fpath) as f:
                    s = f.read()
                    if file_re.search(s):
                        print("Updating HTML file %s" % fpath)
                        s = file_re.sub("\\1%s" % cur_time, s)
                        with open("%s" % fpath, "w") as f:
                            f.write(s)


def is_minified(f):
    return "-min." in f or ".min." in f


def is_js_or_css(f):
    return f.endswith(".js") or f.endswith(".css")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s <static files prefix>" % sys.argv[0])

    prefix = sys.argv[1]

    processed = []
    for dname, dirs, files in os.walk(prefix):
        for fname in files:
            if is_js_or_css(fname) and not is_minified(fname):
                f = os.path.join(dname, fname)
                m = minified_name(f)
                process = False
                if not os.path.isfile(m):
                    print("Creating %s" % m)
                    process = True
                elif os.path.getmtime(f) > os.path.getmtime(m):
                    print("Updating %s" % m)
                    process = True
                else:
                    print("Skipping %s" % m)
                if process:
                    if f.endswith(".js"):
                        js_compile(f)
                    else:
                        css_minify(f)
                    processed.append(m)

    for m in processed:
        update_timestamps(os.path.basename(m))
