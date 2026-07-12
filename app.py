 ============================================================
# AL-BARAKAH ENTERPRISES
# BILLING SOFTWARE 2026
# PART 1A-1
# ============================================================

# Install Required Libraries
!pip -q install openpyxl xlsxwriter ipywidgets pandas

# ============================================================
# IMPORT LIBRARIES
# ============================================================

import os
import json
import pandas as pd

from datetime import datetime

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

from google.colab import files

# ============================================================
# COMPANY INFORMATION
# ============================================================

COMPANY_NAME = "AL-BARAKAH ENTERPRISES"

DATA_FILE = "billing_database.json"

# ============================================================
# PRODUCT LIST (1-17)
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
# DATABASE
# ============================================================

database = {
    "next_bill_no": 1,
    "bills": []
}

# ============================================================
# SAVE DATABASE
# ============================================================

def save_database():

    with open(DATA_FILE, "w") as f:
        json.dump(database, f, indent=4)

# ============================================================
# LOAD DATABASE
# ============================================================

def load_database():

    global database

    if os.path.exists(DATA_FILE):

        with open(DATA_FILE, "r") as f:
            database = json.load(f)

    else:

        save_database()

load_database()

# ============================================================
# DATAFRAME
# ============================================================

products_df = pd.DataFrame(PRODUCTS)

# ============================================================
# GLOBAL VARIABLES
# ============================================================

selected_product = None

current_bill = []

# ============================================================
# SOFTWARE STARTUP
# ============================================================

print("=" * 60)
print(COMPANY_NAME)
print("Billing Software 2026 Ready")
print("Products :", len(PRODUCTS))
print("Saved Bills :", len(database["bills"]))
print("Next Bill No :", database["next_bill_no"])
print("=" * 60)
 ============================================================
# PART 1B
# CREATE ALL WIDGETS
# ============================================================

display(HTML(f"""
<h2 style="color:green;">
{COMPANY_NAME}
</h2>
"""))

# ============================================================
# BILL INFORMATION
# ============================================================

bill_no = widgets.IntText(
    value=database["next_bill_no"],
    description="Bill No:",
    disabled=True,
    layout=widgets.Layout(width="220px")
)

bill_date = widgets.Text(
    value=datetime.now().strftime("%d-%m-%Y"),
    description="Date:",
    disabled=True,
    layout=widgets.Layout(width="220px")
)

# ============================================================
# CUSTOMER INFORMATION
# ============================================================

shop_name = widgets.Text(
    description="Shop:",
    placeholder="Enter Shop Name",
    layout=widgets.Layout(width="500px")
)

order_booker = widgets.Text(
    description="Booker:",
    placeholder="Enter Order Booker",
    layout=widgets.Layout(width="500px")
)

salesman = widgets.Text(
    description="Salesman:",
    placeholder="Enter Salesman",
    layout=widgets.Layout(width="500px")
)

delivery_man = widgets.Text(
    description="Delivery:",
    placeholder="Enter Delivery Man",
    layout=widgets.Layout(width="500px")
)

# ============================================================
# PRODUCT INFORMATION
# ============================================================

code_input = widgets.Text(
    description="Code:",
    placeholder="Product Code",
    layout=widgets.Layout(width="220px")
)

product_name = widgets.HTML(
    value="<b style='color:red;'>No Product Selected</b>"
)

cartons = widgets.IntText(
    value=0,
    description="Cartons:",
    layout=widgets.Layout(width="220px")
)

boxes = widgets.IntText(
    value=0,
    description="Boxes:",
    layout=widgets.Layout(width="220px")
)

# ============================================================
# PRICE (EDITABLE)
# ============================================================

tp_carton = widgets.FloatText(
    value=0,
    description="TP/Carton:",
    disabled=False,
    layout=widgets.Layout(width="220px")
)

tp_box = widgets.FloatText(
    value=0,
    description="TP/Box:",
    disabled=False,
    layout=widgets.Layout(width="220px")
)

# ============================================================
# BILL TOTAL
# ============================================================

discount = widgets.FloatText(
    value=0,
    description="Discount %:",
    layout=widgets.Layout(width="220px")
)

gross = widgets.FloatText(
    value=0,
    description="Gross:",
    disabled=True,
    layout=widgets.Layout(width="220px")
)

net = widgets.FloatText(
    value=0,
    description="Net:",
    disabled=True,
    layout=widgets.Layout(width="220px")
)

# ============================================================
# BUTTONS
# ============================================================

btn_calculate = widgets.Button(
    description="🧮 Calculate",
    button_style="warning"
)

