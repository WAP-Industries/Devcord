import sys
sys.dont_write_bytecode = True

from dotenv import load_dotenv
from bot import *

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    load_dotenv()
    Devcord.Bot.run(os.environ.get("TOKEN"))


if __name__=="__main__":
    main()