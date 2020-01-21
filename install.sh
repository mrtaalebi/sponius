#!/bin/bash


sudo pip3 install -r requirements.txt

echo ""
echo "sponius is spotify + genius"
echo ""

sudo mkdir -p /etc/sponius/
sudo cp sponius.py /etc/sponius/

sudo tee /usr/local/bin/sponius << EOF
#!/bin/bash
python3 /etc/sponius/sponius.py
EOF
sudo chmod +x /usr/local/bin/sponius

echo ""
echo "successfully installed sponius"
echo "just type \`sponius\` when listening to spotify"
echo "enjoy!"
echo ""

