<p align="center">
    <img src="devcord.png" width=200 height=200>
</p>

## Description
Devcord turns Discord into a code IDE for Python.

---

## Dependencies
- <b>Python 3.8 or higher</b>
- <b>`discord.py-self`</b>
    ```
    $ git clone https://github.com/dolfies/discord.py-self
    $ cd discord.py-self
    $ python3 -m pip install -U .[voice]
    ```

---

## Usage
- <b>Running</b>
    - Download and extract this repository
    - Open the `.env` file and add your discord token after `TOKEN=`
    - `cd` to the root directory of the extracted folder
    - Run `python main.py`
- <b>Folders</b>
    - Creating a channel will create a folder in the root directory of the Devcord source code
- <b>Files</b>
    - Creating a thread in a channel will save a file into the folder bearing the channel's name, and will send a fenced markdown code block into the thread
    - You can write code in the code block - changes will be reflected back to the file
    - To run the file with Python, react to the code block with `⏯️`/`:play_pause:`
