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
                                                     description='{}'.format(
                                                         res),
                                                     on_enter=CopyToClipboardAction(res)))
            else:
                error_info = "Coundn't find defination/ synonym for that word"
                items = [ExtensionSmallResultItem(icon='images/error.png',
                                                  name=error_info,
                                                  on_enter=CopyToClipboardAction(error_info))]
            return RenderResultListAction(items)

    def conv(self, val, bools):
        try:
            if bools:
                result = json.loads(vb.synonym(" ".join(val)))
            else:
                result = json.loads(vb.meaning(" ".join(val)))
        except Exception:
            return False

        length = len(result)
        results = [result[i]['text']
                   for i in range(8 if length > 8 else length)]
        return results


if __name__ == '__main__':
    DemoExtension().run()
