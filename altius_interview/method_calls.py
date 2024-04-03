from models import InvoiceHeader,InvoiceItem,InvoiceSundry,db

# def validate_invoice(invoice):
#     try:
        
# #         Validations for InvoiceItems:
# # Amount = Quantity x Price
# # Price, Quantity, and Amount must be greater than zero.
# # Validations for BillSundrys:
# # The amount can be negative or positive.
# # Validations for Invoice:
# # TotalAmount = Sum(InvoiceItems’s Amount) + Sum(InvoiceBillSundry’s Amount)
# # InvoiceNumber should autoincremental and hence should be unique.

        
#         unique_invoices = {}
#         invoiceItems = invoice['InvoiceItems']  #list holding all the invoice items
        
#         for item in invoiceItems:
#             if 0 not in item.values():
#                 cal_amt = item["Price"] * item["Quantity"]
#                 if cal_amt != item['Amount']:
#                     return f"Amount Mismatch in Invoice Item {item.id}"
#                 unique_invoices[item['Id']] = unique_invoices.get(item['Id'],0) + item['Amount']
        
#         billSundrys = invoice['BIllSundrys']  #list Holding the bill Sundrys

#         unique_billsundrys = {}
#         for item in billSundrys:
#             if not isinstance(item['Amount'],int):
#                 return f"Invalid Amount type in BillSUndry  : {item["id"]}"
#             unique_billsundrys[item['Id']] = unique_billsundrys.get(item['Id'],0) + item['Amount']
            
#         invoices = invoice['invoices']  #key is subject to change,list of invoices
#         unique_invoices = {}
#         for item in invoices:
#             if unique_invoices.get(item['Id']):
#                 return f"Duplicate Invoice Found : {item['Id']}"
#             InvoiceItemAmount = unique_invoices[item['Id']]
#             BillSunDryAmount = unique_billsundrys[item['Id']]
            
#             if item['Amount'] != (InvoiceItemAmount + BillSunDryAmount):
#                 return f"Amount Mismatched for Invoice :{item['Id']}"
            
#         return "Valid Invoice"
#     except Exception:
#         return "Could Not Process at the time, please try after sometime."


def validate_invoice(invoice):
    try:
        if not invoice.get('invoiceNumber') or not isinstance(invoice['invoiceNumber'], int):
            return "Invoice number is required and must be an integer."

        # Validate Invoice Items
        invoice_items = invoice.get('InvoiceItems', [])
        if not invoice_items:
            return "Invoice must include at least one invoice item."

        total_items_amount = 0
        for item in invoice_items:
            if not all(k in item for k in ('itemName', 'Quantity', 'Price', 'Amount')):
                return "Missing fields in one of the invoice items."

            quantity, price, amount = item['Quantity'], item['Price'], item['Amount']
            if any(type(x) not in [int, float] for x in [quantity, price, amount]):
                return "Quantity, Price, and Amount must be numeric values in invoice items."

            if quantity <= 0 or price <= 0:
                return "Quantity and Price must be greater than zero in invoice items."

            calculated_amount = quantity * price
            if calculated_amount != amount:
                return f"Amount mismatch in invoice item: expected {calculated_amount}, got {amount}."

            total_items_amount += amount

        # Validate Bill Sundrys
        bill_sundrys = invoice.get('BillSundrys', [])
        total_sundry_amount = 0
        for sundry in bill_sundrys:
            if not all(k in sundry for k in ('billSundryName', 'Amount')):
                return "Missing fields in one of the bill sundries."

            amount = sundry['Amount']
            if not isinstance(amount, (int, float)):
                return "Amount must be a numeric value in bill sundries."

            total_sundry_amount += amount

        # Validate Total Amount
        expected_total_amount = total_items_amount + total_sundry_amount
        if 'totalAmount' not in invoice or invoice['totalAmount'] != expected_total_amount:
            return f"Total amount mismatch: expected {expected_total_amount}, got {invoice.get('totalAmount')}."

        return "Valid Invoice"
    except Exception as e:
        return f"Validation error: {str(e)}"

    




# def store_in_db(invoice):
#     try:
#         new_invoice = InvoiceHeader(
#             invoiceNumber = invoice['invoiceNumber'],
#             customerName = invoice['customerName'],
#             billingAddress = invoice['billingAddress'],
#             gstin = invoice['gstin'],
#             totalAmount = invoice['totalAmount']
#         )
#         db.session.add(new_invoice)

#         for item in invoice['InvoiceItems']:
#             new_invoice_item = InvoiceItem(
#                itemName = item['itemName'], 
#                quantity = item['Quantity'], 
#                price = item['Price'],
#                amount = item["Amount"] 
#             )
#             db.session.add(new_invoice_item)
        
#         for item in invoice['BillSunDry']:
#             new_invoice_bill_sundry = InvoiceSundry(
#                 itemName = item['billSundryName'],
#                 amount = item["Amount"]
#             )
#             db.session.add(new_invoice_bill_sundry)

        
#         db.session.commit()

#         return True
#     except Exception:
#         return False

def store_in_db(invoice_data):
    try:
        new_invoice = InvoiceHeader(
            invoiceNumber=invoice_data['invoiceNumber'],
            customerName=invoice_data['customer_name'],
            billingAddress=invoice_data['billing_address'],
            gstin=invoice_data['gstin'],
            totalAmount=invoice_data['totalAmount']
        )
        db.session.add(new_invoice)
        db.session.commit()
        print(new_invoice.id)
        

        for item in invoice_data['InvoiceItems']:
            new_item = InvoiceItem(
                itemName=item['itemName'],
                quantity=item['Quantity'],
                price=item['Price'],
                amount=item['Amount'],
                header_id=new_invoice.id  # This assumes back_populates or similar in your relationship
            )
            db.session.add(new_item)

        for sundry in invoice_data['BillSundrys']:
            new_sundry = InvoiceSundry(
                itemName=sundry['billSundryName'],
                amount=sundry['Amount'],
                header_id=new_invoice.id  # This assumes back_populates or similar in your relationship
            )
            db.session.add(new_sundry)

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

def fetch_invoice(id = None):
    try:
        invoice = InvoiceHeader.query.get(id)
        invoice_list = [invoice.to_dict()]
        return invoice_list
    except Exception:
        return []
    
def fetch_all_invoices():
    try:
        invoices = InvoiceHeader.query.all()
        print(invoices)
        invoice_list = [invoice.to_dict() for invoice in invoices]
        return invoice_list
    except Exception:
        return []


# priyanshu.b@altiushub.com