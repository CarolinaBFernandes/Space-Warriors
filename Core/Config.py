#coding=utf-8

def get_config():
    import os.path
    import json
        
    config_file = open('config.json')
    config = json.load(config_file)
        
    config_file.close()
        
    # Configurações de desenvolvimento
    if(os.path.exists('config.development.json')):
        development_config_file = open('config.development.json')
        development_config = json.load(development_config_file)
            
        development_config_file.close()
            
        config.update(development_config)
    
    return config