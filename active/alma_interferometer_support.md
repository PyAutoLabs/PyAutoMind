# ALMA interferometer support in PyAutoReduce

Type: feature
Target: PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Original request (verbatim):

Can we do ALMA in PyAutoReduce, noting that here I have lots of feedback and direction from a user who does ALMA modeling we can follow so a lot less research should be required (but do a bit).

## Slack conversation with Aris (ALMA modeler, 2026-07-09)

Aris [12:20 PM]: yeah I dont mind.
[12:21 PM] but just so you know one doesnt need to run the data reduction pipeline anymore, you can now download the reduced data from the ALMA archive (you used to download the raw and run the pipeline yourself)
[12:22 PM] what my custom codes do is take the calibrated data and extract visibilities, uv_wavelengths, etc... in a format that autolens wants
[12:22 PM] this is what I can send you

Jam [12:22 PM]: yeah i will tell claude to set up both in PyAutoReduce with download the default

Aris [12:31 PM]: This is an example script that reads .ms.split.cal

ms -> this stands for measurement set. This is how ALMA data are delivered.

If multiple execution blocks are carried out (either on the same day or different days - think of it as different exposures), you get multiple measurement sets. These have different names (or rather ids). In this example there are 2:

uids = ["A002_Xb9b1b9_X3046", "A002_Xb99cbd_X2456"]

Then for each measurement set you get 4 spectral windows (spw). You can extract all of them or however many you like (one spw might have an emission line so in this case you disregard it). In this example only two spw are extracted:

spws = ["1", "2"]

Then you select how many channels in each spw to collapse. For continuum modelling I usually collapse the whole spw (different spw might have different number of channels - for emission lines the observer usually chooses more channels). The parameter that controls how many channels are collapsed is width. In this example width = 240.

Finally, main_func(uid=uid, field="G09v1.40", spws=spws, width=width, directory=".", clean=False) takes all these inputs and outputs visibilities per uid per spw (which will have shape [2, Nvis, 2], the first 2 is the polarization).

autolens wants visibilities and uv_wavelengths in shape (Nvis, 2). You can concatenate them accordingly before feeding into autolens.

[12:32 PM] This script runs in CASA
[12:32 PM] so on the terminal type casa and a new window pops up. There you can do execute("name_of_the_file")
[12:33 PM] you can probably write a python script and have python open and execute in a CASA env in the background, but I have never managed to make this work

## Aris's example script (main_2016.1.00282.S_G09v1.40.py, runs inside CASA)

