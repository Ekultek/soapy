<div style="text-align:center"><img src ="https://user-images.githubusercontent.com/14183473/42889564-6227433a-8a70-11e8-8c92-71a2f80930be.png" /></div>

This repo is apart of the [warmind project](https://github.com/Project-WARMIND) for a clone of the code see [here](https://gist.github.com/Ekultek/e3dbccb1464b98ae0d5a2e33acfdb821) or you can get the code from [here](https://github.com/ekultek/soapy). For a version you can download with `curl`/`wget` see [here](https://gist.githubusercontent.com/Ekultek/e3dbccb1464b98ae0d5a2e33acfdb821/raw/3b93cb9f9578e61bb774d687c4673a8823d80e16/soa.py).

# Scenario

Post exploitation tools are far and in between, they are used after you have successfully exploited a system and need to either;

 - Do some things, pull hashes, ip addresses, etc.
 - Map the network
 - Anything that has to do with being on the network itself that you don't want to be caught doing

What soa.py does is create a sort of `container` that will host a root terminal shell while the log files are being monitored (default logs: `/var/log`). After you have completed your session, the log files are scrubbed back to the second soa.py was launched.

# Commands

Soapy has a few available commands for you to pass:

```bash
usage: sudo soa.py [-n|-l|-d] PATH|DIR1 DIR2 ...

optional arguments:
  -h, --help            show this help message and exit
  -l PATH, --log PATH   pass the path to log files (*default=/var/log)
  -d DIR1 DIR2 ... [DIR1 DIR2 ... ...], --dirs DIR1 DIR2 ... [DIR1 DIR2 ... ...]
                        provide directories that you want files deleted out of
                        afterwards (*default=None)
  -n, --no-prompt       delete the files in the provided directory without
                        prompting for deletion (*default=raw_input)
```

# Demo video

[![soapdemo](https://user-images.githubusercontent.com/14183473/42889914-1c67fdac-8a71-11e8-935d-74e96e946357.png)](https://vimeo.com/280556246)
