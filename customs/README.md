# customs
You can place any custom python files here that you'd like. Squishy will attempt to load them as discord.py extensions, with python files in premain being loaded before the main modules, and postmain files being loaded after the main modules. Any file prefixed with a - is not loaded. Files are loaded in alphabetical order, so if you want to load your modules in a particular order, you could structure your folder as;
- 1.literature
- 2.flaskserver

To load them in that order.