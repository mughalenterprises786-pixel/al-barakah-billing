# ============================================================
# EXCEL EXPORT - WITH FONT SIZE 14 & LEFT ALIGNMENT
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
    # COLUMN WIDTHS - AS REQUESTED
    # ============================================================
    
    worksheet.set_column("A:A", 47.86)  # Product
    worksheet.set_column("B:B", 23.71)  # Shop Name / Code
    worksheet.set_column("C:C", 12.71)  # Boxes
    worksheet.set_column("D:D", 12.71)  # TP/Box
    worksheet.set_column("E:E", 12.71)  # Gross
    worksheet.set_column("F:F", 12.14)  # Discount %
    worksheet.set_column("G:G", 13.14)  # Net
    worksheet.set_column("H:H", 14.14)  # Date
    
    # ============================================================
    # FORMATS
    # ============================================================
    
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
    
    # ============================================================
    # NEW CELL FORMAT: Font 14, Left Aligned
    # ============================================================
    
    cell_left = workbook.add_format({
        "font_size": 14,          # Font size 14
        "border": 1,
        "align": "left"           # Left alignment
    })
    
    # Center format for numbers (Code, Boxes, TP/Box, Gross, Discount %, Net)
    cell_center = workbook.add_format({
        "font_size": 14,          # Font size 14
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
    
    # ============================================================
    # COMPANY HEADER
    # ============================================================
    
    worksheet.merge_range("A1:H1", COMPANY_NAME, title)
    
    # ============================================================
    # BILL INFO
    # ============================================================
    
    first_bill = shop_bills[0]
    
    worksheet.write("A3", "Shop Name", header)
    worksheet.write("B3", first_bill["Shop"], cell_center)  # Center alignment for Shop Name
    
    worksheet.write("D3", "Booker", header)
    worksheet.write("E3", first_bill["Order Booker"], cell_center)
    
    worksheet.write("G3", "Bill No", header)
    worksheet.write("H3", first_bill["Bill No"], cell_center)
    
    worksheet.write("G4", "Date", header)
    worksheet.write("H4", first_bill["Date"], cell_center)
    
    # ============================================================
    # TABLE HEADER
    # ============================================================
    
    row = 6
    
    headers = ["Product", "Code", "Boxes", "TP/Box", "Gross", "Discount %", "Net"]
    
    for col, value in enumerate(headers):
        worksheet.write(row, col, value, header)
    
    row += 1
    
    # ============================================================
    # WRITE BILL DATA: Products LEFT aligned, Numbers CENTER aligned
    # ============================================================
    
    gross_total = 0
    
    for bill in shop_bills:
        # Product Name - LEFT aligned with Font 14
        worksheet.write(row, 0, bill["Product"], cell_left)
        
        # All other fields - CENTER aligned with Font 14
        worksheet.write(row, 1, bill["Code"], cell_center)
        worksheet.write(row, 2, bill["Boxes"], cell_center)
        worksheet.write(row, 3, bill["TP/Box"], cell_center)
        worksheet.write(row, 4, bill["Gross"], cell_center)
        worksheet.write(row, 5, bill["Discount %"], cell_center)
        
        # Net = Gross - Discount % (Excel Formula)
        excel_row = row + 1
        worksheet.write_formula(
            row, 6,
            f"=E{excel_row}-(E{excel_row}*F{excel_row}/100)",
            cell_center
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