btn_add = widgets.Button(
    description="➕ Add Bill",
    button_style="success"
)

btn_refresh = widgets.Button(
    description="🔄 Refresh Bill",
    button_style="danger"
)

btn_export = widgets.Button(
    description="📄 Export Bill",
    button_style="info"
)

btn_load = widgets.Button(
    description="📦 Export Load Form",
    button_style="primary"
)

btn_load_refresh = widgets.Button(
    description="🗑 Refresh Load Form",
    button_style="danger"
)

# ============================================================
# OUTPUT
# ============================================================

bill_output = widgets.Output()

print("✅ PART 1B COMPLETE")
# ============================================================
# PART 2A
# DISPLAY BILLING FORM
# ============================================================

display(widgets.HBox([bill_no, bill_date]))

display(shop_name)
display(order_booker)
display(salesman)
display(delivery_man)

display(HTML("<hr>"))

display(code_input)
display(product_name)

display(widgets.HBox([
    cartons,
    boxes
]))

display(widgets.HBox([
    tp_carton,
    tp_box
]))

display(widgets.HBox([
    discount,
    gross,
    net
]))

display(HTML("<br>"))

display(widgets.HBox([
    btn_calculate,
    btn_add,
    btn_refresh
]))

display(widgets.HBox([
    btn_export,
    btn_load,
    btn_load_refresh
]))

display(HTML("<hr>"))

display(bill_output)

print("✅ PART 2A COMPLETE")
# ============================================================
# PART 2B
# PRODUCT SEARCH + CALCULATION
# ============================================================

selected_product = None

# ------------------------------------------------------------
# FIND PRODUCT
# ------------------------------------------------------------

def find_product(change=None):

    global selected_product

    code = code_input.value.strip()

    selected_product = None

    for product in PRODUCTS:

        if product["code"] == code:

            selected_product = product

            product_name.value = f"""
            <h4 style='color:green;margin:0'>
            {product['name']}
            </h4>
            """

            # Auto Prices (Editable)
            tp_box.value = float(product["price"])
            tp_carton.value = float(product["price"] * 12)

            calculate_total()

            return

    product_name.value = "<b style='color:red;'>Product Not Found</b>"

    tp_box.value = 0
    tp_carton.value = 0
    gross.value = 0
    net.value = 0


code_input.observe(find_product, names="value")


# ------------------------------------------------------------
# CALCULATE TOTAL
# ------------------------------------------------------------

def calculate_total(change=None):

    # Box Total
    box_total = boxes.value * tp_box.value

    # Carton Total
    carton_total = cartons.value * tp_carton.value

    gross_total = box_total + carton_total

    gross.value = gross_total

    discount_amount = gross_total * (discount.value / 100)

    net.value = gross_total - discount_amount


# Auto Calculate
boxes.observe(calculate_total, names="value")
cartons.observe(calculate_total, names="value")
tp_box.observe(calculate_total, names="value")
tp_carton.observe(calculate_total, names="value")
discount.observe(calculate_total, names="value")


# ------------------------------------------------------------
# CALCULATE BUTTON
# ------------------------------------------------------------

def calculate_bill(btn):

    calculate_total()

    with bill_output:

        bill_output.clear_output()

        print("✅ Calculation Completed")


try:
    btn_calculate._click_handlers.callbacks.clear()
except:
    pass

btn_calculate.on_click(calculate_bill)

print("✅ PART 2B COMPLETE")
 ============================================================
# PART 3A
# ADD BILL
# ============================================================

def add_bill(btn=None):

    global selected_product

    # ------------------------------------
    # CHECK PRODUCT
    # ------------------------------------

    if selected_product is None:

        with bill_output:
            bill_output.clear_output()
            print("❌ Please Select Product")

        return

    # ------------------------------------
    # CHECK QUANTITY
    # ------------------------------------

    if cartons.value <= 0 and boxes.value <= 0:

        with bill_output:
            bill_output.clear_output()
            print("❌ Enter Boxes or Cartons")

        return

    # ------------------------------------
    # CREATE BILL
    # ------------------------------------

    bill = {

        "Bill No": bill_no.value,

        "Date": bill_date.value,

        "Shop": shop_name.value.strip(),

        "Order Booker": order_booker.value.strip(),

        "Salesman": salesman.value.strip(),

        "Delivery Man": delivery_man.value.strip(),

        "Code": selected_product["code"],

        "Product": selected_product["name"],

        "Cartons": cartons.value,

        "Boxes": boxes.value,

        "TP/Carton": tp_carton.value,

        "TP/Box": tp_box.value,

        "Discount %": discount.value,

        "Gross": gross.value,

        "Net": net.value

    }

    # ------------------------------------
    # SAVE
    # ------------------------------------

    database["bills"].append(bill)

    database["next_bill_no"] += 1

    save_database()

    # ------------------------------------
    # NEXT BILL
    # ------------------------------------

    bill_no.value = database["next_bill_no"]

    # ------------------------------------
    # CLEAR PRODUCT FIELDS
    # ------------------------------------

    selected_product = None

    code_input.value = ""

    product_name.value = "<b style='color:red;'>No Product Selected</b>"

    cartons.value = 0
    boxes.value = 0

    tp_carton.value = 0
    tp_box.value = 0

    discount.value = 0

    gross.value = 0
    net.value = 0

    # ------------------------------------
    # SUCCESS MESSAGE
    # ------------------------------------

    with bill_output:

        bill_output.clear_output()

        print("✅ Bill Added Successfully")

        print("Bill No :", bill_no.value - 1)

        print("Total Bills :", len(database["bills"]))


