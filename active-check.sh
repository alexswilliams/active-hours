#!/usr/bin/env bash

now=$(/bin/date +"%Y-%m-%d %H:%M")

if [ $(uname -p) == "arm" ]; then

  # Apple Silicon:
  # 0 when asleep, non-zero when displaying
  brightness=$(/usr/sbin/ioreg -lw0 -n disp0 -r AppleCLCD2 -c AppleCLCD2 | /usr/bin/grep IOMFBBrightnessLevelIDAC | /usr/bin/sed 's/^.*"IOMFBBrightnessLevelIDAC" = \([0-9][0-9]*\).*$/\1/' | /usr/bin/head -n 1)
  if [ $brightness == "0" ]; then
    screen_state=0
  else
    screen_state=4
  fi
  echo "apple,$now,$screen_state,$brightness"

else

  # Intel:
  # 4 = awake, 1 = asleep, 0 = off
  screen_state=$(/usr/sbin/ioreg -w0 -cIODisplayWrangler -r IODisplayWrangler | /usr/bin/grep CurrentPowerState | /usr/bin/sed 's/^.*"CurrentPowerState"=\([0-9][0-9]*\)[^0-9].*$/\1/' | /usr/bin/head -n 1)
  echo "intel,$now,$screen_state"

fi


