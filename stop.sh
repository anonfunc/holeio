#!/bin/bash

kill $(ps aux | grep [hH]oleio.app | awk '{print $2}')
