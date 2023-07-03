import numpy as np


def sliding_window(imgH, imgW, edgeH, edgeW, edge_size, wmask_b, p_min, p_max):
    """
    It sliding the array to define the window size for each pixel:
    :param p_min: minimum ratio value;
    :param p_max: maximum ratio value;
    :return: array with window size values.
    """
    # List content the window-size used to define the optimal w-size -> MNDWI index.
    # Here, the values are expressed as half of the total w-size. The maximum size is 5 km.
    list_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 37, 50, 62, 75, 87, 100, 112, 125]
    # Output Array (m x n):
    output = np.ones((edgeH, edgeW), dtype='float32')
    # It does along the each water-pixel multiple-iterations (33 iterations per pixel).
    for ax_y in np.arange(edge_size, imgH + edge_size):
        for ax_x in np.arange(edge_size, imgW + edge_size):
            mndwi_value_ = wmask_b[ax_y, ax_x]
            if mndwi_value_ == 1:
                for iterate in list_:
                    # It breaks the wmask_b in iterative parts considering the window-size:
                    roi_ = wmask_b[ax_y - iterate: ax_y + iterate + 1, ax_x - iterate: ax_x + iterate + 1]
                    # It verifies the proportion of non-water:
                    occurrence_total_ = np.sum(roi_ >= 0)
                    nonwater_ = (np.sum(roi_ == 0) / occurrence_total_) * 100
                    # It observes the proportion of non-water. If the non-water value is within the defined interval,
                    # the output-array receives the non-water value and code break. Unlike, if the non-water value is
                    # out off the defined interval, the code will observe the defined window values around the target
                    # pixel (box 3-by-3) and will return the max-value for the pixel.
                    if (nonwater_ >= p_min) and (nonwater_ <= p_max):
                        output[ax_y, ax_x] = roi_.shape[:2][0]
                        break
                    else:
                        box = output[ax_y - 1:ax_y + 1 + 1, ax_x - 1:ax_x + 1 + 1]
                        max_value = np.amax(box)
                        output[ax_y, ax_x] = max_value
            else:
                # When the pixel is non-water, the output-array receives value equal to 1:
                output[ax_y, ax_x] = int(1)
    windowsize = output[edge_size:imgH + edge_size, edge_size:imgW + edge_size]
    return (windowsize)