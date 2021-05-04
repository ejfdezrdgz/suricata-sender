# suricata-sender
Compile and send Suricata's latest stats to your desired Zabbix server

# Disclaimer
I made this in an attempt to use [cvandeplas' suricata_stats](https://github.com/cvandeplas/suricata_stats), but after much trouble I ended up learning a bit of Python and just refactored the thing almost entirely to suit my needs. I'm not responsible for any damages your systems may endure by using this script, use at your own risk.

# Programs used
* Python 2.7.18
* Suricata 6.0.2
* Zabbix 4.4.10 with the template in this same repo
* Maybe a few things I might be forgetting

# Usage
Install the things stated above, download the script and edit the global vars according to your setup. Then execute the script such as:

    python2 suricata.py -z
    
If you want it to not output the full summary use it like:

    python2 suricata.py -z -q
    
If you have other ways to invoke your Python, change the command syntax accordingly

# Considerations
* After executing the script successfully you may see a number of "failed" datapoints. That's no issue, __AS LONG AS YOUR "PROCESSED" COUNT IS MORE THAN 0__. It just means your template doesn't have those keys encoded as items. You may add them to your Zabbix template and it should work perfectly. If your "processed" count is 0, you might not have something correctly configured, your Zabbix server may be down or any other problem.
* The script has been updated from Cristophe's such as it won't need you to input how many threads Suricata has configured (as it already does the stat compression) nor how many lines you want to get from the file (as it just gets the last full block). It also checks for Suricata's process status and sends a datapoint with the state.
* The script could of course be more polished, but as it stands, it works for me so don't expect updates on this. Fork it, copy it or whatever you want.
* Could I have made it not require the "-z"? I guess, but I couldn't care enough. If you do care enough, edit the script, it's not that difficult. You can do a pull request too if you want.