```python
import os, sys
import numpy as np

try:
    from astropy import (
        units,
        constants,
    )
    from astropy.io import fits
    astropy_is_imported = True
except:
    astropy_is_imported = False


def getcol_wrapper(ms, table, colname):
    if os.path.isdir(ms):
        tb.open("{}/{}".format(ms, table))
        col = np.squeeze(tb.getcol(colname))
        tb.close()
    else:
        raise IOError("{} does not exist".format(ms))
    return col


def get_num_chan(ms):
    return getcol_wrapper(ms=ms, table="SPECTRAL_WINDOW", colname="NUM_CHAN")


def get_spw_ids(ms):
    return getcol_wrapper(ms=ms, table="DATA_DESCRIPTION", colname="SPECTRAL_WINDOW_ID")


def get_visibilities(ms):
    if os.path.isdir(ms):
        data = getcol_wrapper(ms=ms, table="", colname="DATA")
    else:
        raise IOError("{} does not exist".format(ms))
    visibilities = np.stack(arrays=(data.real, data.imag), axis=-1)
    return visibilities


def export_visibilities(ms, filename):
    if os.path.isfile(filename):
        print("{} already exists".format(filename))
    else:
        visibilities = get_visibilities(ms=ms)
        print("shape (visibilities):", visibilities.shape)
        if astropy_is_imported:
            fits.writeto(filename=filename + ".fits", data=visibilities, overwrite=True)
        else:
            with open(filename + ".numpy", 'wb') as file:
                np.save(file, visibilities)


def convert_array_to_wavelengths(array, frequency):
    if astropy_is_imported:
        array_converted = ((array * units.m) * (frequency * units.Hz) / constants.c).decompose().value
    else:
        array_converted = array * frequency / 299792458.0
    return array_converted


def get_uv_wavelengths(ms):
    if os.path.isdir(ms):
        uvw = getcol_wrapper(ms=ms, table="", colname="UVW")
    else:
        raise IOError("{} does not exist".format(ms))

    chan_freq = getcol_wrapper(ms=ms, table="SPECTRAL_WINDOW", colname="CHAN_FREQ")

    chan_freq_shape = np.shape(chan_freq)
    if np.shape(chan_freq):
        u_wavelengths, v_wavelengths = np.zeros(shape=(2, chan_freq_shape[0], uvw.shape[1]))
        for i in range(chan_freq_shape[0]):
            u_wavelengths[i, :] = convert_array_to_wavelengths(array=uvw[0, :], frequency=chan_freq[i])
            v_wavelengths[i, :] = convert_array_to_wavelengths(array=uvw[1, :], frequency=chan_freq[i])
    else:
        u_wavelengths = convert_array_to_wavelengths(array=uvw[0, :], frequency=chan_freq)
        v_wavelengths = convert_array_to_wavelengths(array=uvw[1, :], frequency=chan_freq)
    uv_wavelengths = np.stack(arrays=(u_wavelengths, v_wavelengths), axis=-1)
    return uv_wavelengths


def export_uv_wavelengths(ms, filename):
    if os.path.isfile(filename):
        print("{} already exists".format(filename))
    else:
        uv_wavelengths = get_uv_wavelengths(ms=ms)
        print("shape (uv_wavelengths):", uv_wavelengths.shape)
        if astropy_is_imported:
            fits.writeto(filename=filename + ".fits", data=uv_wavelengths, overwrite=True)
        else:
            with open(filename + ".numpy", 'wb') as file:
                np.save(file, uv_wavelengths)


def get_frequencies(uid, field, spw):
    ms = "{}_field_{}_spw_{}.ms.split.cal".format(uid, field, spw)
    if os.path.isdir(ms):
        chan_freq = getcol_wrapper(ms=ms, table="SPECTRAL_WINDOW", colname="CHAN_FREQ")
    else:
        raise IOError("The directory {} does not exist".format(ms))
    return chan_freq


def export_frequencies(uid, field, spw):
    chan_freq = get_frequencies(uid=uid, field=field, spw=spw)
    filename = "./{}_spw_{}_frequencies".format(uid, spw)
    if astropy_is_imported:
        fits.writeto(filename="{}.fits".format(filename), data=chan_freq)
    else:
        with open("{}.numpy".format(filename), 'wb') as file:
            np.save(file, chan_freq)


def get_antennas(ms):
    antenna1 = getcol_wrapper(ms=ms, table="", colname="ANTENNA1")
    antenna2 = getcol_wrapper(ms=ms, table="", colname="ANTENNA2")
    return np.array([antenna1, antenna2])


def export_antennas(ms, filename):
    if not os.path.isdir(ms):
        raise IOError("The ms does not exist.")
    antennas = get_antennas(ms=ms)
    print("shape (antennas):", antennas.shape)
    if astropy_is_imported:
        filename += ".fits"
    else:
        filename += ".numpy"
    if filename.endswith(".fits"):
        fits.writeto(filename=filename, data=antennas, overwrite=True)
    else:
        with open(filename, 'wb') as file:
            np.save(file, antennas)


def get_time(ms):
    time = getcol_wrapper(ms=ms, table="", colname="TIME")
    return np.asarray(time)


def export_time(ms, filename):
    time = get_time(ms=ms)
    if astropy_is_imported:
        filename += ".fits"
    else:
        filename += ".numpy"
    if filename.endswith(".fits"):
        fits.writeto(filename=filename, data=time, overwrite=True)
    else:
        with open(filename, 'wb') as file:
            np.save(file, time)


def get_scans(ms):
    scans = getcol_wrapper(ms=ms, table="", colname="SCAN_NUMBER")
    return np.asarray(scans)


def export_scans(ms, filename):
    scans = get_scans(ms=ms)
    if astropy_is_imported:
        filename += ".fits"
    else:
        filename += ".numpy"
    if filename.endswith(".fits"):
        fits.writeto(filename=filename, data=scans, overwrite=True)
    else:
        with open(filename, 'wb') as file:
            np.save(file, scans)


def main_func(uid, field, spws, width, directory=".", clean=False):
    if not os.path.isdir("{}/uid___{}.ms.split.cal".format(directory, uid)):
        raise IOError("The ms does not exist.")

    # split out the target field if not already done
    if not os.path.isdir("{}/uid___{}_{}.ms.split.cal".format(directory, uid, field)):
        split(
            vis="{}/uid___{}.ms.split.cal".format(directory, uid),
            outputvis="{}/uid___{}_{}.ms.split.cal".format(directory, uid, field),
            keepmms=True,
            field=field,
            spw="",
            datacolumn="data",
            keepflags=False,
        )

    for spw in spws:
        # split per spw, averaging channels by `width`
        if not os.path.isdir("{}/uid___{}_{}_spw_{}_width_{}.ms.split.cal".format(directory, uid, field, spw, width)):
            split(
                vis="{}/uid___{}_{}.ms.split.cal".format(directory, uid, field),
                outputvis="{}/uid___{}_{}_spw_{}_width_{}.ms.split.cal".format(directory, uid, field, spw, width),
                keepmms=True,
                field=field,
                spw=spw,
                datacolumn="data",
                width=width,
                keepflags=False,
            )

        ms_split = "{}/uid___{}_{}_spw_{}_width_{}.ms.split.cal".format(directory, uid, field, spw, width)

        filename_uv_wavelengths = "{}/uv_wavelengths_{}_{}_spw_{}_width_{}".format(directory, uid, field, spw, width)
        if not (os.path.isfile(filename_uv_wavelengths + ".fits") or os.path.isfile(filename_uv_wavelengths + ".numpy")):
            export_uv_wavelengths(ms=ms_split, filename=filename_uv_wavelengths)

        filename_visibilities = "{}/visibilities_{}_{}_spw_{}_width_{}".format(directory, uid, field, spw, width)
        if not (os.path.isfile(filename_visibilities + ".fits") or os.path.isfile(filename_visibilities + ".numpy")):
            export_visibilities(ms=ms_split, filename=filename_visibilities)

        export_antennas(ms=ms_split, filename="{}/antennas_{}_{}_spw_{}_width_{}".format(directory, uid, field, spw, width))
        export_scans(ms=ms_split, filename="{}/scans_{}_{}_spw_{}_width_{}".format(directory, uid, field, spw, width))

    if clean:
        pass


uids = ["A002_Xb9b1b9_X3046", "A002_Xb99cbd_X2456"]
spws = ["1", "2"]
width = 240
for uid in uids:
    main_func(uid=uid, field="G09v1.40", spws=spws, width=width, directory=".", clean=False)
```

