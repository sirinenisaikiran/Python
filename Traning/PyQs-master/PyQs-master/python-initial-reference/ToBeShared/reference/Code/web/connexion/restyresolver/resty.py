import logging

import connexion
from connexion.resolver import RestyResolver

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__)
app.add_api('resty-api.yaml',
            arguments={'title': 'RestyResolver Example'},
            resolver=RestyResolver('api'))
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
                
if __name__ == '__main__':
    app.run(port=9090)