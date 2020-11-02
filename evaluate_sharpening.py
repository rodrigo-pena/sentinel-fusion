import os
import cv2
import click
import tempfile

import numpy as np
import snappy_utils as su


@click.command()
@click.option('--low_res_lst', required=True,
              type=click.Path(dir_okay=False, exists=True),
              help='Low resolution BEAM-DIMAP LST')
@click.option('--sharp_lst', required=True,
              type=click.Path(dir_okay=False, exists=True),
              help='Sharpened (high resolution) BEAM-DIMAP LST')
@click.option('--gt_high_res_lst', required=True,
              type=click.Path(dir_okay=False, exists=True),
              help='Ground-truth (high resolution) BEAM-DIMAP LST')
@click.option('--save_residuals', default=False, show_default=True,
              type=bool,
              help='Whether to save residuals as a BEAM-DIMAP product or not')
@click.option('--output_residual', required=False, default=None,
              type=click.Path(dir_okay=False, exists=False),
              help='Save path for the residuals BEAM-DIMAP product')
def main(low_res_lst, sharp_lst, gt_high_res_lst, save_residuals,
         output_residual):

    # Read rasters from BEAM-DIMAP products
    low_res_raster, _ = su.read_snappy_product(low_res_lst,
                                               band_name='LST')
    sharp_raster, geo_coding = su.read_snappy_product(sharp_lst,
                                                      band_name='LST')
    gt_high_res_raster, _ = su.read_snappy_product(gt_high_res_lst,
                                                   band_name='LST')

    height, width = sharp_raster.shape

    # Create baseline nearest-neighbor-interpolation sharpening
    baseline_raster = cv2.resize(low_res_raster,
                                 dsize=(width, height),
                                 interpolation=cv2.INTER_NEAREST)

    # Make sure ground-truth and sharpened LST are the same size
    gt_high_res_raster = cv2.resize(gt_high_res_raster,
                                    dsize=(width, height),
                                    interpolation=cv2.INTER_NEAREST)

    # Get quality pixels
    quality_mask = ~np.isnan(sharp_raster)  # Ignore pixels with NaN values
    n_quality_pixels = np.sum(quality_mask)

    # Evaluate baseline
    baseline_residual = gt_high_res_raster - baseline_raster
    rmse = np.sqrt(
        np.nansum(baseline_residual[quality_mask]**2) / n_quality_pixels
    )
    median_bias = np.nanmedian(baseline_residual[quality_mask])
    std_bias = np.nanstd(baseline_residual[quality_mask])
    print("\nBaseline nearest neighbor upsampling:")
    print("\tRMSE: {:.2f}".format(rmse))
    print("\tMedian bias: {:.2f}".format(median_bias))
    print("\tStandard deviation of bias: {:.2f}".format(std_bias))

    # Evaluate sharpening
    sharp_residual = gt_high_res_raster - sharp_raster
    rmse = np.sqrt(
        np.nansum(sharp_residual[quality_mask]**2) / n_quality_pixels
    )
    median_bias = np.nanmedian(sharp_residual[quality_mask])
    std_bias = np.nanstd(sharp_residual[quality_mask])
    print("\nSharpening:")
    print("\tRMSE: {:.2f}".format(rmse))
    print("\tMedian bias: {:.2f}".format(median_bias))
    print("\tStandard deviation of bias: {:.2f}".format(std_bias))

    if save_residuals:  # Save the residuals
        baseline_band = {
            "band_name": "baseline_LST_residual",
            "description": "Residual of the baseline LST upsampling via " +
                           "nearest neighbor interpolation",
            "unit": "K",
            "band_data": baseline_residual
        }
        sharp_band = {
            "band_name": "sharp_LST_residual",
            "description": "Residual of the sharpened LST",
            "unit": "K",
            "band_data": sharp_residual
        }
        if output_residual is None:
            output_residual = os.path.splitext(low_res_lst)[0] + \
                              'residuals.dim'
        su.write_snappy_product(output_residual,
                                [baseline_band, sharp_band],
                                "sharpening_residuals",
                                geo_coding)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:" + str(e))
