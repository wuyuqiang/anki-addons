from source_widget import SourceWidget


class QueryIterator:

    class ItemIter:
        def __init__(self, queue):
            self._queue = None
            self._idx = 0
            self._len = 0
            self.reset(queue)

        def reset(self, queue=None):
            if queue is not None:
                self._queue = queue
            self._idx = 0
            self._len = len(self._queue)

        def cur_idx(self):
            return self._idx

        def inc(self):
            self._idx += 1

        def is_end(self):
            return self._idx >= self._len

        def inc_and_is_end(self):
            self.inc()
            return self.is_end()

        def get_current(self):
            if self.is_end():
                return None
            return self._queue[self._idx]

    def __init__(self, notes, src_list):
        self._notes = QueryIterator.ItemIter(notes)
        self._src_queue = QueryIterator.ItemIter(src_list)
        self._dest_queue = QueryIterator.ItemIter(self._src_queue.get_current()["dest_list"])
        self._phrases = QueryIterator.ItemIter([])
        self._gen_phrases(self._notes.get_current(), self._src_queue.get_current())

    def _gen_phrases(self, note, src_conf):
        split = src_conf["split"]
        src_field = src_conf["src"]
        src_content = note[src_field]
        if split:
            phrases = src_content.split("|")
        else:
            phrases = [src_content]
        self._phrases.reset(phrases)

    def is_finished(self):
        return self._notes.is_end()

    def next_item(self):
        if self.is_finished():
            return None

        item = {}
        item["note"] = self._notes.get_current()

        src_conf = self._src_queue.get_current()
        item["src"] = src_conf["src"]
        item["write_mode"] = src_conf.get("write_mode", SourceWidget.REMOVE_APPEND_MODE)

        item["phrase"] = self._phrases.get_current()
        if self._phrases.cur_idx() > 0:
            item["write_mode"] = SourceWidget.ONLY_APPEND_MODE

        dest_conf = self._dest_queue.get_current()
        item["dest"] = dest_conf["dest"]
        item["svc_id"] = dest_conf["service"]
        item["options"] = {
            "voice": dest_conf["voice"]
        }

        # print item
        self._next_cursor()
        return item

    def _next_cursor(self):
        if not self._dest_queue.inc_and_is_end():
            return

        if not self._phrases.inc_and_is_end():
            self._dest_queue.reset()
            return

        if not self._src_queue.inc_and_is_end():
            src_conf = self._src_queue.get_current()
            self._dest_queue.reset(src_conf["dest_list"])
            self._gen_phrases(self._notes.get_current(), src_conf)
            return

        if not self._notes.inc_and_is_end():
            self._src_queue.reset()
            src_conf = self._src_queue.get_current()
            self._dest_queue.reset(src_conf["dest_list"])
            self._gen_phrases(self._notes.get_current(), src_conf)


class QueryIterator1:

    def __init__(self, notes, src_list):
        self._notes = notes
        self._source_list = src_list

        self._notes_cur_idx = 0
        self._notes_len = len(self._notes)
        self._cur_note = self._notes[self._notes_cur_idx]

        self._src_cur_idx = 0
        self._src_len = 0
        self._cur_src_sec = None

        self._dest_cur_idx = 0
        self._dest_len = 0
        self._cur_dest_sec = None

        self._reset_src()
        self._reset_dest()

        self._is_finished = self._notes_cur_idx >= self._notes_len

    def _reset_src(self):
        self._src_cur_idx = 0
        self._src_len = len(self._source_list)
        self._cur_src_sec = self._source_list[self._src_cur_idx]

    def _reset_dest(self):
        self._dest_cur_idx = 0
        self._dest_len = len(self._cur_src_sec["dest_list"])
        self._cur_dest_sec = self._cur_src_sec["dest_list"][self._dest_cur_idx]

    def is_finished(self):
        return self._is_finished

    def next_item(self):
        if self.is_finished():
            return None
        item = {}
        item["note"] = self._cur_note
        item["write_mode"] = self._cur_src_sec.get("write_mode", SourceWidget.REMOVE_APPEND_MODE)
        item["src"] = self._cur_src_sec["src"]
        item["phrase"] = self._cur_note[item["src"]]
        item["dest"] = self._cur_dest_sec["dest"]
        item["svc_id"] = self._cur_dest_sec["service"]
        item["options"] = {
            "voice": self._cur_dest_sec["voice"]
        }
        print item
        self._next_cursor()
        return item

    def _next_cursor(self):
        self._dest_cur_idx += 1
        if self._dest_cur_idx < self._dest_len:
            self._cur_dest_sec = self._cur_src_sec["dest_list"][self._dest_cur_idx]
            return

        self._src_cur_idx += 1
        if self._src_cur_idx < self._src_len:
            self._cur_src_sec = self._source_list[self._src_cur_idx]
            self._reset_dest()
            return

        self._notes_cur_idx += 1
        if self._notes_cur_idx < self._notes_len:
            self._cur_note = self._notes[self._notes_cur_idx]

            self._reset_src()
            self._reset_dest()
            return
        self._is_finished = True


if __name__ == '__main__':
    json_data = {
        "c1": [
            {
                "src": "f1",
                "split": True,
                "dest_list": [
                    {
                        "dest": "field2",
                        "voice": "group_2",
                        "service": "group_id"
                    }
                ]
            },
            {
                "src": "f2",
                "split": False,
                "dest_list": [
                    {
                        "dest": "field1",
                        "voice": "group_2",
                        "service": "group_id"
                    }
                ]
            },
            {
                "src": "f3",
                "split": False,
                "dest_list": [
                    {
                        "dest": "field1",
                        "voice": "group_2",
                        "service": "group_id"
                    }
                ]
            }
        ]
    }
    notes = [
        {"f1":"f2|f11|f22|f44 f55", "f2":"f3", "f3":"f4"},
        {"f1":"f3", "f2":"f4", "f3":"f5"},
    ]
    q = QueryIterator(notes, json_data['c1'])
    while not q.is_finished():
        q.next_item()