# ============================================================
# CONNECT BUTTON
# ============================================================

try:
    btn_add._click_handlers.callbacks.clear()
except:
    pass

btn_add.on_click(add_bill)

print("✅ PART 3A COMPLETE")
# ============================================================
# PART 3B
# REFRESH BILL + SHOW BILLS
# ============================================================

def refresh_bill(btn=None):

    global selected_product

    selected_product = None

    # ---------------------------------------
    # CLEAR PRODUCT FIELDS
    # ---------------------------------------

    code_input.value = ""

    product_name.value = "<b style='color:red;'>No Product Selected</b>"

    cartons.value = 0
    boxes.value = 0

    tp_carton.value = 0
    tp_box.value = 0

    discount.value = 0

    gross.value = 0

    net.value = 0

    with bill_output:

        bill_output.clear_output()

        print("✅ Ready For Next Product")


# ============================================================
# SHOW ALL BILLS
# ============================================================

def show_bills(btn=None):

    with bill_output:

        bill_output.clear_output()

        if len(database["bills"]) == 0:

            print("❌ No Bills Found")

            return

        df = pd.DataFrame(database["bills"])

        display(df)


# ============================================================
# SHOW BILL BUTTON
# ============================================================

btn_show = widgets.Button(

    description="📋 Show Bills",

    button_style="primary"

)

btn_show.on_click(show_bills)


# ============================================================
# CONNECT REFRESH BUTTON
# ============================================================

try:
    btn_refresh._click_handlers.callbacks.clear()
except:
    pass

btn_refresh.on_click(refresh_bill)


# ============================================================
# DISPLAY SHOW BUTTON
# ============================================================

display(btn_show)

print("✅ PART 3B COMPLETE")
 ============================================================
# PART 4A-1
# EXPORT BILL (FORMAT)
# ============================================================

import xlsxwriter

