import os
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = "9eDWTyTL9hr9ReEGvYdJBQzN35JfgY3P7CCwad59wDACxfUpEMv2dWjq4TAUmnMw"

from routes.contents import contents as contents
app.register_blueprint(contents)
if __name__ == '__main__':
  app.run(debug = True)
