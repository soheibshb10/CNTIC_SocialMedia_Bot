from instagrapi import Client
from tempfile import NamedTemporaryFile
import os


def login_instgram(Credentials):
    username = Credentials[0]
    password = Credentials[1]
    client = Client()
    client.login(username, password)
    return client


def sendStory(Credentials, photo_data):
    print("Inside sendStory")
    print("type:", type(photo_data))
    client = login_instgram(Credentials)

    # Check if photo_data is a string (file path) or bytes
    if isinstance(photo_data, str):
        # If it's a string (file path), use it directly
        client.photo_upload_to_story(path=photo_data)
        return 1
    elif isinstance(photo_data, bytes):
        # If it's bytes, create a temporary file and upload it
        suffixes = [".jpg", ".png"]
        for suffix in suffixes:
            with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(photo_data)

            client.photo_upload_to_story(path=temp_file.name)

            os.remove(temp_file.name)  # Remove the temporary file
            return 1
    else:
        print("Unsupported photo_data format")
        return -1


# Example usage:
# sendStory(Credentials, "path_to_photo.jpg")  # Pass a file path
# sendStory(Credentials, bytes_data)  # Pass bytes data


def sendPost(Credentials, photo_path, ph_caption="instgram post #instgram_boot"):
    client = login_instgram(Credentials)

    if isinstance(photo_path, str):
        media = client.photo_upload(path=photo_path, caption=ph_caption)

    elif isinstance(photo_path, bytes):
        with NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(photo_path)

            media = client.photo_upload(path=temp_file.name, caption=ph_caption)

        os.remove(temp_file.name)  # Remove the temporary file
        return 1

    else:
        print("Unsupported photo_data format")
        return -1

    # usertags=


# try:
# with open("credential.txt", "r") as f:
#     username, password = f.read().strip().split(" ")
# ph_path = "test.jpg"
# ph_caption = "cntic_test #instgram_boot"
# client = Client()
# client.login(username, password)

# media = client.photo_upload(
#     path=ph_path,
#     caption=ph_caption
#     # usertags=
# )

# client.photo_upload_to_story(path=ph_path)

# except Exception as e:
#     print(f"An error occurred: {e}")
# hashtag="programming"
# medias=client.hashtag_medias_recent(hashtag)
