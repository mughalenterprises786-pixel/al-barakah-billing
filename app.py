import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="AL-BARAKAH ENTERPRISES - Billing", layout="wide")

COMPANY_NAME = "AL-BARAKAH ENTERPRISES"

DATA_FILE = "billing_database.json"

PRODUCTS = [
    {"code":"1","name":"OKAY CHOCOLATE VANILLA LAYER CAKE","price":215},
    {"code":"2","name":"OKAY STRAWBERRY VANILLA LAYER CAKE","price":215},
    {"code":"3","name":"MINT GUM CENTER FILLED COATED BUBBLE","price":208},
    {"code":"4","name":"BADAM DELIGHT CANDY BOX","price":125},
    {"code":"5","name":"KHATU APPLE CANDY","price":400},
    {"code":"6","name":"CRISPEE WAFER BANANA","price":130},
    {"code":"7","name":"CRISPEE WAFER ORANGE","price":130},
    {"code":"8","name":"CRISPEE WAFER STRAWBERRY","price":130},
    {"code":"9","name":"MINI CONE STRAWBERRY","price":225},
    {"code":"10","name":"LUSH STAR CHOC. HAZELNUT","price":270},
    {"code":"11","name":"CHOCOLATE CONE WITH PEANUT CHUNKS","price":263},
    {"code":"12","name":"KOKO MASTI CHOCOLATE TUBE","price":210},
    {"code":"13","name":"KIDS JOY EGG CHOCOLATE WITH BISCUIT","price":445},
    {"code":"14","name":"KOKO MASTI STRAWBERRY TUBE","price":210},
    {"code":"15","name":"STRAWBERRY FLAVORED CONE BOX","price":208},
    {"code":"16","name":"KOKO MASTI MILK CREAM TUBE","price":210},
    {"code":"17","name":"CUP CAKE CHOCOLATE","price":215},
    {"code":"18","name":"MELLOW JOY MANGO MARSHMALLOW","price":206},
    {"code":"19","name":"MAX STRAWBERRY 3-D JELLY","price":205},
    {"code":"20","name":"SUPREME SOFT CAKE","price":215},
    {"code":"21","name":"SWISS ROLL CAKE STRAWBERRY","price":215},
    {"code":"22","name":"SWISS ROLL CAKE CHOCOLATE","price":215},
    {"code":"23","name":"O-MILK NATURAL OAT ENERGY","price":215},
    {"code":"24","name":"FISHU BIG CHOCO STICK","price":180},
    {"code":"25","name":"BADAM CONE BOX","price":208},
    {"code":"26","name":"MICKEY POP FRUITY BOX","price":137},
    {"code":"27","name":"KULFI PISTA MILKY LOLLIPOP BOX","price":130},
    {"code":"28","name":"NUT KHAT CHOCOLATE","price":130},
    {"code":"29","name":"CHOCOLATE CONE","price":208},
    {"code":"30","name":"STRAWBERRY CONE","price":208},
    {"code":"33","name":"MAX GUAVA 3-D JELLY","price":205},
    {"code":"34","name":"JIM JAM","price":145},
    {"code":"35","name":"CHOKOZO STRAWBERRY","price":135},
    {"code":"36","name":"CHOKOZO CHOCOLATE","price":135},
    {"code":"37","name":"CHOCOFY STRAWBERRY","price":135},
    {"code":"38","name":"CHOCOFY CHOCOLATE","price":135},
    {"code":"39","name":"MAKHAN BADAMI 10","price":215},
    {"code":"40","name":"MAKHAN BADAMI TOFFEE","price":138},
    {"code":"41","name":"DONUT CAKE","price":220},
    {"code":"42","name":"CHOCO BITE CRUSHED PEANUT","price":210},
    {"code":"43","name":"HEART BROWMIES","price":215},
    {"code":"44","name":"MAKHAN WAALA","price":140},
    {"code":"45","name":"COCONUT WAALA","price":145},
    {"code":"46","name":"PANDA SPONGE CAKE","price":215},
    {"code":"47","name":"MAGIC LOLLY POP","price":133},
    {"code":"48","name":"ROLLEX WAFER STRAWBERRY","price":215},
    {"code":"49","name":"ROLLEX WAFER CHOCOLATE","price":215},
    {"code":"50","name":"YUMMY DONUT STRAWBERRY","price":218},
    {"code":"51","name":"BOOMZ LIQUID MANGO","price":135}
]

