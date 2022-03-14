from request_api_data import main
from coodesh_app.management.commands import load_api_data
from coodesh_app.management.commands import delete_all_models_data

def run():

    main()
    delete_all_api_data = delete_all_models_data.Command()
    delete_all_api_data.handle()
    load_data = load_api_data.Command()
    load_data.handle()
