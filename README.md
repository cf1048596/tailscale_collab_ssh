# attain a ssh session to a google collab instance via tailscale

Created this so I could have a terminal on a google collab machine even on the free tier.<br>
Yes, the inherent downside is that the machine will cease after however so long/compute used even if you use the same notebook.

Simply invoke the script in a google collab cell like.

```console
$ !cd /path/to/directory && python start.py install
```
To install tailscale and setup a default user and password as a super user according to the env variables specified in the `.env` file.
then do the same as before but change `install` to `up`.

Due to the limitation of no simultaneous/execution of cells in a notebook (at least on the free tier anyway),
`up` will merely start the `tailscaled` daemon in with userspace networking.<br>
You have to stop the cell yourself to then run
'start.py up' to then setup tailscale as usual.

Of course replace `'/path/to/directory'` where ever you downloaded the script to.<br>
Place your `.env` file in the same directory as the script.
