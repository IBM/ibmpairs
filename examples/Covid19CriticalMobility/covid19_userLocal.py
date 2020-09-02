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


def query_population_aggregated(pairs_id_list, overwriteExisting=True):
    """
    """
    # Query the population density (aggregated by the polygons)
    rasterAggQueryDef = {
        "layers" : [
            {"id" : 48774}, # 1km population density
        ],
        "spatial" : {
            "type" : "square",
            "coordinates" : [-89.9, -179.9, 89.9, 179.9], #[23, -125, 50, -67],
            "aggregation": {
                "aoi": [
                    i for i in pairs_id_list
                    #i for i in range(121, 175) # ConUS State PAIRS polygons
                ]
            }
        },
        "temporal" : {
            "intervals": [
                {
                    "snapshot": "2030-01-01T00:00:00Z",
                }
            ]
        }
    }

    # create PAIRS query instance
    rasterAggQuery = paw.PAIRSQuery(
        rasterAggQueryDef,
        pairsHost = 'https://'+PAIRS_SERVER,
        auth = PAIRS_CREDENTIALS,
        baseURI = BASE_URI,
        overwriteExisting = overwriteExisting,
    )
    # submit and download modified query
    rasterAggQuery.submit()
    rasterAggQuery.poll_till_finished(printStatus=True)
    rasterAggQuery.download()
    rasterAggQuery.create_layers()
    
    # assign the result to the PAIRS query vector data frame
    rasterAggQuery.vdf = list(rasterAggQuery.data.values())[0]
    
    # Calculate the sum from mean and count
    rasterAggQuery.vdf['population'] = rasterAggQuery.vdf['mean()'] * rasterAggQuery.vdf['count()[unit: km^2]'] 

    return rasterAggQuery