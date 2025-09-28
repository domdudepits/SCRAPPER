#include <stdio.h>
#include <string.h>
using namespace std;

#define MAX_BOOKS 100
#define FILENAME "books.dat"

typedef struct {
    char isbn[20];
    char title[50];
    char author[50];
} Book;

void addBook(Book books[], int *count);
void displayBooks(const Book books[], int count);
int searchBookByISBN(const Book books[], int count, const char *isbn);
void updateBook(Book books[], int count, const char *isbn);
void deleteBook(Book books[], int *count, const char *isbn);
void saveToFile(const Book books[], int count, const char *filename);
void loadFromFile(Book books[], int *count, const char *filename);
void menu();

int main() {
    Book books[MAX_BOOKS];
    int count = 0;
    loadFromFile(books, &count, FILENAME);
    menu(books, &count);
    saveToFile(books, count, FILENAME);
    return 0;
}

void menu(Book books[], int *count) {
    int choice;
    char isbn[20];
    char author[50];
    char title[50];

    do {
        printf("\nLibrary Management System\n");
        printf("1. Add a new book record\n");
        printf("2. Display all book records\n");
        printf("3. Search a book by its ISBN\n");
        printf("4. Search a book by its Author\n");
        printf("5. Search a book by its Title\n");
        printf("6. Update a book record\n");
        printf("7. Delete a book record\n");
        printf("8. Save book records to a file\n");
        printf("9. Load book records from a file\n");
        printf("10. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                addBook(books, count);
                break;
            case 2:
                displayBooks(books, *count);
                break;
            case 3:
                printf("Enter ISBN to search: ");
                scanf("%s", isbn);
                int index = searchBookByISBN(books, *count, isbn);
                if (index != -1) {
                    printf("Book found: %s by %s\n", books[index].title, books[index].author);
                } else {
                    printf("Book not found!\n");
                }
                break;
            case 4:
                printf("Enter Author to search: ");
                scanf("%s", author);
                for (int i = 0; i < *count; i++) {
                    if (strcmp(books[i].author, author) == 0) {
                        printf("Book found: %s (ISBN: %s)\n", books[i].title, books[i].isbn);
                    }
                }
                break;
            case 5:
                printf("Enter Title to search: ");
                scanf("%s", title);
                for (int i = 0; i < *count; i++) {
                    if (strcmp(books[i].title, title) == 0) {
                        printf("Book found: %s by %s (ISBN: %s)\n", books[i].title, books[i].author, books[i].isbn);
                    }
                }
                break;
            case 6:
                printf("Enter ISBN to update: ");
                scanf("%s", isbn);
                updateBook(books, *count, isbn);
                break;
            case 7:
                printf("Enter ISBN to delete: ");
                scanf("%s", isbn);
                deleteBook(books, count, isbn);
                break;
            case 8:
                saveToFile(books, *count, FILENAME);
                break;
            case 9:
                loadFromFile(books, count, FILENAME);
                break;
            case 10:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice! Please try again.\n");
        }
    } while (choice != 10);
}

void addBook(Book books[], int *count) {
    if (*count >= MAX_BOOKS) {
        printf("Book list is full!\n");
        return;
    }
    printf("Enter ISBN: ");
    scanf("%s", books[*count].isbn);
    printf("Enter Title: ");
    scanf("%s", books[*count].title);
    printf("Enter Author: ");
    scanf("%s", books[*count].author);
    (*count)++;
}

void displayBooks(const Book books[], int count) {
    for (int i = 0; i < count; i++) {
        printf("ISBN: %s, Title: %s, Author: %s\n", books[i].isbn, books[i].title, books[i].author);
    }
}

int searchBookByISBN(const Book books[], int count, const char *isbn) {
    for (int i = 0; i < count; i++) {
        if (strcmp(books[i].isbn, isbn) == 0) {
            return i;
        }
    }
    return -1;
}

void updateBook(Book books[], int count, const char *isbn) {
    int index = searchBookByISBN(books, count, isbn);
    if (index == -1) {
        printf("Book not found!\n");
        return;
    }
    printf("Enter new Title: ");
    scanf("%s", books[index].title);
    printf("Enter new Author: ");
    scanf("%s", books[index].author);
}

void deleteBook(Book books[], int *count, const char *isbn) {
    int index = searchBookByISBN(books, *count, isbn);
    if (index == -1) {
        printf("Book not found!\n");
        return;
    }
    for (int i = index; i < (*count) - 1; i++) {
        books[i] = books[i + 1];
    }
    (*count)--;
}

void saveToFile(const Book books[], int count, const char *filename) {
    FILE *file = fopen(filename, "wb");
    if (!file) {
        printf("Error opening file for writing!\n");
        return;
    }
    fwrite(&count, sizeof(int), 1, file);
    fwrite(books, sizeof(Book), count, file);
    fclose(file);
}

void loadFromFile(Book books[], int *count, const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (!file) {
        printf("Error opening file for reading!\n");
        return;
    }
    fread(count, sizeof(int), 1, file);
    fread(books, sizeof(Book), *count, file);
    fclose(file);



}