from giant_pulse.file_manipulation import combine_files_freq

# Simple test to confirm the import works
print("Import successful!")
print(f"Function available: {combine_files_freq.__name__}")
print(f"Function docstring: {combine_files_freq.__doc__[:50]}...")

def test_import():
    """Test to ensure combine_files_freq can be imported and is callable."""
    from giant_pulse.file_manipulation import combine_files_freq
    assert callable(combine_files_freq), "combine_files_freq should be callable"


def test_combine_files_freq():
    """Test the combine_files_freq function using the mock data in the data folder."""

    from giant_pulse.file_manipulation import combine_files_freq
    from baseband import guppi
    import numpy as np
    import astropy.units as u
    from pathlib import Path

    axis = 2  # Frequency axis
    samples_per_frame = 1024

    # Get paths relative to this test file's location
    test_dir = Path(__file__).parent
    data_dir = test_dir.parent / 'data'
    file_paths = [str(data_dir / 'puppi1.raw'), str(data_dir / 'puppi2.raw'), str(data_dir / 'puppi3.raw')]

    combined = combine_files_freq(file_paths, samples_per_frame=samples_per_frame, axis=axis)

    f1 = guppi.open(str(data_dir / 'puppi1.raw'), 'rs')
    f2 = guppi.open(str(data_dir / 'puppi2.raw'), 'rs')
    f3 = guppi.open(str(data_dir / 'puppi3.raw'), 'rs')

    d1 = f1.read()
    d2 = f2.read()
    d3 = f3.read()
    header1 = f1.header0
    header2 = f2.header0
    header3 = f3.header0    
    
    f1.close()
    f2.close()
    f3.close()

    combined_data = combined.read()

    # Check that the combined data has the correct shape
    expected_shape = list(d1.shape)
    expected_shape[axis] = d1.shape[axis] + d2.shape[axis] + d3.shape[axis]
    assert combined_data.shape == tuple(expected_shape), "Combined data has incorrect shape"

    # Check that the frequency axis is correctly defined
    base_freq = header1["OBSFREQ"]
    chan_bw = header1["CHAN_BW"]
    n_chans = header1["OBSNCHAN"]
    total_chans = n_chans * 3  # Three files combined
    expected_freqs = base_freq * u.MHz + np.linspace(0, total_chans - 1, total_chans) * chan_bw * u.MHz
    np.testing.assert_array_almost_equal(combined.frequency.value, expected_freqs.value, decimal=2,
                                         err_msg="Frequency axis is incorrectly defined")
    
    # test that appending data of mock files matches combined data
    appended_data = np.concatenate((d1, d2, d3), axis=axis)
    np.testing.assert_array_equal(combined_data, appended_data,
                                  err_msg="Combined data does not match appended data from individual files")

