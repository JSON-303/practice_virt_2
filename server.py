from flask import Flask, render_template, redirect, session
import requests
from pprint import pprint
from flask_app import app


URL = "https://rickandmortyapi.com/api/character"


@app.get("/")
def index():
    """This route renders the home page."""
    if "url" not in session:
        session["url"] = URL

    response = requests.get(session["url"])
    data = response.json()
    results = []

    for item in data["results"]:
        character = {}
        character["name"] = item["name"]
        character["image"] = item["image"]
        character["species"] = item["species"]
        character["gender"] = item["gender"]
        results.append(character)

    for result in results:
        pprint(result["name"])

    session["next"] = data["info"]["next"]
    session["prev"] = data["info"]["prev"]
    pprint(f"NEXT: {session['next']}, PREV: {session['prev']}")

    return render_template("index.html", results=results)


@app.get("/next")
def next():
    session["url"] = session["next"]
    return redirect("/")


@app.get("/prev")
def prev():
    session["url"] = session["prev"]
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
