# pan_scripts
Misc scripts to interact with PA devices for testing and data collection

* cli.txt         CLI command set to be automated with pan_cli.exp
* commit.txt      List of imported config files to be loaded and committed with pan_commit.exp
* pan_cli.exp     Expect script to interact with PA/PAN and issue the CLI command set in cli.txt repeatedly over a testing period
* pan_commit.exp  Expect script to interact with PA/PAN, load and commit imported config files listed in commit.txt
