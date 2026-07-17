# ============================================================
# AL-BARAKAH ENTERPRISES
# BILLING SOFTWARE 2026 - TABLE DESIGN
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
# PRODUCT LIST (51 Products)
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
    
    # Store selected products with quantities
    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = {}
    
    if 'grand_total' not in st.session_state:
        st.session_state.grand_total = 0

def save_database():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.database, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# ============================================================
# EXCEL EXPORT - SAME FORMAT AS BEFORE
# ============================================================

def export_bill_excel(shop_name, bills_data):
    if not bills_data:
        return None
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Bill")
    
    worksheet.set_paper(9)
    worksheet.set_portrait()
    worksheet.fit_to_pages(1, 1)
    
    worksheet.set_column("A:A", 47.86)
    worksheet.set_column("B:B", 23.71)
    worksheet.set_column("C:C", 12.71)
    worksheet.set_column("D:D", 12.71)
    worksheet.set_column("E:E", 12.71)
    worksheet.set_column("F:F", 12.14)
    worksheet.set_column("G:G", 13.14)
    worksheet.set_column("H:H", 14.14)
    
    title = workbook.add_format({
        "bold": True,
        "font_size": 18,
        "align": "center",
        "border": 2
    })
    
    header = workbook.add_format({
        "bold": True,
        "font_size": 12,
        "bg_color": "#D9EAD3",
        "align": "center",
        "border": 2
    })
    
    cell_left = workbook.add_format({
        "font_size": 14,
        "border": 1,
        "align": "left"
    })
    
    cell_center = workbook.add_format({
        "font_size": 14,
        "border": 1,
        "align": "center"
    })
    
    total = workbook.add_format({
        "bold": True,
        "font_size": 14,
        "bg_color": "#FFF2CC",
        "align": "center",
        "border": 2
    })
    
    worksheet.merge_range("A1:H1", COMPANY_NAME, title)
    
    first_bill = bills_data[0]
    worksheet.write("A3", "Shop Name", header)
    worksheet.write("B3", first_bill["Shop"], cell_center)
    worksheet.write("D3", "Booker", header)
    worksheet.write("E3", first_bill["Order Booker"], cell_center)
    worksheet.write("G3", "Bill No", header)
    worksheet.write("H3", first_bill["Bill No"], cell_center)
    worksheet.write("G4", "Date", header)
    worksheet.write("H4", first_bill["Date"], cell_center)
    
    row = 6
    headers = ["Product", "Code", "Boxes", "TP/Box", "Gross", "Discount %", "Net"]
    
    for col, value in enumerate(headers):
        worksheet.write(row, col, value, header)
    
    row += 1
    
    gross_total = 0
    
    for bill in bills_data:
        worksheet.write(row, 0, bill["Product"], cell_left)
        worksheet.write(row, 1, bill["Code"], cell_center)
        worksheet.write(row, 2, bill["Boxes"], cell_center)
        worksheet.write(row, 3, bill["TP/Box"], cell_center)
        worksheet.write(row, 4, bill["Gross"], cell_center)
        worksheet.write(row, 5, bill["Discount %"], cell_center)
        
        excel_row = row + 1
        worksheet.write_formula(
            row, 6,
            f"=E{excel_row}-(E{excel_row}*F{excel_row}/100)",
            cell_center
        )
        
        gross_total += bill["Gross"]
        row += 1
    
    worksheet.write(row, 2, "TOTAL", total)
    worksheet.write(row, 4, gross_total, total)
    worksheet.write_blank(row, 5, None, total)
    worksheet.write_formula(
        row, 6,
        f"=E{row+1}-(E{row+1}*F{row+1}/100)",
        total
    )
    
    workbook.close()
    output.seek(0)
    return output

def export_load_form_excel(booker, bills_data):
    if not bills_data:
        return None
    
    summary = {}
    for bill in bills_data:
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
    
    title = workbook.add_format({
        "bold": True,
        "font_size": 16,
        "align": "center",
        "border": 2
    })
    
    header = workbook.add_format({
        "bold": True,
        "font_size": 12,
        "bg_color": "#D9EAD3",
        "align": "center",
        "border": 2
    })
    
    cell_left = workbook.add_format({
        "font_size": 14,
        "border": 1,
        "align": "left"
    })
    
    cell_center = workbook.add_format({
        "font_size": 14,
        "border": 1,
        "align": "center"
    })
    
    total = workbook.add_format({
        "bold": True,
        "font_size": 14,
        "bg_color": "#FFF2CC",
        "align": "center",
        "border": 2
    })
    
    worksheet.set_column("A:A", 47.86)
    worksheet.set_column("B:B", 12.71)
    
    worksheet.merge_range("A1:B1", COMPANY_NAME, title)
    
    worksheet.write("A3", "Order Booker", header)
    worksheet.write("B3", booker, cell_center)
    
    worksheet.write("A5", "Product", header)
    worksheet.write("B5", "Boxes", header)
    
    row = 5
    total_boxes = 0
    
    for item in summary.values():
        worksheet.write(row, 0, item["Product"], cell_left)
        worksheet.write(row, 1, item["Boxes"], cell_center)
        total_boxes += item["Boxes"]
        row += 1
    
    worksheet.write(row, 0, "TOTAL", total)
    worksheet.write(row, 1, total_boxes, total)
    
    workbook.close()
    output.seek(0)
    return output

