# Concept Table

The revctrl Rosetta stone.  Table of concepts available to revision control systems and (if available) the corresponding commands.

Please add your own.  Note: I'm using GUI mode to edit this table
||'''concept''' ||'''bzr''' ||'''darcs''' ||'''hg''' ||'''svn''' ||
||branch ||branch ||get ||clone ||copy ||
||checkout ||checkout ||''see branch '' ||update ||checkout ||
||commit locally ||commit --local ||record ||commit ||''    na'' ||
||commit to repo ||commit ||''see push/send'' ||''see push'' ||commit ||
||create new repository ||init ||init ||init ||import ||
||diff local ||diff ||whatsnew ||diff || diff ||
||diff repos or versions ||diff ||diff ||incoming/outgoing/diff -r ||diff ||
||<style="vertical-align: top;">file copy ||<style="vertical-align: top;">na||<style="vertical-align: top;">''na'' ||<style="vertical-align: top;">copy ||<style="vertical-align: top;">copy ||
||<style="vertical-align: top;">file move ||<style="vertical-align: top;">mv||<style="vertical-align: top;">mv ||<style="vertical-align: top;">move ||<style="vertical-align: top;">move ||
||log ||log ||changes ||log ||log ||
||manifest ||ls ||query manifest ||manifest ||ls ||
||pull ||pull ||pull ||pull ||update ||
||push ||push ||push ||push ||''na'' ||
||revert ||revert ||revert ||revert ||revert ||
||send by mail ||merge-directive --mail-to ||send ||email (with patchbomb extension) || ||
||summarise local changes ||status ||whatsnew -s ||status ||status ||
||summarise remote changes ||missing --theirs-only||pull --dry-run ||incoming ||update? ||
||tag changes/revisions ||tag||tag ||tag ||copy ||
||update from repo ||update ||''see pull'' ||pull -u ||update ||


== Concepts ==
 * manifest - to see what files are under version control
 * tag changes/revisions - to mark a certain revision, or set of changes as special in some way, like "PRERELEASE", or "2.0.3"
 * what's the difference between pull and "update from repo"?
== Notes ==
 * ''na'' - this concept is not available in this revctrl system
 * ''see...'' - this concept is not available, but the revctrl system uses a different concept in its place

== See also ==

 * Rosetta Stone from a [[http://wiki.darcs.net/RosettaStone|Darcs perspective]]
