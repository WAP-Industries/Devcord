<p align="center">
    <img src="devcord.png" width=300 height=300>
</p>

## Description
Devcord turns Discord into a code IDE for Python.

## Dependencies
- `discord.py-self`
    ```
    $ git clone https://github.com/dolfies/discord.py-self
    $ cd discord.py-self
    $ python3 -m pip install -U .[voice]
    ```

## Usage
- Folders
    - Creating a channel will create a folder in the root directory of the Devcord source code
- Files
    - Creating a thread in a channel will save a file into the folder with the channel name
    - This will automatically send a markdown code block into the thread
    - To run the file with Python, react to the code block with `⏯️`