def export_bill(btn=None):

    if len(database["bills"]) == 0:

        with bill_output:
            bill_output.clear_output()
            print("❌ No Bills Found")
        return

    # ----------------------------------------
    # FILE NAME
    # ----------------------------------------

    shop = shop_name.value.strip()

    if shop == "":
        shop = "Bill"

    invalid = ['\\','/',':','*','?','"','<','>','|']

    for ch in invalid:
        shop = shop.replace(ch,"")

    file_name = f"{shop}.xlsx"

    writer = pd.ExcelWriter(file_name, engine="xlsxwriter")

    workbook = writer.book

    worksheet = workbook.add_worksheet("Bill")

    writer.sheets["Bill"] = worksheet

    # ----------------------------------------
    # PAGE SETUP
    # ----------------------------------------

    worksheet.set_paper(9)
    worksheet.set_portrait()
    worksheet.fit_to_pages(1,1)

    worksheet.set_column("A:A",40)
    worksheet.set_column("B:B",10)
    worksheet.set_column("C:C",10)
    worksheet.set_column("D:D",10)
    worksheet.set_column("E:E",14)
    worksheet.set_column("F:F",14)
    worksheet.set_column("G:G",14)
    worksheet.set_column("H:H",12)
    worksheet.set_column("I:I",16)

    # ----------------------------------------
    # FORMATS
    # ----------------------------------------

    title = workbook.add_format({
        "bold":True,
        "font_size":18,
        "align":"center",
        "border":2
    })

    header = workbook.add_format({
        "bold":True,
        "bg_color":"#D9EAD3",
        "align":"center",
        "border":2
    })

    cell = workbook.add_format({
        "border":1,
        "align":"center"
    })

    total = workbook.add_format({
        "bold":True,
        "bg_color":"#FFF2CC",
        "align":"center",
        "border":2
    })

    # ----------------------------------------
    # COMPANY
    # ----------------------------------------

    worksheet.merge_range("A1:I1", COMPANY_NAME, title)

    worksheet.write("A3","Shop Name",header)
    worksheet.write("B3",shop_name.value,cell)

    worksheet.write("D3","Order Booker",header)
    worksheet.write("E3",order_booker.value,cell)

    worksheet.write("G3","Bill No",header)
    worksheet.write("H3",bill_no.value-1,cell)

    worksheet.write("G4","Date",header)
    worksheet.write("H4",bill_date.value,cell)

    # ----------------------------------------
    # TABLE HEADER
    # ----------------------------------------

    row = 6

    headers = [

        "Product",

        "Code",

        "Cartons",

        "Boxes",

        "TP/Carton",

        "TP/Box",

        "Gross",

        "Discount %",

        "Net"

    ]

    for col, value in enumerate(headers):

        worksheet.write(row,col,value,header)

    row += 1

    gross_total = 0
    net_total = 0
    box_total = 0
        # ----------------------------------------
    # WRITE BILL DATA
    # ----------------------------------------

    for bill in database["bills"]:

        # Sirf isi Shop ke bills export karo
        if bill["Shop"].strip() != shop_name.value.strip():
            continue

        worksheet.write(row, 0, bill["Product"], cell)
        worksheet.write(row, 1, bill["Code"], cell)
        worksheet.write(row, 2, bill["Cartons"], cell)
        worksheet.write(row, 3, bill["Boxes"], cell)
        worksheet.write(row, 4, bill["TP/Carton"], cell)
        worksheet.write(row, 5, bill["TP/Box"], cell)
        worksheet.write(row, 6, bill["Gross"], cell)
        worksheet.write(row, 7, bill["Discount %"], cell)

        # Net = Gross - Discount %
        excel_row = row + 1

        worksheet.write_formula(
            row,
            8,
            f"=G{excel_row}-(G{excel_row}*H{excel_row}/100)",
            cell
        )

        gross_total += bill["Gross"]
        net_total += bill["Net"]
        box_total += bill["Boxes"]

        row += 1

    # ----------------------------------------
    # TOTAL ROW
    # ----------------------------------------

    worksheet.write(row, 2, "TOTAL", total)

    worksheet.write(row, 3, box_total, total)

    worksheet.write(row, 6, gross_total, total)

    worksheet.write_blank(row, 7, None, total)

    worksheet.write_formula(
        row,
        8,
        f"=G{row+1}-(G{row+1}*H{row+1}/100)",
        total
    )

    # ----------------------------------------
    # SAVE FILE
    # ----------------------------------------

    writer.close()

    files.download(file_name)

    with bill_output:

        bill_output.clear_output()

        print("✅ Bill Exported Successfully")

        print("📄 File :", file_name)


# ============================================================
# CONNECT EXPORT BUTTON
# ============================================================

try:
    btn_export._click_handlers.callbacks.clear()
except:
    pass

btn_export.on_click(export_bill)

print("✅ PART 4A COMPLETE")
# ============================================================
# PART 4B
# EXPORT LOAD FORM
# ============================================================

import xlsxwriter

