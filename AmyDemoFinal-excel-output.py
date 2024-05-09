import cv2
from gaze_tracking import GazeTracking
from datetime import time
import time
import threading
import os
import pyautogui
import pandas as pd

def eye_tracking_and_presentation():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    start_time = time.time()
    total_left_time = 0
    total_left_count = 0
    total_right_time = 0
    total_right_count = 0
    data = {'Timestamp': [], 'Direction': [], 'Time Spent': []}
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
            total_right_time += time.time() - start_time
            total_right_count += 1
            data['Direction'].append('Right')
            data['Time Spent'].append(time.time() - start_time)
            data['Timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        elif gaze.is_left():
            text = "Looking left"
            total_left_time += time.time() - start_time
            total_left_count += 1
            data['Direction'].append('Left')
            data['Time Spent'].append(time.time() - start_time)
            data['Timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        elif gaze.is_center():
            text = "Looking center"
        start_time = time.time()

        cv2.putText(frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()  # Close the OpenCV window after the loop ends

    # Create a DataFrame from the collected data
    current_df = pd.DataFrame(data)

    # Create a summary DataFrame
    summary_data = {
        'Total Left Time': [total_left_time],
        'Total Right Time': [total_right_time],
        'Total Left Count': [total_left_count],
        'Total Right Count': [total_right_count],
        'Finish Time': [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]
    }
    summary_df = pd.DataFrame(summary_data)

    # Write both DataFrames to separate sheets in an Excel file
    with pd.ExcelWriter('c:\Amy\eye_tracking_results.xlsx') as writer:
        current_df.to_excel(writer, sheet_name='Current Data', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

    print("Data has been saved to eye_tracking_results.xlsx")

    print("Total time spent looking left:", total_left_time)
    print("Total time spent looking right:", total_right_time)
    print("Total counts looking left:", total_left_count)
    print("Total counts looking right:", total_right_count)

def open_powerpoint(file_path):
    os.startfile(file_path)
    time.sleep(1)  # Wait for PowerPoint to open

    # Maximize PowerPoint window (Windows shortcut: Alt + Space, then press x)
    pyautogui.hotkey('alt', 'space')
    pyautogui.press('x')
    time.sleep(1)  # Wait for window to maximize

    # Play presentation (F5)
    pyautogui.hotkey('f5')
    time.sleep(1)  # Wait for presentation to start

    slides_count = 0
    while slides_count < 9:  # Assuming there are 9 slides, adjust this according to your presentation
        if slides_count < 5:
            time.sleep(3)  # Assuming each slide lasts for 3 seconds, adjust this as needed
        elif slides_count == 8:
            time.sleep(0.5)  # Assuming the last slide lasts for 0.5 seconds, adjust this as needed
        else:
            time.sleep(12)  # Assuming each slide lasts for 15 seconds, adjust this as needed
        pyautogui.press('right')  # Navigate to the next slide
        slides_count += 1

    # Close PowerPoint presentation (Alt + F4)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)  # Wait for PowerPoint to close



if __name__ == "__main__":
    powerpoint_file = r"c:\Amy\TestCase.pptx"  # Change this to the path of your PowerPoint file

    # Create a thread for running eye tracking and presentation concurrently
    eye_tracking_thread = threading.Thread(target=eye_tracking_and_presentation)
    PPT_thread = threading.Thread(target=open_powerpoint, args=(powerpoint_file,))

    # Start the eye tracking and presentation thread
    eye_tracking_thread.start()
    PPT_thread.start()

    # Wait for the eye tracking thread to finish
    eye_tracking_thread.join()

    cv2.destroyAllWindows()