# Initialize session
if 'database' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            st.session_state.database = json.load(f)
    else:
        st.session_state.database = {"next_bill_no": 1, "bills": []}

if 'selected_items' not in st.session_state:
    st.session_state.selected_items = {}

def save_database():
    with open(DATA_FILE, 'w') as f:
        json.dump(st.session_state.database, f, indent=4)

# HEADER
st.markdown(f"""
<div style="background: linear-gradient(135deg, #1a472a 0%, #2d8a4e 100%);
            padding: 25px; border-radius: 12px; text-align: center;">
    <h1 style="color: white; margin: 0;">{COMPANY_NAME}</h1>
    <p style="color: #ffd700; margin: 5px 0 0 0;">🧾 Billing Software 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# BILL INFO
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.text_input("📌 Bill No:", value=st.session_state.database["next_bill_no"], disabled=True)
with col2:
    st.text_input("📅 Date:", value=datetime.now().strftime("%d-%m-%Y"), disabled=True)
with col3:
    shop_name = st.text_input("🏪 Shop:", placeholder="Enter Shop Name")
with col4:
    order_booker = st.text_input("📝 Booker:", placeholder="Enter Order Booker")

st.markdown("---")

# PRODUCT TABLE
st.markdown("### 📋 Select Products")

col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1.5, 1.5, 2])
with col1: st.markdown("**✅**")
with col2: st.markdown("**Product Name**")
with col3: st.markdown("**Price/Box**")
with col4: st.markdown("**Boxes**")
with col5: st.markdown("**Total**")

st.markdown("---")

grand_total = 0

for idx, product in enumerate(PRODUCTS):
    key = f"p_{product['code']}"
    col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1.5, 1.5, 2])
    
    with col1:
        selected = st.checkbox("", key=f"select_{key}", 
                              value=st.session_state.selected_items.get(f"select_{key}", False))
        st.session_state.selected_items[f"select_{key}"] = selected
    
    with col2:
        st.markdown(product['name'])
    
    with col3:
        st.markdown(f"₹{product['price']:.2f}")
    
    with col4:
        if selected:
            boxes = st.number_input("", min_value=0, value=st.session_state.selected_items.get(f"boxes_{key}", 0),
                                    step=1, key=f"boxes_{key}")
            st.session_state.selected_items[f"boxes_{key}"] = boxes
        else:
            st.markdown("—")
            st.session_state.selected_items[f"boxes_{key}"] = 0
    
    with col5:
        if selected:
            total = product['price'] * st.session_state.selected_items.get(f"boxes_{key}", 0)
            st.markdown(f"**₹{total:,.2f}**")
            grand_total += total
        else:
            st.markdown("₹0.00")

st.markdown("---")

# GRAND TOTAL
st.markdown(f"""
<div style="background: #d4edda; padding: 15px; border-radius: 8px;
            text-align: center; font-size: 22px; font-weight: bold; color: #155724;">
    🧾 Grand Total: ₹{grand_total:,.2f}
</div>
""", unsafe_allow_html=True)

# DISCOUNT
col1, col2, col3 = st.columns(3)
with col1:
    discount = st.number_input("🎯 Discount %:", min_value=0.0, max_value=100.0, value=0.0, step=0.5)

discount_amount = grand_total * (discount / 100)
net_total = grand_total - discount_amount

with col2:
    st.metric("💰 Gross Amount", f"₹{grand_total:,.2f}")
with col3:
    st.metric("✅ Net Amount", f"₹{net_total:,.2f}", delta=f"-{discount_amount:,.2f}" if discount > 0 else None)

st.markdown("---")

# BUTTONS
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add Bill", use_container_width=True, type="primary"):
        selected_items = []
        for idx, product in enumerate(PRODUCTS):
            key = f"p_{product['code']}"
            if st.session_state.selected_items.get(f"select_{key}", False):
                boxes = st.session_state.selected_items.get(f"boxes_{key}", 0)
                if boxes > 0:
                    selected_items.append({
                        "code": product["code"],
                        "name": product["name"],
                        "price": product["price"],
                        "boxes": boxes
                    })
        
        if not selected_items:
            st.error("❌ Please select at least one product with quantity > 0")
        elif shop_name.strip() == "":
            st.error("❌ Please enter Shop Name")
        elif order_booker.strip() == "":
            st.error("❌ Please enter Booker name")
        else:
            for item in selected_items:
                bill = {
                    "Bill No": st.session_state.database["next_bill_no"],
                    "Date": datetime.now().strftime("%d-%m-%Y"),
                    "Shop": shop_name,
                    "Order Booker": order_booker,
                    "Code": item["code"],
                    "Product": item["name"],
                    "Boxes": item["boxes"],
                    "TP/Box": item["price"],
                    "Discount %": discount,
                    "Gross": item["price"] * item["boxes"],
                    "Net": (item["price"] * item["boxes"]) - ((item["price"] * item["boxes"]) * discount / 100)
                }
                st.session_state.database["bills"].append(bill)
            
            st.session_state.database["next_bill_no"] += 1
            save_database()
            st.success(f"✅ Bill Added Successfully! Bill No: {st.session_state.database['next_bill_no'] - 1}")
            st.balloons()
            
            for idx, product in enumerate(PRODUCTS):
                key = f"p_{product['code']}"
                st.session_state.selected_items[f"select_{key}"] = False
                st.session_state.selected_items[f"boxes_{key}"] = 0
            st.rerun()

with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        for idx, product in enumerate(PRODUCTS):
            key = f"p_{product['code']}"
            st.session_state.selected_items[f"select_{key}"] = False
            st.session_state.selected_items[f"boxes_{key}"] = 0
        st.rerun()

with col3:
    if st.button("📋 Show Bills", use_container_width=True):
        if st.session_state.database["bills"]:
            df = pd.DataFrame(st.session_state.database["bills"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No bills found")

# ============================================================
# DELETE BILL BY NUMBER - DELETE FEATURE
# ============================================================

st.markdown("---")
st.markdown("### 🗑 Delete Bill by Number")

col1, col2 = st.columns(2)
with col1:
    delete_bill_no = st.number_input("Bill No to Delete:", min_value=0, value=0, step=1)

with col2:
    if st.button("🗑 Delete Bill", use_container_width=True, type="secondary"):
        if delete_bill_no <= 0:
            st.error("❌ Please enter a valid Bill No")
        else:
            # Check if bill exists
            bill_exists = False
            for bill in st.session_state.database["bills"]:
                if bill["Bill No"] == delete_bill_no:
                    bill_exists = True
                    break

            if not bill_exists:
                st.error(f"❌ Bill No {delete_bill_no} not found")
            else:
                # Delete all items with this Bill No
                new_bills = [b for b in st.session_state.database["bills"] if b["Bill No"] != delete_bill_no]
                deleted_count = len(st.session_state.database["bills"]) - len(new_bills)
                st.session_state.database["bills"] = new_bills
                save_database()
                st.success(f"✅ Bill No {delete_bill_no} deleted successfully ({deleted_count} items)")
                st.rerun()

# FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666;">
    <p>📦 Products: {len(PRODUCTS)} | 🧾 Bills: {len(st.session_state.database['bills'])} | 📌 Next Bill: {st.session_state.database['next_bill_no']}</p>
    <p style="font-size: 12px;">⌨️ Tab: Next Field | Enter: Add Bill</p>
</div>
""", unsafe_allow_html=True)
