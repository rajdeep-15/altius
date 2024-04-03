from flask_restful import Resource
from flask import request,jsonify
from method_calls import validate_invoice,store_in_db,fetch_invoice,fetch_all_invoices


class CreateInvoice(Resource):
    def post(self):
        invoice = request.get_json()

        # Validate invoice
        validation_message = validate_invoice(invoice)
        if validation_message != "Valid Invoice":
            return {"message": validation_message}

        # Store in DB
        if store_in_db(invoice):
            return {"message": "Invoice Created!"}
        else:
            return {"message": "Could not create Invoice at this moment."}



class Update(Resource):
    def post(self):
        pass


class Retrieve(Resource):
    def get(self,id):
        req_id = int(id)
        if not isinstance(req_id,int):
            return {"message" : "Invalid Id format"}
        
        get_invoice = fetch_invoice(req_id)
        
        return get_invoice

class Delete(Resource):
    def post(self):
        pass

class List(Resource):
    def get(self):
        invoices = fetch_all_invoices()
        return invoices