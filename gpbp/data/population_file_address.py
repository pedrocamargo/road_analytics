import pandas as pd


def population_source(model_place: str) -> str:
    pop_path = f'/population/all_raster_pop_source.csv'
    df = pd.read_csv(pop_path)
    return df[df.Country.str.upper() == model_place.upper()].data_link.values[0]
