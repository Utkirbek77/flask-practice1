from pathlib import Path

from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
import pandas as pd

app = Flask(__name__)
app.config["RESTX_JSON"] = {"ensure_ascii": False}
api = Api(
    app,
    version="1.0",
    title="Sales API",
    description="수량과 단가를 받아 총액을 예측한다",
    doc="/api/docs",
    prefix="/api",
)
ns = api.namespace("sales", description="총액 예측")

# Always load the submitted model located beside this application.
model = joblib.load(Path(__file__).resolve().parent / "sales_model.pkl")

order = api.model("Order", {
    "quantity": fields.Integer(required=True, example=40, description="수량"),
    "unit_price": fields.Float(required=True, example=200000, description="단가 (원)"),
})

@ns.route("/predict")
class Predict(Resource):
    @ns.doc("총액 예측")
    @ns.expect(order, validate=True)
    def post(self):
        """수량과 단가를 받아 예측 총액을 반환한다."""
        d = api.payload
        x = pd.DataFrame(
            [[d["quantity"], d["unit_price"]]],
            columns=["quantity", "unit_price"],
        )
        # Exactly the same feature engineering as in training (hw6.ipynb).
        x["qp"] = x["quantity"] * x["unit_price"]
        return {"total_sales": int(round(model.predict(x)[0]))}


if __name__ == "__main__":
    app.run(debug=False)
