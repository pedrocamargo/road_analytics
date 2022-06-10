

def set_source(source):

    if source == 'WorldPop':
        return 'WorldPop'
    elif source == 'Meta':
        return 'Meta'
    else:
        return ValueError("No population source found.")
