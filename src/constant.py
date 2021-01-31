import os

SPRING = "spring"
SUMMER = "summer"
WINTER = "winter"
FALL = "fall"
# path to the root of the source files
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
CACHE_PATH = SRC_PATH + "/../cache"
SCOPE = "user-library-read playlist-read-private playlist-modify-private playlist-modify-public"
UPDATE_FREQUENCY = 600 # in seconds
DATABASE_NAME = SRC_PATH + "/../database.db"
ERROR_THRESHOLD = 30