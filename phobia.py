from threading import Thread
from queue import Queue, LifoQueue
import time


"""
Phobia Workshop: https://www.youtube.com/watch?v=koNwUeG-iKE

Lee: fear of the word AAGH
Jim: fear of apologies SORRY
Karen: fear of repetition
Ronni: fear of awkward silences
Tim: bark at other people's phobias
"""


class Lee(Thread):
    def __init__(self, messages: LifoQueue, speech: Queue) -> None:
        super(Lee, self).__init__()

        self.name = 'Lee'
        self.word = 'AAGH'
        self.fear = 'AAGH'
        self.messages = messages
        self.speech = speech
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            time.sleep(0.01)
            if self.messages.empty():
                continue

            name, word, _ = self.messages.queue[-1]
            if name != self.name and word == self.fear:
                self.speech.put_nowait((self.name, self.word))
                self.messages.put_nowait((self.name, self.word, time.time()))


class Jim(Thread):
    def __init__(self, messages: LifoQueue, speech: Queue) -> None:
        super(Jim, self).__init__()

        self.name = 'Jim'
        self.word = 'AAGH'
        self.fear = 'SORRY'
        self.messages = messages
        self.speech = speech
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            time.sleep(0.01)
            if self.messages.empty():
                continue

            _, word, _ = self.messages.queue[-1]
            if word == self.fear:
                self.speech.put_nowait((self.name, self.word))
                self.messages.put_nowait((self.name, self.word, time.time()))


class Karen(Thread):
    def __init__(self, messages: LifoQueue, speech: Queue) -> None:
        super(Karen, self).__init__()

        self.name = 'Karen'
        self.word = 'AAGH'
        self.tolerance = 4
        self.messages = messages
        self.speech = speech
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            time.sleep(0.01)
            if self.messages.qsize() < 2:
                continue

            name1, word1, date1 = self.messages.queue[-1]
            if name1 == self.name:
                continue
            for name2, word2, date2 in reversed(self.messages.queue[:-1]):
                if name2 == self.name:
                    break
                if (
                    word1 == word2
                    and name1 != name2
                    and date1 - date2 <= self.tolerance
                ):
                    self.speech.put_nowait((self.name, self.word))
                    self.messages.put_nowait((self.name, self.word, time.time()))


class Ronni(Thread):
    def __init__(self, messages: LifoQueue, speech: Queue) -> None:
        super(Ronni, self).__init__()

        self.name = 'Ronni'
        self.word = 'AAGH'
        self.tolerance = 10
        self.last = time.time()
        self.messages = messages
        self.speech = speech
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            time.sleep(0.01)
            if not self.messages.empty():
                self.last = self.messages.queue[-1][2]

            if time.time() - self.last >= self.tolerance:
                self.speech.put_nowait((self.name, self.word))
                self.messages.put_nowait((self.name, self.word, time.time()))


class Tim(Thread):
    def __init__(self, messages: LifoQueue, speech: Queue) -> None:
        super(Tim, self).__init__()

        self.name = 'Tim'
        self.word = 'WOOF'
        self.fear = 'AAGH'
        self.tolerance = 0.25
        self.messages = messages
        self.speech = speech
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            time.sleep(0.01)

            if self.messages.empty():
                continue

            name, word, date = self.messages.queue[-1]
            if (
                word == self.fear
                and name != self.name
                and time.time() - date > self.tolerance
            ):
                self.speech.put_nowait((self.name, self.word))
                self.messages.put_nowait((self.name, self.word, time.time()))


class Speaker(Thread):
    def __init__(self, speech: Queue) -> None:
        super(Speaker, self).__init__()

        self.speech = speech
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            time.sleep(0.01)

            if not self.speech.empty():
                name, word = self.speech.get_nowait()
                print(f'{name}: {word}')


def main():
    messages = LifoQueue()
    speech = Queue()

    Lee(messages, speech).start()
    Jim(messages, speech).start()
    Karen(messages, speech).start()
    Ronni(messages, speech).start()
    Tim(messages, speech).start()
    Speaker(speech).start()

    while True:
        s = input()
        if s == 'stop':
            break
        messages.put_nowait(('Admin', s, time.time()))


if __name__ == '__main__':
    main()
