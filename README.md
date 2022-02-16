# hbm-perception-controller


Automated Windows GUI control for the HBM GEN3 Perception Application

Note: This should be ran in the command prompt/terminal 

This project was created to automate the controls of the perception applcation ran on the GEN3 from HBM.
It leverage Python and several Python libraries to look for images on the screen, and control the mouse and keyboard as a response.

The image files are used as what to look for when running the perception application.


The project is a bit messy but this was cleaned up slight as record keeping. Overall, it works well after the list of assumptions are created:
1. The first recorded file name is already set. Usually followed a specific format that is changed in the update_recording_file function.
2. The export settings is already set to the desired export. For our case, it was exported to .mat file with a specific sample rate.
3. The Perception Icons and appearance remain the same due to the images being used.

Potential future updates:
1. Create a more robust timeout feature to timeout when searching for images
2. Make into GUI application rather than script ran in a terminal


