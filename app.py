
# ============================================================
# AL-BARAKAH ENTERPRISES
# BILLING SOFTWARE 2026 - STREAMLIT VERSION
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
# PRODUCT LIST (1-33)
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

def save_database():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.database, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# ============================================================
# EXCEL EXPORT FUNCTIONS
# ============================================================

def export_bill_excel(shop_name):
    shop_bills = [b for b in st.session_state.database["bills"] if b["Shop"].strip() == shop_name.strip()]
    if not shop_bills:
        return None
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Bill")
    
    # Page Setup
    worksheet.set_paper(9)
    worksheet.set_portrait()
    worksheet.fit_to_pages(1, 1)
    
    worksheet.set_column("A:A", 40)
    worksheet.set_column("B:B", 10)
    worksheet.set_column("C:C", 10)
    worksheet.set_column("D:D", 10)
    worksheet.set_column("E:E", 14)
    worksheet.set_column("F:F", 14)
    worksheet.set_column("G:G", 14)
    worksheet.set_column("H:H", 12)
    worksheet.set_column("I:I", 16)
    
    # Formats
    title = workbook.add_format({"bold": True, "font_size": 18, "align": "center", "border": 2})
    header = workbook.add_format({"bold": True, "bg_color": "#D9EAD3", "align": "center", "border": 2})
    cell = workbook.add_format({"border": 1, "align": "center"})
    total = workbook.add_format({"bold": True, "bg_color": "#FFF2CC", "align": "center", "border": 2})
    
    # Company Header
    worksheet.merge_range("A1:I1", COMPANY_NAME, title)
    
    first_bill = shop_bills[0]
    worksheet.write("A3", "Shop Name", header)
    worksheet.write("B3", first_bill["Shop"], cell)
    worksheet.write("D3", "Order Booker", header)
    worksheet.write("E3", first_bill["Order Booker"], cell)
    worksheet.write("G3", "Bill No", header)
    worksheet.write("H3", first_bill["Bill No"], cell)
    worksheet.write("G4", "Date", header)
    worksheet.write("H4", first_bill["Date"], cell)
    
    # Table Header
    row = 6
    headers = ["Product", "Code", "Cartons", "Boxes", "TP/Carton", "TP/Box", "Gross", "Discount %", "Net"]
    for col, value in enumerate(headers):
        worksheet.write(row, col, value, header)
    row += 1
    
    # Data
    gross_total = 0
    box_total = 0
    for bill in shop_bills:
        worksheet.write(row, 0, bill["Product"], cell)
        worksheet.write(row, 1, bill["Code"], cell)
        worksheet.write(row, 2, bill["Cartons"], cell)
        worksheet.write(row, 3, bill["Boxes"], cell)
        worksheet.write(row, 4, bill["TP/Carton"], cell)
        worksheet.write(row, 5, bill["TP/Box"], cell)
        worksheet.write(row, 6, bill["Gross"], cell)
        worksheet.write(row, 7, bill["Discount %"], cell)
        
        excel_row = row + 1
        worksheet.write_formula(row, 8, f"=G{excel_row}-(G{excel_row}*H{excel_row}/100)", cell)
        
        gross_total += bill["Gross"]
        box_total += bill["Boxes"]
        row += 1
    
    # Total Row
    worksheet.write(row, 2, "TOTAL", total)
    worksheet.write(row, 3, box_total, total)
    worksheet.write(row, 6, gross_total, total)
    worksheet.write_blank(row, 7, None, total)
    worksheet.write_formula(row, 8, f"=G{row+1}-(G{row+1}*H{row+1}/100)", total)
    
    workbook.close()
    output.seek(0)
    return output

