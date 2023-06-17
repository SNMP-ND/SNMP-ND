# SNMP Network Discovery 🔎

## Summary
- [Installing the dependencies](#install-the-necessary-dependencies)
- [Configure the trap receiver](#configure-the-trap-receiver)
- [Usage](#usage)

## Install the necessary dependencies 📦

### Using pip
```bash
pip install -r requirements.txt
```

### Using pipenv
```bash
pipenv install && pipenv shell
```

## Configure the trap receiver ⚙️ 

### Copy the traps configuration and handler file
```bash
cd traps
# Copy the configuration files
sudo cp snmptrapd.conf /etc/snmp
sudo cp snmpd.conf /usr/share/snmp

# Copy the trap handler
sudo mkdir /etc/snmp/scripts
sudo cp trap_handler.sh /etc/snmp/scripts
sudo chmod +x /etc/snmp/scripts/trap_handler.sh
```

### Start the snmpd and snmpdtrapd services
```bash
sudo systemctl start snmpd
sudo systemctl start snmptrapd
```

## Usage 📕
```bash
python main.py <community> <ip>
```
