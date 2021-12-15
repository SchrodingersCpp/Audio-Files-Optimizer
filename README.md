# Audio Files Optimizer

## Description

Helps to reduce the size of your audio files. The script removes all the metadata from input audio files, adds `Title` and `Artist` data, and reduces `kbps` for output audio files.

## How to Use

1. In `getInfo.py` file, change `folder` and `out` variables.
   - `folder` is the path to the folder which contains audio files that are to be processed.
   - `out` is the path to the folder to which an output CSV file will be written.

2. In the output CSV file, change `File Name (new)`,	`Title (new)`, and	`Artist (new)` fields.

   **Notes:**
   - `File Name (new)` requires a basename only (file name without extension) for a processed file. Leave it empty, if the file should not be processed.
   - `Title (new)` is the title of the audio in the file.
   - `Artist (new)` is the artist of the audio in the file.

3. In `audioConverter.py` file, change `infoFile`, `outFolder`, and `outkbps` variables.
   - `infoFile` is the full name of the modified CSV file.
   - `outFolder` is the folder to which processed audio files will be written.
   - `outkbps` is the `kbps` parameter for the processed files.

   **Note:** If `kbps` of an input file is smaller than that of the processed file, `kbps` of original file will be left.
