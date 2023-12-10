from flask import Flask, render_template, request, redirect, url_for, send_file
import requests, os
from PIL import Image

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
  return render_template("bg-prompt.html", file_path=file_path)


@app.route("/prompt-upload", methods=["POST"])
def upload_prompt():
  file_path = request.args.get("file_path")
  prompt = request.form["bg-prompt"].replace(" ", "%20")
  api_url = f"https://image.pollinations.ai/prompt/{prompt}"
  response = requests.get(api_url)
  image_data = response.content
  with open(f'{file_path}background_image.jpg', 'wb') as f:
    f.write(image_data)
  background_image = Image.open(f"{file_path}background_image.jpg")
  overlay_image = Image.open(file_path)
  position = (int(background_image.width / 2 - (overlay_image.width / 2)),
              int(background_image.height / 2 - (overlay_image.height / 2)))
  background_image.paste(overlay_image, position, overlay_image)
  background_image.save(f"./static/images/{file_path}output_image.jpg")
  os.remove(file_path)
  os.remove(f"./{file_path}background_image.jpg")
  return redirect(url_for("img_result", out_file = f"./static/images/{file_path}output_image.jpg"))

@app.route("/result")
def img_result():
  out_file = request.args.get("out_file")
  print(out_file)
  return render_template("result.html", out_file=out_file)

@app.route("/download-out")
def download_out():
  out_file = request.args.get("out_file")
  if out_file == None:
    out_file = "./static/images/BackAI-Logo.png"
  return send_file(out_file, as_attachment=True)
  
app.run("0.0.0.0", 8080, debug=True)