# ============================================================
# CSS
# ============================================================

def add_css():
    st.markdown("""
    <style>
    .stTextInput label, .stNumberInput label {
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    .stTextInput input, .stNumberInput input {
        font-size: 16px !important;
        padding: 8px 12px !important;
        height: 44px !important;
    }
    
    .stButton button {
        font-size: 16px !important;
        padding: 10px 16px !important;
        height: 48px !important;
    }
    
    /* Product table styling */
    .product-table {
        font-size: 14px !important;
    }
    
    .product-table th {
        background-color: #D9EAD3 !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 8px !important;
    }
    
    .product-table td {
        padding: 6px !important;
        border: 1px solid #ddd !important;
    }
    
    .grand-total {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #155724 !important;
        background-color: #d4edda !important;
        padding: 10px !important;
        border-radius: 8px !important;
        text-align: center !important;
    }
    
    .stMetric label {
        font-size: 16px !important;
        font-weight: bold !important;
    }
    .stMetric div {
        font-size: 24px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
    
    add_css()
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a472a 0%, #2d8a4e 100%); 
                padding: 25px; border-radius: 12px; text-align: center;">
        <h1 style="color: white; margin: 0;">{COMPANY_NAME}</h1>
        <p style="color: #ffd700; margin: 5px 0 0 0;">🧾 Billing Software 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # BILL INFORMATION
    # ============================================================
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("📌 Bill No:", value=st.session_state.database["next_bill_no"], disabled=True)
    with col2:
        st.text_input("📅 Date:", value=datetime.now().strftime("%d-%m-%Y"), disabled=True)
    with col3:
        shop_name = st.text_input("🏪 Shop:", placeholder="Enter Shop Name", key="shop_input")
    with col4:
        order_booker = st.text_input("📝 Booker:", placeholder="Enter Order Booker", key="booker_input")
    
    # ============================================================
    # PRODUCT TABLE - NEW DESIGN
    # ============================================================
    
    st.markdown("### 📋 Select Products")
    
    # Create columns for table
    col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1.5, 1.5, 2])
    
    # Headers
    with col1:
        st.markdown("**✅**")
    with col2:
        st.markdown("**Product Name**")
    with col3:
        st.markdown("**Price/Box**")
    with col4:
        st.markdown("**Boxes**")
    with col5:
        st.markdown("**Total**")
    
    st.markdown("---")
    
    # Initialize grand total
    grand_total = 0
    
    # Display each product with checkbox and quantity
    for idx, product in enumerate(PRODUCTS):
        # Create a unique key for each product
        key_prefix = f"p_{product['code']}"
        
        col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1.5, 1.5, 2])
        
        with col1:
            # Checkbox - Green tick when selected
            selected = st.checkbox(
                "", 
                key=f"select_{key_prefix}",
                value=st.session_state.selected_products.get(f"select_{key_prefix}", False)
            )
            st.session_state.selected_products[f"select_{key_prefix}"] = selected
        
        with col2:
            st.markdown(f"{product['name']}")
        
        with col3:
            st.markdown(f"₹{product['price']:.2f}")
        
        with col4:
            if selected:
                boxes = st.number_input(
                    "", 
                    min_value=0, 
                    value=st.session_state.selected_products.get(f"boxes_{key_prefix}", 0),
                    step=1,
                    key=f"boxes_{key_prefix}"
                )
                st.session_state.selected_products[f"boxes_{key_prefix}"] = boxes
            else:
                st.markdown("—")
                st.session_state.selected_products[f"boxes_{key_prefix}"] = 0
        
        with col5:
            if selected:
                total = product['price'] * st.session_state.selected_products.get(f"boxes_{key_prefix}", 0)
                st.markdown(f"**₹{total:,.2f}**")
                grand_total += total
            else:
                st.markdown("₹0.00")
    
    # ============================================================
    # GRAND TOTAL
    # ============================================================
    
    st.markdown("---")
    
    st.markdown(f"""
    <div class="grand-total">
        🧾 Grand Total: ₹{grand_total:,.2f}
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.grand_total = grand_total
    
    # ============================================================
    # DISCOUNT & NET
    # ============================================================
    
    col1, col2, col3 = st.columns(3)
    with col1:
        discount = st.number_input("🎯 Discount %:", min_value=0.0, max_value=100.0, value=0.0, step=0.5, format="%.1f", key="discount_input")
    
    discount_amount = grand_total * (discount / 100)
    net_total = grand_total - discount_amount
    
    with col2:
        st.metric("💰 Gross Amount", f"₹{grand_total:,.2f}")
    with col3:
        st.metric("✅ Net Amount", f"₹{net_total:,.2f}", delta=f"-{discount_amount:,.2f}" if discount > 0 else None)
    
    st.markdown("---")
    
    # ============================================================
    # BUTTONS
    # ============================================================
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add Bill", use_container_width=True, type="primary"):
            # Get selected products with quantities
            selected_items = []
            for idx, product in enumerate(PRODUCTS):
                key_prefix = f"p_{product['code']}"
                if st.session_state.selected_products.get(f"select_{key_prefix}", False):
                    boxes = st.session_state.selected_products.get(f"boxes_{key_prefix}", 0)
                    if boxes > 0:
                        selected_items.append({
                            "code": product["code"],
                            "name": product["name"],
                            "price": product["price"],
                            "boxes": boxes,
                            "total": product["price"] * boxes
                        })
            
            if not selected_items:
                st.error("❌ Please select at least one product with quantity > 0")
            elif shop_name.strip() == "":
                st.error("❌ Please enter Shop Name")
            elif order_booker.strip() == "":
                st.error("❌ Please enter Booker name")
            else:
                # Create bill entries
                for item in selected_items:
                    bill = {
                        "Bill No": st.session_state.database["next_bill_no"],
                        "Date": datetime.now().strftime("%d-%m-%Y"),
                        "Shop": shop_name,
                        "Order Booker": order_booker,
                        "Salesman": "",
                        "Delivery Man": "",
                        "Code": item["code"],
                        "Product": item["name"],
                        "Boxes": item["boxes"],
                        "TP/Box": item["price"],
                        "Discount %": discount,
                        "Gross": item["total"],
                        "Net": item["total"] - (item["total"] * discount / 100)
                    }
                    st.session_state.database["bills"].append(bill)
                
                st.session_state.database["next_bill_no"] += 1
                save_database()
                
                st.success(f"✅ Bill Added Successfully! Bill No: {st.session_state.database['next_bill_no'] - 1}")
                st.balloons()
                
                # Reset selections
                for idx, product in enumerate(PRODUCTS):
                    key_prefix = f"p_{product['code']}"
                    st.session_state.selected_products[f"select_{key_prefix}"] = False
                    st.session_state.selected_products[f"boxes_{key_prefix}"] = 0
                
                st.rerun()
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            for idx, product in enumerate(PRODUCTS):
                key_prefix = f"p_{product['code']}"
                st.session_state.selected_products[f"select_{key_prefix}"] = False
                st.session_state.selected_products[f"boxes_{key_prefix}"] = 0
            st.rerun()
    
    with col3:
        if st.button("📋 Show Bills", use_container_width=True):
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
        if st.button("📄 Export Bill (Excel)", use_container_width=True):
            if shop_name.strip() == "":
                st.error("❌ Please enter Shop Name first")
            else:
                shop_bills = [b for b in st.session_state.database["bills"] if b["Shop"].strip() == shop_name.strip()]
                if shop_bills:
                    excel_file = export_bill_excel(shop_name, shop_bills)
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
        if st.button("📦 Export Load Form (Excel)", use_container_width=True):
            if order_booker.strip() == "":
                st.error("❌ Please enter Order Booker name")
            else:
                booker_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"].strip() == order_booker.strip()]
                if booker_bills:
                    excel_file = export_load_form_excel(order_booker, booker_bills)
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
        if st.button("🗑 Refresh Load Form", use_container_width=True):
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
    <div style="text-align: center; color: #666; font-size: 15px;">
        <p>📦 Products: {len(PRODUCTS)} | 🧾 Bills: {len(st.session_state.database['bills'])} | 📌 Next Bill: {st.session_state.database['next_bill_no']}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    main()
