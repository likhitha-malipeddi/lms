from django.urls import path
from rest_framework.routers import DefaultRouter
from library.views import(
LibraryViewSet, BookViewSet, AuthorViewSet, CategoryViewSet, MemberViewSet, BorrowingViewSet, ReviewViewSet,
BookSearchView, BookAvailabilityView, MemberBorrowingHistoryView, BorrowBookView, ReturnBookView, StatisticsView,
)

router = DefaultRouter()
router.register(r"libraries", LibraryViewSet)
router.register(r"books", BookViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"members", MemberViewSet)
router.register(r"borrowings", BorrowingViewSet)
router.register(r"reviews", ReviewViewSet)

urlpatterns = router.urls + [

    path("api/books/search/", BookSearchView.as_view()),
    path("api/books/<int:book_id>/availability/", BookAvailabilityView.as_view()),
    path("api/members/<int:member_id>/borrowings/", MemberBorrowingHistoryView.as_view()),
    path("api/borrow/", BorrowBookView.as_view()),
    path("api/return/", ReturnBookView.as_view()),
    path("api/stats/", StatisticsView.as_view()),
]
