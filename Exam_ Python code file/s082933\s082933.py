import json

from os import walk
from os import path


def parse_dir(my_dir):
    """
    @param my_dir: string representing a path
    @return: a tuple with two lists. One containing file names and the other containing the files path
    """
    dir_list = []
    for file in walk(my_dir):
        for f in file[2]:
            dir_list.append(path.join(file[0], f))

        return dir_list, file[2]

def build_objects(my_dir, rating=0, tags=None):
    """
    @param my_dir: string representing a path
    @param rating: an int representing a rating
    @param tags: a list of tags
    @return: a list of Video objects
    """
    if not tags: tags = []
    dirs, files = parse_dir(my_dir)

    video_objects = []
    count = 0
    for file in files:
        video_objects.append(Video(file, rating, dirs[count], tags))
        count += 1

    return video_objects

def save_content_to_disk(data, place):
    with open(place, 'w') as file:
        file.write(data)

class Video:
    """
    Represents a video where you can give a rating and tags to the video.
    It will also contain the path to the video and the file name.
    """

    def __init__(self, file, rating, video_path, tags=None):
        if not tags: tags = []
        self.file = file
        self.rating = rating
        self.video_path = video_path
        self.tags = tags

    def change_rating(self, rating = 0):
        self.rating = rating

    def add_tag(self, tag = ""):
        self.tags.append(tag)

    def del_tag(self, name):
        self.tags.remove(name)

    def print_attributes(self):
        print("file is:", self.file)
        print("rating is:", self.rating)
        print("path to video is:", self.video_path)
        print("file tags are:", self.tags)

class VideoJsonEncoder(json.JSONEncoder):
    """
    Convert a object of instance video to json.
    """
    def default(self, o):
        if isinstance(o, Video):
            return [o.file, o.rating, o.video_path, o.tags]
        return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    video1 = build_objects("c:\\test")

    video1[0].print_attributes()
    print("")
    video1[1].print_attributes()
    print("")
    video1[2].print_attributes()
    print("")

    json_encoded_data = VideoJsonEncoder().encode(video1[2])
    json_decoded_data = json.loads(json_encoded_data)

    print("Json encoded data:", json_encoded_data)
    print("json decoded data:", json_decoded_data)
    print("")
    print("Convert json data to objects and print the attributes:")
    video2 = Video(json_decoded_data[0], json_decoded_data[1], json_decoded_data[2], json_decoded_data[3])
    video2.print_attributes()

    save_content_to_disk(json_encoded_data, "c:\\test\\jsondata.json")