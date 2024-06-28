from flask import Flask
from threading import Thread 
app = Flask(__name__)


@app.route("/")
def hello():
  return "Stay alive"


def run():
  app.run()

def stay_alive():
  t = Thread(target=run)
  t.start()
