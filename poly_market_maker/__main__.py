import sys
from poly_market_maker.app import App

# __main__ is the entry point for the market maker. 
App(sys.argv[1:]).main()
