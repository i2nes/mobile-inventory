import sys
import os.path

# The appengine_config.py file gets loaded when starting a new application instance.
# Adding `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))