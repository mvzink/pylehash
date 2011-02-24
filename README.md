pylehash
========

> Ants are more like the parts of an animal than entities on their own.
> They are mobile cells, circulating through a dense connective tissue of
> other ants in a matrix of twigs. The circuits are so intimately interwoven
> that the anthill meets all the essential criteria of an organism.
--Lewis Thomas

A python implementation of [TeleHash](http://telehash.org/): all of the organism, none of the anthill.

Part of a class project viewable [here](http://brick.cs.uchicago.edu/Courses/CMSC-16200/2011/pmwiki/pmwiki.php/Student/TeleHash).

*Releasing too early as an ongoing bad habit has brought this project to you today rather than never by [Michael Victor Zink](http://zuwiki.net/).*

Current major to do list:

* Seeding
* A way to build a test network
* _ring/_line mechanics
* A .see handler
* Correct external tap handling (depends on _ring/_line)
* Correct k-bucket mechanics
** Not filling up, checking that they exist, etc.
* Traffic congestion management
** _hop and _br
