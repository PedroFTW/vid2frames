import argparse
import os
import random
import sys
import uuid

import cv2 as cv


def get_args():
    parser  = argparse.ArgumentParser(description='Grab random frames from a video file')
    parser.add_argument('-f', '--filepath', type=str, required=True, help='Path to video file')
    parser.add_argument('-q', '--quantity', type=int, required=False, default=100, help='Amount of frames to generate from the video')
    parser.add_argument('-o', '--outputdir', type=str, required=False, default='./', help='Output directory for the frames')

    return parser.parse_args()

def get_frames(filepath: str, quantity: int, outputdir: str):
    if not os.path.isfile(filepath):
        print(f"Can't find file: {filepath} does not exist")
        sys.exit(1)

    if not os.path.isdir(outputdir):
        print(f"Can't find output directory: {outputdir} does not exist")
        sys.exit(1)

    capture = cv.VideoCapture(filepath)
    frame_count = int(capture.get(cv.CAP_PROP_FRAME_COUNT))

    if frame_count < quantity:
        print("The video's frame count is lower than the quantity")
        print(f"Video's frame count: {frame_count}, requested quantity: {quantity}")
        sys.exit(1)

    random_numbers = random.sample(range(0, frame_count), quantity)

    for i in range(0, len(random_numbers)):
        progress = (i / len(random_numbers)) * 100
        sys.stdout.write(f"\r{progress:.1f}% complete")
        random_frame = random_numbers[i]
        capture.set(cv.CAP_PROP_POS_FRAMES, random_frame)
        success, frame = capture.read()
        if success:
            cv.imwrite(f"{outputdir}/frame_{uuid.uuid4()}.jpg", frame)

    sys.stdout.write(f"\r{100:.1f} % complete")

def main():
    args = get_args()
    get_frames(args.filepath, args.quantity, args.outputdir)
    print()