import perception_controller as pc
import os
import shutil


"""
Program logic:
1. Establish the folder path for the images that it will use. It will default to specific folder names.
2. Prompt user for information: staring index, ending index, and the trigger number.
    starting index: The starting number for the recording. It will be used as part of the naming for the recording
    ending index: The ending number for the recording. ending - starting will give us how many recordings we will have.
    It will be used as part of the naming for the recording. When we reach the ending index we know we are done 
    recording data
    trigger number: The number of triggered for each recording. This is used to know when to STOP the current recording
    then export.
3. Check if perception is active, if not, make it active
4. Change recording name
5. Start the recording
6. Wait for the trigger amount
7. Once the trigger amount is done, stop the recording
8. Export the data
9. Increment the index
10. If the index is at the ending index, stop the program. If not, go back to step 4.    


increment the index

"""


def set_up_recording_setting():
    # Ask for a starting index to be used as part of the file name
    file_start_index = 0
    file_end_index = 0
    trigger_num = 5

    temp = input("Input the file STARTING INDEX you want to use.\n" +
                 "Press Enter to use the default: {}\n".format(file_start_index))
    if temp != "":
        file_start_index = int(temp)

    # Ask for an ending index to be used to know when testing is complete
    temp = input("Input the file ENDING INDEX you want to use.\n")
    if temp != "":
        file_end_index = int(temp)

    # Ask for the number of triggers expected for the test. This is used to determine when it is ready to export
    temp = input("Input expected number of triggers for each export ranging from 5 - 50.\n")
    if temp != "":
        trigger_num = temp

    return file_start_index, file_end_index, trigger_num


def main():
    app_dir = os.path.dirname(os.path.realpath(__file__))
    trigger_img_dir = os.path.join(app_dir, '../triggers_images')
    perception_img_dir = os.path.join(app_dir, '../perception_images')

    pc.set_up_files(perception_img_dir, trigger_img_dir)

    total, used, free = shutil.disk_usage("/")
    free = free // 2 ** 30

    # Prompt user of the current space on the drive.
    if free < 100:
        print(f'The free space is less than 100 GB (Free Space: {free}GB). "')

    # file_index, end_index, trigger_num = set_up_recording_setting()
    file_index, end_index, trigger_num = 0, 2, "5"

    while file_index < end_index:
        print(file_index)
        # Make sure perception application is active when we start. This will run each loop.
        # pc.make_perception_active()

        # Start the recording
        pc.start_record()

        # We now wait for the trigger number to be reached. There is a timeout of 30 minutes.
        # If it takes longer than 30 minutes to reach the trigger the timeout needs to be changed
        pc.wait_for_trigger(trigger_num)

        # After the trigger amount
        pc.stop_record()

        # Run the exporting sequence
        pc.export_file()

        # pc.change_recording_name(file_index)

        file_index += 1


if __name__ == "__main__":
    main()
