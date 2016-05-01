#!/usr/bin/env sh

# Start a name service
python -m Pyro4.naming


# See what objects exist
python -m Pyro4.nsc list
