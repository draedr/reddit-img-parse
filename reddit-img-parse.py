import requests
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import os
import shutil
from sys import platform
import click
import logging

version = "0.2.0"
author = "Draedr"
logger = logging.getLogger(__name__)

def url_extraction(url):
    r = requests.get(url)

    if(r.status_code != 200):
        logger.info("Request was not successful!")
        exit()

    html_doc = r.content.decode('utf-8')

    soup = BeautifulSoup(html_doc, 'html.parser')
    galleries = soup.find_all('gallery-carousel')
    
    if(len(galleries) == 0):
        logger.error("No gallery found!")
        exit()
        
    if(len(galleries) > 1):
        logger.error("No gallery found!")
        exit()

    gallery = galleries[0]
    images_holders = gallery.find_all('li')
    images_urls = []

    for ih in images_holders:
        imgs = ih.find_all('img')
        
        for img in imgs:
            try:
                img_url = img['data-lazy-src']
                if img_url not in images_urls:
                    images_urls.append(img_url)
            except KeyError:
                logger.info("No data-lazy-src found!")
                logger.debug(img)

                try:
                    img_url = img['src']
                    if img_url not in images_urls:
                        images_urls.append(img_url)
                except KeyError:
                    logger.error("No src found!")
                    logger.debug(img)
                    continue

    logger.info("Found " + str(len(images_urls)) + " images!")

    return images_urls

def create_folder(output_folder, overwrite):
    try:
        os.makedirs(output_folder, exist_ok=False)
    except Exception as e:
        if overwrite:
            try:
                shutil.rmtree(output_folder)
                os.makedirs(output_folder, exist_ok=False)
            except Exception as e:
                logger.error("Error while overwriting Folder " + output_folder + "!")
                logger.error(e)
                exit()
        else:
            logger.error("Error while creating Folder " + output_folder + "!")
            logger.error(e)
            exit()

def download_image_files(output_folder, images_urls, enumerate):
    for img_url in images_urls:
        # f.write(img_url + '\n')
        data = requests.get(img_url).content

        filename = img_url.split('/')[-1].split('?')[0]

        if enumerate:
            filename = str(images_urls.index(img_url)) + '_' + filename
        
        with open(os.path.join(output_folder, filename), 'wb') as img_file:
            img_file.write(data)
            img_file.close()

            logger.info("Saved " + filename + "!")

def get_output_folder(url, output_folder, download_folder):
    if download_folder != '':
        extraction_folder = download_folder
    else:
        extraction_folder = url[:len(url)-1].split('/')[-1] if url[-1] == '/' else url.split('/')[-1]

    if output_folder == '':
        output_folder = os.getcwd()
    else:
        if not os.path.exists(output_folder):
            logger.error("Output folder does not exist!")
            exit()

    output_folder = os.path.join(output_folder, extraction_folder)
    logger.info("Images will be downloaded in: " + extraction_folder)

    return output_folder

def open_output(output_folder):
    if platform == "linux" or platform == "linux2":
        os.system("xdg-open " + output_folder)
    elif platform == "darwin":
        os.system("open " + output_folder)
    elif platform == "win32":
        os.startfile(output_folder)
    else:
        exit()

@click.command(epilog="Code available at https://github.com/draedr/reddit-img-parse")
@click.version_option(version=version, prog_name="reddit-img-parse", message="%(prog)s version %(version)s")
@click.argument('url')
@click.option('--output_folder', default='', help='Output folder for downloaded images (A new folder will be created inside of it). By deafult, the current working directory will be used.')
@click.option('--enumerate', default=False, help='Prefix the filenames with their index. Default is False.')
@click.option('--overwrite', is_flag=True, help='Overwrites download folder if already exists by deleting it first. Default is False.')
@click.option('--logfile', is_flag=True, help='Save logging to file.')
@click.option('--logpath', default='debug.log', help='Which file to save the logs. Default is debug.log.')
@click.option('--debug', is_flag=True, help='Enable debug mode.')
@click.option('--keeplogs', is_flag=True, help='Keep logs after execution. Default is False.')
@click.option('--foldername', default='', help='Name of the folder created in output_folder where the images will be saved.')
def main(url, output_folder, enumerate, overwrite, logfile, logpath, debug, keeplogs, foldername):
    """A python script to download images from a Reddit post with a gallery.
    
    URL must be the link to page url, not the image url or something else.
    Example: https://www.reddit.com/r/wholesomememes/comments/1x2y3z/this_is_a_test_post/
    """
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    if logfile:
        logger.info("Logs will be saved to file " + logpath + "!")
        logging.basicConfig(filename=logpath, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.FileHandler(logpath, mode='a' if keeplogs else 'w')
    else:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
        
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.info("Debug mode enabled!")

    output_folder = get_output_folder(url, output_folder, foldername)

    images_urls = url_extraction(url)
    create_folder(output_folder, overwrite)
    download_image_files(output_folder, images_urls, enumerate)

    logger.info("All images downloaded!")

    open_output(output_folder)

if __name__ == "__main__":
    main()