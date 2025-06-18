from flask import Flask, render_template, request
import requests 
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    username = None
    repos = []
    if request.method == "POST":
        username = request.form.get("username")

        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)

        if response.status_code == 200:

            repos_data = response.json()
            total_stars = 0
            languages = {}
            top_repos = []

            for repo in repos_data :

                total_stars += repo["stargazers_count"]
                lang = repo["language"]

                if lang:
                    languages[lang] = languages.get(lang, 0) + 1

                top_repos.append({
                    "name": repo["name"],
                    "stars": repo["stargazers_count"],
                    "url": repo["html_url"]
                })
            top_repos = sorted(top_repos, key=lambda r: r["stars"], reverse=True)[:3]
        else:
            repos_data = []
            total_stars = 0
            languages = {}
            top_repos = []
        
    return render_template("index.html",
                       username=username,
                       repos=repos_data,
                       total_stars=total_stars,
                       languages=languages,
                      top_repos=top_repos)

if __name__ == "__main__":
    app.run(debug=True)
