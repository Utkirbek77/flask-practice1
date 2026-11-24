# HW6 — TOSHBOEV UTKIRBEK UKTAM UGLI (23012866)

총액 예측 회귀모델 비교 및 Flask REST API. 교수님 *Note 9-4*의 HW6 ①~⑦ 지침에 따라 작성했습니다.

## 실행 방법

**Python 환경:** Python 3, pandas, scikit-learn, joblib, jupyter, flask, flask-restx가 필요합니다.

**저장소 최상위 폴더**에서 `.venv` 가상환경을 만들거나 기존 환경을 사용합니다. `.venv`를 Git에 올리지 마세요.

```bash
# flask-practice1/ 폴더에서 실행
python3 -m venv .venv            # 이미 있다면 생략
source .venv/bin/activate        # macOS/Linux
# Windows: .venv\Scripts\activate
python -m pip install pandas scikit-learn joblib jupyter flask flask-restx
cd HW6
jupyter notebook hw6.ipynb
```

노트북 메뉴에서 **Kernel → Restart & Run All**을 실행합니다. 모든 셀이 끝난 뒤 저장하여 출력까지 포함합니다. 실행 결과 `sales_model.pkl`이 생성됩니다.

서버는 `HW6/`에서 별도 터미널로 실행합니다.

```bash
flask --app app run
```

Swagger 문서: http://127.0.0.1:5000/api/docs  
**POST `/api/sales/predict` → Try it out → Execute**에서 다음 JSON을 사용합니다.

```json
{"quantity": 40, "unit_price": 200000}
```

예상 **Response body**: `{"total_sales": 8000000}`. 서버의 실제 Execute 결과를 스크린샷으로 저장한 `docs.png`를 같은 폴더에 넣습니다.

## 단계 ③ 답

기본 linear regression은 `quantity`와 `unit_price`의 **가중합**만 표현할 수 있으므로, 두 입력값의 **곱셈**인 총액 관계를 그대로 학습하기 어렵다. 그래서 test R²는 **0.862**이다.  
`qp = quantity × unit_price`라는 특성을 추가하면 `total_sales = 1 × qp`를 학습할 수 있어 **linear + qp의 test R²가 1.000**이 된다. 서버에서도 반드시 같은 `qp`를 생성한다.

## 단계 ⑤ 결정과 이유

결정트리는 **max_depth=8**을 선택했다. 5-fold 교차검증 평균 R²는 depth 8에서 **0.992**, depth 12에서 **0.995**로 차이가 **0.003**에 불과하다. 반면 잎 수는 **250개 vs 781개**로, 거의 같은 정확도라면 더 단순한 모델이 합리적이다. 전체 결과를 보면 depth 무제한의 training R²는 1.000, test R²는 0.994로 차이가 작으며 이는 총액에 실제 곱셈 규칙이 있기 때문이다.

## 단계 ⑦ 답

최종 API 모델은 **linear regression + qp**로 선택한다. 수량 **40**, 단가 **200,000원**의 실제 총액은 **8,000,000원**이다. **linear + qp는 8,000,000원**, **tree(depth=8)는 약 7,362,301원**을 예측한다.  
총액은 수량과 단가의 곱이라는 명확한 공식으로 정해지므로, 그 공식을 특성으로 사용하는 linear + qp가 더 정확하고 해석하기 쉽다.
