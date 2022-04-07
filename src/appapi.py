import uvicorn
import os
import sys
import logging
import platform
import json
import configparser

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

k_version = "1.0.0"

k_path_log =  "/usr/src/appapi/log"
k_path_conf = "/usr/src/appapi/conf"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler("%s/appapi.log" % k_path_log)
output_file_handler.setFormatter(logging.Formatter("F;%(asctime)s;%(levelname)s;%(message)s"))

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter("S;%(asctime)s;%(levelname)s;%(message)s"))

logger.addHandler(output_file_handler)
logger.addHandler(stdout_handler)


#read config file --------------------------------------------
config = configparser.ConfigParser()

try:    
    filecfg =  '%s/appapi.properties' % k_path_conf   
    config.read(filecfg)
    cfgvar1 = config['section1']['cfgvar1']
    cfgvar2 = config['section1']['cfgvar2']
except Exception as e:
    logger.error ("XCP: error reading file %s : X:%s" % (filecfg, str(e)))
    sys.exit(1)

# default values
apihost = "0.0.0.0"
apiport = 8080
if "APIHOST"   in os.environ:  apihost = os.environ["APIHOST"]
if "APIPORT"   in os.environ:  apiport = int(os.environ["APIPORT"])

myvar=""
if "MYVAR" in os.environ:  myvar = os.environ["MYVAR"]

hostname = platform.node()
res_base = {'hostname':hostname}

async def startup():
    logger.info("in startup")

async def shutdown():
    logger.info("in shutdown")

async def getState(request):
    try:
        logger.info("-------------- in getState, url:%s, client:%s" % (request.url, request.client))
        res = {}
        res['url'] = str(request.url)
        res['client'] = str(request.client)
        res['version'] =  k_version
        res['myenvvar'] =  myvar

        res['cfgvar1'] =  cfgvar1    
        res['cfgvar2'] =  cfgvar2
        
        headers = {}
        for key in request.headers:
            headers[key] = str(request.headers[key])
        res['headers'] = headers

        # add base dict entries
        res.update(res_base)

    except Exception as e: 
        res = {'error': str(e)}
    
    return JSONResponse(res)

routes = [
    Route("/appapi/state",  endpoint=getState, methods=["GET"]),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], 
                               allow_methods=['*'],
                               allow_headers=['*'],
                               allow_credentials=True)
]

app = Starlette(debug=True, 
                routes = routes,
                middleware = middleware,
                on_startup=[startup],
                on_shutdown=[shutdown])

if __name__ == '__main__':
    
    logger.info ("===> Running on %s:%d, version:%s" % (apihost,apiport, k_version))
    
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "UVICORNA:%(asctime)s - %(levelprefix)s - %(client_addr)s - %(request_line)s - %(status_code)s"
    log_config["formatters"]["default"]["fmt"] = "UVICORND:%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run(app, 
                host=apihost,
                port=apiport, 
                lifespan='on',
                proxy_headers='enable',
                log_config=log_config   )
    