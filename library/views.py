import logging
from django.db.models import Count
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Sum
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View
import csv
from .forms import *
from .models import Book, BorrowedBook, Member, Transaction

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
class HomeView(View):
    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        books = Book.objects.all()
        borrowed_books = BorrowedBook.objects.filter(returned=False)
        overdue_books = BorrowedBook.objects.filter(return_date__lt=timezone.now().date(), returned=False)

        total_members = members.count()
        total_books = books.count()
        total_borrowed_books = borrowed_books.count()
        total_overdue_books = overdue_books.count()

        recently_added_books = books.order_by("-created_at")[:5]

        total_amount = sum([payment.amount for payment in Transaction.objects.all()])
        overdue_amount = sum([book.fine for book in overdue_books])

        CATEGORY_CHOICES = (
            ("fiction", "Fiction"),
            ("non-fiction", "Non-Fiction"),
            ("biography", "Biography"),
            ("history", "History"),
            ("science", "Science"),
            ("tech", "Tech"),
            ("poetry", "Poetry"),
            ("drama", "Drama"),
            ("religion", "Religion"),
            ("children", "Children"),
            ("other", "Other"),
        )

        category_frequency = {}
        for book in borrowed_books:
            category = book.book.category
            category_frequency[category] = category_frequency.get(category, 0) + 1

        returned_books_data = BorrowedBook.objects.filter(returned=True).count()
        non_returned_books_data = BorrowedBook.objects.filter(returned=False).count()

        
        context = {
            "total_members": total_members,
            "total_books": total_books,
            "total_borrowed_books": total_borrowed_books,
            "total_overdue_books": total_overdue_books,
            "recently_added_books": recently_added_books,
            "total_amount": total_amount,
            "overdue_amount": overdue_amount,
            "category_frequency": category_frequency,
            "returned_books_data": returned_books_data,
            "non_returned_books_data": non_returned_books_data,
        }

        return render(request, "index.html", context)

@method_decorator(login_required, name="dispatch")
class AddMemberView(View):
    def get(self, request, *args, **kwargs):
        form = AddMemberForm()
        return render(request, "members/add-member.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AddMemberForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            logger.info("New member added successfully.")
            return redirect("members")

        logger.error(f"Error occurred while adding member: {form.errors}")

        return render(request, "members/add-member.html", {"form": form})

@method_decorator(login_required, name="dispatch")
class MembersListView(View):

    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        return render(request, "members/list-members.html", {"members": members})

    def post(self, request, *args, **kwargs):
        query = request.POST.get("query")
        members = Member.objects.filter(name__icontains=query)
        return render(request, "members/list-members.html", {"members": members})


@method_decorator(login_required, name="dispatch")
class UpdateMemberDetailsView(View):
    def get(self, request, *args, **kwargs):
        member = Member.objects.get(pk=kwargs["pk"])
        form = UpdateMemberForm(instance=member)
        return render(request, "members/update-member.html", {"form": form, "member": member})

    def post(self, request, *args, **kwargs):
        member = Member.objects.get(pk=kwargs["pk"])
        form = UpdateMemberForm(request.POST,request.FILES,instance=member)

        if form.is_valid():
            form.save()
            logger.info("Member details updated successfully.")
            return redirect("members")

        logger.error(f"Error occurred while updating member: {form.errors}")

        return render(request, "members/update-member.html", {"form": form, "member": member})


@method_decorator(login_required, name="dispatch")
class DeleteMemberView(View):

    def get(self, request, *args, **kwargs):
        member = Member.objects.get(pk=kwargs["pk"])
        member.delete()
        logger.info("Member deleted successfully.")
        return redirect("members")


@method_decorator(login_required, name="dispatch")
class AddBookView(View):
    def get(self, request, *args, **kwargs):
        form = AddBookForm()
        return render(request, "books/add-book.html", {"form": form})
    def post(self, request, *args, **kwargs):
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            if book.quantity == 0:
                book.status = "not-available"
            else:
                book.status = "available"
            book.save()

            logger.info("New book added successfully.")
            return redirect("books")

        logger.error(f"Error occurred while adding book: {form.errors}")

        return render(request, "books/add-book.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class BooksListView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        return render(request, "books/list-books.html", {"books": books})

    def post(self, request, *args, **kwargs):
        query = request.POST.get("query")
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return render(request, "books/list-books.html", {"books": books})


@method_decorator(login_required, name="dispatch")
class UpdateBookDetailsView(View):
    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=kwargs["pk"])
        form = AddBookForm(instance=book)
        return render(request, "books/update-book.html", {"form": form, "book": book})

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(pk=kwargs["pk"])
        form = AddBookForm(request.POST, instance=book)

        if form.is_valid():
            book = form.save(commit=False)
            if book.quantity == 0:
                book.status = "not-available"
            else:
                book.status = "available"
            book.save()

            logger.info("Book details updated successfully.")
            return redirect("books")

        logger.error(f"Error occurred while updating book: {form.errors}")

        return render(request, "books/update-book.html", {"form": form, "book": book})


@method_decorator(login_required, name="dispatch")
class DeleteBookView(View):

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=kwargs["pk"])
        book.delete()
        logger.info("Book deleted successfully.")
        return redirect("books")


