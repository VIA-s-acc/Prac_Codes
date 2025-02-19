### REPOSITROY
[GitHub](https://github.com/VIA-s-acc/builder/tree/main)

#### WINDOWS REQ
>[!NOTE]
>Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### GLOBAL REQ
> [!NOTE]
>Install Python 3.10 or greater
>pip install -r requirements.txt

#### BUILD

- Go to Main_Codes directory and run `build.py` script

```ruby
usage: build.py [-h] [--modules MODULES [MODULES ...]] [--create CREATE [CREATE ...]] [--reset]

Build and manage modules in the project.

options:
  -h, --help            show this help message and exit
  --modules MODULES [MODULES ...], -m MODULES [MODULES ...]
                        Specify the modules to build. Use 'all' to build everything.
  --create CREATE [CREATE ...], -c CREATE [CREATE ...]
                        Create new modules. Format: module.submodule (e.g., utils.parser).
  --reset, -r           Reset the build configuration.
```
