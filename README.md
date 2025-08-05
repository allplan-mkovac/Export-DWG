BatchExportDWG
This script is designed for batch exporting drawings to DWG format within the Allplan environment using PythonParts.

Script Features
Scans a folder containing XML files (which describe favourites for selected drawings - by default it is folder ...prj/your project/bim/rematrice).

Automatically loads, activates, and exports the required drawings based on the state and activation values found in the XML.

Saves the resulting DWG files into a specific output directory (by default c:/output), organized to subfolders by project name and timestamp.

Main Features:
Compatible with Allplan 2026.
Integrates with the Allplan property palette and actionbar.
Allows saving and loading of favorite parameter sets (favorites).
Input XML files with the correct structure describing drawing layers.

Usage:
Run the script from library (library/office/allplan-cz/batchexport) or via actionbar (plugin can be found under plugin section in configuration of actionbar).

In the user interface user can select the *.NTH for export configuration.
In the user interface, select the folder with input XML files.
Select aoutput folder.
After pressing the action button, all XML files will be processed and the corresponding DWG files will be exported into the target directory.

Successful export is confirmed with a message.

Contact
For questions or bug reports, please contact Allplan Česko hotline at support.cz@allplan.com
