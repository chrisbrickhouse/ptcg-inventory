import pandas as pd
from sqlalchemy import create_engine, text, URL
import os
from math import isnan
import json

COLUMN_NAMES = [
        'id',
        'card_id',
        'card_name',
        'super_type',
        'subtypes',
        'hp',
        'types',
        'regulation_mark',
        'rules',
        'expanded_legal',
        'standard_legal',
        'unlimited_legal'
    ]

def drop_cols( df ):
    cols = [
            'attacks',
            'weaknesses',
            'resistances',
            'abilities',
            'images',
            'ancientTrait',
            'legalities'  # See normalize legalities
        ]
    cols_to_remove = [x for x in cols if x in df.columns]
    df = df.drop(columns=cols_to_remove)
    return df

def drop_nonSQL_cols( df ):
    cols_to_remove = [x for x in df.columns if x not in COLUMN_NAMES]
    return df.drop(columns = cols_to_remove)

def normalize_legalities( df ):
    legal_expanded  = []
    legal_standard  = []
    legal_unlimited = []
    for legalities in df.legalities:
        try:
            if 'expanded' in legalities:
                legal_expanded.append( True )
            else:
                legal_expanded.append( False )
            if 'standard' in legalities:
                legal_standard.append( True )
            else:
                legal_standard.append( False )
            if 'unlimited' in legalities:
                legal_unlimited.append( True )
            else:
                legal_unlimited.append( False )
        except KeyError:
            legal_expanded.append( None )
            legal_standard.append( None )
            legal_unlimited.append( None )
        except Exception as e:
            raise(e)
    df['expanded']  = legal_expanded
    df['standard']  = legal_standard
    df['unlimited'] = legal_unlimited
    return df

def replace_null_loop( df, field, default, condition_callback = lambda x: x ):
    """Run a for loop to recode data

    Params:
    df pandas.DataFrame The dataframe to operate on
    field str The name of the column in df to recode
    default any The value to replace null values with
    condition_callback callable A callable that rakes a row value and returns a bool
        If condition_callback return True, the value is replaced with default.
    """
    if field not in df.columns:
        df[field] = [default] * len(df.index)
        return df
    recoded = []
    for item in df[field]:
        if condition_callback( item ):
            recoded.append( default )
        else:
            recoded.append( item )
    df[ field ] = recoded
    return df

def normalize_hp( df, has_field = True ):
    return replace_null_loop(
            df,
            "hp",
            0,
            lambda x: isnan(x)
        )

def normalize_ArrayField( df, field ):
    return replace_null_loop(
            df,
            field,
            [],
            lambda x: type(x) is not list
        )

def normalize_CharField( df, field ):
    return replace_null_loop(
            df,
            field,
            "",
            lambda x: type(x) is None
        )

def normalize_PozIntField( df, field ):
    return replace_null_loop(
            df,
            field,
            0,
            lambda x: isnan(x)
        )

def rename_for_schema( df ):
    column_mapping = {
            "id": 'card_id',
            "name": 'card_name',
            "supertype": 'super_type',
            "regulationMark": 'regulation_mark',
            "expanded": 'expanded_legal',
            "standard": 'standard_legal',
            "unlimited": 'unlimited_legal'
        }
    return df.rename(columns=column_mapping)

def make_fixture_from_row( row, model_name, idx ):
    fixture_template = {
            "model": model_name,
            "fields": {}
        }
    for k,v in row.items():
        fixture_template["fields"][k] = v
    return fixture_template

def clean_set_data( cards ):
    cards = normalize_legalities( cards )
    cards = normalize_PozIntField( cards, "hp" )
    cards = normalize_ArrayField( cards, "types" )
    cards = normalize_ArrayField( cards, "rules" )
    cards = normalize_ArrayField( cards, "subtypes" )
    cards = normalize_CharField( cards, "regulationMark" )
    cards = rename_for_schema( cards )
    cards = drop_nonSQL_cols ( cards )
    return cards

def main( 
         input_path = 'pokemon-tcg-data/cards/en',
         output_path = 'cardsite/decks/fixtures'
         ):
    existing_fixtures = os.listdir( output_path )
    for set_ in os.listdir( input_path ):
        if set_ in existing_fixtures:
            continue
        setname = set_.split('.json')[0]
        cards = pd.read_json( os.path.join( input_path, set_ ) )
        cards = clean_set_data ( cards )
        card_fixture = []
        for idx, row in cards.iterrows():
            card_fixture.append( make_fixture_from_row( row, 'decks.Card', idx ) )
        with open( os.path.join( output_path, set_ ), 'w' ) as f:
            json.dump( card_fixture, f, indent = 4 )

if __name__ == "__main__":
    main()
