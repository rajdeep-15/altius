from app import app,db
from flask_restful import Api
from flask_executor import Executor
import controlller


api = Api(app)



api.add_resource(controlller.CreateInvoice,'/create')
api.add_resource(controlller.Update,'/update')
api.add_resource(controlller.Delete,'/delete')
api.add_resource(controlller.Retrieve,"/retrieve/<id>")
api.add_resource(controlller.List,'/list')


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    app.run()