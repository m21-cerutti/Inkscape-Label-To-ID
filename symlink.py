from pathlib import Path
import os

# Windows only and run as admin
files  = [
    Path( "label_to_id.inx" ), 
    Path( "label_to_id.py" )
    ]

dest = Path(os.getenv('APPDATA'))/r"inkscape\extensions"
for file in files:
    path = dest/file
    path.symlink_to(file.absolute())
