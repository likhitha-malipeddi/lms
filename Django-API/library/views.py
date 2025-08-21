from datetime import date, timedelta
from django.db.models import Q, Count, F
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import(
extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes, OpenApiExample
)

from .models import(
Library, Book, Author, Category, BookAuthor, Member, Borrowing, Review
)
from .serializers import(
LibrarySerializer, BookSerializer, AuthorSerializer, CategorySerializer, BookAuthorSerializer, MemberSerializer, BorrowingSerializer, ReviewSerializer, BorrowRequestSerializer, ReturnRequestSerializer,
)

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all().order_by("library_id")
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "campus_location"]
    search_fields = ["name", "campus_location", "phone_number", "contact_email"]
    ordering_fields = ["library_id", "name", "campus_location"]
    ordering = ["library_id"]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("category", "library").all().order_by("book_id")
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "library", "isbn", "published_year"]
    ordering_fields = ["book_id", "title", "published_year", "total_copies", "available_copies"]
    ordering = ["book_id"]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("author_id")
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name", "bio"]
    ordering_fields = ["author_id", "name"]
    ordering = ["author_id"]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("category_id")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["category_id", "name"]
    ordering = ["name"]

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by("member_id")
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["member_type", "email"]
    search_fields = ["name", "email", "phone_number"]
    ordering_fields = ["member_id", "name", "member_type"]
    ordering = ["member_id"]

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "member").all().order_by("borrowing_id")
    serializer_class = BorrowingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["book", "member", "borrow_date", "due_date", "return_date"]
    search_fields = ["member_name", "book_title"]
    ordering_fields = ["borrowing_id", "borrow_date", "due_date", "return_date"]
    ordering = ["borrowing_id"]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("book", "member").all().order_by("review_id")
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["book", "member", "rating", "review_date"]
    search_fields = ["comment", "book_title", "member_name"]
    ordering_fields = ["review_id", "rating", "review_date"]
    ordering = ["-review_date"]


