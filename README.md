<div align="center">
<img src="https://user-images.githubusercontent.com/16024979/203432210-4ae7ea61-4d11-4a5f-9633-ab9b4b682780.png" alt="eksitui screenshot"/>
<a href="https://github.com/agmmnn/eksitui/releases">
<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/agmmnn/eksitui"></a>
<a href="https://pypi.org/project/eksitui/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/eksitui"></a>

Terminal User Interface for Turkish collaborative hypertext dictionary [ekşi sözlük](https://eksisozluk.com/). With the power of the [textual](https://github.com/Textualize/textual) framework.

</div>

## Install

```
pip install eksitui
```

---

> _**ekşi sözlük** is a collaborative hypertext dictionary based on the concept of Web sites built up on user contribution. It is currently one of the largest online communities in Turkey._

> _As an online public sphere, ekşi sözlük is not only utilized by thousands for information sharing on various topics ranging from scientific subjects to everyday life issues, but also used as a virtual socio-political community to communicate disputed political contents and to share personal views. -[wiki](https://en.wikipedia.org/wiki/Ek%C5%9Fi_S%C3%B6zl%C3%BCk)_

## Usage

```python
$ eksi
# or
$ eksi <topic>
# directly starts the application with given topic
```

![ss2](https://user-images.githubusercontent.com/16024979/203432272-dfa799ac-e3d4-4320-85a2-1bb6855cf843.png)

### Shourtcuts:

```
      T: Dark/Light Theme
 Ctrl+S: Saves the Screenshot in app's folder
      F: Focus Search Input
 Ctrl+X: Clear Search Input
      Q: Previous Page
      W: Next Page
 Ctrl+O: Hide/Show Footer Bar
 Ctrl+Q: Quit
```

## Dev

```
$ pip install "textual[dev]"
$ textual console
$ textual run --dev eksitui.main:EksiTUIApp
```

### Dependencies

- [textual](https://pypi.org/project/textual/)
- [requests](https://pypi.org/project/requests/)

### Thanks to:

- [Ekşisözlük Unofficial API](https://github.com/e4c6/eksi_unofficial_api) by [e4c6](https://github.com/e4c6)
