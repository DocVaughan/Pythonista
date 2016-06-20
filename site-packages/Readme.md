This directory is included in the default import path of both Python interpreters (2.7 and 3.5), so that you can put reusable modules here.

Please note that site packages will *not* be reloaded automatically when you run a script. This is different from modules in other user directories, so you should typically only put modules here that you don't intend to change.

If you create a module named `pythonista_startup` in this directory, it will automatically be executed when the interpreter is initialized (shortly after the app launches). If you have version-specific `pythonista_startup` modules in `site-packages-2` or `site-packages-3`, they will be executed instead of the module in this directory.

Please use the `site-packages-2` and `site-packages-3` folders for modules that are not compatible with both Python versions.