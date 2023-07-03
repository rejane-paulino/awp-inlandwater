import numpy as np
import warnings


def AdaptativeConvolution(array_band, band, array_wsize, Weight_general):
    """
    Recovers the adjacency effect magnitude.
    """
    warnings.filterwarnings("ignore")
    # Retrievals the shape of the band:
    (imgH, imgW) = array_band.shape[:2]
    # Creates the output array. It has same dimensions the input band:
    output = np.zeros((imgH, imgW), dtype='float32')
    # Process the adaptive convolution. It used different kernel sizes along the band:
    edge_size = 124 # Default. It uses the maximum window size defined in 5000 meters.
    for ax_y in np.arange(edge_size, imgH + edge_size):
        for ax_x in np.arange(edge_size, imgW + edge_size):
            # It selects the window's size value in array_wsize:
            wsize_value = array_wsize[ax_y - edge_size, ax_x - edge_size]
            if int(wsize_value) == 1:
                # In this case, the value equal to 1 refers to pixels uncorrected (e.g., land-pixels)
                # by adjacency effects.
                # It selects the reflectance value and attributes it in a new array:
                roi = band[ax_y, ax_x]
                # Inserts the values (p_adj) at their location within the new array::
                output[ax_y - edge_size, ax_x - edge_size] = roi
            else:
                # In this case, the w_size != 1 refers to pixels that will receive the adjacency effect correction:
                # It creates the kernel:
                # Size and properties of kernel:
                w_general = 249  # Default value
                WxH = wsize_value
                # It builds a kernel with zero values with standard size:
                kernel_control = np.zeros((w_general, w_general))
                # It builds a binary kernel [0 and 1] where one-value occupies the horizontal window size range:
                xlim = int((w_general - 1) / 2) - int((WxH - 1) / 2)
                ylim = int((w_general - 1) / 2) + int((WxH - 1) / 2) + 1
                kernel_control[xlim:ylim, xlim:ylim] = 1
                # It Calculates the contribution window to each pixel. For each pixel the APSF window size is
                # controlled by adaptive kernel:
                AdptativeKernel_ = kernel_control * Weight_general
                # Selects the part of interest of the array:
                roi = band[ax_y - edge_size:ax_y + edge_size + 1, ax_x - edge_size:ax_x + edge_size + 1]
                # Calculates the adjacency effect reflectance:
                p_adj = (np.sum(roi * AdptativeKernel_)) * (1 / np.sum(AdptativeKernel_))  # Considering the weighted average...
                # Inserts the values (p_adj) at their location within the new array::
                output[ax_y - edge_size, ax_x - edge_size] = p_adj
    return (output)
