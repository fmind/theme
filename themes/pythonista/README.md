# Pythonista

Fmind light theme for [Pythonista 3](https://omz-software.com/pythonista/) on iOS.

Format: [Pythonista 3.0 theme editor](https://omz-software.com/pythonista/docs-3.4/py3/ios/new.html#version-3-0-2016-06-14) · [add-theme links from the theme editor](https://omz-software.com/forum/archive/3655_atom-one-dark-inspired-theme-for-pythonista.html) · [bundled Default theme](https://github.com/pome-ta/pystaColorThemeDev/blob/main/default.json)

## Installation

1. On the iOS device, open this link, for example by pasting it into the Safari address bar, and let it open Pythonista 3. Pythonista adds [Fmind.json](Fmind.json) to your themes.

   ```text
   pythonista3://?action=add-theme&theme-data=eNqtVd3SmjAQvfcpHHsrHUS02gfoazCbZNGUkGVCaD_nm-_dGwKKCFKc0RkuTM7Zn7MnyediuVxpyHH1c7n6lUstVut6CYW0ZBLgVpIuE8lJJwx4djJUOYwDf0v97zncSm09cHfciX00CiyooD9oBqE36TaNG4aSzIC5TGW_Qm4ZNz9ihH2zac9VzjRIlTAyAo0HHAHCK0BgCpWyicWPhh2F0SZqs4-HdMikRIW-iy5tHB1217IZmKmSLbCpputtK63CQUElFmCg1lBJjYNmJlKeKmtxsqgrotOpPwiNiXZitnv3Y3UKoCldxRLUgIjGuHJv8sIuxBBb7cFkSYYXRmDqelJQJTZ9ciqwdEuf7l83pduCW-KkyNwL5De-1g2htEbq0zg-FPtdJPp4QfxVyk2MEfxxGx_DsI93jf4l3-cIoTVYj5CTqLwHRvD7w0bAoY9PK-0tOT8Dq6Ry_p0mTqVyc5nMtr7upKRtUNpL42lG6kFMrqAsn0ZrS3gt2vxuOOU56ifuao3en4wzbn_0jD6C7mwFHT1FTPm2K90D_RG7BzHGw3gUZC9F3WTcdyty8tfACxMjk4O1Tx0-1iYngUwRz5zWYF7Qx0_kDv2_eUkLSvL5zdQRghmk2YY5IwgnTbB5j5uv4aL3htu-J5y7yrN5kepbO2jN1twPK-duNP7xGVhlXszxU9I9GC3daGd-4_qu6oMcfQ976QpDv937-4rH-Bl55g5Wr8puzZoKR_GBII0TpFvNLW4QyEKZDYM8np8pzeuXKUOq7OohcO8sjxA13ea0qL-vxT9ul5cX
   ```

2. In Pythonista's theme settings, select **Fmind**.

The link holds `Fmind.json` compressed with zlib and encoded as URL-safe Base64, with `=` replaced by `~`. After editing the theme, regenerate it from the repository root:

```sh
python3 -c 'import base64, sys, zlib; print("pythonista3://?action=add-theme&theme-data=" + base64.urlsafe_b64encode(zlib.compress(open(sys.argv[1], "rb").read(), 9)).decode().replace("=", "~"))' themes/pythonista/Fmind.json
```
