# ============================================================
# AL-BARAKAH ENTERPRISES
# BILLING SOFTWARE 2026 - STREAMLIT APP (FULL SIZE)
# ============================================================

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import io
import xlsxwriter

# ============================================================
# COMPANY INFORMATION
# ============================================================

COMPANY_NAME = "AL-BARAKAH ENTERPRISES"
DATA_FILE = "billing_database.json"

# ============================================================
# PRODUCT LIST (UPDATED - 51 Products)
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

# ============================================================
# DATABASE FUNCTIONS
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
    
    if 'tp_box_value' not in st.session_state:
        st.session_state.tp_box_value = 0.0
    
    if 'boxes_value' not in st.session_state:
        st.session_state.boxes_value = 0

def save_database():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.database, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# ============================================================
# EXCEL EXPORT - FULL SIZE
# ============================================================

def export_bill_excel(shop_name):
    shop_bills = [b for b in st.session_state.database["bills"] if b["Shop"].strip() == shop_name.strip()]
    if not shop_bills:
        return None
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Bill")
    
    # ============================================================
    # PAGE SETUP
    # ============================================================
    
    worksheet.set_paper(9)
    worksheet.set_portrait()
    worksheet.fit_to_pages(1, 1)
    
    # ============================================================
    # FULL SIZE COLUMN WIDTHS
    # ============================================================
    
    worksheet.set_column("A:A", 30)     # Product - Full width
    worksheet.set_column("B:B", 15)     # Code
    worksheet.set_column("C:C", 15)     # Boxes
    worksheet.set_column("D:D", 20)     # TP/Box
    worksheet.set_column("E:E", 20)     # Gross
    worksheet.set_column("F:F", 18)     # Discount %
    worksheet.set_column("G:G", 22)     # Net
    
    # ============================================================
    # BIG FONTS
    # ============================================================
    
    title = workbook.add_format({
        "bold": True,
        "font_size": 22,        # Big Title
        "align": "center",
        "border": 2
    })
    
    header = workbook.add_format({
        "bold": True,
        "font_size": 16,        # Big Header
        "bg_color": "#D9EAD3",
        "align": "center",
        "border": 2
    })
    
    cell = workbook.add_format({
        "font_size": 14,        # Big Cell Data
        "border": 1,
        "align": "center"
    })
    
    total = workbook.add_format({
        "bold": True,
        "font_size": 16,        # Big Total
        "bg_color": "#FFF2CC",
        "align": "center",
        "border": 2
    })
    
    # ============================================================
    # COMPANY HEADER
    # ============================================================
    
    worksheet.merge_range("A1:G1", COMPANY_NAME, title)
    
    # ============================================================
    # BILL INFO
    # ============================================================
    
    first_bill = shop_bills[0]
    
    worksheet.write("A3", "Shop Name", header)
    worksheet.write("B3", first_bill["Shop"], cell)
    
    worksheet.write("D3", "Booker", header)
    worksheet.write("E3", first_bill["Order Booker"], cell)
    
    worksheet.write("G3", "Bill No", header)
    worksheet.write("H3", first_bill["Bill No"], cell)
    
    worksheet.write("G4", "Date", header)
    worksheet.write("H4", first_bill["Date"], cell)
    
    # ============================================================
    # TABLE HEADER
    # ============================================================
    
    row = 6
    
    headers = ["Product", "Code", "Boxes", "TP/Box", "Gross", "Discount %", "Net"]
    
    for col, value in enumerate(headers):
        worksheet.write(row, col, value, header)
    
    row += 1
    
    # ============================================================
    # WRITE BILL DATA
    # ============================================================
    
    gross_total = 0
    
    for bill in shop_bills:
        worksheet.write(row, 0, bill["Product"], cell)
        worksheet.write(row, 1, bill["Code"], cell)
        worksheet.write(row, 2, bill["Boxes"], cell)
        worksheet.write(row, 3, bill["TP/Box"], cell)
        worksheet.write(row, 4, bill["Gross"], cell)
        worksheet.write(row, 5, bill["Discount %"], cell)
        
        # Net = Gross - Discount % (Excel Formula)
        excel_row = row + 1
        worksheet.write_formula(
            row, 6,
            f"=E{excel_row}-(E{excel_row}*F{excel_row}/100)",
            cell
        )
        
        gross_total += bill["Gross"]
        row += 1
    
    # ============================================================
    # TOTAL ROW
    # ============================================================
    
    worksheet.write(row, 2, "TOTAL", total)
    worksheet.write(row, 4, gross_total, total)
    worksheet.write_blank(row, 5, None, total)
    worksheet.write_formula(
        row, 6,
        f"=E{row+1}-(E{row+1}*F{row+1}/100)",
        total
    )
    
    # ============================================================
    # SAVE
    # ============================================================
    
    workbook.close()
    output.seek(0)
    return output

