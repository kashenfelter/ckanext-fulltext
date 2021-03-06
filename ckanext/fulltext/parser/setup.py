import sys

from jcc import cpp

options = {
    'include': ('lib/tika-app-1.6.jar','lib/org.eclipse.osgi.jar','lib/log4j.properties.jar', 'lib/microsoft-translator-java-api-0.6.2.jar', 'lib/json-simple-1.1.jar', 'lib/jackson-databind-2.4.0.jar', 'lib/cxf-rt-frontend-jaxrs-2.7.8.jar', 'lib/cxf-api-2.7.8.jar'),
    'jar': ('lib/tika-parsers-1.6.jar', 'lib/tika-core-1.6.jar', 'lib/tika-translate-1.6.jar'),
    'package': ('org.xml.sax', 'java.lang', 'java.util', 'java.text', 'java.io'),
    'python': 'tika',
    'version': '1.6',
    'module': 'tikaparser',
    'reserved': ('asm',),
    'classes': ('java.io.File', 'java.io.FileInputStream', 'java.io.ByteArrayInputStream', 'java.lang.System','java.lang.Runtime','java.util.Arrays','java.util.Collections','java.util.HashMap','java.util.HashSet','java.util.TreeSet','java.lang.IllegalStateException','java.lang.IndexOutOfBoundsException','java.util.NoSuchElementException','java.text.SimpleDateFormat','java.text.DecimalFormat','java.text.Collator','java.io.StringReader','java.io.DataInputStream','java.net.URL','java.net.URI'),
}

import sys
import os.path

jcc_args = []

for dir in sys.path:
    probe_dir = os.path.join(dir, 'jcc')
    if os.path.exists(probe_dir):
        print "Found jcc library at: %s" % probe_dir
        jcc_args = [os.path.join(probe_dir, 'nonexistent-argv-0')]
        break

if not jcc_args:
    raise Exception("tika library not found in sys.path: %s" % sys.path)

for k, v in options.iteritems():
    if k == 'classes':
        jcc_args.extend(v)
    elif hasattr(v, '__iter__'):
        for value in v:
            jcc_args.append('--%s' % k)
            jcc_args.append(value)
    else:
        jcc_args.append('--%s' % k)
        jcc_args.append(v)

setup_args = []
egg_info_mode = False
maxheap = '64m'

i = 1

while i < len(sys.argv):
    arg = sys.argv[i]

    if arg == 'install':
        jcc_args.append('--install')
    elif arg == 'build':
        jcc_args.append('--build')
    elif arg == '-c':
        # forwarded_args.append(arg)
        pass
    elif arg == 'egg_info':
        jcc_args.append('--egg-info')
    elif arg == '--vmarg':
        jcc_args.append(arg)
        i += 1
        jcc_args.append(sys.argv[i])
    elif arg == '--maxheap':
        i += 1
        maxheap = sys.argv[i]
    else:
        setup_args.append(arg)
    i += 1
    
for extra_arg in setup_args:
    jcc_args.append('--extra-setup-arg')
    jcc_args.append(extra_arg)

jcc_args.extend(['--maxheap', maxheap])

print "jcc_args = %s" % jcc_args

cpp.jcc(jcc_args)
