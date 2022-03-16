from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")
ap.add_argument("-r", "--result-path", required = True,
	help = "Path to the result path")
args = vars(ap.parse_args())

#os.system('index.py --dataset C:\Users\TalGeva\Downloads\TestImages --index C:\Users\TalGeva\Downloads\Index\index.csv')

cd = ColorDescriptor((8, 12, 3))

query = cv2.imread(args["query"])
features = cd.describe(query)
searcher = Searcher(args["index"])
results = searcher.search(features)
cv2.imshow("Query", query)
print(results[0])

#for (score, resultID) in results:
#	result = cv2.imread(args["result_path"] + "/" + resultID)
#	cv2.imshow("Result", result)
#	cv2.waitKey(0)

