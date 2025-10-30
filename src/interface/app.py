from flask import Flask, render_template, jsonify
from emprestimo.service import LoanService

app = Flask(__name__, template_folder="templates", static_folder="static")

service = LoanService()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/emprestimos")
def emprestimos():
    return render_template("emprestimos.html")

@app.route("/devolucoes")
def devolucoes():
    return render_template("devolucoes.html")

@app.route("/api/loans")
def get_loans():
    loans = service.list_loans()
    return jsonify(loans)

@app.route("/api/loans/<int:loan_id>/return", methods=["POST"])
def return_loan(loan_id):
    result = service.return_book(loan_id)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
