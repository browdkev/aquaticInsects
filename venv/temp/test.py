import os, time, uuid
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

ENDPOINT = "https://customvisionmacroi-prediction.cognitiveservices.azure.com/"
prediction_key = "d066eee92f694255a041c5633f5929c7"
prediction_resource_id = "/subscriptions/f7100ba6-4602-4e10-9b4a-2717a466db77/resourceGroups/epiic-ml-rg/providers/Microsoft.CognitiveServices/accounts/customvisionmacroi-Prediction"

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

with open(os.path.join ("test", "test_image.jpg"), mode="rb") as test_data:
    results = predictor.detect_image(project.id, publish_iteration_name, test_data)

# Display the results.    
for prediction in results.predictions:
    print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height))