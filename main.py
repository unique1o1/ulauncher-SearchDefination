from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import json
from vocabulary.vocabulary import Vocabulary as vb


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def __help(self):
        items = [ExtensionSmallResultItem(icon='images/info.png',
                                          name="Type your word for its defination", on_enter=HideWindowAction())]
        return items

    def on_event(self, event, extension):
        items = []
        arg = event.get_argument()
        if arg is None:
            items = self.__help()
        else:
            try:
                definition = json.loads(vb.meaning(arg))
                length = len(definition)

                results = [definition[i]['text']
                           for i in range(4 if length > 4 else length)]

                for i, res in enumerate(results):

                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                     name='{} #{}'.format(
                                                         arg, i+1),
                                                     description='{}'.format(
                                                         res),
                                                     on_enter=CopyToClipboardAction(res)))
            except Exception, e:

                items = [ExtensionSmallResultItem(icon='images/error.png',
                                                  name="Coundn't find defination for that word",
                                                  on_enter=CopyToClipboardAction(error_info))]
        return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
