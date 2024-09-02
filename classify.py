import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

def load_model(model_path):
    """
    Load the entire pre-trained model from the specified path.
    
    Args:
    model_path (str): The path to the saved model.

    Returns:
    model: Loaded TensorFlow model.
    """
    model = tf.keras.models.load_model(model_path)
    return model

def predict_image(model, img_path):
    """
    Predict the class of an input image using the pre-trained model.
    
    Args:
    model: Pre-trained TensorFlow model.
    img_path (str): Path to the image file.
    
    Returns:
    predicted_class (str): The predicted class label for the image.
    predicted_prob (float): The confidence level of the prediction.
    """
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Make a prediction
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction[0])
    predicted_prob = prediction[0][predicted_class_index]

    # Class names corresponding to the indices (update these as per your model)
    class_names = ['Abrasions', 'Bruises', 'Burns', 'Cut', 'Ingrown_nails', 'Laceration', 'Stab_wound']

    # Get the predicted class
    predicted_class = class_names[predicted_class_index]

    return predicted_class, predicted_prob
# Example usage
model_path = 'my_full_model.h5'  # Path to your saved model
img_path = 'Wound_dataset/Ingrown_nails/ingrown_nail (13).jpg'  # Example image path
# Load the model
model = load_model(model_path)
# Predict the class of the image
predicted_class, predicted_prob = predict_image(model, img_path)
# Print the result
print(f"Predicted class: {predicted_class}")
print(f"Confidence level: {predicted_prob:.2f}")
