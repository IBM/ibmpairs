import numpy
import pandas
from datetime import datetime, timedelta
import pytz
import os

# IBM PAIRS open-source module
from ibmpairs import paw

PAIRS_USER              = ############
PAIRS_SERVER            = ############
BASE_URI                = ############
PAIRS_PASSWORD          = ############
PAIRS_CREDENTIALS       = ############

def query_local(layerID):
    coronaQueryDef = {
        "layers": [
            {"id": layerID},
        ],
        "spatial": {
            "type" :        "square",
            "coordinates" : [-89, -179, 89, 179], 
        },
        "temporal": {
            "intervals": [
                {
                    "start": "2019-03-01T00:00:00Z",
                    "end": "2030-03-10T23:59:59Z"
                }
            ]
        },
        "outputType": "csv"
    }

    # create PAIRS query instance
    coronaQuery = paw.PAIRSQuery(
        coronaQueryDef,
        pairsHost = 'https://'+PAIRS_SERVER,
        auth = PAIRS_CREDENTIALS,
        baseURI = BASE_URI,
        inMemory    = True,
    )
    # submit and download modified query
    coronaQuery.submit()
    coronaQuery.poll_till_finished(printStatus=True)
    coronaQuery.download()
    coronaQuery.create_layers()

    # associate vector data frame, and show the vector data
    coronaQuery.vdf = coronaQuery.data[list(coronaQuery.metadata.keys())[0]]

    # split property string into individual columns
    #coronaQuery.split_property_string_column()

    new = coronaQuery.vdf['Region'].str.replace(':', '.').str.split('.', expand=True)
    coronaQuery.vdf['pairs_id'] = new[0]
    coronaQuery.vdf['State'] = new[1]
    coronaQuery.vdf['County'] = new[2]
    
    return coronaQuery