@method_decorator(login_required, name="dispatch")
class LendBookView(View):
    def get(self, request, *args, **kwargs):
        form = LendBookForm()
        payment_form = PaymentForm()

        return render(request, "books/lend-book.html", {"form": form, "payment_form": payment_form})

    def post(self, request, *args, **kwargs):
        form = LendBookForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if form.is_valid() and payment_form.is_valid():
            lent_book = form.save(commit=False)
            if lent_book.member.amount_due > 500:
                form.add_error(None, "Member has exceeded the borrowing limit.")
                logger.error("Member has exceeded the borrowing limit.")
            else:
                payment_method = payment_form.cleaned_data["payment_method"]
                books_ids = request.POST.getlist("book")
                amount = 0
                for book_id in books_ids:
                    book = Book.objects.get(pk=book_id)
                    BorrowedBook.objects.create(
                        member=lent_book.member,
                        book=book,
                        return_date=lent_book.return_date,
                        fine=lent_book.fine,
                    )
                    logger.info("Book lent successfully.")

                    book.quantity -= 1
                    book.save()
                    logger.info("Book Quantity updated successfully.")

                    amount += book.borrowing_fee

                Transaction.objects.create(member=lent_book.member, amount=amount, payment_method=payment_method)
                logger.info("Payment made successfully.")

                return redirect("lent-books")

        logger.error(f"Error occurred while issuing book: {form.errors}")

        return render(request, "books/lend-book.html", {"form": form, "payment_form": payment_form})


@method_decorator(login_required, name="dispatch")
class LendMemberBookView(View):
    def get(self, request, *args, **kwargs):
        member = Member.objects.get(pk=kwargs["pk"])
        form = LendMemberBookForm()
        payment_form = PaymentForm()
        return render(
            request, "books/lend-member-book.html", {"form": form, "payment_form": payment_form, "member": member}
        )

    def post(self, request, *args, **kwargs):
        member = Member.objects.get(pk=kwargs["pk"])
        form = LendMemberBookForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if form.is_valid() and payment_form.is_valid():
            if member.amount_due > 500:
                form.add_error(None, "Member has exceeded the borrowing limit.")
                logger.error("Member has exceeded the borrowing limit.")
            else:
                lended_book = form.save(commit=False)
                payment_method = payment_form.cleaned_data["payment_method"]
                book_ids = request.POST.getlist("book")
                amount = 0
                for book_id in book_ids:
                    book = Book.objects.get(pk=book_id)
                    BorrowedBook.objects.create(
                        member=member, book=book, return_date=lended_book.return_date, fine=lended_book.fine
                    )
                    logger.info("Book lent successfully.")

                    book.quantity -= 1
                    book.save()
                    logger.info("Book Quantity updated successfully.")

                    amount += book.borrowing_fee

                Transaction.objects.create(member=member, amount=amount, payment_method=payment_method)
                logger.info("Payment made successfully.")

                return redirect("lent-books")

        logger.error(f"Error occurred while issuing book: {form.errors}")

        return render(
            request, "books/lend-member-book.html", {"form": form, "payment_form": payment_form, "member": member}
        )


@method_decorator(login_required, name="dispatch")
class LentBooksListView(View):
    def get(self, request, *args, **kwargs):
        books = BorrowedBook.objects.select_related("member", "book")
        return render(request, "books/lent-books.html", {"books": books})

    def post(self, request, *args, **kwargs):
        query = request.POST.get("query")
        books = BorrowedBook.objects.filter(
            Q(book__title__icontains=query) | Q(book__author__icontains=query)
        ).select_related("member", "book")
        return render(request, "books/lent-books.html", {"books": books})