def export_load_form_excel(booker):
    booker_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"].strip() == booker.strip()]
    if not booker_bills:
        return None
    
    summary = {}
    for bill in booker_bills:
        code = bill["Code"]
        if code not in summary:
            summary[code] = {"Product": bill["Product"], "Boxes": 0, "Cartons": 0}
        summary[code]["Boxes"] += bill["Boxes"]
        summary[code]["Cartons"] += bill["Cartons"]
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Load Form")
    
    title = workbook.add_format({"bold": True, "font_size": 16, "align": "center", "border": 2})
    header = workbook.add_format({"bold": True, "bg_color": "#D9EAD3", "align": "center", "border": 2})
    cell = workbook.add_format({"border": 1, "align": "center"})
    total = workbook.add_format({"bold": True, "bg_color": "#FFF2CC", "align": "center", "border": 2})
    
    worksheet.set_column("A:A", 40)
    worksheet.set_column("B:B", 12)
    worksheet.set_column("C:C", 12)
    
    worksheet.merge_range("A1:C1", COMPANY_NAME, title)
    worksheet.write("A3", "Order Booker", header)
    worksheet.write("B3", booker, cell)
    worksheet.write("A5", "Product", header)
    worksheet.write("B5", "Boxes", header)
    worksheet.write("C5", "Cartons", header)
    
    row = 5
    total_boxes = 0
    total_cartons = 0
    for item in summary.values():
        worksheet.write(row, 0, item["Product"], cell)
        worksheet.write(row, 1, item["Boxes"], cell)
        worksheet.write(row, 2, item["Cartons"], cell)
        total_boxes += item["Boxes"]
        total_cartons += item["Cartons"]
        row += 1
    
    worksheet.write(row, 0, "TOTAL", total)
    worksheet.write(row, 1, total_boxes, total)
    worksheet.write(row, 2, total_cartons, total)
    
    workbook.close()
    output.seek(0)
    return output

# ============================================================
# MAIN APP
# ============================================================

def main():
    init_session()
    
    st.set_page_config(page_title=f"{COMPANY_NAME} - Billing", page_icon="🧾", layout="wide")
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a472a 0%, #2d8a4e 100%); 
                padding: 25px; border-radius: 12px; text-align: center;">
        <h1 style="color: white; margin: 0;">{COMPANY_NAME}</h1>
        <p style="color: #ffd700; margin: 5px 0 0 0;">🧾 Billing Software 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bill Information
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Bill No:", value=st.session_state.database["next_bill_no"], disabled=True)
    with col2:
        st.text_input("Date:", value=datetime.now().strftime("%d-%m-%Y"), disabled=True)
    
    # Customer Information
    shop_name = st.text_input("Shop:", placeholder="Enter Shop Name")
    order_booker = st.text_input("Booker:", placeholder="Enter Order Booker")
    salesman = st.text_input("Salesman:", placeholder="Enter Salesman")
    delivery_man = st.text_input("Delivery:", placeholder="Enter Delivery Man")
    
    st.markdown("---")
    
    # Product Selection
    code = st.text_input("Code:", placeholder="Product Code")
    
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
    
    # Quantities
    col1, col2 = st.columns(2)
    with col1:
        cartons = st.number_input("Cartons:", min_value=0, value=0, step=1)
    with col2:
        boxes = st.number_input("Boxes:", min_value=0, value=0, step=1)
    
    # Prices (Editable)
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
    
    # Bill Total
    col1, col2, col3 = st.columns(3)
    with col1:
        discount = st.number_input("Discount %:", min_value=0.0, max_value=100.0, value=0.0, step=0.5, format="%.1f")
    
    gross_total = (boxes * tp_box) + (cartons * tp_carton)
    discount_amount = gross_total * (discount / 100)
    net_total = gross_total - discount_amount
    
    with col2:
        st.text_input("Gross:", value=f"₹{gross_total:,.2f}", disabled=True)
    with col3:
        st.text_input("Net:", value=f"₹{net_total:,.2f}", disabled=True)
    
    st.markdown("---")
    
    # Buttons
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
                st.rerun()
            else:
                st.error("❌ Please select a product and enter quantity")
    
    with col3:
        if st.button("🔄 Refresh Bill", use_container_width=True):
            st.rerun()
    
    # Export Buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Bill (Excel)", use_container_width=True):
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
        if st.button("📦 Export Load Form (Excel)", use_container_width=True):
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
        if st.button("🗑 Refresh Load Form", use_container_width=True):
            if order_booker.strip() == "":
                st.error("❌ Please enter Order Booker name")
            else:
                new_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"].strip() != order_booker.strip()]
                st.session_state.database["bills"] = new_bills
                save_database()
                st.success(f"✅ Load form cleared for: {order_booker}")
                st.rerun()
    
    # Show Bills
    st.markdown("---")
    if st.button("📋 Show Bills", use_container_width=True):
        if st.session_state.database["bills"]:
            df = pd.DataFrame(st.session_state.database["bills"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No bills found")
    
    # Footer
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
