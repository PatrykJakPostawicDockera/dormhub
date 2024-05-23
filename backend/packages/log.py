import logging
from packages import au
import datetime
import os


logger = logging.getLogger()


def start_logging():
    created = False
    log_dir = au.get_environ("LOG_DIR")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        created = True

    logging.basicConfig(
        filename=f"{log_dir}/{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log",
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",
    )

    inner_logging = logging.getLogger()
    inner_logging.setLevel(get_logging_level(au.get_environ("LOG_LEVEL")))
    global logger
    logger = inner_logging
    logger.debug(
        f"Directory '{log_dir}' created successfully.")
    cleanup_logs()


def get_logging_level(level: str):
    match level.upper():
        case "DEBUG":
            return logging.DEBUG
        case "INFO":
            return logging.INFO
        case "WARNING":
            return logging.WARNING
        case "ERROR":
            return logging.ERROR
        case "CRITICAL":
            return logging.CRITICAL


def cleanup_logs():
    log_dir = au.get_environ("LOG_DIR")
    log_files = [file for file in os.listdir(log_dir) if file.endswith(".log")]
    log_files.sort(key=lambda x: os.path.getctime(os.path.join(log_dir, x)))

    max_logs = int(au.get_environ("MAX_LOGS"))
    if max_logs <= 0:
        return

    num_files_to_delete = max(0, len(log_files) - max_logs)

    for i in range(num_files_to_delete):
        file_to_delete = os.path.join(log_dir, log_files[i])
        os.remove(file_to_delete)
        logger.debug(f"Deleted log file: {file_to_delete}")
