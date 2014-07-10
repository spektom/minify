#!/usr/bin/env python2.7

import httplib, urllib, sys, glob, os.path, re, json, datetime

HTML_EXT = ('.py', '.html', '.js')

def minified_name(f):
	return re.sub('\.([^\.]*)$', '.min.\\1', f)

# Reads response from the service, and writes the result
# into the minified version file.
def read_response(f, conn):
	response = conn.getresponse()
	data = response.read()
	conn.close()
	if response.status != 200:
		sys.exit("\nWrong HTTP status: %d\n%s" % (response.status, data))

	if (len(data) < 3):
		sys.exit("\nERROR: can't process %s" % f)

	with open(minified_name(f), 'w') as w:
		w.write(data)
	print "Written %s" % minified_name(f)

# Minify CSS file
def css_minify(f):
	print "Minifying CSS %s" % f
	data = { "input" : file(f, 'r').read() }
	headers = { "Content-type": "application/json" }
	conn = httplib.HTTPConnection('cssminifier.com')
	conn.request('POST', '/raw', json.dumps(data), headers)
	read_response(f, conn)

# Compile JS file
def js_compile(f):
	print "Compiling JS %s" % f
	params = urllib.urlencode([
		('js_code', file(f, 'r').read()),
		('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
		('output_format', 'text'),
		('output_info', 'compiled_code'),
	])
	headers = { "Content-type": "application/x-www-form-urlencoded" }
	conn = httplib.HTTPConnection('closure-compiler.appspot.com')
	conn.request('POST', '/compile', params, headers)
	read_response(f, conn)

# Updates timestamps
def update_timestamps(m):
	cur_time = datetime.datetime.now().strftime('v%Y%m%d-%H%M')
	file_re = re.compile('(%s.*)v\d{8}\-\d{4}' % re.escape(m))

	for dname, dirs, files in os.walk("."):
		for fname in files:
			if fname.endswith(HTML_EXT):
				fpath = os.path.join(dname, fname)
				with open(fpath) as f:
					s = f.read()
					if file_re.search(s):
						print "Updating HTML file %s" % fpath 
						s = file_re.sub('\\1%s' % cur_time, s)
						with open("%s" % fpath, "w") as f:
							f.write(s)

def is_minified(f):
	return "-min." in f or ".min." in f

def is_js_or_css(f):
	return f.endswith(".js") or f.endswith(".css")

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('Usage: %s <static files prefix>' % sys.argv[0])

	prefix = sys.argv[1]

	processed = []
	for dname, dirs, files in os.walk(prefix):
		for fname in files:
			if is_js_or_css(fname) and not is_minified(fname):
				f = os.path.join(dname, fname)
				m = minified_name(f)
				process = False
				if not os.path.isfile(m):
					print "Creating %s" % m
					process = True
				elif os.path.getmtime(f) > os.path.getmtime(m):
					print "Updating %s" % m
					process = True
				if process:
					if f.endswith(".js"):
						js_compile(f)
					else:
						css_minify(f)
					processed.append(m)

	for m in processed:
		update_timestamps(os.path.basename(m))

