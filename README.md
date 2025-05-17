Usage: reddit-img-parse.py [OPTIONS] URL

  A python script to download images from a Reddit post with a gallery.

  URL must be the link to page url, not the image url or something else.
  Example:
  https://www.reddit.com/r/wholesomememes/comments/1x2y3z/this_is_a_test_post/

Options:
  --version             Show the version and exit.
  --output_folder TEXT  Output folder for downloaded images (A new folder will
                        be created inside of it). By deafult, the current
                        working directory will be used.
  --enumerate BOOLEAN   Prefix the filenames with their index. Default is
                        False.
  --overwrite           Overwrites download folder if already exists by
                        deleting it first. Default is False.
  --logfile             Save logging to file.
  --logpath TEXT        Which file to save the logs. Default is debug.log.
  --debug               Enable debug mode.
  --keeplogs            Keep logs after execution. Default is False.
  --foldername TEXT     Name of the folder created in output_folder where the
                        images will be saved.
  --help                Show this message and exit.

  Code available at https://github.com/draedr/reddit-img-parse
