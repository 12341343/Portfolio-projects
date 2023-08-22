from flask import Flask, render_template, request
import requests
from mail_sender import Mail_sender
app = Flask(__name__)
mail_send = Mail_sender()
response = requests.get(url="https://api.npoint.io/f15f7b35cddc672d96ab").json()

@app.route("/")
def home():
    return render_template("index.html", data=response)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    def_text = ""
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        mail_send.send_mail(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)


    return render_template("contact.html", msg_sent=False)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/<int:post_id>")
def posts(post_id):
    current_post = response[post_id]
    post_title = current_post["title"]
    post_description = current_post["body"]
    return render_template('post.html', post_title=post_title, post_description=post_description)




if __name__ == "__main__":
    app.run(debug=True)
