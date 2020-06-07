
def voice_recognition():
    import speech_recognition as sr
    label_file = open('Sample_TFLite_model/labelmap.txt','r')
    
    label_map = label_file.readlines()
    
    item = ''
    while item not in label_map:
    # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Sphinx
        item = r.recognize_sphinx(audio)
        
    return item
    


