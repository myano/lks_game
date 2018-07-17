#!/usr/bin/env bash

## This will set up every user on the system with a 'game' folder and the appropriate permissions

#if [[ $EUID -ne 0 ]]; then
    #/bin/mkdir -p /home/$USER/game
    #/bin/chgrp -R game /home/$USER/game
    #/bin/chmod -R g+rs /home/$USER/game
#fi

for user in /home/* ; do
    #if [[ -d $user && ! -d $user/game ]]; then
        ## Create their game folder
    echo $user
    arrIN=(${user//\// })
    echo ${arrIN[1]}:game

    /bin/mkdir -p $user/game
    /bin/chown -R ${arrIN[1]}:game $user/game
    /bin/chmod -R g+rs $user/game
    /bin/chmod -R o-rwx $user/game
    echo
    #fi
done

#mkdir -i -p ~/game/
#chgrp game ~/game/
#chmod -R r+w ~/game/

