import os
import numpy as np
import cv2
import argparse

# Parse all arguments
parser = argparse.ArgumentParser(
    description='Thermal screening demo by Codevector Labs.')
parser.add_argument('-t', '--threshold_temperature', dest='threshold_temperature', default=100.5, type=float,
                    help='Threshold temperature in Farenheit (float)', required=False)
parser.add_argument('-b', '--binary_threshold', dest='binary_threshold', default=200, type=int,
                    help='Threshold pixel value for binary threshold (between 0-255)', required=False)
parser.add_argument('-c', '--conversion_factor', dest='conversion_factor', default=2.25, type=float,
                    help='Conversion factor to convert pixel value to temperature (float)', required=False)
parser.add_argument('-a', '--min_area', dest='min_area', default=2400, type=int,
                    help='Minimum area of the rectangle to consider for further porcessing (int)', required=False)
parser.add_argument('-i', '--input_video', dest='input_video', default=os.path.join("data", "input.mp4"), type=str,
                    help='Input video file path (string)', required=False)
parser.add_argument('-o', '--output_video', dest='output_video', default=os.path.join("output", "output.avi"), type=str,
                    help='Output video file path (string)', required=False)
parser.add_argument('-f', '--fps', dest='fps', default=15, type=int,
                    help='FPS of output video (int)', required=False)

args = parser.parse_args().__dict__


def convert_to_temperature(pixel_avg):
    """
    Converts pixel value (mean) to temperature (farenheit) depending upon the camera hardware
    """
    return pixel_avg / args['conversion_factor']


def process_frame(frame):

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    heatmap_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    heatmap = cv2.applyColorMap(heatmap_gray, cv2.COLORMAP_HOT)

    # Binary threshold
    _, binary_thresh = cv2.threshold(
        heatmap_gray, args['binary_threshold'], 255, cv2.THRESH_BINARY)

    # Image opening: Erosion followed by dilation
    kernel = np.ones((5, 5), np.uint8)
    image_erosion = cv2.erode(binary_thresh, kernel, iterations=1)
    image_opening = cv2.dilate(image_erosion, kernel, iterations=1)

    # Get contours from the image obtained by opening operation
    contours, _ = cv2.findContours(image_opening, 1, 2)

    image_with_rectangles = np.copy(heatmap)

    for contour in contours:
        # rectangle over each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Pass if the area of rectangle is not large enough
        if (w) * (h) < args['min_area']:
            continue

        # Mask is boolean type of matrix.
        mask = np.zeros_like(heatmap_gray)
        cv2.drawContours(mask, contour, -1, 255, -1)

        # Mean of only those pixels which are in blocks and not the whole rectangle selected
        mean = convert_to_temperature(cv2.mean(heatmap_gray, mask=mask)[0])

        # Colors for rectangles and textmin_area
        temperature = round(mean, 2)
        color = (0, 255, 0) if temperature < args['threshold_temperature'] else (
            255, 255, 127)

        # Callback function if the following condition is true
        if temperature >= args['threshold_temperature']:
            # Call back function here
            cv2.putText(image_with_rectangles, "High temperature detected!!!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

        # Draw rectangles for visualisation
        image_with_rectangles = cv2.rectangle(
            image_with_rectangles, (x, y), (x+w, y+h), color, 2)

        # Write temperature for each rectangle
        cv2.putText(image_with_rectangles, "{} F".format(temperature), (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

    return image_with_rectangles


def main():
    """
    Main driver function
    """
    video = cv2.VideoCapture(args['input_video'])
    video_frames = []

    while True:
        ret, frame = video.read()

        if not ret:
            break

        # Process each frame
        frame = process_frame(frame)
        height, width, _ = frame.shape
        video_frames.append(frame)

        # Show the video as it is being processed in a window
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    # Save video to output
    size = (height, width)
    out = cv2.VideoWriter(args['output_video'],
                          cv2.VideoWriter_fourcc(*'DIVX'), args['fps'], size)
    for i in range(len(video_frames)):
        out.write(video_frames[i])
    out.release()


if __name__ == "__main__":
    main()
