from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime



class InvoiceHeader(db.Model):
    # Id: UUID
    # Date: string (UTC)
    # InvoiceNumber: number
    # CustomerName: string
    # BillingAddress: string
    # ShippingAddress: string
    # GSTIN: string
    # TotalAmount: Decimal

    __tablename__ = 'InvoiceHeader'
    id =db.Column(db.Integer,primary_key = True)
    invoiceNumber = db.Column(db.Integer,nullable = False)
    customerName = db.Column(db.String(30),nullable = False)
    billingAddress = db.Column(db.String(30))
    gstin = db.Column(db.String(30),nullable = False)
    totalAmount = db.Column(db.DECIMAL(),nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow())
    invoiceitem = db.relationship('InvoiceItem',backref = "InvoiceHeader")
    invoicesundry = db.relationship('InvoiceSundry',backref = "InvoiceHeader")


    def __repr__(self):
        return f"Invoice number : {self.invoiceNumber} of amount {self.totalAmount} for {self.customerName}"
    def to_dict(self):
        inv_obj = {
            "id" : self.id,
            "invoiceNumber" : self.invoiceNumber,
            "totalAmount" : float(self.totalAmount),
            "date" : str(self.date)
        }
        return inv_obj


class InvoiceItem(db.Model):
#     Id: UUID
# itemName: string
# Quantity: decimal
# Price: decimal
# Amount: decimal


    id =db.Column(db.Integer,primary_key = True)
    itemName = db.Column(db.Integer,nullable = False)
    quantity = db.Column(db.DECIMAL(),nullable = False)
    price = db.Column(db.DECIMAL())
    amount = db.Column(db.DECIMAL(),nullable = False)
    header_id = db.Column(db.Integer,db.ForeignKey('InvoiceHeader.id'),nullable = False)

    def __repr__(self):
        return f"Invoice number : {self.invoiceNumber} of amount {self.totalAmount} for {self.customerName}"
    

class InvoiceSundry(db.Model):
#     Id: UUID
# billSundryName: string
# Amount: decimal



    id =db.Column(db.Integer,primary_key = True)
    itemName = db.Column(db.Integer,nullable = False)
    amount = db.Column(db.DECIMAL,nullable = False)
    header_id = db.Column(db.Integer,db.ForeignKey('InvoiceHeader.id'),nullable = False)

    def __repr__(self):
        return f"Invoice number : {self.invoiceNumber} of amount {self.totalAmount} for {self.customerName}"