## Key facts distilled from the conversation

- Modern workflow: download already-calibrated/reduced data from the ALMA archive (no need to run the ALMA reduction pipeline locally). Download-first should be the default in PyAutoReduce; running extraction on locally-provided measurement sets is the second path.
- ALMA data are delivered as measurement sets (`.ms.split.cal` directories); one per execution block (uid), each typically with 4 spectral windows (spw).
- Extraction pipeline per (uid, spw): CASA `split` to isolate field, then `split` again per spw with channel averaging (`width`; for continuum modelling collapse the whole spw), then read MS tables (`DATA`, `UVW`, `SPECTRAL_WINDOW/CHAN_FREQ`, `ANTENNA1/2`, `TIME`, `SCAN_NUMBER`) via the `tb` tool.
- Outputs per uid per spw: visibilities shape [2, Nvis, 2] (leading 2 = polarizations), uv_wavelengths (UVW meters -> wavelengths via chan_freq/c), antennas, scans, frequencies, times.
- PyAutoLens wants visibilities and uv_wavelengths in shape (Nvis, 2) — polarizations averaged/concatenated across uids and spws before feeding into autolens.
- The script must run inside CASA (`tb`, `split` are CASA globals). Aris runs it via `casa` then `execute("file")`; a python-driven headless CASA invocation should be possible (e.g. modular casatools/casatasks pip packages, or `casa --nogui -c script.py`) — Aris never got this working, worth solving in PyAutoReduce.
- Aris can send further scripts/data; example project 2016.1.00282.S, field G09v1.40.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/f376bea2-dd78-47b9-885c-8ab3e11d743e/scratchpad/alma_intake_raw.md -->
