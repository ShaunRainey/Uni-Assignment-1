Current flaws:

When an item is deleted, there's no traceability. 
Validation of inputs could be improved, currently very basic
Could use getters and setters to remove direct access to objects
Could expand search to include a date filter
Some of the functions could be combined and made generic, to stick to DRY principles
When creating/updating you're currently locked into the task unless you complete it

Currently a bug where if the update fails, the item being updated is just deleted