# gig_server.wsgi
import sys
sys.path.append('/usr/local/var/www/gig_server')
sys.path.append('/var/www/html/gig_server')

from gig_server import app as application
