
from flask import Flask, render_template, request
from pipeline import run_freshcheck

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    answer = ""
    error = None

    if request.method == "POST":
        answer = request.form.get("answer", "").strip()

        if not answer:
            error = "Please enter an answer to verify."
        else:
            try:
                report = run_freshcheck(answer)
            except Exception as e:
                error = f"Verification failed: {str(e)}"

    return render_template(
        "index.html",
        report=report,
        answer=answer,
        error=error
    )

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "project": "FreshCheck AI",
        "tavily": "configured",
        "bifrost": "configured"
    }

if __name__ == "__main__":
    app.run(debug=True)
