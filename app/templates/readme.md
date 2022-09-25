# Template folder structure
This readme servers to provide a basic overview of how this directory is structured and what each directory represents. This is my own convention, and so I'm documenting my thought processes for anyone who finds themselves looking through this project.

1. **Objects** = Blocks of html relating to a specific singular entity (e.g. a tweet, a user profile, a pop-up notification bubble etc.). One key distinguishing feature between this and a layout, is that an object might be used multiple times on single page


2. **Layouts** = Typically only used once on a page, these are the building pieces for the page, e.g. the menu, the footer, or a particular section (such as a grid displaying tweets.)


3. **Pages** = This is where the individual building blocks are pieced together into the complete web page. Additionally, the pages directory should closely resemble the structure of the website.


Generally speaking... objects are used by layouts, and layouts are used by pages.