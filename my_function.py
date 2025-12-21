import os


def rasterization(in_vector, out_image, field_name, dtype=None):
    """
    See otbcli_rasterisation for details on parameters
    """

    # define command pattern to fill with paremeters
    cmd_pattern = ("gdal_rasterize -a {field_name} "
                "-tr {sptial_resolution} {sptial_resolution} "
                "-te {xmin} {ymin} {xmax} {ymax} -ot Byte -of GTiff "
                "{in_vector} {out_image}")

    # fill the string with the parameter thanks to format function
    cmd = cmd_pattern.format(in_vector=in_vector, xmin=xmin, ymin=ymin, xmax=xmax,
                            ymax=ymax, out_image=out_image, field_name=field_name,
                            sptial_resolution=sptial_resolution)

    # execute the command in the terminal
    os.system(cmd)