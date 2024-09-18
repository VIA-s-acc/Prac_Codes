class CLOGGER:
    def init(self, NAME, NO, COLOR, ICON):
        self.NAME = NAME
        self.NO = NO
        self.COLOR = COLOR
        self.ICON = ICON
    

class loggers:
    def __init__(self, loggers):
        for logger in loggers:
            if not logger.upper().startswith("STDERR.") and len(logger) > 0:
                try:
                    setattr(self, f'__LCNO{logger.upper()}__', int(logger))
                except:
                    setattr(self, f'__L{logger.upper()}__', logger)
            
            elif logger.upper().startswith("STDERR."):
                splited = logger.split(".")
                name = splited[0]
                level = splited[1]
                try:
                    setattr(self, f'__L{name.upper()}__', int(level))
                except:
                    setattr(self, f'__L{name.upper()}__', level)
            

                
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
