from app import create_app ,db
from flask_script import  Manager,Shell
from app.models import User,Role,Customer,Gasconsumption,GasconsumptionTest,Portrait,ConsumptionUseCase,GasPredictionSale
from random import randint,randrange
from decimal import Decimal
from flask_migrate import Migrate,MigrateCommand
app=create_app('default')
manager=Manager(app)
migrate=Migrate(app,db)
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Customer=Customer,Gasconsumption=Gasconsumption,GasconsumptionTest=GasconsumptionTest,
                Portrait=Portrait,ConsumptionUseCase=ConsumptionUseCase,randint=randint,randrange=randrange,Decimal=Decimal,
                GasPredictionSale=GasPredictionSale)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
if __name__=='__main__':
    manager.run()
