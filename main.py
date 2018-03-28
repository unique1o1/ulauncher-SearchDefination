from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.event import PreferencesEvent
from ulauncher.api.shared.event import PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import json
import re
import os

import options


from vocabulary.vocabulary import Vocabulary as vb


data = {}


getupdate = options.onupdate()


class dictionary():
    def init_dictionary(self):
        self.data = json.load(
            open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictionary.json")))


getdictionary = dictionary()


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        if event.id == 'limit':
            getupdate.option = event.new_value

        elif event.id == 'options':

            getupdate.option = event.new_value
            if getupdate.option == 'offline':
                getdictionary.init_dictionary()


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        getupdate.limit = event.preferences['limit']
        getupdate.option = event.preferences['options']

        if event.preferences['options'] == 'offline':

            getdictionary.init_dictionary()


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent,
                       PreferencesUpdateEventListener())
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def __help(self):
        items = [ExtensionSmallResultItem(icon='images/info.png',
                                          name="Type your word for its definition", on_enter=HideWindowAction())]
        return items

    def on_event(self, event, extension):
        items = []
        arg = event.get_argument()
        if arg is None:
            items = self.__help()
        else:
            args = arg.split(' ')
            if args[0] == 's':
                results = self.conv(args[1:], 1)

            else:

                results = self.conv(args[0:], 0)

            if results:

                for i, res in enumerate(results):
                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                     name='{} #{}'.format(
                                                         arg, i+1),
                                                     description=res.encode(
                                                         'utf-8'),
                                                     on_enter=CopyToClipboardAction(res.encode('utf-8'))))
            else:
                error_info = "Coundn't find definition/ synonym for that word"
                items = [ExtensionSmallResultItem(icon='images/error.png',
                                                  name=error_info,
                                                  on_enter=CopyToClipboardAction(error_info))]
        return RenderResultListAction(items)

    def conv(self, val, bools):
        limit = int(getupdate.limit)

        try:
            if bools:

                result = json.loads(vb.synonym(" ".join(val)))
                length = len(result)
                result = [result[i]['text']
                          for i in range(limit if length > limit else length)]
            else:

                limit = int(getupdate.limit)

                result = re.split(r'[0-9]\.', getdictionary.data[" ".join(val)])[
                    1:limit+1] if getupdate.option == "offline" else json.loads(vb.meaning(" ".join(val)))

                if getupdate.option != "offline":
                    length = len(result)
                    result = [result[i]['text']
                              for i in range(limit if length > limit else length)]

        except Exception as e:

            return False
        return result


if __name__ == '__main__':
    DemoExtension().run()
