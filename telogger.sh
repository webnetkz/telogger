#!/bin/bash

INSTALL_DIR="/etc/telogger"

BOT_TOKEN="your_bot_token"
CHAT_ID="your_chat_id"

if ! command -v systemctl &> /dev/null; then
    echo "Need Systemd"
    exit 1
fi

if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR"
fi

sudo cp telogger.sh "$INSTALL_DIR/"


echo "Setup systemd service..."
echo "[Unit]
Description=Telegram Logger Service
After=network.target

[Service]
ExecStart=$INSTALL_DIR/telogger.sh
WorkingDirectory=$INSTALL_DIR
StandardOutput=null
StandardError=null
Type=simple
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/telogger.service

sudo systemctl daemon-reload
sudo systemctl enable telogger.service
sudo systemctl start telogger.service

cd ../; sudo rm -rf ./telogger;

echo "Started Telogger"
