from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import string
import os
import itertools as it
import functools
import unicodedata
import argparse
import sys

punct_deleter = dict.fromkeys(i for i in range(sys.maxunicode)
                              if unicodedata.category(chr(i)).startswith('P'))
space_deleter = dict.fromkeys(i for i in range(sys.maxunicode)
                              if unicodedata.category(chr(i)).startswith('Z'))


def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    return '\n\n'.join(text)


def count_stats(writers_dir = "C:\\Users\\annag\\Documents\\Писатели для MLDS"):
    stats = dict()
    for writer in os.listdir(writers_dir):
        stats[writer] = dict()
        stats[writer]['words_avg_length'] = word_avg_length(writer, writers_dir)

    return stats


def get_books_as_text_iterator(writer, writers_dir):
    book_list = os.listdir(os.path.join(writers_dir, writer))
    full_book_path = functools.partial(os.path.join, writers_dir, writer)
    books = map(lambda book_name: epub.read_epub(full_book_path(book_name)), book_list)
    chapters = [book.get_items_of_type(ebooklib.ITEM_DOCUMENT) for book in books][:-2]
    return map(chapter_to_str, it.chain.from_iterable(chapters))


def word_avg_length(writer, writers_dir):
    words_cnt = 0
    total_length = 0

    for text in get_books_as_text_iterator(writer, writers_dir):
        words_cnt += len(text.translate(punct_deleter).split())
        total_length += len(text.translate(punct_deleter).translate(space_deleter))

    return total_length / words_cnt


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_dir", help="root folder of all books")
    args = argparser.parse_args()
    print(count_stats(writers_dir=args.data_dir))
