#!/usr/bin/env python
import os
import web
from controler.weixin import Weixin
urls = (
   '/','Weixin',
)

#app = web.application(urls, globals()).wsgifunc()
app = web.application(urls, globals())
#application = sae.create_wsgi_app(app)
if __name__ == "__main__":
    app.run()
