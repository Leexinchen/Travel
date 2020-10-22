from robot.sdk.AbstractPlugin import AbstractPlugin
import sys
sys.path.append('/home/pi/Travel-1')
import start_project


class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('已经在启动啦!', cache=True)
        start_project.start()
        self.say('启动完成，放心地出门吧!', cache=True)

    def isValid(self, text, parsed):
        return "我要出行" in text