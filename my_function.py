import os
import numpy as np
from osgeo import gdal


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


def write_image(out_filename, array, data_set=None, gdal_dtype=None,
                transform=None, projection=None, driver_name=None,
                nb_col=None, nb_ligne=None, nb_band=None, nodata=None):
    """
    Write a array into an image file.

    Parameters
    ----------
    out_filename : str
        Path of the output image.
    array : numpy.ndarray
        Array to write
    nb_col : int (optional)
        If not indicated, the function consider the `array` number of columns
    nb_ligne : int (optional)
        If not indicated, the function consider the `array` number of rows
    nb_band : int (optional)
        If not indicated, the function consider the `array` number of bands
    data_set : osgeo.gdal.Dataset
        `gdal_dtype`, `transform`, `projection` and `driver_name` values
        are infered from `data_set` in case there are not indicated.
    gdal_dtype : int (optional)
        Gdal data type (e.g. : gdal.GDT_Int32).
    transform : tuple (optional)
        GDAL Geotransform information same as return by
        data_set.GetGeoTransform().
    projection : str (optional)
        GDAL projetction information same as return by
        data_set.GetProjection().
    driver_name : str (optional)
        Any driver supported by GDAL. Ignored if `data_set` is indicated.
    nodata : int (optional)
        Value of Nodata.
    Returns
    -------
    None
    """
    # Get information from array if the parameter is missing
    nb_col = nb_col if nb_col is not None else array.shape[1]
    nb_ligne = nb_ligne if nb_ligne is not None else array.shape[0]
    array = np.atleast_3d(array)
    nb_band = nb_band if nb_band is not None else array.shape[2]

    # Get information from data_set if provided
    transform = transform if transform is not None else data_set.GetGeoTransform()
    projection = projection if projection is not None else data_set.GetProjection()
    gdal_dtype = gdal_dtype if gdal_dtype is not None \
        else data_set.GetRasterBand(1).DataType
    driver_name = driver_name if driver_name is not None \
        else data_set.GetDriver().ShortName

    # Create DataSet
    driver = gdal.GetDriverByName(driver_name)
    output_data_set = driver.Create(out_filename, nb_col, nb_ligne, nb_band,
                                    gdal_dtype)
    output_data_set.SetGeoTransform(transform)
    output_data_set.SetProjection(projection)

    # Fill it and write image
    for idx_band in range(nb_band):
        output_band = output_data_set.GetRasterBand(idx_band + 1)
        output_band.WriteArray(array[:, :, idx_band])

        if nodata is not None:
            output_band.SetNoDataValue(nodata)

        output_band.FlushCache()

    del output_band
    output_data_set = None
