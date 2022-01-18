"""
========== RUN FILE ==========
This file runs the simulation of MESA.
The simulation will run through it.
==============================
"""
try:
    from vialis_server import server
    server.port = 8521
    server.launch()
except KeyboardInterrupt:
    print("=====Session closed=====")