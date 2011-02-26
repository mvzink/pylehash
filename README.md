pylehash
========

A python implementation of [TeleHash](http://telehash.org/).

Part of a class project viewable [here](http://brick.cs.uchicago.edu/Courses/CMSC-16200/2011/pmwiki/pmwiki.php/Student/TeleHash).

*Releasing too early as an ongoing bad habit has brought this project to you today rather than never. By [Michael Victor Zink](http://zuwiki.net/).*

Stuff that doesn't exist yet
----------------------------

* Seeding
* A way to build a test network
* `_ring`/`_line` mechanics
* A `.see` handler
* Actually using the handlers for handling
* Correct external tap handling (depends on `_ring`/`_line`)
* Correct k-bucket mechanics
** Not filling up, checking that they exist, etc.
* Traffic congestion management utilities
** `_hop` and `_br`

In general terms, how it works
------------------------------

Open to change without warning, I guess. Also, not quite fully implemented.

* Telex
** Really just a dictionary with convenience construction and JSON import/export
* Handler
** A callable object implementing two methods:
**1. `matches`, to determine if a given Telex should be processed by this Handler given the sender and current Switch state
**2. `handle`, to actually handle the Telex and interact appropriately with the Switch (including sending new Telexes)
** Calling the object will run `handle` if it `matches`
* Switch
*1. Implements a [Twisted](http://twistedmatrix.com/) UDP protocol
*2. Gobbles JSON from the network, turning it into a Telex
*3. Runs the Telex by every Handler currently attached to the Switch
*4. Provides a send function which automatically manages traffic and ring/line stuff
