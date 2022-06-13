from aequilibrae import Project, Parameters


def trigger_network(project: Project, folder:str):

    print(folder)
    
    try:
        project.new(folder)
    except FileNotFoundError:
        print('Location already exists. The existing directory will be loaded.')
        project.load(folder)

    

