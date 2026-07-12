# ============================================================
# AL-BARAKAH ENTERPRISES
# STREAMLIT BILLING SOFTWARE
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
# PRODUCT LIST (Complete 31 Products)
# ============================================================

PRODUCTS = [
    {"code": "1", "name": "OKAY CHOCOLATE VANILLA LAYER CAKE", "price": 215},
    {"code": "2", "name": "OKAY STRAWBERRY VANILLA LAYER CAKE", "price": 215},
    {"code": "3", "name": "MINT GUM CENTER FILLED COATED BUBBLE", "price": 208},
    {"code": "4", "name": "BADAM DELIGHT CANDY BOX", "price": 125},
    {"code": "5", "name": "KHATU APPLE CANDY", "price": 400},
    {"code": "6", "name": "CRISPEE WAFER BANANA", "price": 130},
    {"code": "7", "name": "CRISPEE WAFER ORANGE", "price": 130},
    {"code": "8", "name": "CRISPEE WAFER STRAWBERRY", "price": 130},
    {"code": "9", "name": "MINI CONE STRAWBERRY", "price": 225},
    {"code": "10", "name": "LUSH STAR CHOC. HAZELNUT", "price": 270},
    {"code": "11", "name": "CHOCOLATE CONE WITH PEANUT CHUNKS", "price": 263},
    {"code": "12", "name": "KOKO MASTI CHOCOLATE TUBE", "price": 210},
    {"code": "13", "name": "KIDS JOY EGG CHOCOLATE WITH BISCUIT", "price": 445},
    {"code": "14", "name": "KOKO MASTI STRAWBERRY TUBE", "price": 210},
    {"code": "15", "name": "STRAWBERRY FLAVORED CONE BOX", "price": 208},
    {"code": "16", "name": "KOKO MASTI MILK CREAM TUBE", "price": 210},
    {"code": "17", "name": "CUP CAKE CHOCOLATE", "price": 215},
    {"code": "18", "name": "MELLOW JOY MANGO MARSHMALLOW", "price": 206},
    {"code": "19", "name": "MAX STRAWBERRY 3-D JELLY", "price": 205},
    {"code": "20", "name": "SUPREME SOFT CAKE", "price": 215},
    {"code": "21", "name": "SWISS ROLL CAKE STRAWBERRY", "price": 215},
    {"code": "22", "name": "SWISS ROLL CAKE CHOCOLATE", "price": 215},
    {"code": "23", "name": "O-MILK NATURAL OAT ENERGY", "price": 215},
    {"code": "24", "name": "FISHU BIG CHOCO STICK", "price": 180},
    {"code": "25", "name": "BADAM CONE BOX", "price": 208},
    {"code": "26", "name": "MICKEY POP FRUITY BOX", "price": 137},
    {"code": "27", "name": "KULFI PISTA MILKY LOLLIPOP BOX", "price": 130},
    {"code": "28", "name": "NUT KHAT CHOCOLATE", "price": 130},
    {"code": "29", "name": "CHOCOLATE CONE", "price": 208},
    {"code": "30", "name": "STRAWBERRY CONE", "price": 208},
    {"code": "33", "name": "MAX GUAVA 3-D JELLY", "price": 205}
]

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session():
    """Initialize all session state variables"""
    
    # Database
    if 'database' not in st.session_state:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    st.session_state.database = json.load(f)
            except:
                st.session_state.database = {"next_bill_no": 1, "bills": []}
        else:
            st.session_state.database = {"next_bill_no": 1, "bills": []}
    
    # Product selection
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None
    
    # Code input
    if 'product_code' not in st.session_state:
        st.session_state.product_code = ""

# ============================================================
# SAVE DATABASE
# ============================================================

