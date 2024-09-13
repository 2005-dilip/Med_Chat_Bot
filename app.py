
from flask import Flask, render_template, request, jsonify
import os
import json
from werkzeug.utils import secure_filename
from gpt import med_bot, wound_bot
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

wound_dict = {
    'Abrasions': 'Abrasions',
    'Bruises': 'Bruises',
    'Burns': 'Burns',
    'Cut': 'Cut',
    'Ingrown_nails': 'Ingrown Nails',
    'Laceration': 'Laceration',
    'Stab_wound': 'Stab Wound'
}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat():
    if request.content_type == 'application/json':
        user_message = request.json.get('message')
        bot_message = med_bot(user_message=user_message)
        print(bot_message)
        return bot_message
    else:
        print("Hi")
        print(request.json.get('message'))
        return jsonify({"response": "Unsupported media type"}), 415


@app.route('/wound-detection', methods=['POST'])
def wound_detection():
    # Ensure that the Content-Type is multipart/form-data
    if 'multipart/form-data' in request.content_type:
        user_message = request.form.get('message')
        image_file = request.files.get('image')

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            from main import predict_image
            image_data = predict_image()
            list_of_aids = wound_bot(wounds=image_data)

            bot_message = (
                f"The Image is Recognised as:{wound_dict[image_data]}\n The First Aid Steps are:\n"
                f"{list_of_aids[0]}\n"
                f"{list_of_aids[1]}\n"
                f"{list_of_aids[2]}\n"
                f"{list_of_aids[3]}\n"
                f"{list_of_aids[4]}"
            )

        else:
            bot_message = "No valid image uploaded. Processing wound detection..."

        return jsonify({"response": bot_message})
    else:
        return jsonify({"response": "Unsupported media type"}), 415


@app.route('/custom-feature', methods=['POST'])
def custom_feature():
    if request.content_type == 'application/json':
        user_message = request.json.get('message')  # Change from request.form.get to request.json.get
        print(user_message)
        from qa_model import qa_chain
        result = qa_chain(user_message)
        return jsonify({"response": result})
    else:
        return jsonify({"response": "Unsupported media type"}), 415



if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/get", methods=["GET", "POST"])
# def chat():
#     msg = request.form["msg"]
#     print("User input:", msg)
#     result = qa_chain(msg)
#     print(result)
#     return result
    # # Process response to include a random doctor recommendation
    # a = len(result)
    # for i in range(a):
    #     if i >= (a / 2):
    #         if result[i] == '.':
    #             b = result[:i]
    #             break
    # else:
    #     b = result

    # Sample data for doctors


    # Creating DataFrame


    # # Function to convert a DataFrame row to a string
    # def doctor_to_string(row):
    #     return f"Name: {row['Name']}, Location: {row['Location']}, Contact: {row['Contact']}"
    #
    # # Example usage
    #
    # return str(b)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
