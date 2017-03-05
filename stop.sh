#!/bin/bash

kill $(ps a | grep [hH]oleio.app | awk '{print $1}')
