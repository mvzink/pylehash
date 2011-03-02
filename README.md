pylehash
========

A python implementation of [TeleHash][telehash].

Part of a class project viewable [here][class project].

*Releasing too early as an ongoing bad habit has brought this project to you today rather than never. By [Michael Victor Zink](http://zuwiki.net/).*

Stuff that doesn't exist yet
----------------------------

Ordered roughly by priority

* See handler should return nearby ends if there are none in the same bucket
* An example app
* `_ring`/`_line` mechanics
* Correct k-bucket mechanics
	* Not filling up, checking that they exist, etc.
* Correct external tap management (depends on `_ring`/`_line`)
* An *easy* way to build a test network

In general terms, how it works
------------------------------

Open to change without warning, I guess. Also, not quite fully implemented.

* Telex
	* Really just a dictionary with convenience construction and JSON import/export
* Handler
	* A callable object implementing two methods:
		1. `matches`, to determine if a given Telex should be processed by this Handler given the sender and current Switch state
		2. `handle`, to actually handle the Telex and interact appropriately with the Switch (including sending new Telexes)
	* Calling the object will run `handle` if it `matches`
* Switch
	1. Implements a [Twisted][twisted] UDP protocol
	2. Gobbles JSON from the network, turning it into a Telex
	3. Runs the Telex by every Handler currently attached to the Switch
	4. Provides a send function which automatically manages traffic and ring/line stuff

[class project]: http://brick.cs.uchicago.edu/Courses/CMSC-16200/2011/pmwiki/pmwiki.php/Student/TeleHash (Wiki page for the class project)

[telehash]: http://telehash.org/ (Official TeleHash page. Courtesy of Jeremie Miller, I believe.)

[twisted]: http://twistedmatrix.com/ (Event-driven networking infrastructure for Python)
