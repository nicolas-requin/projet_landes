import os


def rasterization(in_vector, out_image, field_name, sptial_resolution):
    """
    Rasterisation d'un shapefile en appelant la fonction gdal_rasterize

    Paramètres:
    -------------
        in_vector (str): Shapefile à rasteriser
        out_image (str): Chemin d'accès et nom du raster de sortie
        field_name (str): Nom du champ de référence pour la rasterisation
        sptial_resolution (int): Résolution spatiale du raster de sortie
    """

    # Raterisation du shapefile
    cmd_pattern = ("gdal_rasterize -a {field_name} "
                   "-tr {sptial_resolution} {sptial_resolution} "
                   "-ot Byte -of GTiff "
                   "{in_vector} {out_image} "
                   "-a_nodata 0")

    # fill the string with the parameter thanks to format function
    cmd = cmd_pattern.format(in_vector=in_vector, out_image=out_image,
                             field_name=field_name, sptial_resolution=sptial_resolution)

    # execute the command in the terminal
    os.system(cmd)
