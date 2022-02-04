import numpy as np
from config import logg_lims

def bin_f_binary_in_logg(metadata, binaries_mask, mask, logg_bins):
    logg_binc = 0.5 * (logg_bins[:-1] + logg_bins[1:])
    
    H_bin, _ = np.histogram(metadata['LOGG'][binaries_mask & mask], 
                            bins=logg_bins)
    H_all, _ = np.histogram(metadata['LOGG'][mask], 
                            bins=logg_bins)
    
    # TODO: can use math to do this instead, lazy 
    ratio = (np.random.poisson(H_bin, size=(1_000, len(H_bin))) / 
             np.random.poisson(H_all, size=(1_000, len(H_all))))

    data_x = logg_binc
    data_y = np.mean(ratio, axis=0)
    data_yerr = np.std(ratio, axis=0)

    sort_idx = np.argsort(data_x)
    data_x = data_x[sort_idx]
    data_y = data_y[sort_idx]
    data_yerr = data_yerr[sort_idx]

    good_idx = np.isfinite(data_y) & (data_y != 0) & (data_yerr != 0)
    data_x = data_x[good_idx]
    data_y = data_y[good_idx]
    data_yerr = data_yerr[good_idx]
    
    return data_x, data_y, data_yerr

def mask_metallicity(metadata, m_low, m_high):
    mask = (
        (metadata['M_H'] > m_low) &
        (metadata['M_H'] <= m_high) &
        (metadata['LOGG'] > logg_lims[0]) & 
        (metadata['LOGG'] < logg_lims[1])
    )
    return mask