<div style="text-align:center"><img src ="https://user-images.githubusercontent.com/14183473/42889564-6227433a-8a70-11e8-8c92-71a2f80930be.png" /></div>

This repo is apart of the [warmind project](https://github.com/Project-WARMIND) for a clone of the code see [here](https://gist.github.com/Ekultek/e3dbccb1464b98ae0d5a2e33acfdb821) or you can get the code from [here](https://github.com/ekultek/soapy)

# Scenario

Post exploitation tools are far and in between, they are used after you have successfully exploited a system and need to either;

 - Do some things, pull hashes, ip addresses, etc.
 - Map the network
 - Anything that has to do with being on the network itself

What soa.py does is create a sort of `container` that will host a root terminal shell while the log files are being monitored (default logs: `/var/log`). After you have completed your session, the log files are scrubbed back to the second soa.py was launched.

# Demo video

[![soapdemo](https://user-images.githubusercontent.com/14183473/42889914-1c67fdac-8a71-11e8-935d-74e96e946357.png)](https://vimeo.com/280556246)