@method_decorator(login_required, name="dispatch")
class UpdateBorrowedBookView(View):
    def get(self, request, *args, **kwargs):
        book = BorrowedBook.objects.get(pk=kwargs["pk"])
        form = UpdateBorrowedBookForm(instance=book)
        return render(request, "books/update-borrowed-book.html", {"form": form, "book": book})

    def post(self, request, *args, **kwargs):
        book = BorrowedBook.objects.get(pk=kwargs["pk"])
        form = UpdateBorrowedBookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            logger.info("Borrowed book details updated successfully.")
            return redirect("lent-books")
        logger.error(f"Error occurred while updating borrowed book: {form.errors}")

        return render(request, "books/update-borrowed-book.html", {"form": form, "book": book})


@method_decorator(login_required, name="dispatch")
class DeleteBorrowedBookView(View):
    def get(self, request, *args, **kwargs):
        borrowed_book = BorrowedBook.objects.get(pk=kwargs["pk"])

        book = borrowed_book.book
        book.quantity += 1
        book.save()
        logger.info("Book Quantity updated successfully.")

        borrowed_book.delete()

        logger.info("Borrowed book deleted successfully.")
        return redirect("lent-books")


@method_decorator(login_required, name="dispatch")
class ReturnBookView(View):
    def get(self, request, *args, **kwargs):
        borrowed_book = BorrowedBook.objects.get(pk=kwargs["pk"])
        if borrowed_book.return_date < timezone.now().date():
            return redirect("return-book-fine", pk=borrowed_book.pk)

        else:
            borrowed_book.returned = True
            borrowed_book.save()
            logger.info("Book returned successfully.")

            book = borrowed_book.book
            book.quantity += 1
            book.save()
            logger.info("Book Quantity updated successfully.")

            return redirect("lent-books")


@method_decorator(login_required, name="dispatch")
class ReturnBookFineView(View):
    def get(self, request, *args, **kwargs):
        form = PaymentForm()
        book = BorrowedBook.objects.get(pk=kwargs["pk"])
        return render(request, "books/return-book-fine.html", {"book": book, "form": form})

    def post(self, request, *args, **kwargs):
        form = PaymentForm(request.POST)
        book = BorrowedBook.objects.get(pk=kwargs["pk"])

        if form.is_valid():
            payment_method = form.cleaned_data["payment_method"]
            fine = book.fine

            book.returned = True
            book.save()
            logger.info("Book returned successfully.")

            book.book.quantity += 1
            book.book.save()
            logger.info("Book Quantity updated successfully.")

            Transaction.objects.create(member=book.member, amount=fine, payment_method=payment_method)

            return redirect("lent-books")
        logger.error(f"Error occurred while returning book: {form.errors}")

        return render(request, "books/return-book-fine.html", {"book": book, "form": form})


@method_decorator(login_required, name="dispatch")
class ListPaymentsView(View):
    def get(self, request, *args, **kwargs):
        payments = Transaction.objects.select_related("member")
        return render(request, "payments/list-payments.html", {"payments": payments})

    def post(self, request, *args, **kwargs):
        query = request.POST.get("query")
        payments = Transaction.objects.filter(member__name__icontains=query).select_related("member")
        return render(request, "payments/list-payments.html", {"payments": payments})


@method_decorator(login_required, name="dispatch")
class DeletePaymentView(View):
    def get(self, request, *args, **kwargs):
        payment = Transaction.objects.get(pk=kwargs["pk"])
        payment.delete()
        logger.info("Payment deleted successfully.")
        return redirect("payments")


class OverdueBooksView(View):
    def get(self, request, *args, **kwargs):
        overdue_books = BorrowedBook.objects.filter(
            return_date__lt=timezone.now().date(), returned=False
        ).select_related("member", "book")
        return render(request, "books/overdue-books.html", {"books": overdue_books})

    def post(self, request, *args, **kwargs):
        query = request.POST.get("query")
        overdue_books = BorrowedBook.objects.filter(
            Q(book__title__icontains=query) | Q(book__author__icontains=query),
            return_date__lt=timezone.now().date(),
            returned=False,
        ).select_related("member", "book")
        return render(request, "books/overdue-books.html", {"books": overdue_books})
    

@method_decorator(login_required, name="dispatch")
class BooksExportView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Books.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Category', 'Quantity', 'Description', 'BorrowingFee', 'Status'])
        for book in books:
            writer.writerow([book.title, book.author, book.category, book.quantity, book.description, book.borrowing_fee, book.status])
        return response

@method_decorator(login_required, name="dispatch")
class MembersExportView(View):
    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Members.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Contact', 'Address', 'AmountDue'])
        for member in members:
            writer.writerow([member.name, member.email, member.contact, member.address, member.amount_due])
        return response