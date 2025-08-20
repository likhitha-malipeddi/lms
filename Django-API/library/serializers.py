from django.utils import timezone
from rest_framework import serializers
from .models import (Library, Author, Book, Category, BookAuthor, Borrowing, Member, Review
)

class LibrarySerializer(serializers.ModelSerializer):
    contact_email = serializers.EmailField(allow_null=True, allow_blank=True, required=False)
    phone_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Library
        fields = "__all__"

        def validate_phone_number(self, value):
            if not value:
                return value
            if not value.isdigit() or len(value) != 10:
                raise serializers.ValidationError("Phone number must be exactly 10 digits.")
            return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ["book", "author"]

        def validate(self, attrs):
            book = attrs.get("book")
            author = attrs.get("author")
            if book and author and BookAuthor.objects.filter(book=book, author=author,).exists():
                raise serializers.ValidationError("This book-author mapping already exists.")
            return attrs

class BookSerializer(serializers.ModelSerializer):
    published_year = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Book
        fields = ["book_id", "title", "isbn", "published_year", "total_copies", "available_copies", "category", "library"]

        def validate_isbn(self, value):
            v = (value or "").strip()
            if len(v) != 13 or not v.isdigit():
                raise serializers.ValidationError("ISBN must be exactly 13 digits.")
            return v

        def validate_published_year(self, value):
            if value is None:
                return value
            v = str(value).strip()
            if not v.isdigit():
                raise serializers.ValidationError("published_year must contain only digits")
            year = int(v)
            year_now = timezone.now().year
            if value < 0 or value > year_now:
                raise serializers.ValidationError(f"published_year must be between 0 and {year_now}.")
            return v
        def validate(self, data):
            total = data.get("total_copies", getattr(self.instance, "total_copies", None))
            available = data.get("available_copies", getattr(self.instance, "available_copies", None))

            if total is not None and total < 0:
                raise serializers.ValidationError({"total_copies": "Must be >= 0."})
            if available is not None and available < 0:
                raise serializers.ValidationError({"available_copies": "Must be >= 0."})
            if total is not None and available is not None and available > total:
                raise serializers.ValidationError("Available copies cannot exceed total copies.")
            return data

class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_null=True,allow_blank=True,required=False)
    phone_number = serializers.CharField(allow_null=True,allow_blank=True,required=False)

    class Meta:
        model = Member
        fields = "__all__"

        def validate_member_type(self, value):
            if value not in ("Student", "Faculty"):
                raise serializers.ValidationError("member_type must be 'Student' or 'Faculty'.")
            return value

        def validate_phone_number(self, value):
            if not value:
                return value
            if not value.isdigit() or len(value) != 10:
                raise serializers.ValidationError("phone number must be exactly 10 digits.")
            return value

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

        def validate_rating(self, value):
            if not (1 <= value <= 5):
                raise serializers.ValidationError("Rating must be between 1 and 5.")
            return value









