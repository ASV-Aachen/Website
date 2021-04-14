#!/bin/sh

apt install cron
systemctl enable cron

cp InitFiles/cron/cronJobs /var/spool/cron/cronJobs

