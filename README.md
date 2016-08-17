# img2url

## Introduction 

img2url transforms a local image file to an url by uploading the file to remote. img2url helps you write portable document, especially markdown file, in such a way you don't need to worry about where to place the static resource like images!

Supported remotes:

* GitHub Repository (by default).
* Qiqiu Object Storage.

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
https://cdn.rawgit.com/huntzhan/img2url-repo/master/image1.png

$ img2url --markdown image2.png 
![image2.png](https://cdn.rawgit.com/huntzhan/img2url-repo/master/image2.png)
```

## Configuration

User should configure img2url before actually using it, so that img2url knows where to upload the files.

Path of configuration file:

* `~/.img2url.yml`, by default.
* `IMG2URL_CONFIG_PATH`, customized path.

Currently, img2url supports following remotes, remote is specified by setting `remote` key in configuration file. If `remote` is not defined, `github` is selected as remote by default.

| Remote               | Field Setting    |
| -------------------- | ---------------- |
| GitHub Repository    | `remote: github` |
| Qiqiu Object Storage | `remote: qiniu`  |

### Configuration of GitHub Repository

Example of `.img2url.yml`:

```yaml
remote: github

githu_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
githu_user: img2url-testing
githu_repo: img2url-testing-travisci

proxies:
  https: socks5://127.0.0.1:1080
```

Supported fields:

| field                     | required | default                                  |
| ------------------------- | -------- | ---------------------------------------- |
| `github_token`            | yes      | -                                        |
| `github_user`             | yes      | -                                        |
| `github_repo`             | yes      | -                                        |
| `github_branch`           | no       | `"master"`                               |
| `github_path`             | no       | `""`                                     |
| `github_commiter_name`    | no       | `"huntzhan"`                             |
| `github_commiter_email`   | no       | `"programmer.zhx@gmail.com"`             |
| `message_template_create` | no       | `"{filename} created by img2url at {time}."` |
| `message_template_update` | no       | `"{filename} updated by img2url at {time}."` |
| `proxies`                 | no       | `None`                                   |

Meaning of fields:

* `github_token`: [Personal access tokens](https://github.com/settings/tokens) of your GitHub account. If you don't have one, click "Generate new token" and **select the "repo" scope**, then record the generated token.
* `github_user`: Account of GitHub.
* `github_repo`: The repository to store images.


* `github_branch`: If not defined, use `master` as the default branch.
* `github_path`: Path to store the uploaded files in your repository. If not defined, use the root of repository by default.
* `proxies`: If defined, use proxy to make API requests instead of connecting directly.
* `message_template_create`: Message template for creating new file, supported variables: `{filename}`, `sha`, `time`.
* `message_template_update`: Message template for updating existed file, supported variables: `{filename}`, `sha`, `time`.
* `github_commiter_name`: Username for commit message.
* `github_commiter_email`: Email for commit message.

### Configuration of Qiqiu Object Storage

Example of `.img2url.yml`:

```yaml
remote: qiniu

qiniu_access_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
qiniu_secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
qiniu_bucket: img2url
qiniu_base_url: xxxxxxxxx.bkt.clouddn.com
```

Supported fields:

| field               | required | default |
| ------------------- | -------- | ------- |
| ` qiniu_access_key` | yes      | -       |
| ` qiniu_secret_key` | yes      | -       |
| ` qiniu_bucket`     | yes      | -       |
| ` qiniu_base_url`   | yes      | -       |

Meaning of fields:

* `qiniu_access_key`, `qiniu_secret_key`: [Access/Secret Key](https://portal.qiniu.com/user/key)
* `qiniu_bucket`: the name of Qiniu object storage space.
* `qiniu_base_url`: domain of Qiniu object storage space.