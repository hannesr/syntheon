#!/bin/bash
#............................................
#. Syntheon install script
#. Hannes R.
#............................................

SRC_DIR=.
TARGET_DIR=/opt/syntheon

# check preconditions
if [ $(id -u) -ne 0 ]; then
  echo "Script must be run as root"
  exit 1
fi
dpkg -s jackd2 &>/dev/null
if [ $? -ne 0 ]; then
  echo "Jack is not installed"
  exit 1
fi
dpkg -s rakarrack &>/dev/null
if [ $? -ne 0 ]; then
  echo "Rakarrack is not installed"
  exit 1
fi
pidof systemd &>/dev/null
if [ $? -ne 0 ]; then
  echo "System is not running systemd, therefore not compatible"
  exit 1
fi

# copy files
mkdir -p $TARGET_DIR
cp -r $SRC_DIR/systemd $TARGET_DIR
cp -r $SRC_DIR/control $TARGET_DIR
mkdir -p $TARGET_DIR/data

# jack installation
systemctl is-active jack &>/dev/null
if [ $? -ne 0 ]; then
  ln -sf $TARGET_DIR/systemd/jack.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable jack
  systemctl start jack
fi

# rakarrack installation
systemctl is-active rakarrack &>/dev/null
if [ $? -ne 0 ]; then
  # TODO: check if rakarrack configuration is in place
  # if not, create configuration from scratch
  # if it is, edit some keys
  ln -sf $TARGET_DIR/systemd/rakarrack.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable rakarrack
  systemctl start rakarrack
fi

# zynaddsubfx installation
systemctl is-active zynaddsubfx &>/dev/null
if [ $? -ne 0 ]; then
  ln -sf $TARGET_DIR/systemd/zynaddsubfx.service /etc/systemd/system/
  systemctl daemon-reload
  # note: service is started manually
fi
