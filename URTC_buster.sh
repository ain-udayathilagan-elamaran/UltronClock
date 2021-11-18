mkdir -p /home/pi/URTC



chown -R pi:pi /home/pi/URTC

ServiceFile=/etc/systemd/system/URTC.service


echo '[Unit]'>$ServiceFile
echo 'Description=Ultron Clock'>>$ServiceFile
echo ''>>$ServiceFile
echo '[Service]'>>$ServiceFile
echo 'WorkingDirectory=/home/pi/URTC'>>$ServiceFile
echo 'Environment="TERM=xterm"'>>$ServiceFile
echo 'ExecStart=/home/pi/URTC/new_rtc'>>$ServiceFile
echo 'Restart=on-failure'>>$ServiceFile
echo ''>>$ServiceFile
echo '[Install]'>>$ServiceFile
echo 'WantedBy=default.target'>>$ServiceFile



systemctl daemon-reload
systemctl enable URTC.service


sudo wget  -O /home/pi/URTC/log.conf  https://files.aparinnosys.com/s/32gcK32C69wMjdc/download

sudo wget  -O /home/pi/URTC/new_rtc https://files.aparinnosys.com/s/MEzG7w7rydYH5GH/download
sudo chmod +x /home/pi/URTC/new_rtc



echo "done"

sudo systemctl restart URTC.service