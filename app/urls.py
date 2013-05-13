#!/usr/local/bin/python
#conding: utf-8
#author: He.Kang@dev-engine.com


from Handler.home import HomeHandler
from Handler.dback import DbackHandler
from Handler.wback import WbackHandler
from Handler.diary import DiaryListHandler,\
                          DiaryDetailHandler,\
                          DiaryLoadHandler, DiaryRssHandler
from Handler.admin import *
from Handler.comment import CommentAddHandler, CommentDelHandler,\
                            CommentReplyHandler
from Handler.gallary import GallaryHandler
from Handler.category import CategoryListHandler, CategoryPagingHandler
from Handler.tag import TagListHandler
from Handler.error import ErrorHandler
from Handler.page import AboutHandler
from Handler.search import SearchHandler

urls = [
    (r'/', HomeHandler),
    (r'/dback', DbackHandler),
    (r'/wback', WbackHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/feed', DiaryRssHandler),
    (r'/gallary', GallaryHandler),
    (r'/about', AboutHandler),

    (r'/diary/add', DiaryAddHandler),
    (r'/diary/load', DiaryLoadHandler),
    (r'/diary/detail/([0-9]+)', DiaryDetailHandler),
    (r'/diary/list/([0-9]+)', DiaryListHandler),

    (r'/admin', AdminHandler),
    (r'/admin/all-post/([0-9]+)', AdminDiaryListHandler),
    (r'/admin/category', AdminCategoryHandler),
    (r'/admin/diary/edit/([0-9]+)', DiaryUpdateHandler),
    (r'/admin/diary/del/([0-9]+)', DiaryDelHandler),
    (r'/admin/diary/set-date', DiarySetDateHandler),
    (r'/admin/diary/add-photo', DiaryAddPhotoHandler),
    (r'/admin/comments/all-comment/([0-9]+)', AdminCommentHandler),
    (r'/admin/comment/del', CommentDelHandler),
    (r'/admin/comment/reply', CommentReplyHandler),
    (r'/admin/gallary/all-gallary', AdminGallaryHandler),
    (r'/admin/gallary/add', AdminGallaryAddHandler),
    (r'/admin/gallary/detail/([0-9]+)', AdminGallaryDetailHandler),
    (r'/admin/gallary/add-photo', AdminGallaryAddPhotoHandler),
    (r'/admin/category/add', AdminCategoryAddHandler),
    (r'/admin/category/del/([0-9]+)', AdminCategoryDelHandler),
    (r'/admin/category/detail/([0-9]+)', AdminCategoryDetailHandler),
    (r'/admin/category/detail/del/([0-9]+)', AdminCategoryDelDiaryHandler),
    (r'/admin/page', AdminPageHandler),
    (r'/admin/page/add', AdminPageAddHandler),
    (r'/admin/page/edit/([0-9]+)', AdminPageEditHandler),
    (r'/admin/page/del/([0-9]+)', AdminPageDelHandler),

    (r'/comment/add', CommentAddHandler),

    (r'/category/([0-9]+)', CategoryListHandler),
    (r'/category/([0-9]+)/page/([0-9]+)', CategoryPagingHandler),

    (r'/tag/([0-9a-zA-Z_%^\s]+)', TagListHandler),

    (r'/search', SearchHandler),

    (r'.*', ErrorHandler)
]