def export_load_form(btn=None):

    booker = order_booker.value.strip()

    if booker == "":

        with bill_output:
            bill_output.clear_output()
            print("❌ Please Enter Order Booker")

        return

    # --------------------------------------------
    # SUMMARY
    # --------------------------------------------

    summary = {}

    for bill in database["bills"]:

        if bill["Order Booker"].strip() != booker:
            continue

        code = bill["Code"]

        if code not in summary:

            summary[code] = {

                "Product": bill["Product"],

                "Boxes": 0,

                "Cartons": 0

            }

        summary[code]["Boxes"] += bill["Boxes"]

        summary[code]["Cartons"] += bill["Cartons"]

    if len(summary) == 0:

        with bill_output:
            bill_output.clear_output()
            print("❌ No Bills Found")

        return

    # --------------------------------------------
    # FILE
    # --------------------------------------------

    file_name = f"{booker}_Load_Form.xlsx"

    writer = pd.ExcelWriter(file_name, engine="xlsxwriter")

    workbook = writer.book

    worksheet = workbook.add_worksheet("Load Form")

    writer.sheets["Load Form"] = worksheet

    # --------------------------------------------
    # FORMATS
    # --------------------------------------------

    title = workbook.add_format({

        "bold":True,

        "font_size":16,

        "align":"center",

        "border":2

    })

    header = workbook.add_format({

        "bold":True,

        "bg_color":"#D9EAD3",

        "align":"center",

        "border":2

    })

    cell = workbook.add_format({

        "border":1,

        "align":"center"

    })

    total = workbook.add_format({

        "bold":True,

        "bg_color":"#FFF2CC",

        "align":"center",

        "border":2

    })

    worksheet.set_column("A:A",40)
    worksheet.set_column("B:B",12)
    worksheet.set_column("C:C",12)

    worksheet.merge_range("A1:C1", COMPANY_NAME, title)

    worksheet.write("A3","Order Booker",header)
    worksheet.write("B3",booker,cell)

    worksheet.write("A5","Product",header)
    worksheet.write("B5","Boxes",header)
    worksheet.write("C5","Cartons",header)

    row = 5

    total_boxes = 0
    total_cartons = 0

    for item in summary.values():

        worksheet.write(row,0,item["Product"],cell)
        worksheet.write(row,1,item["Boxes"],cell)
        worksheet.write(row,2,item["Cartons"],cell)

        total_boxes += item["Boxes"]
        total_cartons += item["Cartons"]

        row += 1

    worksheet.write(row,0,"TOTAL",total)
    worksheet.write(row,1,total_boxes,total)
    worksheet.write(row,2,total_cartons,total)

    writer.close()

    files.download(file_name)

    with bill_output:

        bill_output.clear_output()

        print("✅ Load Form Exported Successfully")

        print(file_name)


# ============================================================
# CONNECT BUTTON
# ============================================================

try:
    btn_load._click_handlers.callbacks.clear()
except:
    pass

btn_load.on_click(export_load_form)

print("✅ PART 4B COMPLETE")
# ============================================================
# PART 5
# REFRESH LOAD FORM
# ============================================================

def refresh_load_form(btn=None):

    global selected_product

    booker = order_booker.value.strip()

    if booker == "":

        with bill_output:
            bill_output.clear_output()
            print("❌ Please Enter Order Booker")

        return

    # -----------------------------------------
    # DELETE ONLY CURRENT BOOKER DATA
    # -----------------------------------------

    new_bills = []

    for bill in database["bills"]:

        if bill["Order Booker"].strip() != booker:

            new_bills.append(bill)

    database["bills"] = new_bills

    save_database()

    # -----------------------------------------
    # RESET PRODUCT SECTION
    # -----------------------------------------

    selected_product = None

    code_input.value = ""

    product_name.value = "<b style='color:red;'>No Product Selected</b>"

    cartons.value = 0
    boxes.value = 0

    tp_carton.value = 0
    tp_box.value = 0

    discount.value = 0

    gross.value = 0
    net.value = 0

    with bill_output:

        bill_output.clear_output()

        print("✅ Load Form Cleared Successfully")

        print("Order Booker :", booker)


# ============================================================
# CONNECT BUTTON
# ============================================================

try:
    btn_load_refresh._click_handlers.callbacks.clear()
except:
    pass

btn_load_refresh.on_click(refresh_load_form)

print("✅ PART 5 COMPLETE")
# ============================================================
# PART 6
# FINAL STARTUP
# ============================================================

# -----------------------------------------
# REMOVE DUPLICATE BUTTON EVENTS
# -----------------------------------------

buttons = [
    btn_calculate,
    btn_add,
    btn_refresh,
    btn_export,
    btn_load,
    btn_load_refresh
]

for button in buttons:

    try:
        # Existing callbacks ko clear karein (agar support ho)
        button._click_handlers.callbacks = button._click_handlers.callbacks[-1:]
    except Exception:
        pass

# -----------------------------------------
# SOFTWARE READY
# -----------------------------------------

with bill_output:

    bill_output.clear_output()

    print("=" * 60)
    print(" AL-BARAKAH ENTERPRISES ")
    print("=" * 60)
    print("✅ Billing Software Loaded Successfully")
    print()
    print(f"Products      : {len(PRODUCTS)}")
    print(f"Saved Bills   : {len(database['bills'])}")
    print(f"Next Bill No  : {database['next_bill_no']}")
    print()
    print("Features:")
    print("✔ Bill Entry")
    print("✔ Editable TP/Box")
    print("✔ Editable TP/Carton")
    print("✔ Discount %")
    print("✔ Excel Export")
    print("✔ Shop Name File")
    print("✔ Load Form Export")
    print("✔ Booker Wise Summary")
    print("✔ Refresh Bill")
    print("✔ Refresh Load Form")
    print("=" * 60)

print("✅ SOFTWARE IS READY")
