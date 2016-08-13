# img2url

## Introduction 

img2url transfers a local image file to an url by uploading the file to GitHub. img2url helps you write portable document, especially markdown file, in such a case you don't need to worry about where to place the static resource like images!

## Install

img2url is a Python project, use `pip` to install:

```
pip install img2url
```

## Command-Line Interface

And the CLI is pretty simple:

```
$ img2url --help 
Usage:
    img2url <path>
    img2url (-m | --markdown) <path>

Options:
    -m, --markdown
```

Example:

```
$ ls -al
total 56
drwxr-xr-x  4 haoxun  staff    136 Aug 13 21:26 .
drwxr-xr-x  8 haoxun  staff    272 Aug 13 21:23 ..
-rw-r--r--@ 1 haoxun  staff  23975 Aug 13 21:26 image1.png
-rw-r--r--@ 1 haoxun  staff   3727 Aug 13 21:26 image2.png

$ img2url image1.png 
https://raw.githubusercontent.com/img2url-testing/img2url-testing-travisci/master/image1.png

$ img2url --markdown image2.png 
![image2.png](https://raw.githubusercontent.com/img2url-testing/img2url-testing-travisci/master/image2.png)
```

## Configuration

User should configure img2url before actually using it, so that img2url knows where to upload the files. Currently, img2url only supports uploading to GitHub public repository.

Path of configuration file:

* `~/.img2url.yml`, by default.
* `IMG2URL_CONFIG_PATH`, customized path.

Example of `.img2url.yml`:

```yaml
token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
user: img2url-testing
repo: img2url-testing-travisci
proxies:
  https: socks5://127.0.0.1:1080
```

Required fields:

* `token`: [Personal access tokens](https://github.com/settings/tokens) of your GitHub account. If you don't have one, click "Generate new token" and **select the "repo" scope**, then record the generated token.
* `user`: Account of GitHub.
* `repo`: The repository to store images.

Optional fields:

* `proxies`: If defined, use proxy to make API requests instead of connecting directly.
* `message_template_create`: Message template for creating new file, supported variables: `{filename}`, `sha`, `time`.
* `message_template_update`: Message template for updating existed file, supported variables: `{filename}`, `sha`, `time`.
* `commiter_name`: Username for commit message.
* `commiter_email`: Email for commit message.