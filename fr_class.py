import face_recognition
import cv2
import numpy as np
import os

result = ""

def set_result():
    global result
    result = "error"
    return result

def get_result():
    global result
    return result

def identifikasi_wajah():
    # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
    # other example, but it includes some basic performance tweaks to make things run a lot faster:
    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it
    puji_image = face_recognition.load_image_file("images/puji.png")
    puji_face_encoding = face_recognition.face_encodings(puji_image)[0]

    andree_image = face_recognition.load_image_file("images/andree.png")
    andree_face_encoding = face_recognition.face_encodings(andree_image)[0]

    dwi_image = face_recognition.load_image_file("images/dwiputra.png")
    dwi_face_encoding = face_recognition.face_encodings(dwi_image)[0]

    shafa_image = face_recognition.load_image_file("images/shafa.png")
    shafa_face_encoding = face_recognition.face_encodings(shafa_image)[0]

    aldo_image = face_recognition.load_image_file("images/aldo.png")
    aldo_face_encoding = face_recognition.face_encodings(aldo_image)[0]

    firdaus_image = face_recognition.load_image_file("images/firdaus.png")
    firdaus_face_encoding = face_recognition.face_encodings(firdaus_image)[0]
    # Create arrays of known face encodings and their names
    known_face_encodings = [
        puji_face_encoding,
        andree_face_encoding,
        dwi_face_encoding,
        shafa_face_encoding,
        aldo_face_encoding,
        firdaus_face_encoding
    ]
    known_face_names = [
        "Puji",
        "Andree",
        "Dwi",
        "Shafa",
        "Aldo",
        "Firdaus"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    temp_name = ""
    count = 0
    name = ""

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    if (temp_name != name):
                        temp_name = name
                        count = 0
                    else:
                        count = count + 1
                
                face_names.append(name)

                # os.system('cls')

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (127,255,0), 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 8, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        if (count == 5):
            print("absen for " + name + ", has held " + str(count) + "x frame")
            break

        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

        # Display the resulting image
        # cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Release handle to the webcam
    global result
    result = name
    video_capture.release()
    cv2.destroyAllWindows()
    
    