# ============================================================
# EXPORT LOAD FORM - FULL SIZE
# ============================================================

def export_load_form_excel(booker):
    booker_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"].strip() == booker.strip()]
    if not booker_bills:
        return None
    
    summary = {}
    for bill in booker_bills:
        code = bill["Code"]
        if code not in summary:
            summary[code] = {
                "Product": bill["Product"],
                "Boxes": 0
            }
        summary[code]["Boxes"] += bill["Boxes"]
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Load Form")
    
    # ============================================================
    # BIG FONTS
    # ============================================================
    
    title = workbook.add_format({
        "bold": True,
        "font_size": 20,        # Big Title
        "align": "center",
        "border": 2
    })
    
    header = workbook.add_format({
        "bold": True,
        "font_size": 16,        # Big Header
        "bg_color": "#D9EAD3",
        "align": "center",
        "border": 2
    })
    
    cell = workbook.add_format({
        "font_size": 14,        # Big Cell Data
        "border": 1,
        "align": "center"
    })
    
    total = workbook.add_format({
        "bold": True,
        "font_size": 16,        # Big Total
        "bg_color": "#FFF2CC",
        "align": "center",
        "border": 2
    })
    
    worksheet.set_column("A:A", 30)     # Product - Full width
    worksheet.set_column("B:B", 15)     # Boxes
    
    worksheet.merge_range("A1:B1", COMPANY_NAME, title)
    
    worksheet.write("A3", "Order Booker", header)
    worksheet.write("B3", booker, cell)
    
    worksheet.write("A5", "Product", header)
    worksheet.write("B5", "Boxes", header)
    
    row = 5
    total_boxes = 0
    
    for item in summary.values():
        worksheet.write(row, 0, item["Product"], cell)
        worksheet.write(row, 1, item["Boxes"], cell)
        total_boxes += item["Boxes"]
        row += 1
    
    worksheet.write(row, 0, "TOTAL", total)
    worksheet.write(row, 1, total_boxes, total)
    
    workbook.close()
    output.seek(0)
    return output

# ============================================================
# CSS - BIG FONTS
# ============================================================

