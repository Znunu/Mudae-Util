## Install
1. Download the [EzMudae.py](https://github.com/Znunu/EzMudae/blob/master/EzMudae.py) file and place it in the root with the rest of the files
2. Modify main.py to include your token and prefix
3. In data.json modify the following fields:
    - **server** id of your server
    - **channel** id of your mudae channel
    - **role** if of your mudae role
4. Note the time between each roll reset (RM) and claim reset (CM)
5. Note the time until next roll reset (RR) and claim reset (CR)
6. Run `python -m EzMudae --rr RR --cr CR --rm RM --cm CM` with the values noted from earlier 
7. Note the value printed (The value will change every time you run the command, this is normal)
8. In data.json modify the **timing** field with your newly attained value
9. You can now start the bot

## Starting the bot
Run `python -m main` to start the bot
