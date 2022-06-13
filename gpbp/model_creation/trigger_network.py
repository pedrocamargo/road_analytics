from aequilibrae import Project, Parameters


def trigger_network(project: Project, folder:str):

    try:
        project.new(folder)
    except FileNotFoundError:
        print('Location already exists. The existing directory will be loaded.')
        print(folder)
        project.load(folder)

    

