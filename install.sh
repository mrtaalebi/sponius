#!/bin/bash


sudo pip install -r requirements.txt

echo ""
echo "sponus is spotify + genius"
echo ""

sudo mkdir -p /etc/sponus/
sudo cp sponus.py /etc/sponus/

sudo tee /usr/bin/sponus << EOF
#!/bin/bash
python3 /etc/sponus/sponus.py
EOF
sudo chmod +x /usr/bin/sponus

echo ""
echo "successfully installed sponus"
echo "just type \`sponus\` when listening to spotify"
echo "enjoy!"
echo ""

