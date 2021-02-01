import logging
import logging.handlers
import os
import time


class RecordLog:
    def __init__(self):
        self.logger = logging.getLogger("")
        # 创建文件目录
        logs_dir = "logs"
        if not os.path.exists(logs_dir) or not os.path.isdir(logs_dir):
            os.mkdir(logs_dir)

        # 修改log保存位置
        time_stamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        log_file_name = '%s.log' % time_stamp
        log_file_path = os.path.join(logs_dir, log_file_name)
        rotating_file_handler = logging.handlers.RotatingFileHandler(filename=log_file_path,
                                                                     maxBytes=1024 * 1024 * 50,
                                                                     backupCount=5)
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d]'
                                      ' %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        rotating_file_handler.setFormatter(formatter)

        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.NOTSET)
        console.setFormatter(formatter)

        # 添加内容到日志句柄中
        self.logger.addHandler(rotating_file_handler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.NOTSET)


if __name__ == "__main__":
    log = RecordLog().logger
    log.info("info")
    log.warning("warning")
    log.error("error")
    log.debug("debug")
