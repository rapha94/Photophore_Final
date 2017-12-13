import cv2

## Documentation checkBox function
#  @param path1 path of the first image
#  @param path2 path of the second image
#
#   Method that returns distance between given images
def distance(path1,path2):
    img1 = cv2.imread(path1, 0)
    img2 = cv2.imread(path2, 0)

    surf = cv2.xfeatures2d.SURF_create(400)

    kp1, des1 = surf.detectAndCompute(img1,None)
    kp2, des2 = surf.detectAndCompute(img2,None)


    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    all_matches =len(matches)
    good_matches = len(good)
    pourcentage_matching = good_matches*100/all_matches
    return pourcentage_matching

