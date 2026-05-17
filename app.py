from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
import cohere
import json
import PyPDF2
import secrets 

from docx import Document

# -------------------------------
# App & Config
# -------------------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# -------------------------------
# MongoDB
# -------------------------------
MONGO_URI = "mongodb+srv://ayushrnj18:Spincricket%4018@cluster0.lsac64b.mongodb.net/library_system"
client = MongoClient(MONGO_URI)
db = client["library_system"]

users_col = db.users
documents_col = db.documents

# -------------------------------
# Upload Config
# -------------------------------
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------------------
# Cohere
# -------------------------------
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# -------------------------------
# Google OAuth
# -------------------------------
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)


# -------------------------------
# Decorators
# -------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_role") != "admin":
            return "Access Denied", 403
        return f(*args, **kwargs)
    return decorated

# -------------------------------
# Home
# -------------------------------
@app.route("/")
def home():
    return render_template("home.html")

# -------------------------------
# Google Auth
# -------------------------------

@app.route("/login")
def login():
    nonce = secrets.token_urlsafe(16)
    session["oidc_nonce"] = nonce

    return google.authorize_redirect(
        url_for("auth_callback", _external=True),
        nonce=nonce
    )


@app.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()

    nonce = session.pop("oidc_nonce", None)

    user_info = google.parse_id_token(token, nonce=nonce)

    email = user_info["email"]
    name = user_info.get("name")
    picture = user_info.get("picture")

    user = users_col.find_one({"email": email})

    if not user:
        users_col.insert_one({
            "email": email,
            "name": name,
            "picture": picture,
            "role": "user",
            "created_at": datetime.now()
        })
        role = "user"
    else:
        role = user.get("role", "user")

    session["user_email"] = email
    session["user_role"] = role

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# -------------------------------
# Library Main
# -------------------------------
@app.route("/index")
@login_required
def index():
    return render_template("index.html")

# -------------------------------
# Search
# -------------------------------
@app.route("/search/title")
@login_required
def search_title():
    title = request.args.get("title", "")
    results = list(documents_col.find({
        "title": {"$regex": title, "$options": "i"}
    }))

    if results:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], results[0]["file_path"])
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                session["context_content"] = f.read()[:4000]
                session["context_title"] = results[0]["title"]
        except:
            session["context_content"] = ""
            session["context_title"] = ""

    return render_template("search_results.html", results=results, query=title)


@app.route("/search/recent")
@login_required
def search_recent():
    results = list(documents_col.find().sort("created_at", -1).limit(10))
    return render_template("search_results.html", results=results, query="Recent")

# -------------------------------
# Upload
# -------------------------------
@app.route("/upload/new", methods=["POST"])
@login_required
def upload_new():
    title = request.form.get("title")
    document = request.files.get("document")

    if document and title:
        filename = secure_filename(document.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        document.save(save_path)

        documents_col.insert_one({
            "title": title,
            "uploaded_by": session["user_email"],
            "created_at": datetime.now(),
            "file_path": filename
        })

        return redirect(url_for("upload_manage"))

    return "Upload failed", 400


@app.route("/upload/manage")
@login_required
def upload_manage():
    documents = list(documents_col.find({
        "uploaded_by": session["user_email"]
    }))
    return render_template("manage_uploads.html", documents=documents)

# -------------------------------
# Admin Example Route
# -------------------------------
@app.route("/admin/users")
@login_required
@admin_required
def admin_users():
    users = list(users_col.find())
    return render_template("admin_users.html", users=users)

# -------------------------------
# Chatbot
# -------------------------------
@app.route("/chatbot/query", methods=["POST"])
@login_required
def chatbot_query():
    user_input = request.json.get("message")

    response = co.chat(
        message=user_input,
        model="command-r-plus"
    )

    return jsonify({"reply": response.text})

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