def save_database():
    """Save database to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.database, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving database: {e}")
        return False

# ============================================================
# MAIN APP
# ============================================================

def main():
    # Initialize session
    init_session()
    
    # ============================================================
    # PAGE CONFIG
    # ============================================================
    
    st.set_page_config(
        page_title=f"{COMPANY_NAME} - Billing",
        page_icon="🧾",
        layout="wide"
    )
    
    # ============================================================
    # HEADER
    # ============================================================
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a472a 0%, #2d8a4e 100%); 
                padding: 25px; 
                border-radius: 12px; 
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="color: white; margin: 0; font-size: 2.5em;">{COMPANY_NAME}</h1>
        <p style="color: #ffd700; margin: 5px 0 0 0; font-size: 1.1em;">
            🧾 Billing Software 2026
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # BILL INFORMATION
    # ============================================================
    
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        st.text_input(
            "📌 Bill No:",
            value=st.session_state.database["next_bill_no"],
            disabled=True,
            key="bill_no_display"
        )
    
    with col2:
        st.text_input(
            "📅 Date:",
            value=datetime.now().strftime("%d-%m-%Y"),
            disabled=True,
            key="date_display"
        )
    
    with col3:
        total_bills = len(st.session_state.database["bills"])
        st.metric("📊 Total Bills", total_bills)
    
    # ============================================================
    # CUSTOMER INFORMATION
    # ============================================================
    
    with st.expander("📋 Customer Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            shop_name = st.text_input(
                "🏪 Shop Name:",
                placeholder="Enter Shop Name",
                key="shop_name"
            )
            
            salesman = st.text_input(
                "👤 Salesman:",
                placeholder="Enter Salesman",
                key="salesman"
            )
        
        with col2:
            order_booker = st.text_input(
                "📝 Order Booker:",
                placeholder="Enter Order Booker",
                key="order_booker"
            )
            
            delivery_man = st.text_input(
                "🚚 Delivery Man:",
                placeholder="Enter Delivery Man",
                key="delivery_man"
            )
    
    st.markdown("---")
    
    # ============================================================
    # PRODUCT SELECTION
    # ============================================================
    
    st.subheader("🛍️ Product Selection")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Product Code Input
        code = st.text_input(
            "🔢 Product Code:",
            placeholder="Enter Code (1-33)",
            key="code_input",
            value=st.session_state.product_code
        )
        
        # Auto-find product when code changes
        if code:
            product = next((p for p in PRODUCTS if p["code"] == code), None)
            if product:
                st.session_state.selected_product = product
                st.success(f"✅ Found: {product['name']}")
            else:
                st.session_state.selected_product = None
                st.error("❌ Product Not Found")
        else:
            st.session_state.selected_product = None
            st.info("💡 Enter product code")
    
    with col2:
        if st.session_state.selected_product:
            product = st.session_state.selected_product
            st.markdown(f"""
            <div style="background-color: #d4edda; 
                        padding: 18px; 
                        border-radius: 8px; 
                        border-left: 6px solid #28a745;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <h4 style="color: #155724; margin: 0;">{product['name']}</h4>
                <p style="margin: 8px 0 0 0; color: #155724;">
                    💰 Price: <strong>₹{product['price']:,.2f}</strong> per box
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #f8d7da; 
                        padding: 18px; 
                        border-radius: 8px; 
                        border-left: 6px solid #dc3545;">
                <h4 style="color: #721c24; margin: 0;">⚠️ No Product Selected</h4>
                <p style="margin: 5px 0 0 0; color: #721c24;">
                    Please enter a valid product code
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================================
    # QUANTITIES
    # ============================================================
    
    st.subheader("📦 Quantities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cartons = st.number_input(
            "📦 Cartons:",
            min_value=0,
            value=0,
            step=1,
            key="cartons",
            help="Number of cartons (12 boxes per carton)"
        )
    
    with col2:
        boxes = st.number_input(
            "📦 Boxes:",
            min_value=0,
            value=0,
            step=1,
            key="boxes",
            help="Number of individual boxes"
        )
    
    # ============================================================
    # PRICES (Editable)
    # ============================================================
    
    st.subheader("💰 Price Details")
    
    # Auto-populate price if product selected
    default_tp_box = 0.0
    default_tp_carton = 0.0
    
    if st.session_state.selected_product:
        default_tp_box = float(st.session_state.selected_product['price'])
        default_tp_carton = default_tp_box * 12
    
    col1, col2 = st.columns(2)
    
    with col1:
        tp_carton = st.number_input(
            "💵 TP/Carton:",
            min_value=0.0,
            value=default_tp_carton,
            step=1.0,
            key="tp_carton",
            format="%.2f",
            help="Total Price per Carton (12 boxes)"
        )
    
    with col2:
        tp_box = st.number_input(
            "💵 TP/Box:",
            min_value=0.0,
            value=default_tp_box,
            step=1.0,
            key="tp_box",
            format="%.2f",
            help="Total Price per Box"
        )
    
    # ============================================================
    # CALCULATIONS
    # ============================================================
    
    st.subheader("🧮 Bill Summary")
    
    # Calculate totals
    gross_total = (boxes * tp_box) + (cartons * tp_carton)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        discount_percent = st.number_input(
            "🎯 Discount %:",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.5,
            key="discount",
            format="%.1f"
        )
    
    discount_amount = gross_total * (discount_percent / 100)
    net_total = gross_total - discount_amount
    
    with col2:
        st.metric(
            "💰 Gross Amount",
            f"₹{gross_total:,.2f}",
            delta=None,
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "📉 Discount",
            f"₹{discount_amount:,.2f}",
            delta=f"-{discount_percent}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "✅ Net Amount",
            f"₹{net_total:,.2f}",
            delta=None,
            delta_color="normal"
        )
    
    # ============================================================
    # ACTION BUTTONS
    # ============================================================
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🧮 Calculate", use_container_width=True, type="secondary"):
            st.success("✅ Calculation Completed")
            st.balloons()
    
    with col2:
        if st.button("➕ Add Bill", use_container_width=True, type="primary"):
            if st.session_state.selected_product and (cartons > 0 or boxes > 0):
                # Create bill
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
                    "Discount %": discount_percent,
                    "Gross": gross_total,
                    "Net": net_total
                }
                
                # Save to database
                st.session_state.database["bills"].append(bill)
                st.session_state.database["next_bill_no"] += 1
                
                if save_database():
                    st.success(f"✅ Bill Added Successfully! Bill No: {bill['Bill No']}")
                    st.balloons()
                    
                    # Reset product fields
                    st.session_state.selected_product = None
                    st.session_state.product_code = ""
                    st.rerun()
                else:
                    st.error("❌ Failed to save bill")
            else:
                st.error("❌ Please select a product and enter quantity")
    
    with col3:
        if st.button("🔄 Refresh Bill", use_container_width=True):
            st.session_state.selected_product = None
            st.session_state.product_code = ""
            st.rerun()
            st.success("✅ Refreshed")
    
    with col4:
        if st.button("📋 Show Bills", use_container_width=True):
            if st.session_state.database["bills"]:
                df = pd.DataFrame(st.session_state.database["bills"])
                st.dataframe(df, use_container_width=True, height=400)
            else:
                st.info("📭 No bills found")
    
    # ============================================================
    # EXPORT OPTIONS
    # ============================================================
    
    st.markdown("---")
    st.subheader("📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export All Bills", use_container_width=True):
            if st.session_state.database["bills"]:
                df = pd.DataFrame(st.session_state.database["bills"])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"bills_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.error("❌ No bills to export")
    
    with col2:
        if st.button("📦 Export Load Form", use_container_width=True):
            if order_booker:
                booker_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"] == order_booker]
                if booker_bills:
                    # Create summary
                    summary = {}
                    for bill in booker_bills:
                        code = bill["Code"]
                        if code not in summary:
                            summary[code] = {
                                "Product": bill["Product"],
                                "Boxes": 0,
                                "Cartons": 0
                            }
                        summary[code]["Boxes"] += bill["Boxes"]
                        summary[code]["Cartons"] += bill["Cartons"]
                    
                    df = pd.DataFrame([{
                        "Product": v["Product"],
                        "Boxes": v["Boxes"],
                        "Cartons": v["Cartons"]
                    } for v in summary.values()])
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Load Form",
                        data=csv,
                        file_name=f"{order_booker}_Load_Form_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.error(f"❌ No bills found for: {order_booker}")
            else:
                st.error("❌ Please enter Order Booker name")
    
    with col3:
        if st.button("🗑 Clear Load Form", use_container_width=True, type="secondary"):
            if order_booker:
                # Delete only current booker's bills
                new_bills = [b for b in st.session_state.database["bills"] if b["Order Booker"] != order_booker]
                st.session_state.database["bills"] = new_bills
                if save_database():
                    st.success(f"✅ Cleared all bills for: {order_booker}")
                    st.rerun()
                else:
                    st.error("❌ Failed to clear")
            else:
                st.error("❌ Please enter Order Booker name")
    
    # ============================================================
    # FOOTER - Database Stats
    # ============================================================
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Products", len(PRODUCTS))
    
    with col2:
        st.metric("🧾 Total Bills", len(st.session_state.database["bills"]))
    
    with col3:
        st.metric("📌 Next Bill No", st.session_state.database["next_bill_no"])
    
    with col4:
        if st.session_state.database["bills"]:
            last_bill = st.session_state.database["bills"][-1]
            st.metric("🕐 Last Bill", last_bill.get("Date", "N/A"))
        else:
            st.metric("🕐 Last Bill", "No bills yet")

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    main()
