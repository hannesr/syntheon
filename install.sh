#!/bin/bash
#............................................
#. Syntheon install script
#. Hannes R.
#............................................

SRC_DIR=.
TARGET_DIR=/opt/syntheon

echo "... checking preconditions"
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

echo "... copying files"
mkdir -p $TARGET_DIR
cp -r $SRC_DIR/systemd $TARGET_DIR
cp -r $SRC_DIR/control $TARGET_DIR
cp -r $SRC_DIR/data $TARGET_DIR

# jack installation
systemctl is-active jack &>/dev/null
if [ $? -ne 0 ]; then
  echo "... installing jack service"
  ln -sf $TARGET_DIR/systemd/jack.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable jack
  systemctl start jack
else
  echo "... jack service already installed"
fi

# rakarrack installation
systemctl is-active rakarrack &>/dev/null
if [ $? -ne 0 ]; then
  echo "... installing rakarrack service"
  # TODO: check if rakarrack configuration is in place
  # if not, create configuration from scratch
  # if it is, edit some keys
  ln -sf $TARGET_DIR/systemd/rakarrack.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable rakarrack
  systemctl start rakarrack
else
  echo "... rakarrack service already installed"
fi

# zynaddsubfx installation
test -f $TARGET_DIR/systemd/zynaddsubfx.service
if [ $? -ne 0 ]; then
  echo "... installing zynaddsubfx service"
  ln -sf $TARGET_DIR/systemd/zynaddsubfx.service /etc/systemd/system/
  systemctl daemon-reload
  # note: service is started manually
else
  echo "... zynaddsubfx service already installed"
fi

# syntheon control process installation
systemctl is-active syntheon &>/dev/null
if [ $? -ne 0 ]; then
  echo "... installing syntheon service"
  test -f $TARGET_DIR/data/syntheon.yaml || \
    cp $TARGET_DIR/data/syntheon.yaml.example $TARGET_DIR/data/syntheon.yaml
  ln -sf $TARGET_DIR/systemd/syntheon.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable syntheon
  systemctl start syntheon
else
  echo "... syntheon service already installed"
fi

echo "... install complete"
