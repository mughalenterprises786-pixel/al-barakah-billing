# ============================================================
# AL-BARAKAH ENTERPRISES
# STREAMLIT BILLING SOFTWARE (EXACT COLAB VERSION)
# ============================================================

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ============================================================
# COMPANY INFORMATION
# ============================================================

COMPANY_NAME = "AL-BARAKAH ENTERPRISES"
DATA_FILE = "billing_database.json"

# ============================================================
# PRODUCT LIST - EXACT SAME AS COLAB
# ============================================================

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
    {"code":"33","name":"MAX GUAVA 3-D JELLY","price":205}
]

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session():
    if 'database' not in st.session_state:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    st.session_state.database = json.load(f)
            except:
                st.session_state.database = {"next_bill_no": 1, "bills": []}
        else:
            st.session_state.database = {"next_bill_no": 1, "bills": []}
    
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None
    
    if 'product_code' not in st.session_state:
        st.session_state.product_code = ""

def save_database():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.database, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving database: {e}")
        return False

# ============================================================
# MAIN APP - EXACT COLAB LAYOUT
# ============================================================

def main():
    init_session()
    
    st.set_page_config(
        page_title=f"{COMPANY_NAME} - Billing",
        page_icon="🧾",
        layout="wide"
    )
    
    # ============================================================
    # HEADER
    # ============================================================
    
    st.markdown(f"""
    <div style="background-color: #1a472a; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: white; margin: 0;">{COMPANY_NAME}</h1>
        <p style="color: #ffd700; margin: 0;">Billing Software 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # BILL INFORMATION - EXACT COLAB
    # ============================================================
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Bill No:", value=st.session_state.database["next_bill_no"], disabled=True)
    with col2:
        st.text_input("Date:", value=datetime.now().strftime("%d-%m-%Y"), disabled=True)
    
    # ============================================================
    # CUSTOMER INFORMATION - EXACT COLAB
    # ============================================================
    
    shop_name = st.text_input("Shop:", placeholder="Enter Shop Name")
    order_booker = st.text_input("Booker:", placeholder="Enter Order Booker")
    salesman = st.text_input("Salesman:", placeholder="Enter Salesman")
    delivery_man = st.text_input("Delivery:", placeholder="Enter Delivery Man")
    
    st.markdown("---")
    
    # ============================================================
    # PRODUCT SELECTION - EXACT COLAB
    # ============================================================
    
    code = st.text_input("Code:", placeholder="Product Code", key="code_input")
    
    # Product display - EXACT same as Colab
    if code:
        product = next((p for p in PRODUCTS if p["code"] == code), None)
        if product:
            st.session_state.selected_product = product
            st.markdown(f"<h4 style='color:green;margin:0;'>{product['name']}</h4>", unsafe_allow_html=True)
        else:
            st.session_state.selected_product = None
            st.markdown("<b style='color:red;'>Product Not Found</b>", unsafe_allow_html=True)
    else:
        st.session_state.selected_product = None
        st.markdown("<b style='color:red;'>No Product Selected</b>", unsafe_allow_html=True)
    
    # ============================================================
    # QUANTITIES - EXACT COLAB
    # ============================================================
    
    col1, col2 = st.columns(2)
    with col1:
        cartons = st.number_input("Cartons:", min_value=0, value=0, step=1)
    with col2:
        boxes = st.number_input("Boxes:", min_value=0, value=0, step=1)
    
    # ============================================================
    # PRICES - EDITABLE (EXACT COLAB)
    # ============================================================
    
    # Auto-populate price if product selected - EXACT Colab behavior
    default_tp_box = 0.0
    default_tp_carton = 0.0
    
    if st.session_state.selected_product:
        default_tp_box = float(st.session_state.selected_product['price'])
        default_tp_carton = default_tp_box * 12
    
    col1, col2 = st.columns(2)
    with col1:
        tp_carton = st.number_input("TP/Carton:", min_value=0.0, value=default_tp_carton, step=1.0, format="%.2f")
    with col2:
        tp_box = st.number_input("TP/Box:", min_value=0.0, value=default_tp_box, step=1.0, format="%.2f")
    
    # ============================================================
    # BILL TOTAL - EXACT COLAB
    # ============================================================
    
    col1, col2, col3 = st.columns(3)
    with col1:
        discount = st.number_input("Discount %:", min_value=0.0, max_value=100.0, value=0.0, step=0.5, format="%.1f")
    
    # Calculate - EXACT Colab formula
    gross_total = (boxes * tp_box) + (cartons * tp_carton)
    discount_amount = gross_total * (discount / 100)
    net_total = gross_total - discount_amount
    
    with col2:
        st.text_input("Gross:", value=f"₹{gross_total:,.2f}", disabled=True)
    with col3:
        st.text_input("Net:", value=f"₹{net_total:,.2f}", disabled=True)
    
    st.markdown("---")
    
    # ============================================================
    # BUTTONS - EXACT COLAB
    # ============================================================
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧮 Calculate", use_container_width=True):
            st.success("✅ Calculation Completed")
    
    with col2:
        if st.button("➕ Add Bill", use_container_width=True, type="primary"):
            if st.session_state.selected_product and (cartons > 0 or boxes > 0):
                bill = {
                    "Bill No": st.session_state.database["next_bill_no"],
                    "Date": datetime.now().strftime("%d-%m-%Y"),
                    "Shop": shop_name,
                    "Order Booker": order_booker,
                    "Salesman": salesman,
                    "Delivery Man": delivery_man,
                    "Code": st.session_state.selected_product["code"],
                    "Product": st.session_state.selected_product["name"],
                    "Cartons": cartons,
                    "Boxes": boxes,
                    "TP/Carton": tp_carton,
                    "TP/Box": tp_box,
                    "Discount %": discount,
                    "Gross": gross_total,
                    "Net": net_total
                }
                
                st.session_state.database["bills"].append(bill)
                st.session_state.database["next_bill_no"] += 1
                save_database()
                
                st.success(f"✅ Bill Added Successfully! Bill No: {bill['Bill No']}")
                st.balloons()
                
                # Reset - EXACT Colab behavior
                st.session_state.selected_product = None
                st.session_state.product_code = ""
                st.rerun()
            else:
                st.error("❌ Please select a product and enter quantity")
    
    with col3:
        if st.button("🔄 Refresh Bill", use_container_width=True):
            st.session_state.selected_product = None
            st.session_state.product_code = ""
            st.rerun()
    
    # ============================================================
    # EXPORT BUTTONS - EXACT COLAB
    # ============================================================
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Bill", use_container_width=True):
            if st.session_state.database["bills"]:
                df = pd.DataFrame(st.session_state.database["bills"])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"bills_export_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.error("❌ No bills to export")
    
    with col2:
        if st.button("📦 Export Load Form", use_container_width=True):
            if order_booker:
                booker_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"] == order_booker]
                if booker_bills:
                    summary = {}
                    for bill in booker_bills:
                        code = bill["Code"]
                        if code not in summary:
                            summary[code] = {"Product": bill["Product"], "Boxes": 0, "Cartons": 0}
                        summary[code]["Boxes"] += bill["Boxes"]
                        summary[code]["Cartons"] += bill["Cartons"]
                    
                    df = pd.DataFrame([{"Product": v["Product"], "Boxes": v["Boxes"], "Cartons": v["Cartons"]} 
                                      for v in summary.values()])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Load Form",
                        data=csv,
                        file_name=f"{order_booker}_Load_Form.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"❌ No bills found for: {order_booker}")
            else:
                st.error("❌ Please enter Order Booker name")
    
    with col3:
        if st.button("🗑 Refresh Load Form", use_container_width=True):
            if order_booker:
                new_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"] != order_booker]
                st.session_state.database["bills"] = new_bills
                save_database()
                st.success(f"✅ Load form cleared for: {order_booker}")
                st.rerun()
            else:
                st.error("❌ Please enter Order Booker name")
    
    # ============================================================
    # SHOW BILLS - EXACT COLAB
    # ============================================================
    
    st.markdown("---")
    if st.button("📋 Show Bills", use_container_width=True):
        if st.session_state.database["bills"]:
            df = pd.DataFrame(st.session_state.database["bills"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No bills found")
    
    # ============================================================
    # FOOTER - EXACT COLAB
    # ============================================================
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666;">
        <p>Products: {len(PRODUCTS)} | Bills: {len(st.session_state.database['bills'])} | Next Bill: {st.session_state.database['next_bill_no']}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    main()
