from flask import Flask, render_template

app = Flask(__name__)

# #flask --app testing.py run     -> error access blocked?
# #gunicorn testing:app       -> error refused to connect?

@app.route('/')
def index():
  return render_template('loginpage.html')


if __name__ == '__main__':
  app.run()
