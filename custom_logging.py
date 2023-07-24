import logging
import sys
from pathlib import Path
from loguru import logger
import json

# intercept standard logging messages toward custom Loguru sinks
class  InterceptHandler(logging.Handler):
    loglevel_mapping={
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]
            
        # find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        log = logger.bind(request_id='app')

        # set options
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level,record.getMessage())


class CustomizeLogger:
    @classmethod
    # config 파일에 맞게, logger 생성
    def make_logger(cls, config_path:Path):
        #JSON config 파일 읽어오기
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        #config 파일에서 설정한 파라미터 읽어오기
        logger = cls.customize_logging(
            logging_config.get('path'),
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=logging_config.get('format')
        )
        return logger
    
    @classmethod
    def customize_logging(cls,
        filepath:Path,
        level:str,
        rotation:str,
        retention:str,
        format:str
    ):
        logger.remove()
        #console 출력
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        # 일반 log - access.log 파일
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        # error log - error.log 파일
        logger.add(
            str('/Users/jiheechoi/Desktop/FastAPI_SQL/planner/log/error.log'),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level='ERROR',
            format=format
        )
        # python logging system에 InterceptHandler 추가 
        logging.basicConfig(handlers=[InterceptHandler()],level=0)
        # uvicorn logger에 InterceptHandler 추가
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        # InterceptHandler 추가
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)
    
    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config


