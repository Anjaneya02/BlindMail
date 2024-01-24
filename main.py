import speech_recognition as sr
import pyttsx3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def get_user_input(prompt, recognizer, source):
    speak_text(prompt)
    recognizer.adjust_for_ambient_noise(source, duration=0.1)
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio).lower()
    print(f"You said: {text}")
    speak_text(f"You said: {text}")
    return text

def confirm_choice(confirmation_prompt, rejection_prompt, recognizer, choice_source):
    while True:
        try:
            audio = recognizer.listen(choice_source)
            choice = recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            speak_text("Sorry, I didn't catch that. Please speak again.")
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak_text("There was an error processing your request. Please try again.")
            continue

        if "yes" in choice or "confirm" in choice:
            speak_text(confirmation_prompt)
            return True
        elif "no" in choice or "discard" in choice:
            speak_text(rejection_prompt)
            return False
        else:
            speak_text("I didn't understand. Please say yes or no.")

def main():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300

    mail = {}  # Empty dictionary to store email information
    
    while True:
        with sr.Microphone() as source:
            try:
                to_email = get_user_input("Please clearly say aloud the email ID you want to send the message to", recognizer, source)
                speak_text("To confirm the address, say yes or no")
                with sr.Microphone() as choice_source:
                    if confirm_choice("Email ID confirmed.", "Restarting the process.", recognizer, choice_source):
                        to_email = to_email.replace(" ", "")
                        if "attherate" in to_email:
                            to_email = to_email.replace("attherate", "@")
                        mail.update({"To": to_email})
                        print(mail)
                        speak_text("Now, please give the subject of the mail.")
                        break
                    else:
                        continue
            except sr.UnknownValueError:
                speak_text("Unknown error occurred. Please try again.")
                return

    while True:
        with sr.Microphone() as source:
            try:
                subject = get_user_input("Please clearly say aloud the subject of the email", recognizer, source)
                speak_text("To confirm the subject, say yes or no")
                with sr.Microphone() as choice_source:
                    if confirm_choice("Subject confirmed.", "Restarting the process.", recognizer, choice_source):
                        mail.update({"Subject": subject})
                        speak_text("Now, please provide the main body of the mail.")
                        break
                    else:
                        continue
            except sr.UnknownValueError:
                speak_text("Unknown error occurred. Please try again.")
                return

    while True:
        with sr.Microphone() as source:
            try:
                main_body = get_user_input("Please clearly say aloud the main body of the email", recognizer, source)
                speak_text("To confirm the main body, say yes or no")
                with sr.Microphone() as choice_source:
                    if confirm_choice("Main body confirmed.", "Restarting the process.", recognizer, choice_source):
                        mail.update({"Main Body": main_body})
                        speak_text("The email is ready to be sent.")
                        break
                    else:
                        continue
            except sr.UnknownValueError:
                speak_text("Unknown error occurred. Please try again.")
                return

    print("Email Information:")
    print(mail)
    speak_text("sending email please wait")
    Sendmail(mail)
def Sendmail(mail):
        from_address = "anjnaymahajan@gmail.com"
        to_address = mail['To']

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = mail['Subject']
        msg['From'] = from_address
        msg['To'] = to_address

        # Create the message (HTML).
        html = f" {mail['Main Body']}"

        # Record the MIME type - text/html.
        part1 = MIMEText(html, 'html')

        # Attach parts into the message container
        msg.attach(part1)

        # Credentials
        username = 'anjnaymahajan@gmail.com'
        password = 'jxraqsrukjcittsr'

        # Sending the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
if __name__ == "__main__":
    main()
