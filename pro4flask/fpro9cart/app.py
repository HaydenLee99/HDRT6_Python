from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "v07rea10h@e!"
app.permanent_session_lifetime = timedelta(minutes=5)

products=[
    {"id":1, "name":"굉장한 노트북", "price":3500000},
    {"id":2, "name":"매끈한 키보드", "price":100000},
    {"id":3, "name":"엄청난 마우스", "price":150000},
    {"id":4, "name":"놀라운 모니터", "price":1500000}
]

@app.route("/")
def product_list():
    return render_template("products.html", products=products)

@app.route("/cart")
def show_cart():
    cart = session.get("cart",{})
    total = sum(info["price"] * info["qty"] for info in cart.values())
    return render_template("cart.html", cart=cart, total=total)

@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    # 세션 카트가 없을 시 빈 {} 생성
    cart = session.get("cart", {})
    # next(...,None) : 묶음형 자료에서 다음 값 1개를 꺼내는 함수
    # 주문 상품이 product에 기억됨
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return "상품을 찾을 수 없어요", 404
    # 주문 상품이 상품목록에 있으면 장바구니에 추가
    item_name = product["name"]
    if item_name in cart:
        cart[item_name]["qty"] += 1         # 카트에 동일 상품이 있는 경우 수량만 증가
    else:
        cart[item_name] = {"price":product["price"], "qty":1}       # cart에 최초 상품일 경우 수량 1 (qty 요소 생성)
    session["cart"] = cart                  # 변수 cart를 세션 "cart" 키에 값으로 저장
    session.permanent = True                # 5분 만료 적용 다시 시작
    return redirect(url_for("show_cart"))   # 카트에 저장 후 장바구니 보기로 이동

@app.route("/remove/<string:product_name>")
def remove_from_cart(product_name):
    cart = session.get("cart")

    if product_name in cart:
        del cart[product_name]

    session["cart"] = cart                  # 변수 cart를 세션 "cart" 키에 값으로 저장    
    return redirect(url_for("show_cart"))

@app.route("/clear")
def clear_cart():
    session.pop("cart", None)               # 세션의 여러개의 키 중에서 "cart"라는 키를 pop
    return redirect(url_for("show_cart"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)