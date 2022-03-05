from request_api_data import main
from coodesh_app.management.commands.load_api_data import Command

def run():

    main()
    load_data = Command()
    load_data.handle()
