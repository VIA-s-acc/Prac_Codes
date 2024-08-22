from flask import request
from configparser import ConfigParser
def get_GlobalRet(requset):
    data = {
            "global_info": {
                "GlobalRet":
                    {
                        "headers": {}, 
                        "path": "", 
                        "full_path": "", 
                        "script_root": "", 
                        "url": "", 
                        "base_url": "", 
                        "url_root": "", 
                        "host_url": "", 
                        "host": "", 
                        "method": ""
                    },
                "link_to_api": "",
                "api_key": "",
        }
    }
    data['global_info']['link_to_api'] = request.base_url
    config = ConfigParser()
    config.read('optimized/optimized_api/static/config.ini')
    data['global_info']['api_key'] = config['DEFAULT']['API_KEY']
    for key in request.headers:
        data['global_info']['GlobalRet']['headers'].update({key[0]: key[1]})
    data['global_info']['GlobalRet']['path'] = request.path
    data['global_info']['GlobalRet']['full_path'] = request.full_path
    data['global_info']['GlobalRet']['script_root'] = request.script_root
    data['global_info']['GlobalRet']['url'] = request.url
    data['global_info']['GlobalRet']['base_url'] = request.base_url
    data['global_info']['GlobalRet']['url_root'] = request.url_root
    data['global_info']['GlobalRet']['host_url'] = request.host_url
    data['global_info']['GlobalRet']['host'] = request.host
    data['global_info']['GlobalRet']['method'] = request.method
    
    return data
    
def add_dicts(dict1, dict2):
    dict1.update(dict2)
    return dict1
        
def process_data(data, request):
    data['global_info']['link_to_api'] = request.url
    if request.args.get('api_key') is not None:
        data['global_info']['api_key'] = request.args.get('api_key')
    # data['global_info']['GlobalRet']['headers'] = request.headers
    for key in request.headers:
        data['global_info']['GlobalRet']['headers'].update({key[0]: key[1]})
    data['global_info']['GlobalRet']['path'] = request.path
    data['global_info']['GlobalRet']['full_path'] = request.full_path
    data['global_info']['GlobalRet']['script_root'] = request.script_root
    data['global_info']['GlobalRet']['url'] = request.url
    data['global_info']['GlobalRet']['base_url'] = request.base_url
    data['global_info']['GlobalRet']['url_root'] = request.url_root
    data['global_info']['GlobalRet']['host_url'] = request.host_url
    data['global_info']['GlobalRet']['host'] = request.host
    data['global_info']['GlobalRet']['method'] = request.method