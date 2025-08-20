# -*- coding: utf-8 -*-
from django.db import models

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'author'

    def __str__(self):
        return self.name


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    isbn = models.CharField(unique=True, max_length=13)
    published_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_copies = models.IntegerField(blank=True, null=True)
    available_copies = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Category', models.DO_NOTHING, blank=True, null=True)
    library = models.ForeignKey('Library', models.DO_NOTHING, blank=True, null=True)
    authors = models.ManyToManyField('Author', through='BookAuthor', related_name='books')

    class Meta:
        managed = True
        db_table = 'book'

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'book_author'
        constraints = [
            models.UniqueConstraint(fields=['book', 'author'], name='uq_book_author')
        ]

    def __str__(self):
        return f"{self.book.title} {self.author.name}"


class Borrowing(models.Model):
    borrowing_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)
    borrow_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'borrowing'

    def __str__(self):
        return self.book


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'category'

    def __str__(self):
        return self.name


class Library(models.Model):
    library_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    campus_location = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'library'

    def __str__(self):
        return self.name


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    member_type = models.CharField(max_length=7)

    class Meta:
        managed = True
        db_table = 'member'

    def __str__(self):
        return self.name


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'review'

    def __str__(self):
        return self.book

