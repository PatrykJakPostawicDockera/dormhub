import ftplib
import io
import uuid

from packages import au
from packages.log import logger
from urllib.parse import urlparse


def get_ftp_handler():
    ftp = ftplib.FTP("ftp")
    credentials = au.get_environ("FTP_FULLLOGIN").split("|")
    ftp.login(user=credentials[0], passwd=credentials[1])
    return ftp


def upload_to_ftp(data, img_format):
    uuid_generated = uuid.uuid4()
    ftp = get_ftp_handler()
    if "images" not in ftp.nlst():
        ftp.mkd("images")
    ftp.cwd("images")  # Change to the directory where you want to upload the file
    with io.BytesIO(data) as image_buffer:
        ftp.storbinary(f'STOR {uuid_generated}.{img_format}', image_buffer)
    ftp.quit()
    return get_photo_url(uuid_generated, port=80, ext=img_format)


def get_photo_url(file_uuid, **kwargs):
    add_f = ""
    add_p = ""
    if "ext" in kwargs:
        add_f += f".{kwargs['ext']}"
    if "port" in kwargs:
        add_p += f":{kwargs['port']}"
    return f'https://dormhub.space/images/{file_uuid}{add_f}'


def delete_files(file_urls):
    filenames = []
    for url_single in file_urls:
        parsed_url = urlparse(url_single)
        filenames.append(parsed_url.path.split('/')[-1])
    ftp = get_ftp_handler()
    ftp.cwd("images")
    for filename in filenames:
        try:
            logger.debug(f"deleting file: {filename}")
            ftp.delete(filename)
        except ftplib.all_errors as e:
            logger.error(f"FTP error: {e}")
            return False
    ftp.quit()
    return True
