# Neutral Interface

To make various GUI tools usable with multiple SCM backends, 
I propose creating an intermediary program (or programs or libraries) to present the 
SCM data to the GUI application in an easily parsed, neutral format.
This will simultaneously make things easier for the GUI and make it work for more users.

=== Sample implementations ===

Tiny sample GIT implementation is available at
http://pasky.or.cz/~xpasky/neutral.sh

=== Strawman functionality ===

```
$ scm identify
type:9:Mercurial
project-name:9:linux-2.6
...
$ scm changeset 9938
identifier:17:9938:e63c00676ed5
parent:17:9937:d0ab52bb481d
tag:3:tip
date:17:1130273508 -25200
user:29:Andrew Morton <akpm@osdl.org>
file:29:drivers/scsi/qla2xxx/qla_os.c
description:532:[PATCH] qlogic lockup fix

If qla2x00_probe_one()'s call to qla2x00_iospace_config() fails, we call
qla2x00_free_device() to clean up.  But because ha->dpc_pid hasn't been set
yet, qla2x00_free_device() tries to stop a kernel thread which hasn't started
yet.  It does wait_for_completion() against an uninitialised completion struct
and the kernel hangs up.

Fix it by initialising ha->dpc_pid a bit earlier.

Cc: Andrew Vasquez <andrew.vasquez@qlogic.com>
Cc: James Bottomley <James.Bottomley@steeleye.com>
Signed-off-by: Andrew Morton <akpm@osdl.org>
Signed-off-by: Linus Torvalds <torvalds@osdl.org>

$ scm -s project-name identify
project-name:9:linux-2.6
$ scm -i
identify+type,project-name

type:3:GIT
:
^D
$ 
```

=== Proposed format ===

Output consists of zero or more tag/value pairs. Some tags are optional, some tags may be repeated.
Each pair is output as "<tag>:<value length>:<value>\n". This allows values to contain embedded newlines.
Tag names are all ASCII, values are ASCII/UTF-8.

If the "-s <field>[,<field>...]" argument is passed before the command name,
it suggests that you are interested only in certain fields of the output,
and the program should not output any other fields. Users are encouraged to
always list all the fields they want here, since various field values may be
expensive to compute based on the particular underlying SCM (e.g. in
GIT, it is relatively expensive to get the value of the 'file' field).

=== Suggested commands and associated output fields ===

version:

 * version - the interface version; for the foreseeable future, this will have the value of 0

identify:

 * type - the type of SCM in use in the current directory
 * project-name - the name of the project (optional)
 * user - the user associated with this instance of the project (optional)

changeset:

 * identifier - a string that identifies this revision
 * parent - a string that identifies a parent of this revision (optional, multiple)
 * tag - a string that identifies a tag associated with this revision (optional, multiple)
 * description - the description text associated with this commit
 * date - the date this commit occurred (decimal seconds from UTC epoch, seconds offset from UTC)
 * file - a file modified in this changeset (optional, multiple)
 * user - a string identifying the user who created the commit (multiple)
 * ...

 ...

=== shell mode (-i) ===

It'd be nice to have a shell mode, where a client can open a pipe to a subprocess and pass commands.
This would reduce fork and other setup overhead. 

To allow for arbitrary data in arguments, shell mode passes arguments as follows:

<command>['+'<field>','<field>','...]<newline>
<argument length>':'<argument><newline>
...
<newline>

example:

```
command\n
14:first argument\n
15:second argument\n
\n
```

Results are returned as in command line mode, followed by a newline.

In the command line, the '+' marker and the field list afterwards is optional.
If it is present, the field list after the '+' marker (non-inclusive; '+' and
no field list means empty field list) is parsed in the same way as the "-s"
argument, and the same considerations apply - it is recommended to always
specify the field list.

=== library (future) ===

Once some implementations exist, it should be easy to wrap all calls into a library. This library can initially call the stand-alone command, or possibly shell mode if available. Once the interface is well-established, the shim library can be replaced with direct calls to the SCM backend for improved performance.
