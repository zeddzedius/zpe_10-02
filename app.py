from flask import Flask, request, render_template, url_for
import logo_gen

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    image_url = None
    error     = None

    if request.method == "POST":
        forma       = request.form.get("forma","").strip()
        style       = request.form.get("style","").strip()
        description = request.form.get("description","").strip()

        result = logo_gen.generate_logo(forma, style, description)

        if result.startswith("Ошибка"):
            error = result
        else:
            # result — путь static/<имя>.jpeg
            filename = result.split("/")[-1]
            image_url = url_for("static", filename=filename)

    return render_template("index.html", image=image_url, error=error)

if __name__ == "__main__":
    app.run(debug=True)
