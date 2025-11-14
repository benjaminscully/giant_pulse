import numpy as np
import astropy.units as u
import baseband_tasks as bbt
import baseband as bb

def combine_files_freq(file_names, samples_per_frame=1024, axis=2):
    """Reads in multiple baseband files and combines them along 
    the frequency axis. Additionally defines the associated frequency
    channels.

    Parameters
    ----------
    file_names : list of str
        List of file paths to the baseband files to combine.

    samples_per_frame : int, optional
        Number of samples per frame for the combined file. Default is 1024.

    axis : int, optional
        Axis along which to combine the files. Should be the frequency axis.
        Default is 2.

    Returns
    -------
    combined : str
        File path to the combined baseband file.
    """

    fs = [bbt.open(filename) for filename in file_names]

    base_freq = fs[0].header0["OBSFREQ"] * u.MHz
    chan_bw = fs[0].header0["CHAN_BW"] * u.MHz
    n_chans = fs[0].header0["OBSNCHAN"]
    band_size = chan_bw * n_chans
    total_chans = n_chans * len(fs)
    freqs = base_freq + np.linspace(0, total_chans - 1, total_chans) * chan_bw

    fs = [bbt.base.SetAttribute(f, samples_per_frame=samples_per_frame) for f in fs]

    combined = bbt.combining.Concatenate(fs, axis=axis)
    combined = bbt.base.SetAttribute(combined, freqs=freqs)

    return combined
