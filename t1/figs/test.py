import optparse

parser = optparse.OptionParser()

parser.add_option('-q', '--query',
    action="store", dest="query",
    help="query string", default="spam")

options, args = parser.parse_args()

print('Query string:', options.query)
# import numpy as np
# import cv2
# from scipy.misc import imshow
#
# width = 32
# height = 32
# bottomLeftCornerOfText = (height//2, width//2)
# font = cv2.FONT_HERSHEY_COMPLEX
# fontScale = .6
# fontColor = 255
# lineType = 1
# text = "9"
#
# img = np.zeros((height, width), dtype=np.uint8)
# textSize, _ = cv2.getTextSize(text, font, fontScale, lineType)
#
# bottomLeftCornerOfText = (int((width-textSize[0])/2), int((height+textSize[1])/2))
# cv2.putText(img, text,
#     bottomLeftCornerOfText,
#     font,
#     fontScale,
#     fontColor,
#     lineType)
#
# imshow(img)