def add_keyboard_css():
    st.markdown("""
    <style>
    .stTextInput label, .stNumberInput label {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    .stTextInput input, .stNumberInput input {
        font-size: 18px !important;
        padding: 10px 14px !important;
        height: 50px !important;
    }
    
    .stButton button {
        font-size: 18px !important;
        padding: 12px 20px !important;
        height: 55px !important;
    }
    
    input:focus, textarea:focus {
        border: 3px solid #2d8a4e !important;
        box-shadow: 0 0 15px rgba(45, 138, 78, 0.3) !important;
        outline: none !important;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        transition: 0.2s;
    }
    
    .product-name {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #155724 !important;
        margin: 10px 0 !important;
        padding: 15px 20px !important;
        background-color: #d4edda !important;
        border-radius: 10px !important;
        border-left: 8px solid #28a745 !important;
        text-align: left !important;
    }
    
    .shop-name {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #004085 !important;
        margin: 8px 0 !important;
        padding: 12px 18px !important;
        background-color: #cce5ff !important;
        border-radius: 10px !important;
        border-left: 8px solid #007bff !important;
    }
    
    .stMetric label {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    .stMetric div {
        font-size: 28px !important;
        font-weight: bold !important;
    }
    
    .keyboard-hint {
        font-size: 16px !important;
        color: #666;
        background: #f0f0f0;
        padding: 6px 12px;
        border-radius: 4px;
        display: inline-block;
        margin: 2px;
    }
    .enter-hint {
        font-size: 16px !important;
        background: #28a745;
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
    }
    
    h1 {
        font-size: 36px !important;
    }
    </style>
    
    <script>
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            var active = document.activeElement;
            if (active && active.tagName === 'INPUT') {
                var buttons = document.querySelectorAll('button');
                for (var btn of buttons) {
                    if (btn.textContent.includes('Add Bill')) {
                        btn.click();
                        break;
                    }
                }
            }
        }
        if (e.key === 'Escape') {
            var buttons = document.querySelectorAll('button');
            for (var btn of buttons) {
                if (btn.textContent.includes('Refresh')) {
                    btn.click();
                    break;
                }
            }
        }
    });
    </script>
    
    <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 15px; text-align: center; border: 1px solid #ddd;">
        <span class="keyboard-hint">⬆⬇ Arrow Keys</span>
        <span class="keyboard-hint">↹ Tab / Shift+Tab</span>
        <span class="enter-hint">↵ Enter = Add Bill</span>
        <span class="keyboard-hint">⎋ Esc = Refresh</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CALCULATE GROSS & NET
# ============================================================

def calculate_totals(boxes, tp_box, discount):
    gross_total = boxes * tp_box
    discount_amount = gross_total * (discount / 100)
    net_total = gross_total - discount_amount
    return gross_total, discount_amount, net_total

# ============================================================
# MAIN APP
# ============================================================

def main():
    init_session()
    
    st.set_page_config(
        page_title=f"{COMPANY_NAME} - Billing",
        page_icon="🧾",
        layout="wide"
    )
    
    add_keyboard_css()
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a472a 0%, #2d8a4e 100%); 
                padding: 30px; border-radius: 12px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 40px;">{COMPANY_NAME}</h1>
        <p style="color: #ffd700; margin: 8px 0 0 0; font-size: 22px;">🧾 Billing Software 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # BILL INFORMATION
    # ============================================================
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("📌 Bill No:", value=st.session_state.database["next_bill_no"], disabled=True)
    with col2:
        st.text_input("📅 Date:", value=datetime.now().strftime("%d-%m-%Y"), disabled=True)
    
    # ============================================================
    # CUSTOMER INFORMATION
    # ============================================================
    
    shop_name = st.text_input("🏪 Shop:", placeholder="Enter Shop Name", key="shop_input")
    
    if shop_name.strip():
        st.markdown(f"""
        <div class="shop-name">
            🏪 {shop_name}
        </div>
        """, unsafe_allow_html=True)
    
    order_booker = st.text_input("📝 Booker:", placeholder="Enter Order Booker", key="booker_input")
    salesman = st.text_input("👤 Salesman:", placeholder="Enter Salesman", key="salesman_input")
    delivery_man = st.text_input("🚚 Delivery:", placeholder="Enter Delivery Man", key="delivery_input")
    
    st.markdown("---")
    
    # ============================================================
    # PRODUCT SELECTION
    # ============================================================
    
    code = st.text_input("🔢 Code:", placeholder="Product Code", key="code_input")
    
    if code:
        product = next((p for p in PRODUCTS if p["code"] == code), None)
        if product:
            st.session_state.selected_product = product
            st.session_state.tp_box_value = float(product["price"])
            st.markdown(f"""
            <div class="product-name">
                ✅ {product['name']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.session_state.selected_product = None
            st.session_state.tp_box_value = 0.0
            st.markdown("<div style='font-size:22px;color:red;font-weight:bold;padding:15px;'>❌ Product Not Found</div>", unsafe_allow_html=True)
    else:
        st.session_state.selected_product = None
        st.markdown("<div style='font-size:22px;color:red;font-weight:bold;padding:15px;'>⚠️ No Product Selected</div>", unsafe_allow_html=True)
    
    # ============================================================
    # QUANTITY - ONLY BOXES
    # ============================================================
    
    boxes = st.number_input("📦 Boxes:", min_value=0, value=st.session_state.boxes_value, step=1, key="boxes_input")
    st.session_state.boxes_value = boxes
    
    # ============================================================
    # PRICE - ONLY TP/Box
    # ============================================================
    
    tp_box = st.number_input(
        "💰 TP/Box:",
        min_value=0.0,
        value=st.session_state.tp_box_value,
        step=1.0,
        format="%.2f",
        key="tpbox_input"
    )
    
    if tp_box != st.session_state.tp_box_value:
        st.session_state.tp_box_value = tp_box
    
    # ============================================================
    # DISCOUNT
    # ============================================================
    
    discount = st.number_input("🎯 Discount %:", min_value=0.0, max_value=100.0, value=0.0, step=0.5, format="%.1f", key="discount_input")
    
    # ============================================================
    # BILL TOTAL
    # ============================================================
    
    gross_total, discount_amount, net_total = calculate_totals(boxes, tp_box, discount)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Gross Amount", f"₹{gross_total:,.2f}")
    with col2:
        st.metric("📉 Discount", f"₹{discount_amount:,.2f}", delta=f"-{discount}%", delta_color="inverse")
    with col3:
        st.metric("✅ Net Amount", f"₹{net_total:,.2f}")
    
    st.markdown("---")
    
    # ============================================================
    # BUTTONS
    # ============================================================
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add Bill (Enter)", use_container_width=True, type="primary", key="add_btn"):
            if st.session_state.selected_product and boxes > 0:
                bill = {
                    "Bill No": st.session_state.database["next_bill_no"],
                    "Date": datetime.now().strftime("%d-%m-%Y"),
                    "Shop": shop_name,
                    "Order Booker": order_booker,
                    "Salesman": salesman,
                    "Delivery Man": delivery_man,
                    "Code": st.session_state.selected_product["code"],
                    "Product": st.session_state.selected_product["name"],
                    "Boxes": boxes,
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
                
                st.session_state.selected_product = None
                st.session_state.tp_box_value = 0.0
                st.session_state.boxes_value = 0
                st.rerun()
            else:
                st.error("❌ Please select a product and enter quantity")
    
    with col2:
        if st.button("🔄 Refresh (Esc)", use_container_width=True, key="refresh_btn"):
            st.session_state.selected_product = None
            st.session_state.tp_box_value = 0.0
            st.session_state.boxes_value = 0
            st.rerun()
    
    with col3:
        if st.button("📋 Show Bills", use_container_width=True, key="show_bills_btn"):
            if st.session_state.database["bills"]:
                df = pd.DataFrame(st.session_state.database["bills"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No bills found")
    
    # ============================================================
    # EXPORT BUTTONS
    # ============================================================
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Bill (Excel)", use_container_width=True, key="export_bill_btn"):
            if shop_name.strip() == "":
                st.error("❌ Please enter Shop Name first")
            else:
                excel_file = export_bill_excel(shop_name)
                if excel_file:
                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_file,
                        file_name=f"{shop_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(f"❌ No bills found for: {shop_name}")
    
    with col2:
        if st.button("📦 Export Load Form (Excel)", use_container_width=True, key="export_load_btn"):
            if order_booker.strip() == "":
                st.error("❌ Please enter Order Booker name")
            else:
                excel_file = export_load_form_excel(order_booker)
                if excel_file:
                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_file,
                        file_name=f"{order_booker}_Load_Form.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(f"❌ No bills found for: {order_booker}")
    
    with col3:
        if st.button("🗑 Refresh Load Form", use_container_width=True, key="refresh_load_btn"):
            if order_booker.strip() == "":
                st.error("❌ Please enter Order Booker name")
            else:
                new_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"].strip() != order_booker.strip()]
                st.session_state.database["bills"] = new_bills
                save_database()
                st.success(f"✅ Load form cleared for: {order_booker}")
                st.rerun()
    
    # ============================================================
    # FOOTER
    # ============================================================
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 18px;">
        <p>📦 Products: {len(PRODUCTS)} | 🧾 Bills: {len(st.session_state.database['bills'])} | 📌 Next Bill: {st.session_state.database['next_bill_no']}</p>
        <p style="font-size: 16px; margin-top: 5px;">
            ⌨️ Tab: Next Field | Shift+Tab: Previous Field | Enter: Add Bill | Esc: Refresh
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    main()