class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer
    @swagger_auto_schema(
        operation_summary="Search books",
        operation_description="Search by title, ISBN, author name, or category name.",
        tags=["Books"],
        manual_parameters=[
            openapi.Parameter(
                "q", openapi.IN_QUERY,
                description="Search text (title/ISBN/author/category",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        responses={200: BookSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = (self.request.query_params.get("q") or "").strip()
        if not query:
            return Book.objects.none()
        return(
            Book.objects.select_related("category", "library")
            .filter(
                Q(title_icontains=query)
                | Q(isbn_icontains=query)
                | Q(bookauthor_author_name_icontains=query)
                | Q(category_name=query)
            )
            .distinct()
            .order_by("book_id")
        )

class MemberBorrowingHistoryView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    @swagger_auto_schema(
        operation_summary="Member borrowing history",
        operation_description="Return borrow/return history for the given number.",
        tags=["Borrowings"],
        manual_parameters=[
            openapi.Parameter(
                "member_id", openapi.IN_PATH,
                description="Member ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: BorrowingSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        member_id = self.Kwargs["member_id"]
        return(
            Borrowing.objects.select_related("book", "member")
            .filter(member_id=member_id)
            .order_by("-borrow_date", "-borrowing_id")
        )

class BookAvailabilityView(APIView):
    @swagger_auto_schema(
        operation_summary="Check book availability",
        operation_description="Returns whether the book is available and how many copies are available.",
        tags=["Books"],
        manual_parameters=[
            openapi.Parameter(
                "book_id", openapi.IN_PATH,
                description="Book ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Availability info",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "available": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        "available_copies": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    },
                ),
            ),
            404: "Not found",
        },
    )
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        available_copies = max(book.available_copies or 0, 0)
        return Response(
            {"available": available_copies > 0, "available_copies": available_copies},
            status=status.HTTP_200_OK,
        )

class BorrowBookView(APIView):
    @swagger_auto_schema(
        operation_summary="Borrow a book",
        operation_description="Creates a borrowing record for the given member and book.",
        tags=["borrowings"],
        request_body=openapi.Schema(
            type=openapi.TYPE_INTEGER,
            required=["book_id", "member_id"],
            properties={
                "book_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Book ID", example=10),
                "member_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Member ID", example=5),
            },
        ),
        responses={
            200: openapi.Responses(
                description="Borrow Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Book borrowed successfully"),
                        "borrow_date": openapi.Schema(type=openapi.TYPE_STRING, example="2025-08-21"),
                        "due_date": openapi.Schema(type=openapi.TYPE_STRING, example="2025-09-04"),
                        "available_copies": openapi.Schema(type=openapi.TYPE_INTEGER, example=4),
                    },
                ),
            ),
            400: "Missing fields or book not available",
            409: "Member already has this book borrowed",
        },

    )
    def post(self, request):
        book_id = request.data.get("book_id")
        member_id = request.data.get("member_id")

        if not book_id or not member_id:
            return Response(
                {"error": "Missing book_id or member_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book = get_object_or_404(Book, pk=book_id)
        member = get_object_or_404(Member, pk=member_id)

        if (book.available_copies or 0) <= 0:
            return Response(
                {"error": "Book not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Borrowing.objects.filter(
            book=book, member=member, return_date_isnull=True
        ).exists():
            return Response(
                {"error": "This member already borrowed this book and has not returned it."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrow_date = timezone.localdate()
        due_date = borrow_date + timedelta(days=14)

        Borrowing.objects.create(
            book=book, member=member, borrow_date=borrow_date, due_date=due_date
        )

        book.available_copies = (book.available_copies or 0) -1
        if book.available_copies < 0:
            book.available_copies = 0
        book.save(update_fields=["available_copies"])

        return Response(
            {
                "message": "Book borrowed Successfully",
                "borrow_date": str(borrow_date),
                "due_date": str(due_date),
                "available_copies": book.available_copies,
            },
            status=status.HTTP_200_OK,
        )

class ReturnBookView(APIView):
    @swagger_auto_schema(
        operation_summary="Return a book",
        operation_description="Marks an active borrowing as returned.",
        tags=["Borrowings"],
        request_body=openapi.Schema(
            type=openapi.TYPE_INTEGER,
            required=["book_id", "member_id"],
            properties={
                "book_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Book_ID", example=10),
                "member_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Book_ID", example=5),
            },
        ),
        responses={
            200: openapi.Response(
                description="Return Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_INTEGER, example="Book returned successfully"),
                        "return_date": openapi.Schema(type=openapi.TYPE_INTEGER, example="2025-08-25"),
                        "late_days": openapi.Schema(type=openapi.TYPE_INTEGER, example="0"),
                        "available_copies": openapi.Schema(type=openapi.TYPE_INTEGER, example="5"),
                    },
                ),
            ),
            400: "Validation error or no active borrowing found",
        },
    )
    def post(self, request):
        book_id = request.data.get("book_id")
        member_id = request.data.get("member_id")

        if not book_id or not member_id:
            return Response(
                {"error": "Missing book_id or member_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing (
            Borrowing.objects.select_related("book")
            .filter(book_id=book_id, member_id=member_id, return_date_isnull=True)
            .first()
        )
        if not borrowing:
            return Response(
                {"error": "No active borrowing found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        borrowing.return_date = timezone.localdate()
        borrowing.save(update_fields=["return_date"])

        book = borrowing.book
        book.available_copies = (book.available_copies or 0) + 1

        if book.total_copies is not None and book.available_copies > (book.total_copies or 0):
            book.available_copies = book.total_copies
        book.save(update_fields=["available_copies"])

        late_days = 0
        if borrowing.return_date and borrowing.due_date and borrowing.return_date > borrowing.due_date:
            late_date = (borrowing.return_date - borrowing.due_date).days

        return Response(
            {
                "message": "Book returned successfully",
                "return_date": str(borrowing.return_date),
                "late_days": late_days,
                "available_copies": book.available_copies,
            },
            status=status.HTTP_200_OK,
        )

class StatisticsView(APIView):
    @swagger_auto_schema(
        operation_summary="Library statistics",
        operation_description="Aggregated metrics: total books, members, borrowings, currently borrowed, and late returns.",
        tags=["Analytics"],
        responses={
            200: openapi.Response(
                description="Statistics payload",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total_books": openapi.schema(type=openapi.TYPE_INTEGER, example=1200),
                        "total_members": openapi.schema(type=openapi.TYPE_INTEGER, example=300),
                        "total_borrowings": openapi.schema(type=openapi.TYPE_INTEGER, example=540),
                        "currently_borrowed": openapi.schema(type=openapi.TYPE_INTEGER, example=440),
                        "late_returns": openapi.schema(type=openapi.TYPE_INTEGER, example=5),
                    }
                )
            )
        }
    )
    def get(self, request):
        total_books = Book.objects.count()
        total_members = Member.objects.count()
        total_borrowings = Borrowing.objects.count()
        currently_borrowed = Borrowing.objects.filter(return_date_isnull=True).count()
        late_returns = Borrowing.objects.filter(return_date_gt=F("due_date").count())

        return Response(
            {
                "total_books": total_books,
                "total_members": total_members,
                "total_borrowings": total_borrowings,
                "currently_borrowed": currently_borrowed,
                "late_returns": late_returns,
            },
            status=status.HTTP_200_OK
        )


class BorrowBookView(APIView):
    @transaction.atomic
    def post(self, request):
        req = BorrowRequestSerializer(data= request.data)
        req.is_valid(raise_exception=True)

        book_id = req.validated_data["book_id"]
        member_id = req.validated_data["member_id"]

        book = get_object_or_404(Book.objects.select_for_update(), pk=book_id)
        member = get_object_or_404(Member, pk=member_id)

        if (book.available_copies or 0) <= 0:
            return Response({"error": "Book not available"}, status=status.HTTP_400_BAD_REQUEST)

        if Borrowing.objects.filter(book=book, member=member, return_date__isnull=True).exists():
            return Response(
                {"error": "This member already borrowed this book and has not returned it."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrow_date = timezone.localdate()
        due_date = borrow_date + timedelta(days=14)

        borrowing = Borrowing.objects.create(
            book=book, member=member, borrow_date=borrow_date, due_date=due_date
        )

        book.available_copies = F("available_copies") - 1
        book.save(update_fields=["available_copies"])
        book.refresh_from_db(fields=["available_copies"])

        return Response(
            {
                "message": "Book borrowed successfully",
                "borrowing": BorrowingSerializer(borrowing).data,
                "available_copies": book.available_copies,
            },
            status=status.HTTP_201_CREATED,
        )

class ReturnBookView(APIView):
    @transaction.atomic
    def post(self, request):
        req = ReturnRequestSerializer(data=request.data)
        req.is_valid=(raise_exception==True)

        borrowing_id = req.validated_data["borrowing_id"]

        borrowing = (
            Borrowing.objects.select_for_update()
            .select_related("book")
            .filter(pk=borrowing_id, return_date__isnull=True)
            .first()
        )
        if not borrowing:
            return Response({"error": "No active borrowing found"}, status=status.HTTP_400_BAD_REQUEST)

        borrowing.return_date = timezone.localdate()
        borrowing.save(update_fields=["return_date"])

        book = borrowing.book
        book.available_copies = F("available_copies") + 1
        book.save(update_fields=["available_copies"])
        book.refresh_from_db(fields=["available_copies"])

        late_days = 0
        if borrowing.return_date and borrowing.due_date and borrowing.return_date > borrowing.due_date:
            late_days = (borrowing.return_date - borrowing.due_date).days

        return Response(
            {
                "message": "Book returned successfully",
                "borrowing": BorrowingSerializer(borrowing).data,
                "late_days": late_days,
                "available_copies": book.available_copies,
            },
            status=status.HTTP_200_OK
        )













