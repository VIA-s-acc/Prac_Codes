class loggers:
    def __init__(self, loggers):
        for logger in loggers:
            setattr(self, f'__L{logger.upper()}__', logger)
            
    def get_loggers(self):     
        return {k: getattr(self, k) for k in dir(self) if k.startswith('__L')}
    
    def print_loggers(self, color_code = "\033[1;36;40m"):
        args = self.get_loggers()
        keys_len = len(list(args.keys()))
        for index, key in enumerate(list(args.keys())):
            if index < keys_len - 1:
                print(f"{color_code}├── {key}:","\033[0m \033[1;31;40m", True,f'\033[0m {color_code}LEVEL: \033[0m \033[1;31;40m ', args[key], "\033[0m")
            else:
                print(f"{color_code}└── {key}:","\033[0m \033[1;31;40m", True,f'\033[0m {color_code}LEVEL: \033[0m \033[1;31;40m ', args[key], "\033[0m")
        