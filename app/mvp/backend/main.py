from flask import Flask,request
from flask_restx import Api,Resource,fields
from config import Devconfig
from model import Recipie
from ext import db
from flask_migrate import Migrate

app=Flask(__name__)
app.config.from_object(Devconfig)

db.init_app(app)
migrate = Migrate(app,db)

api = Api(app,doc='/docs')


recipie_model = api.model(
    'Recipie',{
    'id':fields.Integer(),
    'title':fields.String(required=True),
    'description':fields.String(required=True)
})


@api.route('/hello')
class HelloResource(Resource):
    def get (self):
        return {"txt":"Hi am online"}
    


    
@api.route('/recipies')
class RecipiesResource(Resource):
    
    @api.marshal_with(recipie_model)
    def post(self):
        """create a new recipie"""
        data = request.get_json()

        new_recipie = Recipie(
        title = data.get('title'),
        description = data.get('description')
        )
        new_recipie.save()
        return new_recipie,201

    @api.marshal_list_with(recipie_model)
    def get(self):
        """get all recipies"""
        recipies = Recipie.query.all()
        return recipies
        



@api.route('/recipie/<int:id>')
class RecipieResource(Resource):

    @api.marshal_with(recipie_model)    
    def get(self,id):
        """get a recipie by id"""
        recipie = Recipie.query.get_or_404(id)
        return recipie

    @api.marshal_with(recipie_model)
    def put(self,id):
        """update a recipie by id"""
        recipie_to_update = Recipie.query.get_or_404(id)
        data = request.get_json() #get the data from the request
        recipie_to_update.update(data.get('title'),data.get('description'))
        return recipie_to_update

    @api.marshal_with(recipie_model)
    def delete(self,id):
        """delete a recipie by id"""
        recipie_to_delete = Recipie.query.get_or_404(id)
        recipie_to_delete.delete()
        return recipie_to_delete


if __name__ == '__main__':
    app.run()



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Recipie': Recipie}

