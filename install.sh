#/bin/bash!
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

if [ -f /opt/3c/main.py ];
then
   echo "Already installed... Re-installing."
   echo "You can (probably) ignore any rm errors."
   rm -rf /opt/3c/
   rm /bin/3c
   rm /usr/share/applications/3c.desktop
   mkdir /opt/3c
   cp -rf * /opt/3c/
   cp 3c /bin/
   chmod +x /bin/3c
   cp 3c.desktop /usr/share/applications/
   echo "Finished."
else
   echo "Installing 3C"
   mkdir /opt/3c
   cp -rf * /opt/3c
   cp 3c /bin/
   chmod +x /bin/3c
   cp 3c.desktop /usr/share/applications/
   echo "Finished"
fi
