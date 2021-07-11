import sys
sys.path.append('../')

from flask import Blueprint
from imageRecommender.models import Galleryimages, Imagerecommendations
from imageRecommender import db 
import os
import pickle
from numpy.testing import assert_almost_equal

global numRec
numRec = 6  # TODO: MANUALLY UPDATE NEEDED

def getNames(inputName, similarNames, similarValues):
    images = list(similarNames.loc[inputName, :])
    values = list(similarValues.loc[inputName, :])
    if inputName in images:
        assert_almost_equal(max(values), 1, decimal = 5)
        images.remove(inputName)
        values.remove(max(values))
    return inputName, images[0:numRec], values[0:numRec]


def getImages(inputImage):
    similarNames = pickle.load(open(os.path.join("imageRecommender/static/pickles/similarNames.pkl"), 'rb'))
    similarValues = pickle.load(open(os.path.join("imageRecommender/static/pickles/similarValues.pkl"), 'rb'))
    
    if inputImage in set(similarNames.index):
        return getNames(inputImage, similarNames, similarValues)
    else:
        print("'{}' was not found.".format(inputImage))
        sys.exit(2)

cmd = Blueprint('db', __name__)

@cmd.cli.command('createDB')
def createDB():
    db.create_all()

@cmd.cli.command('dropDB')
def dropDB():
    db.drop_all() 

@cmd.cli.command('importDB')
def importDB():
    images = pickle.load(open(os.path.join("imageRecommender/static/pickles/image_dict"), 'rb'))

    for image in images:
        img = Galleryimages(imageName=image['name'], imageDescription=image['caption'])
        #print(img)
        db.session.add(img)
        db.session.commit()

        inputImage, images, values = getImages(image['name'])
        recArray = []
        for j in range(0, numRec):
            rec = Imagerecommendations(recommendedID = img.id, recommendedName=images[j], similarityValue=values[j])
            #print(rec)
            db.session.add(rec)

        db.session.commit()
    db.session.close() 

# print('Query all')
# allI=Galleryimages.query.all()
# print(allI)
# print(allI[0].imageName)
# print(allI[0].imageDescription)