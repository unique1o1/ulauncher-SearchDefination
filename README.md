# ulauncher-SearchDefinition
Extension for [ulauncher](https://ulauncher.io/) to Search for definitions of words.

![help](https://i.imgur.com/RN57q9g.png)


1. Type the word you want to find definition for.

![definition search](https://i.imgur.com/rT5rwVh.png)

2. type `*keyword* s` to find synonym

![synonym search](https://i.imgur.com/8bQQRKa.png)

**You can press Enter to copy the definition/synonym to your clipboard**

## Installation

    git clone https://github.com/unique1o1/ulauncher-SearchDefinition/
    cp -R ulauncher-SearchDefinition ~/cache/ulauncher_cache/extensions
    sudo pip2.7 install requests

## Contribute

Feel free to [Open an issue](https://github.com/unique1o1/ulauncher-SearchDefinition/).

* **Python module used [Vocabulary](https://github.com/tasdikrahman/vocabulary)**
* **Offline dictionary doesn't have all words. To get most of the words use online dictionary.**

*Change default_value from `online` to `offline` in manifest.json*
## License

MIT © 2018 unique1o1
