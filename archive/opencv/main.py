from __future__ import print_function
import sys
import cv2
from random import randint
import argparse
# /ocean/projects/cis220010p/wzhangk/cv_project/py-MDNet/results/20200805_OneSharkSUPFollowsKids_humans/results.json

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]:
    tracker = cv2.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)

  return tracker

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=str, help='folder with the video frames')
    parser.add_argument('inital_bboxes', type=str, help='json file with the inital bounding boxes')
    parser.add_argument('--tracker', '-t', default=trackerTypes[0], help='type of tracker')

    args = parser.parse_args()


    # Create a video capture object to read videos
    cap = cv2.VideoCapture(args.video)

    # Read first frame
    success, frame = cap.read()
    # quit if unable to read the video file
    if not success:
      print('Failed to read video')
      sys.exit(1)
    
    with open(args.inital_bboxes) as f:
      json_contents = json.load(f)
    
    # ## Select boxes
    # bboxes = []
    # colors = []

    # # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
    # # So we will call this function in a loop till we are done selecting all objects
    # while True:
    #   # draw bounding boxes over objects
    #   # selectROI's default behaviour is to draw box starting from the center
    #   # when fromCenter is set to false, you can draw box starting from top left corner
    #   bbox = cv2.selectROI('MultiTracker', frame)
    #   bboxes.append(bbox)
    #   colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    #   print("Press q to quit selecting boxes and start tracking")
    #   print("Press any other key to select next object")
    #   k = cv2.waitKey(30) & 0xFF
    #   if (k == 113):  # q is pressed
    #     break

    # print('Selected bounding boxes {}'.format(bboxes))
    

    # Specify the tracker type
    trackerType = upper(args.tracker)

    # Create MultiTracker object
    multiTracker = cv2.MultiTracker_create()

    # Initialize MultiTracker
    for bbox in bboxes:
      multiTracker.add(createTrackerByName(trackerType), frame, bbox)

    # Process video and track objects
    while cap.isOpened():
      success, frame = cap.read()
      if not success:
        break

      # get updated location of objects in subsequent frames
      success, boxes = multiTracker.update(frame)

      # draw tracked objects
      for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

      # show frame
      cv2.imshow('MultiTracker', frame)

      # quit on ESC button
      if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break

