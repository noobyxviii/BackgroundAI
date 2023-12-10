from flask import Flask, render_template, request, redirect, url_for
import requests, os

app = Flask(__name__)

@app.route("/")
def main():
  return render_template("index.html")

@app.route("/upload")
def upload_page():
  return render_template("upload.html")

@app.route("/image-upload", methods=["POST"])
def upload_image():
  file = request.files["file"]
  file.save("uploads/" + file.filename)
  file_path = "uploads/" + file.filename
  response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(file_path, 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'cryaZ7rtetoBUTFkZjCD6WmZ'},
  )
  with open(f"{file.filename}-no-bg.png", 'wb') as out:
      out.write(response.content)
  os.remove(file_path)
  return redirect(url_for("bg_prompt", file_path=f"{file.filename}-no-bg.png"))

@app.route("/bg-prompt")
def bg_prompt():
  file_path = request.args.get("file_path")
  return render_template("bg-prompt.html")

@app.route("/result")
def result_page():
  return render_template("result.html")

app.run("0.0.0.0", 8080, debug=True)