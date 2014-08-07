#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):

    def initialize(self, manager):
        self.manager = manager

    def post(self, event_name):
        self.manager.dispatch(event_name, self.request.body_arguments)
        self.set_status(201, 'Data added to aggregation')

def run(manager):
    application = tornado.web.Application([
        (r"^/(.+)$", MainHandler, {'manager': manager}),
    ])

    return application

def main():
    import pyqp.manager
    manager = pyqp.manager.Manager()
    application = run(manager)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
