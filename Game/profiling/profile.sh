#! /bin/sh
python -m cProfile -o binary_profile run.py
python dump_profile.py > profile.txt