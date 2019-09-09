import sys
from pathlib import Path
from PIL import Image
import logging

import logger
from mrc_from_txt import TxtExtract
from mrc_extractor import GetMrc
from marker_maker import Marker
from stitcher import Stitcher
from file_checker import *


def main(args):
    logging.info(f"Running MosaicStitch with arguments {args}")
    if (args[0]) and (Path(args[0]).suffix == ".txt"):
        tiff_file = Path(args[0]).resolve().with_suffix(".tiff")
        with open(args[0], 'rb') as csvfile:
            # Open mrc image file:
            image = GetMrc(csvfile).image
            # Extract image parameters:
            params = TxtExtract(csvfile).get_params()

        mosaic = Stitcher(image, params).make_mosaic()
        mosaic_im = Image.fromarray(mosaic, 'L').transpose(Image.FLIP_TOP_BOTTOM)

        if len(args) > 1 and is_marker_file(args[1]) and Path(args[1]).is_file():
            marked_path = str(tiff_file).replace(".tiff", "_marked.tiff")

            mosaic_rgba = mosaic_im.convert("RGBA")
            annotations = Marker(args[1], params).output_markers(mosaic_rgba)

            annotations.save(
                marked_path, format="tiff",
                save_all=True, append_images=[mosaic_rgba, ],
                )
        else:
            mosaic_im.save(
                str(tiff_file), format="tiff"
                )

    else:
        raise IOError("The first argument must be the text file, not {}".format(args[0]))


if __name__ == "__main__":
    main(sys.argv[1:])
